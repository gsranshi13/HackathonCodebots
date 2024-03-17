import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_google_vertexai import VertexAI
from langchain_google_vertexai import VertexAIEmbeddings
import PyPDF2

import spacy
import uuid

from embeddings import text_embedding

from chroma import collection
from sendtollm import SendToLlm

from RequestResponsePojo import EsgResponse,BenchmarkDetail,Metrics,HealthCheckStatus

nlp = spacy.load("en_core_web_md")


llm = VertexAI(
    model_name="text-bison@001",
    temperature=0.1,
    top_p=0.8,
    top_k=40,
    verbose=True, )

embeddings = VertexAIEmbeddings()


def chunk_data_with_page_and_id(input_file, chunk_size, overlap):
    chunks_with_page_and_id = []
    chunk_id = 0

    pdf_reader = PyPDF2.PdfReader(input_file)

    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        text = page.extract_text()
        paragraphs = text.split('\n')

        for i in range(0, len(paragraphs), chunk_size - overlap):
            chunk = ' '.join(paragraphs[i:i+chunk_size])
            if len(chunk.strip()) > 0:
                chunk_vector = text_embedding(chunk)  # Assuming text_embedding is defined elsewhere
                chunks_with_page_and_id.append((page_number + 1, chunk_id, chunk, chunk_vector))
                chunk_id += 1

    return chunks_with_page_and_id

def chunk_data_with_page_and_id1(input_file, chunk_size, overlap):
    chunks_with_page_and_id = []
    chunk_id = 0

    pdf_reader = PyPDF2.PdfReader(input_file)

    with open("temp.txt", "w", encoding='utf-8') as file:
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            file.write(page.extract_text() + "\n")
            text = page.extract_text()
            paragraphs = text.split('\n')

            for i in range(0, len(paragraphs), chunk_size - overlap):
                chunk = ' '.join(paragraphs[i:i+chunk_size])
                if len(chunk.strip()) > 0:
                    chunk_vector = text_embedding(chunk)  # Assuming text_embedding is defined elsewhere
                    chunks_with_page_and_id.append((page_number + 1, chunk_id, chunk, chunk_vector))
                    chunk_id += 1

    return chunks_with_page_and_id


def create_langchain_index2(input_file):
    print("--indexing---")
    chunk = chunk_data_with_page_and_id(input_file, 1000, 100)
    vectorEmbeddings = []
    metadata = []
    documents = []
    ids = []
    for page_number, chunk_id, chunk_text, chunk_vector in chunk:
        vectorEmbeddings.append(chunk_vector)
        metadata.append({'page_number':page_number})
        documents.append(chunk_text)
        ids.append(str(uuid.uuid4()))

    collection.add(
        documents=documents,
        embeddings=vectorEmbeddings,
        metadatas=metadata,
        ids=ids
    )

@st.cache_resource
def create_langchain_index1(input_file):
    print("--indexing---")
    chunk = chunk_data_with_page_and_id1(input_file, 1000, 100)
    loader = TextLoader("temp.txt", encoding='utf-8')
    print(embeddings)

    index = VectorstoreIndexCreator(vectorstore_cls=DocArrayInMemorySearch, embedding=embeddings).from_loaders([loader])
    return index


@st.cache_data
def get_response(input_text, query):
    print(f"--querying---{query}")
    response = index.query(query, llm=llm)
    return response

def ask_question(question1):
    create_langchain_index2(input_file)
    questionembedding = text_embedding(question1)
    response1 = collection.query(
        query_embeddings=questionembedding,
        n_results=5,
    )
    similarity_results =[]
    for index in range(0, 5):
        context = response1["documents"][0][index]
        metadata = response1["metadatas"][0]
        page_number = metadata[index]["page_number"]
        similarity_results.append({"content": context, "metadata": page_number})

    instance = SendToLlm()

    # Call the runLLM method
    response_content, similarity_response, sources = instance.runLLM(question1, similarity_results)
    
    return response_content, similarity_response, sources



st.title('Question and Answering')

input_file = st.file_uploader("Provide the PDF", type=["pdf"])

summary_response = ""
tweet_response = ""
ln_response = ""
# if st.button("Load"):
if input_file:
    index = create_langchain_index1(input_file)
    summary_query = "Write a 100 words summary of the pdf"
    summary_response = get_response(input_file, summary_query)

    tweet_query = "Write a twitter tweet about pdf"
    tweet_response = get_response(input_file, tweet_query)

    ln_query = "Write a linkedin post for the pdf"
    ln_response = get_response(input_file, ln_query)

    with st.expander('Page Summary'):
        st.info(summary_response)

    with st.expander('Tweet'):
        st.info(tweet_response)

    with st.expander('LinkedIn Post'):
        st.info(ln_response)

st.session_state.input_text = ''
question = st.text_input("Ask a question from the PDF you shared...")
if st.button("Go"):
    if question:
        index = create_langchain_index1(input_file)
        print("******QUESTION")
        print(question)
        # question = text_embedding(question)
        response = get_response(input_file, question)
        # response1 = collection.query(
        #     query_embeddings=question,
        #     n_results=2,
        # )
        st.write(response)
    else:
        st.warning("Please enter a question.")

st.session_state.input_text1 = ''
question1 = st.text_input("Ask a benchmark value")
if st.button("Upload"):
    if question1:
        response_content, similarity_response, sources = ask_question(question1)

        st.write(response_content, similarity_response, sources)
    else:
        benchmark_questions = ["net zero target year", "future emissions reduction % and year", "renewable energy target year and value", "circularity strategy target", "diversity, equity, inclusion target", "employee health and safety audit", "supply chain audit"]
        
        
        benchmark_results = []
        benchmarkDetails_list = []
        
        for question in benchmark_questions:
            benchmarkDetails=BenchmarkDetail(
                question=question
                ,esgType="esgType"
                ,esgIndicators="esgIndicators"
                ,primaryDetails="primaryDetails"
                ,secondaryDetails="secondaryDetails"
                ,citationDetails="citationDe"
                ,pageNumber=1
            )
            response_content, similarity_response, sources = ask_question(question)
            benchmark_results.append((response_content, similarity_response, sources))
            st.write(response_content, similarity_response, sources)