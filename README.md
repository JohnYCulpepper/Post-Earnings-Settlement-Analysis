# Post-Earnings-Settlement-Analysis

## Methodology
### Steps for `price discovery completion metric` (duration-based measurement of settlement days):
1. Calculate the historical daily standard deviation or return of the stock in a period a year before its earnings release to the day of release.
2. Capture the days post-earnings compare | Δ daily(%) | to the Historical SD.
3. When a day's | Δ daily(%) | < historical SD, a snapshot is created.
4. Computes Lower and Upper Bound using Historical SD:\
`LB = Snapshot Day (1 - Historical SD)`\
`UB = Snapshot Day (1 + Historical SD)`
5. Compares each days Lowest and Highest Price to LB and UB, respectively:\
`LB < Lowest and UB > Highest`
6. If after N consecutive days the LB and UB condition in 5. is met, then number of settlement days would be:\
`settlement day = total time elapsed - N`
7. Else, the consecutive days would reset to zero, and the days would continue until the condition in 5. is met for all N days.

### Accounting for Event Window Discrepancies
Sometimes quarterly earnings are announcement before market opens, after close, or on non-trading days. To combat this and provide an accurate representation of time elapsed for the stock price to settle the following adjustments are set:
- After-market Announcement: The event window begins measurement one trading day after the announcement. 
- Before-market Announcement: The event window begins measurement on the day of the announcement.
- Non-trading Day Announcement: The event window is set to begin on the following trading day.

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
## Limitations

This analysis is exploratory and has several constraints that should be considered when interpreting the results.

### Data
- **Data source:** Price and earnings data come from yfinance, which is free but not research-grade. It may contain errors, missing observations, or retroactive adjustments, and it is not point-in-time data.
- **Universe selection:** S&P 500 firms are generally heavily followed by analysts, so results may not generalize to small-cap or less liquid stocks, where PEAD (Post-Earnings Announcement Drift) is typically stronger.
  
### Scope
- This project is for educational and research purposes and is not investment advice.

## Summary

`data_collection.ipynb`: holds all the functions that collect necessary data for data_analysis.ipynb to work (e.g. Earning Dates, Historical Standard Deviation, etc.) and returns each as a `pd.DataFrame`

`data_analysis.ipynb`: evaluates how many days it takes for multiple tickers to settle down post-earnings, using price discovery completion metric, then plots the results in a boxplot and frequency history.

`data_collection.py`: reference file that is imported for `data_analysis.ipynb`

**Due note**: Look at the jupyter notebooks if you want a more extensive, step-by-step explanation of what each function does.

## Project Structure

```
Post-Earnings-Settlement-Analysis/
  data_analysis.ipynb     Utilizes data found from data_collection.py
  data_collection.ipynb    Collects foundational stock data
  README.md
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'pandas'` (or `yfinance`, `matplotlib`)
The notebook's kernel is running a different Python than the one where the packages were installed.

1. Run this in a notebook cell to see which Python the kernel uses:
   ```python
   import sys
   print(sys.executable)
   ```
2. Click the kernel picker (top right of the notebook) → **Select Another Kernel** → **Python Environments**, then choose the `.venv` inside this project folder.
3. If packages are still missing, install them into that environment and restart the kernel:
   ```
   python -m pip install -r requirements.txt
   python -m pip install ipykernel
   ```

### "The kernel failed to start as the Python Environment is no longer available"
The saved interpreter was moved, deleted, or upgraded.

- Run `Python: Select Interpreter` from the VS Code Command Palette (`Ctrl/Cmd+Shift+P`) and pick the `.venv` interpreter.
- If the `.venv` is broken, delete it and recreate it using the steps in **Getting Started**.
- Run `Developer: Reload Window` if the old kernel still shows up.

### `ModuleNotFoundError: No module named 'data_collection'`
The notebook can't find `data_collection.py`. Open the **project folder** in VS Code (File → Open Folder) so the notebook runs from the same directory as the script.

### Virtual environment won't activate on Windows
If PowerShell blocks `.venv\Scripts\activate`, run this once in the same terminal, then activate again:
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Lots of `Pandas4Warning: The inplace keyword ... is deprecated`
These come from inside `yfinance`, not from this project, and they don't affect results. To reduce them, upgrade yfinance:
```
python -m pip install --upgrade yfinance
```
To hide them, add this at the top of the notebook (already added):
```python
import warnings
warnings.filterwarnings("ignore", message=".*inplace.*")
```

### Empty data, `possibly delisted`, or rate-limit errors from yfinance
- Check your internet connection and the ticker spelling.
- Confirm the ticker was publicly traded for the whole date range. Tickers that IPO'd later or changed symbols return no data for the earlier years.
- Wait a few minutes and rerun if Yahoo is rate limiting you, and avoid downloading tickers one at a time in a loop.
- Upgrade yfinance, since Yahoo changes its endpoints often.

### A ticker is missing or `NaN` in the results
The stock either had no price data around that earnings date, or it never met the settlement condition within the available window. Check the raw data for that ticker and quarter.

### Changes don't show up on GitHub
You may have committed but not pushed.
```
git remote -v     # confirms the repo you're connected to
git status        # shows if you're ahead of origin
git push
```
