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
<<<<<<< HEAD
```
=======
```
>>>>>>> 62a7509e8af4d7a4fa44c223cc7a1e7692592cc8
