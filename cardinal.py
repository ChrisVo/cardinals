import re
import requests
import json
import bs4
import unicodedata


class Cardinals:
    def get_cardinals(self):
        """
        Get a list of cardinals from Wikipedia
        """
        headers = {
            "User-Agent": "CardinalsScraper/1.0 (Educational/Research Purpose)",
        }
        response = requests.get(
            "https://en.wikipedia.org/wiki/List_of_current_cardinals",
            headers=headers,
        )
        html_dump = response.content

        # Use BeautifulSoup
        soup = bs4.BeautifulSoup(html_dump, "html.parser")
        # Get table (first wikitable on the page)
        table = soup.find("table", {"class": "wikitable"})

        # Get headers from table
        table_headers = []
        for header in table.find_all("th"):
            table_headers.append(header.text.strip())

        # Grab rows of data
        rows = table.find_all("tr")

        # Create a list of dictionaries
        cardinals = []
        regex = r"([0-9]{4})"
        for row in rows:

            cells = row.find_all("td")
            if len(cells) == 0:
                continue

            cardinal = {}
            for i, cell in enumerate(cells):
                # Normalize text: clean up special characters
                text = cell.text.strip()
                # Normalize to NFC to keep accented characters composed
                text = unicodedata.normalize('NFC', text)
                # Replace various unicode spaces with regular space
                text = re.sub(r'[\u00a0\u2000-\u200b\u202f\u205f\u3000]', ' ', text)
                # Remove zero-width characters
                text = re.sub(r'[\u200b-\u200d\ufeff]', '', text)
                # Collapse multiple spaces into one
                text = re.sub(r'\s+', ' ', text).strip()
                cardinal[table_headers[i]] = text

            # Remove the Ref. key from the dictionary
            cardinal.pop("Ref.", None)
            # If name has asterisk, mark ineligible for conclave
            if "*" in cardinal["Name"]:
                cardinal["PapalConclaveEligible"] = False
            else:
                cardinal["PapalConclaveEligible"] = True
            # If Office has anything but alphanumeric characters, remove it
            if not cardinal["Office"].isalnum():
                cardinal["Office"] = cardinal["Office"].split("[")[0]
            # If name has an asterisk, remove it
            if "*" in cardinal["Name"]:
                cardinal["Name"] = cardinal["Name"].replace("*", "")
            # Remove (age) from DateOfBirth
            cardinal["Born"] = cardinal["Born"].split("(")[0].strip()
            cardinal["CreatedCardinalBy"] = "Pope " + re.sub(
                r"\[.*?\]", "", re.split(regex, cardinal["Consistory"])[2]
            )
            cardinal["Consistory"] = "".join(
                [
                    re.split(regex, cardinal["Consistory"])[0],
                    re.split(regex, cardinal["Consistory"])[1],
                ]
            )

            cardinals.append(cardinal)
        return json.dumps({"Cardinals": cardinals}, ensure_ascii=False)


if __name__ == "__main__":
    cardinals = Cardinals()
    print(cardinals.get_cardinals())
