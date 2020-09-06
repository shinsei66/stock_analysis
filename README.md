# Introduction
This repository shows how to create daily stock asset price data by cleansing the trading historical data downloaded from SBI securities, calling stock prices and the FX rate by utilizing yfinance and forex-python.

## Repository contents
### Codes
- stock_asset.py
- stock_hist_data.py
- stock_price_hist.py
- config.py

### Inputs

### Outputs

# Usage
There are 4 steps as follows that is really simple.
1. Install the required packages.
2. Download the input trading historical data from SBI securities and place them in the this repository.
3. Dowload the monthly detail asset data from moneyforward.
4. Change the setting parameter and file names within the "config.py".
    - partition
5. Run codes.
6. Copy and paste the output file : asset_history_stack_{partition}.csv to the google spread sheet

## Install requirement.txt

```
pip install -r requirements.txt
```
## Dowload input data


## Update config.py
Update the input file names, output file names and the directory path within the "config.py".

## Run
```
python stock_asset.py
```