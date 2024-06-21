# pymhw
**Atenção** ! Ainda em construção !! <br>

pymhw is a Python package to calculate marine heatwaves (MHW) based on sea surface temperature (SST) data.

## Installation

You can install the package using pip: <br>
`pip install git+https://github.com/andrebelem/pymhw.git`


## Usage

```python
import pandas as pd
import pymhw

# Supondo que df e df_clima são seus DataFrames já carregados
df2 = pymhw.detect_MHW(df, df_clima)
mhw_periods = pymhw.calculate_mhw_periods(df2)

print(mhw_periods)
