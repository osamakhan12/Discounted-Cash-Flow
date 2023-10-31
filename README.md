# DCF: Discounted Cash Flow Python Library

## Overview

This Python library facilitates the calculation of discounted cash flows (DCF) directly from a company's financial statements. Its primary goal is to provide a tool for users to explore the impact of different assumptions on the valuation and compare it to historical trading patterns.

## Features

- Direct forecasting of Free Cash Flows (FCF) based on configurable variables.
- Historical DCF calculations for in-depth analysis.
- Sensitivity analysis through configurable variable adjustments.
- Comparison of stock trading patterns to intrinsic value.

## Dependencies

Ensure you have the following dependencies installed:

bash
pip install matplotlib urllib3 seaborn


Basic Usage
As of now, command line arguments are used to parse parameters. See main.py for default values. Here is a description of the parameters:

bash
Copy code
python main.py \
        --period        
        --ticker        
        --years         
        --interval      
        --step_increase 
        --steps         
        --variable      
        --discount_rate 
        --earnings_growth_rate 
        --perpetual_growth_rate
        --apikey
For example:

bash
Copy code
python main.py --t AAPL --i 'annual' --y 3 --eg .15 --steps 2 --s 0.1 --v eg --apikey <secret>
Example Output
The terminal output provides details of the forecasted flows and key financial metrics, such as Enterprise Value, Equity Value, and Per Share Value.

bash
Copy code
Forecasting flows for 5 years out, starting at 2018-12-29.
         DFCF   |    EBIT   |    D&A    |    CWC    |   CAP_EX   |
2019   2.35E+10 |  2.79E+10 |  3.96E+09 |  2.17E+09 |  -3.51E+09 |
2020   2.80E+10 |  3.70E+10 |  5.26E+09 |  1.52E+09 |  -3.82E+09 |
2021   3.82E+10 |  5.54E+10 |  7.86E+09 |  1.06E+09 |  -4.34E+09 |
2022   5.84E+10 |  9.19E+10 |  1.31E+10 |  7.44E+08 |  -5.12E+09 |
2023   9.82E+10 |  1.68E+11 |  2.38E+10 |  5.21E+08 |  -6.27E+09 |

Enterprise Value for AAPL: $1.41E+12.
Equity Value for AAPL: $1.34E+12.
Per share value for AAPL: $2.81E+02.
Future Development
Implement dynamic discount rate calculation.
Multivariable earnings growth rate calculations.
EBITDA multiples for terminal value.
Author
Muhammad Osama Khan

Contact
Feel free to reach out for questions or suggestions: osaamakhan98@gmail.com