import requests
from bs4 import BeautifulSoup as soup
from pdfreader import SimplePDFViewer

req = requests.get("https://exams.keralauniversity.ac.in/Login/check3")

res = soup(req.text, "html.parser")

table = res.find_all("tr")
results = []
# Iterate over each row
for row in table:
    if "tableHeading" in row.get("class", []):
        # Extract the date
        date_text = row.find("td").text.strip()
        current_date = date_text.replace("Published on ", "").strip()
    elif "displayList" in row.get("class", []):
        # Extract the timetable details
        details = row.find_all("td")[1].text.strip()
        pdf_link = row.find("a")["href"]
        if current_date:
            results.append({"date": current_date, "details": details, "link": pdf_link})

# Print the results
for result in results:
    print(
        f"Date: {result['date']}, Details: {result['details']}, Link: {result['link']}"
    )
    pdf_data = requests.get(result["link"]).content
    viewer = SimplePDFViewer(pdf_data)
    viewer.render()

    break
