from fpdf import FPDF

# Sample JSON data

data = {
      "entityName": "Wellsfargo",
      "benchmarkDetails": [
        {
          "question": "net zero target year",
          "esgType": "esgType",
          "esgIndicators": "net zero target year",
          "primaryDetails": "YES",
          "secondaryDetails": "The net zero target year is 2050.",
          "citationDetails": "https://storage.googleapis.com/guru-storage-bucket/2022-Regal-Rexnord-Sustainability-Report (1)-1.pdf",
          "pageNumber": [
            1,
            1
          ]
        },
        {
          "question": "future emissions reduction % and year",
          "esgType": "esgType",
          "esgIndicators": "future emissions reduction % and year",
          "primaryDetails": "YES",
          "secondaryDetails": "The company has committed to reducing its greenhouse gas emissions by 50% by 2030.",
          "citationDetails": "https://storage.googleapis.com/guru-storage-bucket/2022-Regal-Rexnord-Sustainability-Report (1)-1.pdf",
          "pageNumber": [
            2,
            2
          ]
        },
        {
          "question": "renewable energy target year and value",
          "esgType": "esgType",
          "esgIndicators": "renewable energy target year and value",
          "primaryDetails": "NO",
          "secondaryDetails": "The renewable energy target year is 2025 and the value is 10%.",
          "citationDetails": "https://storage.googleapis.com/guru-storage-bucket/2022-Regal-Rexnord-Sustainability-Report (1)-1.pdf",
          "pageNumber": [
            2,
            2
          ]
        },
        {
          "question": "circularity strategy target",
          "esgType": "esgType",
          "esgIndicators": "circularity strategy target",
          "primaryDetails": "YES",
          "secondaryDetails": "The circularity strategy target is to achieve 100% circularity by 2030.",
          "citationDetails": "https://storage.googleapis.com/guru-storage-bucket/2022-Regal-Rexnord-Sustainability-Report (1)-1.pdf",
          "pageNumber": [
            1,
            1
          ]
        },
        {
          "question": "diversity, equity, inclusion target",
          "esgType": "esgType",
          "esgIndicators": "diversity, equity, inclusion target",
          "primaryDetails": "YES",
          "secondaryDetails": "The company has a target of 50% women in leadership positions by 2030.",
          "citationDetails": "https://storage.googleapis.com/guru-storage-bucket/2022-Regal-Rexnord-Sustainability-Report (1)-1.pdf",
          "pageNumber": [
            1,
            1
          ]
        },
        {
          "question": "employee health and safety audit",
          "esgType": "esgType",
          "esgIndicators": "employee health and safety audit",
          "primaryDetails": "YES",
          "secondaryDetails": "The company conducts employee health and safety audits. The company also conducts regulatory audit findings, significant near miss reporting, and safety walks of our sites focused on identifying health and safety improvements.",
          "citationDetails": "https://storage.googleapis.com/guru-storage-bucket/2022-Regal-Rexnord-Sustainability-Report (1)-1.pdf",
          "pageNumber": [
            1,
            1
          ]
        },
        {
          "question": "supply chain audit",
          "esgType": "esgType",
          "esgIndicators": "supply chain audit",
          "primaryDetails": "performance",
          "secondaryDetails": "The text states that \"Regal Rexnord MEASURES SAFETY  PERFORMANCE GLOBALLY  Total Recordable Rate (TRR) and Days Away From Work, Job Restriction, or Transfer (DART) are two primary indicators  that Regal Rexnord uses to measure safety performance globally. We use the current (2020) U.S. Bureau of Labor  Statistics incidence rates tables in order to benchmark our performance compared with companies operating in  industries we believe align closely with our core businesses * motor and power transmission product manufacturing. We  proudly continue to outperform our peers in both of these industries.  Despite our strong",
          "citationDetails": "https://storage.googleapis.com/guru-storage-bucket/2022-Regal-Rexnord-Sustainability-Report (1)-1.pdf",
          "pageNumber": [
            1,
            1
          ]
        }
      ],
      "metrics": {
        "timeTaken": 95,
        "leveragedModel": "text-bison@001",
        "f1Score": 1
      }
    }


# Create PDF object
pdf = FPDF()
pdf.add_page()

# Set font for title
pdf.set_font("Arial", size=16, style='B')

# Add title
pdf.cell(200, 10, txt="Entity Name: " + data["entityName"], ln=True, align='L')

# Set font for content
pdf.set_font("Arial", size=12)

# Add benchmark details
for benchmark in data["benchmarkDetails"]:

    pdf.cell(200, 10, txt=f"Question: {benchmark['question']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Esg Type: {benchmark['esgType']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Esg Indicators: {benchmark['esgIndicators']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Primary Details: {benchmark['primaryDetails']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Secondary Details: {benchmark['secondaryDetails']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Citation Details: {benchmark['citationDetails']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Page Number: {benchmark['pageNumber']}", ln=True, align='L')
    pdf.ln()
    pdf.ln()
    pdf.ln()

# Add metrics
pdf.cell(200, 10, txt=f"Time Taken: {data['metrics']['timeTaken']}", ln=True, align='L')
pdf.cell(200, 10, txt=f"Leveraged Model: {data['metrics']['leveragedModel']}", ln=True, align='L')
pdf.cell(200, 10, txt=f"F1 Score: {data['metrics']['f1Score']}", ln=True, align='L')

# Save the PDF
pdf.output("output.pdf")