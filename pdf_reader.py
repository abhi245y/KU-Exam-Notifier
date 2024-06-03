import fitz  # PyMuPDF
import requests
from io import BytesIO


# Fetch the PDF content from the URL
pdf_url = "https://exams.keralauniversity.ac.in/Images/Time%20Table/2024/06/69656.pdf"
response = requests.get(pdf_url)
pdf_content = response.content

# Save the PDF content to a temporary file-like object

pdf_stream = BytesIO(pdf_content)

# Open the PDF with PyMuPDF
doc = fitz.open(stream=pdf_stream, filetype="pdf")
text = ""
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text += page.get_text()

print(text)
