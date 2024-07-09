# PyMHW: A Python Package for Marine Heatwave Detection and Analysis
**Attention**! Still under construction!! <br>

`pymhw` is a Python package to calculate marine heatwaves (MHW) based on sea surface temperature (SST) data.<br><br>
[![DOI](https://zenodo.org/badge/818381413.svg)](https://zenodo.org/doi/10.5281/zenodo.12700290)<br>
Please, cite this DOI and check new releases.

## Installation

You can install the package using pip: <br>
`pip install git+https://github.com/andrebelem/pymhw.git`

## Usage

```python
import pandas as pd
import pymhw

# Assuming df and df_clima are your already loaded DataFrames
df2 = pymhw.detect_MHW(df, df_clima)
mhw_periods = pymhw.calculate_mhw_periods(df2)

print(mhw_periods) #<-- results are condensated in a dataframe
```

## Example Analysis
There is an example (`Test_Marine_Heat_Waves_detection.ipynb`) with an overview of how to use the pymhw package for analyzing marine heatwaves.

**Key Steps:**
- Detect MHWs: Use the detect_MHW function to preprocess and detect potential MHW events in your SST data.
- Calculate MHW Periods: Use the calculate_mhw_periods function to identify and categorize MHW periods based on their intensity.
- Visualizing MHWs: Some example of graphics you can use (on the `.ipynb` file).

**Future code:**
- Include subsurface analysis and more statistics
- Create a MHW index or impact index
- Perform wavelet analysis on MHW index

**Attention**! This repository is still under construction!! <br>                                                                                                          
                                                                                                               
