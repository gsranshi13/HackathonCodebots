# import requests
# from google.cloud import aiplatform
# from google.auth import credentials
#
# # Replace with your project ID, region, model endpoint, and path to JSON key file
# project_id = "liquid-streamer-417216"
# location = "us-west2"
# endpoint = aiplatform.EndpointName(project=project_id, location=location, model="textembedding-gecko@003")
# json_key_path = r"C:\Users\JOTHISHA\Downloads\liquid-streamer-417216-f06ae09841eb.json"
#
# # Load credentials from JSON key file
# credentials = credentials.from_service_account_file(json_key_path)
#
# # Create authorized HTTP session
# authorized_session = credentials.authorize(requests.Session())
#
# # Create a Vertex AI client object with authorized session
# client = aiplatform.TextEmbeddingsPredictionClient(http=authorized_session)
#
# # Your text data as a list of strings
# text_data = ["This is the first sentence.", "This is the second sentence with similar meaning."]
#
# # Prepare the request object
# instances = [{"text": text} for text in text_data]
#
# # Send the prediction request
# response = client.predict(endpoint=endpoint, instances=instances)
#
# # Process the response
# embeddings = [prediction.embeddings for prediction in response.predictions]
#
# # Print the generated embeddings
# print(embeddings)


from vertexai.language_models import TextEmbeddingModel


def text_embedding(text) -> list:
    """Text embedding with a Large Language Model."""
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([text])
    # embeddings = model.get_embeddings(["What is life?"])
    for embedding in embeddings:
        vector = embedding.values
    return vector
