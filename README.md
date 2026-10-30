# Post-Earnings-Settlement-Analysis

## Requirements

- Git 
- Python 3.12 or newer
- VS Code (other Python IDE)

## Getting Started

1. Clone the GitHub repository once.
```
git clone https://github.com/JohnYCulpepper/Post-Earnings-Settlement-Analysis.git
```
2. Open a terminal in that folder and create a virtual environment.

    Windows:
    ```
    python -m venv .venv
    .venv\Scripts\activate
    ```

    Mac/Linux:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Explanation

`data_analysis.ipynb`: holds all the functions that collect necessary data for data_analysis.ipynb to work (e.g. Earning Dates, Historical Standard Deviation, etc.) and returns each as a `pd.DataFrame`

`data_analysis.ipynb`: evaluates how many days it takes for the tickers to settle down post-earnings, using price discovery completion metric, then plots the results in a boxplot and frequency history.

## Project Structure

```
Work4It/
  data_analysis.py     Utilizes data found from data_collection.py
  data_collection.py    Collects foundational stock data
  README.md
```