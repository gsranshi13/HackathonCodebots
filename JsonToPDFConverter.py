from fpdf import FPDF
import json
from google.cloud import storage
import locale

from RequestResponsePojo import EsgResponse, BenchmarkDetail, Metrics, HealthCheckStatus,PdfOutput,Root


def generate_pdf(data: Root, entityName):
    # Parse JSON data
    esg_response = data.esgResponse
    ##json.loads(data)["esgResponse"]

    # Create instance of FPDF class
    pdf = FPDF()
    pdf.use_unicode = False
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add a custom font
    ##pdf.add_font("DejaVu", "", "/app/DejaVuSansCondensed.ttf", uni=True)
    ##pdf.set_font("DejaVu", size=10)

    pdf.set_font("Arial", size=16, style='B')

    # Add title
    ##pdf.cell(0, 10, "ESG Response", ln=True, align="C")
    pdf.ln()

    # Add headers
    headers = ["Entity Name", "Question", "Primary Details", "Secondary Details", "Citation Details", "Page Number"]
    col_widths = [30, 50, 30, 70, 50, 20]
    for header, col_width in zip(headers, col_widths):
        pdf.cell(col_width, 10, header, 1)
    pdf.ln()

    # Add data rows
    for entity in esg_response:
        entity_detailsList = entity.benchmarkDetails
        for benchmark_detail in entity_detailsList:
            question = str(benchmark_detail.question)
            primary_details = str(benchmark_detail.primaryDetails)
            secondary_details = str(benchmark_detail.secondaryDetails)
            citation_details = str(benchmark_detail.citationDetails)
            page_number = str(benchmark_detail.pageNumber)
            print(entityName.replace(u"\u2013", "*"))
            print(question.replace(u"\u2013", "*"))
            print(primary_details.replace(u"\u2013", "*"))
            print(secondary_details.replace(u"\u2013", "*"))
            pdf.cell(col_widths[0], 10, entityName.replace(u"\u2013", "*"), 1)
            pdf.cell(col_widths[1], 10, question.replace(u"\u2013", "*"), 1)
            pdf.cell(col_widths[2], 10, primary_details.replace(u"\u2013", "*"), 1)
            pdf.cell(col_widths[3], 10, secondary_details.replace(u"\u2013", "*"), 1)
            pdf.cell(col_widths[4], 10, citation_details.replace(u"\u2013", "*"), 1)
            pdf.cell(col_widths[5], 10, page_number, 1)
            pdf.ln()

    bucket_name = "guru-storage-bucket"
    pdf.output("outputw.pdf")
    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    print("Came here1")
    # Get a reference to the bucket
    bucket = storage_client.bucket("guru-storage-bucket")
    blob = bucket.blob("output/"+entityName + ".pdf")
    blob.upload_from_string(pdf.output(dest="S").encode("UTF-8"), content_type="application/pdf")

    # Return URL of the generated PDF file
    ##return f"PDF file uploaded to: {blob.public_url}"
    return "output.pdf"


def main(request):
    request_data = request.get_data()
    pdf_url = generate_pdf(request_data)
    return pdf_url
