from fastapi import FastAPI,Query
main = FastAPI()
from RequestResponsePojo import EsgResponse,BenchmarkDetail,Metrics,HealthCheckStatus
from fastapi import FastAPI, File, UploadFile






@main.post("/esg/benchmark/upload/",response_model=EsgResponse ,summary="Upload ESG for given entity and retrieve all ESG benchmark" )
async def health_check(entityName: str = Query(...),documentUpload: UploadFile = File(...)):
    with open(documentUpload.filename, "wb") as f:
        f.write(await documentUpload.read())


    benchmarkDetails=BenchmarkDetail(
        question="what is your name "
        ,esgType="esgType"
        ,esgIndicators="esgIndicators"
        ,primaryDetails="primaryDetails"
        ,secondaryDetails="secondaryDetails"
        ,citationDetails="citationDe"
        ,pageNumber=1
    )
    metrix=Metrics(
        timeTaken=10
        ,leveragedModel="leveragedModel"
        ,f1Score=1
    )
    benchmarkDetails_list = []
    benchmarkDetails_list.append(benchmarkDetails)
    obj = EsgResponse(
        entityName=entityName
        ,benchmarkDetails=benchmarkDetails_list
        ,metrics=metrix
    )
    return obj



@main.get("/esg/benchmark/keepalive",response_model=HealthCheckStatus)
async def health_check():
    healthCheck = HealthCheckStatus(
        status="Running"
        ,message="Server is Running Healthy"
    )
    return healthCheck


@main.get("/health3", tags=["Health"])
async def health_check():
    return {"status": "healthy3"}




@main.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Uploads a PDF file.

    Args:
        file (UploadFile): The PDF file to upload.

    Returns:
        dict: A dictionary containing the filename of the uploaded file.
    """
    file_data = await file.read()
    with open(file.filename, "wb") as f:
        f.write(file_data)
    return {"filename": file.filename}


import uvicorn
##uvicorn.run(main, host="0.0.0.0", port=8000)
