import re
import html
import requests
import json
import bs4


class Cardinals:
    # def __init__(self):
    #     self.cardinals = self.get_cardinals()

    def get_cardinals(self):
        headers = {
            "accept": 'text/html; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/HTML/2.1.0"',
        }
        response = requests.get(
            "https://en.wikipedia.org/api/rest_v1/page/html/List_of_current_cardinals",
            headers=headers,
        )
        html_dump = response.content

        # Use BeautifulSoup
        soup = bs4.BeautifulSoup(html_dump, "html.parser")
        # Get table
        table = soup.find("table")

        # Get headers from table
        headers = []
        for header in table.find_all("th"):
            headers.append(header.text)

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
                cardinal[headers[i]] = cell.text

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
            cardinal["Born"] = cardinal["Born"].split("(")[0]
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

        # # Create a list of dictionaries
        # cardinals = []
        # for row in rows:
        #     cells = row.find_all("td")
        #     if len(cells) == 0:
        #         continue

        #     regex = r"([0-9]{4})"

        #     cardinal = {
        #         "Rank": cells[0].text,
        #         "Name": cells[1].text,
        #         "Country": cells[2].text,
        #         "DateOfBirth": cells[3].text.split("(")[0],
        #         "Order": cells[4].text,
        #         "ConsistoryDate": "".join(
        #             [
        #                 re.split(regex, cells[5].text)[0],
        #                 re.split(regex, cells[5].text)[1],
        #             ]
        #         ),
        #         "CreatedCardinalBy": re.split(regex, cells[5].text)[-1],
        #         "Office": cells[6].text,
        #     }

        #     # If name has asterisk, mark ineligible for conclave
        #     if "*" in cardinal["Name"]:
        #         cardinal["PapalConclaveEligible"] = False
        #     else:
        #         cardinal["PapalConclaveEligible"] = True
        #     # If Office has anything but alphanumeric characters, remove it
        #     if not cardinal["Office"].isalnum():
        #         cardinal["Office"] = cardinal["Office"].split("[")[0]
        #     # If name has an asterisk, remove it
        #     if "*" in cardinal["Name"]:
        #         cardinal["Name"] = cardinal["Name"].replace("*", "")
        #     # If CreatedCardinalBy has brackets and text, remove it, also decode unicode
        #     if "[" in cardinal["CreatedCardinalBy"]:
        #         cardinal["CreatedCardinalBy"] = (
        #             re.split("(\[.*?\])", cardinal["CreatedCardinalBy"])[-1]
        #             .encode("utf-8")
        #             .decode("ascii", "ignore")
        #         )

        #     cardinals.append(cardinal)

        return json.dumps({"cardinals": cardinals})


if __name__ == "__main__":
    cardinals = Cardinals()
    print(cardinals.get_cardinals())
