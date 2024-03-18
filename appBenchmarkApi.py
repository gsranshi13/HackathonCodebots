import json
from datetime import datetime

from fastapi import FastAPI, Query, File, HTTPException
from JsonToPDFConverter import generate_pdf

main = FastAPI()
from RequestResponsePojo import EsgResponse, BenchmarkDetail, Metrics, HealthCheckStatus,PdfOutput,Root
from fastapi import FastAPI, File, UploadFile
from google.cloud import storage
import os
from Utility import create_langchain_index1, create_langchain_index2, get_response, ask_question
import requests
from io import BytesIO

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"guru-benchmark-4cfaf5e8357e.json"



def abc(entityName: str, filePath):
    print("Code came to Hech Check Finction")

    input_file=filePath
    if input_file:
        index = create_langchain_index1(input_file)
        summary_query = "Write a 100 words summary of the pdf"
        summary_response = get_response(input_file, summary_query,index)

        tweet_query = "Write a twitter tweet about pdf"
        tweet_response = get_response(input_file, tweet_query,index)

        ln_query = "Write a linkedin post for the pdf"
        ln_response = get_response(input_file, ln_query,index)
        print(summary_response)
        print(tweet_query)
        print(ln_query)
    return summary_response,tweet_response , ln_response


def benchMarkParamsforAPI1(entityName,filePath) :
    startTime = datetime.now()
    benchmark_questions = ["net zero target year", "future emissions reduction % and year",
                           "renewable energy target year and value", "circularity strategy target",
                           "diversity, equity, inclusion target", "employee health and safety audit",
                           "supply chain audit"]


    benchmark_results = []

    benchmarkDetails_list = []
    for question in benchmark_questions:

        response_content, similarity_response, sources = ask_question(question,filePath)
        benchmark_results.append((response_content, similarity_response, sources))
        benchmarkDetails = BenchmarkDetail(
            question=question
            , esgType="esgType"
            , esgIndicators=question
            , primaryDetails=similarity_response.text
            , secondaryDetails=response_content
            , citationDetails=filePath
            , pageNumber=sources
        )
        benchmarkDetails_list.append(benchmarkDetails)
    endTime = datetime.now()
    difTime=endTime-startTime
    metrix = Metrics(
        timeTaken=int(difTime.total_seconds())
        , leveragedModel="text-bison@001"
        , f1Score=1
    )

    obj = EsgResponse(
        entityName=entityName
        , benchmarkDetails=benchmarkDetails_list
        , metrics=metrix
    )

    return obj


@main.post("/esg/benchmark/upload/", response_model=Root,
           summary="Upload ESG for given entity and retrieve all ESG benchmark")
async def benchMarkUpload(entityName: str = Query(...), documentUpload: UploadFile = File(...)):
    if documentUpload.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    ##with open(documentUpload.filename, "wb") as f:
    ##f.write(await documentUpload.read())
    print(documentUpload)
    ##abc(entityName, documentUpload.filename)
    print("Came Here")
    # Set the Google Cloud Storage bucket name
    bucket_name = "guru-storage-bucket"

    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    print("Came here1")
    # Get a reference to the bucket
    bucket = storage_client.bucket(bucket_name)
    print(documentUpload)
    print(documentUpload.file)
    print(documentUpload.filename)
    # Upload the file to the bucket
    blob = bucket.blob(documentUpload.filename)
    blob.upload_from_file(documentUpload.file)

    print("Came Here4")
    filePath = f"https://storage.googleapis.com/{bucket_name}/{documentUpload.filename}"
    response = requests.get(filePath)
    response.raise_for_status()

    # Create a file-like object from the downloaded content
    pdf_file = BytesIO(response.content)
    abc(entityName, pdf_file)
    print("Came here5")
    # Return the URL of the uploaded file
    benchObj = benchMarkParamsforAPI1(entityName, filePath)
    esgResponseList=[]
    esgResponseList.append(benchObj)
    esgResponse=Root(esgResponseList)
    ##return {"file_url": f"https://storage.googleapis.com/{bucket_name}/{documentUpload.filename}"}
    return esgResponse


@main.get("/esg/benchmark/keepalive", response_model=HealthCheckStatus)
async def health_check():
    healthCheck = HealthCheckStatus(
        status="Running"
        , message="Server is Running Healthy"
    )
    return healthCheck


@main.post("/esg/benchmark/pdf-report/", response_model=PdfOutput, summary="Upload ESG for given entity and retrieve all ESG benchmark")
async def benchmarkPdf(entityName: str = Query(...), documentUpload: UploadFile = File(...)):
    if documentUpload.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    ##with open(documentUpload.filename, "wb") as f:
    ##f.write(await documentUpload.read())
    print(documentUpload)
    ##abc(entityName, documentUpload.filename)
    print("Came Here")
    # Set the Google Cloud Storage bucket name
    bucket_name = "guru-storage-bucket"

    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    print("Came here1")
    # Get a reference to the bucket
    bucket = storage_client.bucket(bucket_name)
    print(documentUpload)
    print(documentUpload.file)
    print(documentUpload.filename)
    # Upload the file to the bucket
    blob = bucket.blob(documentUpload.filename)
    blob.upload_from_file(documentUpload.file)

    print("Came Here4")
    filePath = f"https://storage.googleapis.com/{bucket_name}/{documentUpload.filename}"
    response = requests.get(filePath)
    response.raise_for_status()

    # Create a file-like object from the downloaded content
    pdf_file = BytesIO(response.content)
    abc(entityName, pdf_file)
    print("Came here5")
    # Return the URL of the uploaded file
    benchObj = benchMarkParamsforAPI1(entityName, filePath)
    esgResponseList = []
    esgResponseList.append(benchObj)
    esgResponse = Root(esgResponseList)
    ##json_string = json.dumps(esgResponse)
    path=generate_pdf(esgResponse,entityName)
    pdfOutput=PdfOutput(
        pdfUrlPath=path
    )
    return pdfOutput


import uvicorn
