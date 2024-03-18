import logging

from vertexai.language_models import TextGenerationModel

from sentimentAnalysis import sentiment_analysis

class SendToLlm:
    def runLLM(self, query, similarity_results):
        context = ""
        sources = []
        for similarity_result in similarity_results:
            context += similarity_result['content']
            sources.append(similarity_result['metadata'])

        prompt = f"Use the following pieces of context to answer the question at the end. If asked for value and year, provide the value of the latest year and the value or percentage: Context: {context}\n Question: {query}\n"

        model = TextGenerationModel.from_pretrained("text-bison@001")
        response = model.predict(prompt,).text

        logging.info(f"Retrieved response from LLM")
        
        sentiment_response = sentiment_analysis(response)

        return response, sentiment_response ,sources
