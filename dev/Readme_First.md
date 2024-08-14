# MARINE HEAT WAVES: A Practical Development Guide

This directory was created with the purpose of organizing and facilitating the theoretical discussion and practical application of a statistical strategy for determining the duration and intensity of Marine Heat Waves (MHW). The starting point for this approach is the work of Hobday et al. (2016), [*Hobday, A. J., Alexander, L. V., Perkins, S. E., Smale, D. A., Straub, S. C., Oliver, E. C., ... & Wernberg, T. (2016). A hierarchical approach to defining marine heatwaves. Progress in Oceanography, 141, 227-238.*](https://www.sciencedirect.com/science/article/pii/S0079661116000057), which provides a well-known basis for the analysis and understanding of these extreme events in the ocean.

## Directory Structure
This folder is divided into Data and a Jupyter Notebook used for the development of the pymhw library. They are:

- `Detection_Marine_Heat_Waves.ipynb`: Notebook containing the theoretical development
- `tupi_OSTIA_sst.parquet`: Time series of the Tupi field in the Santos Basin (South Atlantic Bight)
- `oisst_1982_2011.parquet`: SST time series obtained by OISST at the position 0°N 0°E (coincident with the PIRATA buoy)
- `pirata0n0e.parquet`: SST time series obtained by the PIRATA buoy at the position 0°N 0°E
