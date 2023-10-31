def pretty_print_discounted_cash_flows(dcfs, forecast_years):
    
    if forecast_years > 1:
        for ticker, years_data in dcfs.items():
            print('Ticker: {}'.format(ticker))
            if len(dcfs[ticker].keys()) > 1:
                for year, dcf in years_data.items():
                    print('Date: {} \
                        \nValue: {}'.format(year, dcf))
    else:
        for ticker, value in dcfs.items():
            print('Ticker: {}  \
                  \nValue: {}'.format(ticker, value))

