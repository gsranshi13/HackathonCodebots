import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_google_vertexai import VertexAI
from langchain_google_vertexai import VertexAIEmbeddings
import PyPDF2
import requests
from io import BytesIO

import spacy
import uuid

from embeddings import text_embedding

from chroma import collection
from sendtollm import SendToLlm

from RequestResponsePojo import EsgResponse, BenchmarkDetail, Metrics, HealthCheckStatus

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

    response = requests.get(input_file)
    response.raise_for_status()

    # Create a file-like object from the downloaded content
    pdf_file = BytesIO(response.content)

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        text = page.extract_text()
        paragraphs = text.split('\n')

        for i in range(0, len(paragraphs), chunk_size - overlap):
            chunk = ' '.join(paragraphs[i:i + chunk_size])
            if len(chunk.strip()) > 0:
                chunk_vector = text_embedding(chunk)  # Assuming text_embedding is defined elsewhere
                chunks_with_page_and_id.append((page_number + 1, chunk_id, chunk, chunk_vector))
                chunk_id += 1

    return chunks_with_page_and_id


def chunk_data_with_page_and_id1(input_file, chunk_size, overlap):
    chunks_with_page_and_id = []
    chunk_id = 0
    print("Input File")
    print(input_file)
    pdf_reader = PyPDF2.PdfReader(input_file)

    with open("/tmp/temp.txt", "w", encoding='utf-8') as file:
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            file.write(page.extract_text() + "\n")
            text = page.extract_text()
            paragraphs = text.split('\n')
            for i in range(0, len(paragraphs), chunk_size - overlap):
                chunk = ' '.join(paragraphs[i:i + chunk_size])
                if len(chunk.strip()) > 0:
                    chunk_vector = text_embedding(chunk)  # Assuming text_embedding is defined elsewhere
                    chunks_with_page_and_id.append((page_number + 1, chunk_id, chunk, chunk_vector))
                    chunk_id += 1
    print("chunks_with_page_and_id")
    print(chunks_with_page_and_id)
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
        metadata.append({'page_number': page_number})
        documents.append(chunk_text)
        ids.append(str(uuid.uuid4()))

    collection.add(
        documents=documents,
        embeddings=vectorEmbeddings,
        metadatas=metadata,
        ids=ids
    )



def create_langchain_index1(input_file):
    print("--indexing---")
    chunk = chunk_data_with_page_and_id1(input_file, 1000, 100)
    loader = TextLoader("/tmp/temp.txt", encoding='utf-8')
    print(embeddings)

    index = VectorstoreIndexCreator(vectorstore_cls=DocArrayInMemorySearch, embedding=embeddings).from_loaders([loader])
    return index

def get_response(input_text, query,index):
    print(f"--querying---{query}")
    response = index.query(query, llm=llm)
    return response



def ask_question(question1,input_file):
    create_langchain_index2(input_file)
    questionembedding = text_embedding(question1)
    response1 = collection.query(
        query_embeddings=questionembedding,
        n_results=2,
    )
    similarity_results = []
    for index in range(0, 2):
        context = response1["documents"][0][index]
        metadata = response1["metadatas"][0]
        page_number = metadata[index]["page_number"]
        similarity_results.append({"content": context, "metadata": page_number})

    instance = SendToLlm()

    # Call the runLLM method
    response_content, similarity_response, sources = instance.runLLM(question1, similarity_results)

    return response_content, similarity_response, sources

