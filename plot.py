import sys
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append('..')
from modeling.data import get_historical_prices

sns.set()
sns.set_context('paper')


def visualize_discounted_cash_flows(dcf_prices, current_share_prices, regress=True):
    # TODO: implement visualization logic
    raise NotImplementedError


def visualize_bulk_historicals(dcfs, ticker, condition, apikey):
    dcf_share_prices = {}
    variable_name = list(condition.keys())[0]

    try:
        conditions = [str(cond) for cond in list(condition.values())[0]]
    except IndexError:
        print(condition)
        conditions = [condition['Ticker']]

    for cond in conditions:
        dcf_share_prices[cond] = {}
        years = dcfs[cond].keys()
        for year in years:
            dcf_share_prices[cond][year] = dcfs[cond][year]['share_price']

    for cond in conditions:
        plt.plot(list(dcf_share_prices[cond].keys())[::-1],
                 list(dcf_share_prices[cond].values())[::-1], label=cond)

    historical_stock_prices = get_historical_prices(
        ticker=ticker,
        dates=list(dcf_share_prices[list(dcf_share_prices.keys())[0]].keys())[::-1],
        apikey=apikey)
    plt.plot(list(historical_stock_prices.keys()),
             list(historical_stock_prices.values()), label='${} over time'.format(ticker))

    plt.xlabel('Date')
    plt.ylabel('Share price ($)')
    plt.legend(loc='upper right')
    plt.title('${} Historical Share Prices'.format(ticker))
    plt.savefig('imgs/{}_{}.png'.format(ticker, variable_name))
    plt.show()


def visualize_historicals(dcfs):
    dcf_share_prices = {item['date']: item['share_price'] for item in dcfs.values()}

    xs = list(dcf_share_prices.keys())[::-1]
    ys = list(dcf_share_prices.values())[::-1]

    plt.scatter(xs, ys)
    plt.xlabel('Date')
    plt.ylabel('Share price ($)')
    plt.title('Historical Share Prices')
    plt.show()

# Example usage:
# visualize_discounted_cash_flows(dcf_prices, current_share_prices)
# visualize_bulk_historicals(dcfs, ticker='AAPL', condition={'Growth Rate': [0.1, 0.15]}, apikey='your_api_key')
# visualize_historicals(dcfs)
