import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*inplace.*")

import yfinance as yf
import pandas as pd

# Look at data_collection_nb.ipynb for more indepth explanations and examples
def collect_stock_data(
        tickers: list[str],
        year: int,
        interval: str = "1d"
        ) -> pd.DataFrame | None:
    """
    Downloads price data for multiple tickers over a given year,
    calculates daily returns and a bid-ask spread proxy, and
    reshapes the result into long format (Date, Ticker as rows).

    Returns:
        pd.DataFrame in long format with columns:
        Open, High, Low, Close, Volume, Return, Spread_Proxy
        indexed by (Date, Ticker)
    """
    try:
        start_date = pd.Timestamp(f'{year}-01-01')
        end_date = pd.Timestamp(f'{year+1}-01-1')

        df = yf.download(tickers, start=start_date, end=end_date,
                          interval=interval, auto_adjust=True,
                          progress=False)
        # SAFETY CHECK: Checks whether Yahoo Finance has the data avaliable for tickers
        if df.empty:
            print(f"No data returned for {tickers} in {year}")
            return None

        # Daily returns per ticker
        returns = df['Close'].pct_change()
        returns.columns = pd.MultiIndex.from_product(
            [['Return'], returns.columns], names=['Field', 'Ticker']
        )
        df = pd.concat([df, returns], axis=1)

        # Bid-ask spread proxy per ticker
        spread_values = (df['High'].values - df['Low'].values) / df['Close'].values
        spread_proxy = pd.DataFrame(
            spread_values,
            index = df.index,
            columns=pd.MultiIndex.from_product(
                [['Spread_Proxy'], df['Close'].columns],
                names=['Field', 'Ticker']
            )
        )
        df = pd.concat([df, spread_proxy], axis=1)

        # Reshape from wide MultiIndex to long format
        df_long = df.stack(level='Ticker', future_stack=True)

        return df_long

    except Exception as e:
        print(f"Failed to retrieve data for {tickers}: {e}")
        return None

def tickers_earnings_long(
    tickers: list[str],
    year: int
) -> pd.DataFrame | None:
    """
    Retrieves earnings dates for multiple tickers and returns
    them in long format: one row per ticker-quarter event.
    
    Long format columns:
        earnings_date (index), ticker, quarter, timing
    """
    earnings_data = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            earnings_df = stock.get_earnings_dates(limit=100)

            # SAFETY CHECK: Checks whether earnings_df is empty
            if earnings_df is None or earnings_df.empty:
                print(f"* {ticker}: no earnings data available")
                continue

            qe_df = earnings_df[earnings_df.index.year == year].copy()

            # SAFETY CHECK: Checks whether qe_df is empty
            if qe_df.empty:
                print(f"* {ticker}: no earnings in {year}")
                continue

            # Tag with Ticker and Quarter — long format identifiers
            qe_df['Ticker'] = ticker
            qe_df['Quarter'] = qe_df.index.quarter.map(
                {1: '1', 2: '2', 3: '3', 4: '4'}
            )

            # Delete EPS columns
            del qe_df['EPS Estimate'], qe_df['Reported EPS'], qe_df['Surprise(%)']
            
            earnings_data.append(qe_df)

        except Exception as e:
            print(f"* {ticker}: failed — {e}")
            continue

    if not earnings_data:
        return None

    # Stack every ticker's rows into one long table
    long_table = pd.concat(earnings_data, ignore_index=False)

    
    return long_table.sort_values(by=['Ticker', 'Quarter'])

def tickers_historical_sd(
        tickers: list[str],
        earnings_dates: pd.DataFrame,
        interval: str = '1d',
    ) -> pd.DataFrame:
    """
    Calculates the historical standard deviation (s.d.) of daily
    returns for multiple tickers, using a 365-calendar-day window
    ending the day before each respective quarterly earnings call.

    Returns:
        pd.DataFrame with columns: Ticker, Quarter, Earnings Date,
        Historical Standard Deviation
    """
    results = []

    for ticker in tickers:
        # Gets earnings dates for each ticker
        ticker_qe_dates = earnings_dates[earnings_dates['Ticker'] == ticker]
        
        for quarter in range(1, 5):
            try:
                # Looking to specific Quarter
                quarter_match = ticker_qe_dates[ticker_qe_dates['Quarter'] == str(quarter)].index

                if len(quarter_match) == 0:
                    print(f"* No earnings date for {ticker} Q{quarter}")
                    continue

                date = quarter_match[0]

                start_date = date - pd.Timedelta(days=365)
                end_date = date

                df = yf.download(
                    ticker, start=start_date, end=end_date,
                    interval=interval, auto_adjust=True, progress=False
                )

                if df.empty:
                    print(f"* No price data for {ticker} Q{quarter}")
                    continue

                sd_val = df['Close'].pct_change().std()

                results.append({
                    'Earnings Date': date,
                    'Ticker': ticker,
                    'Quarter': quarter,
                    'Historical SD': sd_val   # Historical Standard Deviation (SD)
                })

            except Exception as e:
                print(f"* {ticker} Q{quarter}: {e}")
                continue
    historical_sd = pd.DataFrame(results)
    return historical_sd