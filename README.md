# Post-Earnings-Settlement-Analysis

The **methodology** that was used was the `price discovery completion metric` (duration-based measurement of settlement days):
1. Calculate the historical daily standard deviation or return of the stock in a period a year before its earnings release to the day of release.
2. Capture the days post-earnings compare |Δdaily(%)| to the historical SD.
3. When a day's |Δdaily(%)| < historical SD, a snapshot is created.
4. If after N consecutive days the |Δdaily(%)| remains less than the stock's historical SD, then number of settlement days would be:\
`settlement day = total time elapsed - N`
5. Else the consecutive days would reset to zero, and the days would continue until the condition mentioned in 4. is met.

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

## Summary

`data_analysis.ipynb`: holds all the functions that collect necessary data for data_analysis.ipynb to work (e.g. Earning Dates, Historical Standard Deviation, etc.) and returns each as a `pd.DataFrame`

`data_analysis.ipynb`: evaluates how many days it takes for multiple tickers to settle down post-earnings, using price discovery completion metric, then plots the results in a boxplot and frequency history.

`data_collection.py`: reference file that is imported for `data_analysis.ipynb`

**Due note**: Look at the jupyter notebooks if you want a more extensive, step-by-step explanation of what each function does.

## Project Structure

```
Work4It/
  data_analysis.py     Utilizes data found from data_collection.py
  data_collection.py    Collects foundational stock data
  README.md
```