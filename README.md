# Stock Performance Generator

> [!NOTE]
> This project is still in progress.
 
This project was created to automate the analysis of a stock portfolio based on transaction history. It generates the performance of the assets in the portfolio as well as the entire portfolio and compares it with the overall market.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- [Setup](#setup)
- [Functionalities](#functionalities)
- [Technologies](#technologies)
- [Contact](#contact)

## Setup

> [!IMPORTANT]
> Prepare spreadsheets with transaction history as specified in the `data/README.md` file to run this program!

The `data/CLOSED POSITIONS.csv` file should look like this:

![Zrzut ekranu 2025-05-01 122857](https://github.com/user-attachments/assets/4fc10637-17fa-42c6-9fcc-af73d971d229)

The `data/OPEN POSITIONS.csv` file should look like this:

![Zrzut ekranu 2025-05-01 122920](https://github.com/user-attachments/assets/043ec628-a089-4bc7-b225-61189c12d755)

## Functionalities

1. Downloads data from the transaction history sheets and prepares it for analysis.
2. Creates a dataframes with the historical daily and total change of each asset in the portfolio composition.
3. Creates a dataframe with the historical daily and total change of the entire portfolio.
4. Visualizes total change and total change in PLN on charts.
5. Generates html raport with the interactive charts.

### Future features:

- Compares portfolio performance with the overall market.

## Technologies
- Python 3
- pandas
- yfinance
- plotly

## Contact
Damian Lebiedź | https://damianlebiedz.github.io/contact.html
