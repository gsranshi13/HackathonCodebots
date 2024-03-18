from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class PdfOutput:
    pdfUrlPath :str

@dataclass
class HealthCheckStatus:
    status: str
    message: str

@dataclass
class BenchmarkDetail:
    question: str
    esgType: str
    esgIndicators: str
    primaryDetails: str
    secondaryDetails: str
    citationDetails: str
    pageNumber: int

    @staticmethod
    def from_dict(obj: Any) -> 'BenchmarkDetail':
        _question = str(obj.get("question"))
        _esgType = str(obj.get("esgType"))
        _esgIndicators = str(obj.get("esgIndicators"))
        _primaryDetails = str(obj.get("primaryDetails"))
        _secondaryDetails = str(obj.get("secondaryDetails"))
        _citationDetails = str(obj.get("citationDetails"))
        _pageNumber = int(obj.get("pageNumber"))
        return BenchmarkDetail(_question, _esgType, _esgIndicators, _primaryDetails, _secondaryDetails, _citationDetails, _pageNumber)
@dataclass
class Metrics:
    timeTaken: int
    leveragedModel: str
    f1Score: int

    @staticmethod
    def from_dict(obj: Any) -> 'Metrics':
        _timeTaken = int(obj.get("timeTaken"))
        _leveragedModel = str(obj.get("leveragedModel"))
        _f1Score = int(obj.get("f1Score"))
        return Metrics(_timeTaken, _leveragedModel, _f1Score)


@dataclass
class EsgResponse:
    entityName: str
    benchmarkDetails: List[BenchmarkDetail]
    metrics: Metrics

    @staticmethod
    def from_dict(obj: Any) -> 'EsgResponse':
        _entityName = str(obj.get("entityName"))
        _benchmarkDetails = [BenchmarkDetail.from_dict(y) for y in obj.get("benchmarkDetails")]
        _metrics = Metrics.from_dict(obj.get("metrics"))
        return EsgResponse(_entityName, _benchmarkDetails, _metrics)



@dataclass
class Root:
    esgResponse: List[EsgResponse]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _esgResponse = [EsgResponse.from_dict(y) for y in obj.get("esgResponse")]
        return Root(_esgResponse)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
