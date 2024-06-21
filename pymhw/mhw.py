import pandas as pd
import numpy as np

def detect_MHW(df, df_clima, freq='1D'):
    # Faz uma cópia do DataFrame para garantir que o original não será modificado
    df2 = df.copy()
    df2_clima = df_clima.copy()

    # Verifica se o índice é um DatetimeIndex
    if not isinstance(df2.index, pd.DatetimeIndex):
        try:
            df2.index = pd.to_datetime(df2.index)
        except Exception as e:
            raise ValueError("O índice não pode ser convertido para DatetimeIndex.") from e

    # Gera um índice regular esperado com base na frequência fornecida
    expected_index = pd.date_range(start=df2.index.min(), end=df2.index.max(), freq=freq)

    # Reindexa o DataFrame para garantir que ele esteja regular
    df2 = df2.reindex(expected_index)

    # Calcula as diferenças de tempo entre as entradas do índice original
    time_diffs = df.index.to_series().diff().dropna()

    # Calcula a moda das diferenças de tempo
    dominant_freq = time_diffs.mode()[0]

    # Compara a frequência dominante com a frequência esperada
    expected_freq = pd.Timedelta(freq)
    if dominant_freq != expected_freq:
        raise ValueError(f"A frequência dominante dos dados ({dominant_freq}) não corresponde à frequência esperada ({expected_freq}).")

    # Estatísticas adicionais
    start_date = df2.index.min()
    end_date = df2.index.max()
    num_points = len(df2)
    num_nans = df2.isna().sum().sum()  # Número total de NaNs
    percent_nans = (num_nans / df2.size) * 100  # Percentual de NaNs

    # Impressão das estatísticas
    print(f"Série de {start_date} até {end_date}")
    print(f"Frequência dominante: {dominant_freq}")
    print(f"Número de pontos: {num_points}")
    print(f"Número de NaNs: {num_nans}")
    print(f"Percentual de NaNs: {percent_nans:.2f}%")

    # Retira o time de index e insere dayofyear
    df2 = df2.reset_index().rename(columns={'index':'time'})
    df2['dayofyear'] = df2.time.dt.dayofyear

    # Calcula a anomalia e compara com std
    df2['anomaly'] = df2.apply(lambda row: row['sst'] - df_clima.loc[row['dayofyear'], ('sst', 'mean')], axis=1)
    df2['zscore'] = df2.apply(lambda row: row['anomaly'] / df_clima.loc[row['dayofyear'], ('sst', 'std')], axis=1)

    # Identificar períodos onde o zscore é maior que 1
    df2['above_1'] = df2['zscore'] > 1

    return df2

def calculate_mhw_periods(df2):
    # Identificar as durações dos períodos em que o zscore é maior que 1
    df2['mhw_id'] = (df2['above_1'] != df2['above_1'].shift()).cumsum()
    mhw_periods = df2[df2['above_1']].groupby('mhw_id').agg(
        start=('time', 'min'),
        end=('time', 'max'),
        duration=('time', 'count'),
        max_zscore=('zscore', 'max')
    ).reset_index(drop=True)

    # Definir graus de intensidade com base no zscore
    mhw_periods['intensity'] = mhw_periods['max_zscore'].apply(lambda x: int(min(max(x, 1), 5)))

    return mhw_periods
