import argparse
import traceback
from decimal import Decimal
from modeling.data import *

def discounted_cash_flow(ticker, ev_statement, income_statement, balance_statement, cashflow_statement, discount_rate, forecast, earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate):
    enterprise_value = calculate_enterprise_value(
        income_statement,
        cashflow_statement,
        balance_statement,
        forecast,
        discount_rate,
        earnings_growth_rate,
        cap_ex_growth_rate,
        perpetual_growth_rate
    )

    equity_value, share_price = calculate_equity_value(enterprise_value, ev_statement)

    print(
        f'\nEnterprise Value for {ticker}: ${"%.2E" % Decimal(str(enterprise_value))}.',
        f'\nEquity Value for {ticker}: ${"%.2E" % Decimal(str(equity_value))}.',
        f'\nPer share value for {ticker}: ${"%.2E" % Decimal(str(share_price))}.\n'
    )

    return {
        'date': income_statement[0]['date'],
        'enterprise_value': enterprise_value,
        'equity_value': equity_value,
        'share_price': share_price
    }


def historical_discounted_cash_flow(ticker, years, forecast, discount_rate, earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate, interval='annual', apikey=''):
    dcfs = {}
    income_statement = get_income_statement(ticker=ticker, period=interval, apikey=apikey)['financials']
    balance_statement = get_balance_statement(ticker=ticker, period=interval, apikey=apikey)['financials']
    cashflow_statement = get_cashflow_statement(ticker=ticker, period=interval, apikey=apikey)['financials']
    enterprise_value_statement = get_EV_statement(ticker=ticker, period=interval, apikey=apikey)['enterpriseValues']

    intervals = years * 4 if interval == 'quarter' else years

    for interval in range(0, intervals):
        try:
            dcf = discounted_cash_flow(
                ticker,
                enterprise_value_statement[interval],
                income_statement[interval:interval + 2],
                balance_statement[interval:interval + 2],
                cashflow_statement[interval:interval + 2],
                discount_rate,
                forecast,
                earnings_growth_rate,
                cap_ex_growth_rate,
                perpetual_growth_rate
            )
        except (Exception, IndexError) as e:
            print(traceback.format_exc())
            print(f'Interval {interval} unavailable, no historical statement.')
        else:
            dcfs[dcf['date']] = dcf
        print('-' * 60)

    return dcfs


def unlevered_free_cash_flow(ebit, tax_rate, non_cash_charges, cwc, cap_ex):
    return ebit * (1 - tax_rate) + non_cash_charges + cwc + cap_ex


def get_discount_rate():
    return 0.1  # TODO: implement


def calculate_equity_value(enterprise_value, enterprise_value_statement):
    equity_value = enterprise_value - enterprise_value_statement['+ Total Debt']
    equity_value += enterprise_value_statement['- Cash & Cash Equivalents']
    share_price = equity_value / float(enterprise_value_statement['Number of Shares'])

    return equity_value, share_price


def calculate_enterprise_value(income_statement, cashflow_statement, balance_statement, period, discount_rate, earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate):
    ebit = float(income_statement[0]['EBIT']) if income_statement[0]['EBIT'] else float(
        input(f"EBIT missing. Enter EBIT on {income_statement[0]['date']} or skip: "))
    tax_rate = float(income_statement[0]['Income Tax Expense']) / float(income_statement[0]['Earnings before Tax'])
    non_cash_charges = float(cashflow_statement[0]['Depreciation & Amortization'])
    cwc = (float(balance_statement[0]['Total assets']) - float(balance_statement[0]['Total non-current assets'])) - \
          (float(balance_statement[1]['Total assets']) - float(balance_statement[1]['Total non-current assets']))
    cap_ex = float(cashflow_statement[0]['Capital Expenditure'])
    discount = discount_rate

    flows = []

    print('Forecasting flows for {} years out, starting at {}.'.format(period, income_statement[0]['date']),
          ('\n         DFCF   |    EBIT   |    D&A    |    CWC     |   CAP_EX   | '))

    for yr in range(1, period + 1):
        ebit *= (1 + (yr * earnings_growth_rate))
        non_cash_charges *= (1 + (yr * earnings_growth_rate))
        cwc *= 0.7  # TODO: evaluate this cwc rate? 0.1 annually?
        cap_ex *= (1 + (yr * cap_ex_growth_rate))

        flow = unlevered_free_cash_flow(ebit, tax_rate, non_cash_charges, cwc
