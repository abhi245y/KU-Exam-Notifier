import requests
from bs4 import BeautifulSoup as soup

req = requests.get("https://exams.keralauniversity.ac.in/Login/check3")

res = soup(req.text, "html.parser")


def fetch_from_site():
    table = res.find_all("tr")

    results = []
    for row in table:
        if "tableHeading" in row.get("class", []):
            date_text = row.find("td").text.strip()
            current_date = date_text.replace("Published on ", "").strip()
        elif "displayList" in row.get("class", []):
            details = row.find_all("td")[1].text.strip()
            pdf_link = row.find("a")["href"]
            if current_date:
                results.append(
                    {
                        "publication_date": current_date,
                        "details": details,
                        "link": pdf_link.replace(" ", "%20"),
                    }
                )
    return results
