import pandas as pd
import numpy as np

def detect_MHW(df, df_clima, freq='1D'):
    # Make a copy of the DataFrame to ensure that the original will not be modified.
    df2 = df.copy()
    df2_clima = df_clima.copy()

    # Verify if the index is a DatetimeIndex
    if not isinstance(df2.index, pd.DatetimeIndex):
        try:
            df2.index = pd.to_datetime(df2.index)
        except Exception as e:
            raise ValueError("The index cannot be converted to a DatetimeIndex.") from e

    # Generate an expected regular index based on the provided frequency.
    expected_index = pd.date_range(start=df2.index.min(), end=df2.index.max(), freq=freq)

    # Reindex the DataFrame to ensure it is regular.
    df2 = df2.reindex(expected_index)

    # Some basic statistics: 
    # Calculate the time differences between entries in the original index.
    time_diffs = df.index.to_series().diff().dropna()

    # Calculate the mode of the time differences.
    dominant_freq = time_diffs.mode()[0]

    # Compare the dominant frequency with the expected frequency
    expected_freq = pd.Timedelta(freq)
    if dominant_freq != expected_freq:
        raise ValueError(f"The dominant frequency of the data ({dominant_freq}) does not match the expected frequency ({expected_freq}).")
    
    # Additional statistics
    start_date = df2.index.min()
    end_date = df2.index.max()
    num_points = len(df2)
    num_nans = df2.isna().sum().sum()  # Total number of NaNs
    percent_nans = (num_nans / df2.size) * 100  # Percentage of NaNs
    
    # Print the statistics
    print(f"Series from {start_date} to {end_date}")
    print(f"Dominant frequency: {dominant_freq}")
    print(f"Number of points: {num_points}")
    print(f"Number of NaNs: {num_nans}")
    print(f"Percentage of NaNs: {percent_nans:.2f}%")

    # Remove the time index and insert dayofyear
    df2 = df2.reset_index().rename(columns={'index':'time'})
    df2['dayofyear'] = df2.time.dt.dayofyear
    
    # Calculate the anomaly and compare with std
    df2['anomaly'] = df2.apply(lambda row: row['sst'] - df_clima.loc[row['dayofyear'], ('sst', 'mean')], axis=1)
    df2['zscore'] = df2.apply(lambda row: row['anomaly'] / df_clima.loc[row['dayofyear'], ('sst', 'std')], axis=1)
    
    # Identify periods where the zscore is greater than 1.28 (90%)
    df2['above_90'] = df2['zscore'] > 1.28
    
    return df2

def calculate_mhw_periods(df2):
    # Define intensity categories based on z-score thresholds
    categories = [
        (1, 1.28),
        (2, 1.645),
        (3, 2.054),
        (4, 2.33)
    ]
    
    mhw_periods_list = []
    
    for category, threshold in categories:
        df2['above_threshold'] = df2['zscore'] > threshold
        
        # Identify the durations of periods where the zscore is greater than the threshold
        df2['mhw_id'] = (df2['above_threshold'] != df2['above_threshold'].shift()).cumsum()
        mhw_periods = df2[df2['above_threshold']].groupby('mhw_id').agg(
            start=('time', 'min'),
            end=('time', 'max'),
            duration=('time', 'count'),
            max_zscore=('zscore', 'max'),
            cum_zscore=('zscore', 'sum')
        ).reset_index(drop=True)
        
        # Filter out periods with duration less than or equal to 5 days
        mhw_periods = mhw_periods[mhw_periods['duration'] > 5]
        
        # Assign the category to the mhw_periods
        mhw_periods['category'] = category
        
        mhw_periods_list.append(mhw_periods)
    
    # Concatenate all mhw_periods into a single dataframe
    mhw_periods_all = pd.concat(mhw_periods_list, ignore_index=True)
    
    # Rename max_zscore to I_max and cum_zscore to I_cum for each MHW period
    mhw_periods_all = mhw_periods_all.rename(columns={'max_zscore': 'I_max', 'cum_zscore': 'I_cum'})
    
    return mhw_periods_all

