# Catholic Cardinals in JSON
List of Roman Catholic Cardinals in `json` format.

To download the latest list of Cardinals, please go to the [releases page](https://github.com/ChrisVo/cardinals/releases), and download the `cardinals.json` file.

## Automated Updates

This repository automatically scrapes cardinal data from Wikipedia **daily at midnight UTC**. When changes are detected:
- The `cardinals.json` file is updated
- A new release is created with the updated data
- Changes are logged in [CHANGELOG.md](CHANGELOG.md)

The workflow detects:
- **New Cardinals** - Recently appointed cardinals
- **Removed Cardinals** - Cardinals who have passed away or resigned
- **Modified Cardinals** - Changes to existing cardinal information (title, office, etc.)

An example of an JSON object:

```
    {
      "Rank": "1",
      "Name": "Giovanni Battista Re",
      "Country": "Italy",
      "Born": "30 January 1934",
      "Order": "CB",
      "Consistory": "21 February 2001",
      "Office": "Prefect emeritus of the Congregation for Bishops",
      "PapalConclaveEligible": false,
      "CreatedCardinalBy": "Pope John Paul II"
    }
```

---

## Requirements
- Python3+

## Usage

1. Clone this repository
2. Install dependencies

    `pip install -r requirements.txt`

3. Run script

    `python cardinal.py`

---
## Sources
[The data is scraped from the "list of cardinals" Wikipedia page](https://en.wikipedia.org/wiki/List_of_current_cardinals)