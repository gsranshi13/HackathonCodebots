from vertexai.language_models import TextGenerationModel

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/Users/gurpreetsingh/Downloads/guru-benchmark-4cfaf5e8357e.json"


parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1,
    "temperature": 0.1,
    "top_p": 0.8,
    "top_k": 40
}


def sentiment_analysis(context):
    context = context

    model = TextGenerationModel.from_pretrained("text-bison@001")
    sentiment_response = model.predict(
        f"""Give me the sentiment of this text, we have two categories: positive, negative. Answer \'YES\' if positive and \'NO\' if negative.
    
    {context}""",
        **parameters
    )

    return sentiment_response
