import requests
import traceback

def get_api_url(data_type, ticker, period, apikey):
    base_url = 'https://financialmodelingprep.com/api/v3/{data_type}/{ticker}?apikey={apikey}'
    if period == 'quarter':
        base_url += '&period=quarter'
    return base_url.format(data_type=data_type, ticker=ticker, apikey=apikey)

def get_jsonparsed_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        if "Error Message" in json_data:
            raise ValueError(f"Error while requesting data from '{url}'. Error Message: '{json_data['Error Message']}'.")
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving {url}: {e}")
        traceback.print_exc()
        raise

def get_financial_statement(ticker, statement_type, period='annual', apikey=''):
    url = get_api_url(f'financials/{statement_type}', ticker=ticker, period=period, apikey=apikey)
    return get_jsonparsed_data(url)

def get_stock_price(ticker, apikey=''):
    url = f'https://financialmodelingprep.com/api/v3/stock/real-time-price/{ticker}?apikey={apikey}'
    return get_jsonparsed_data(url)

def get_batch_stock_prices(tickers, apikey=''):
    prices = {}
    for ticker in tickers:
        prices[ticker] = get_stock_price(ticker=ticker, apikey=apikey)['price']
    return prices

def get_historical_prices(ticker, dates, apikey=''):
    prices = {}
    for date in dates:
        try:
            date_start, date_end = date[0:8] + str(int(date[8:]) - 2), date
        except:
            print(f"Error parsing '{date}' to date.")
            traceback.print_exc()
            continue
        url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={date_start}&to={date_end}&apikey={apikey}'
        try:
            prices[date_end] = get_jsonparsed_data(url)['historical'][0]['close']
        except IndexError:
            try:
                prices[date_start] = get_jsonparsed_data(url)['historical'][0]['close']
            except IndexError:
                print(date + ' ', get_jsonparsed_data(url))
    return prices

if __name__ == '__main__':
    """ quick test, to use run data.py directly """

    ticker = 'AAPL'
    apikey = '<DEMO>'
    
    # Example usage for cash flow statement
    statement_data = get_financial_statement(ticker=ticker, statement_type='cash-flow-statement', apikey=apikey)
    print(statement_data)
