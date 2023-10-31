import argparse
import os

from modeling.data import get_historical_prices
from modeling.dcf import historical_dcf
from visualization.plot import visualize_bulk_historicals
from visualization.printouts import pretty_print_discounted_cash_flows


def main(args):

    if args.step_increase > 0:
        if args.variable is not None:
            if args.variable == 'eg' or args.variable == 'earnings_growth_rate':
                condition, discounted_cash_flows = run_setup(args, variable='earnings_growth_rate')
            elif args.variable == 'cg' or args.variable == 'cap_ex_growth_rate':
                condition, discounted_cash_flows = run_setup(args, variable='cap_ex_growth_rate')
            elif args.variable == 'pg' or args.variable == 'perpetual_growth_rate':
                condition, discounted_cash_flows = run_setup(args, variable='perpetual_growth_rate')
            elif args.variable == 'discount_rate' or args.variable == 'discount':
                condition, discounted_cash_flows = run_setup(args, variable='discount_rate')
            else:
                raise ValueError('args.variable is invalid, must choose from this list -> [earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate, discount_rate]')
        else:
            raise ValueError('If step (--step_increase) is > 0, you must specify the variable via --variable. What was passed is invalid.')
    else:
        condition, discounted_cash_flows = {'Ticker': [args.t]}, {}
        discounted_cash_flows[args.t] = historical_dcf(args.t, args.y, args.p, args.d, args.eg, args.cg, args.pg, args.i, args.apikey)

    if args.y > 1:  # can't graph single timepoint very well....
        visualize_bulk_historicals(discounted_cash_flows, args.t, condition, args.apikey)
    else:
        pretty_print_discounted_cash_flows(discounted_cash_flows, args.y)


def run_setup(args, variable):
    discounted_cash_flows, condition = {}, {args.variable: []}

    for increment in range(1, int(args.steps) + 1):  # default to 5 steps?
        # this should probably be wrapped in another function..
        var = vars(args)[variable] * (1 + (args.step_increase * increment))
        step = '{}: {}'.format(args.variable, str(var)[0:4])

        condition[args.variable].append(step)
        vars(args)[variable] = var
        discounted_cash_flows[step] = historical_dcf(args.t, args.y, args.p, args.d, args.eg, args.cg, args.pg, args.i, args.apikey)

    return condition, discounted_cash_flows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--p', '--period', help='years to forecast', type=int, default=5)
    parser.add_argument('--t', '--ticker', help='pass a single ticker to do historical DCF', type=str, default='AAPL')
    parser.add_argument('--y', '--years', help='number of years to compute DCF analysis for', type=int, default=1)
    parser.add_argument('--i', '--interval', help='interval period for each calc, either "annual" or "quarter"', default='annual')
    parser.add_argument('--s', '--step_increase', help='specify step increase for EG, CG, PG to enable comparisons.', type=float, default=0)
    parser.add_argument('--steps', help='steps to take if --step_increase is > 0', default=5)
    parser.add_argument('--v', '--variable', help='if --step_increase is specified, must specify variable to increase from: [earnings_growth_rate, discount_rate]', default=None)
    parser.add_argument('--d', '--discount_rate', help='discount rate for future cash flow to firm', default=0.1)
    parser.add_argument('--eg', '--earnings_growth_rate', help='growth in revenue, YoY', type=float, default=0.05)
    parser.add_argument('--cg', '--cap_ex_growth_rate', help='growth in cap_ex, YoY', type=float, default=0.045)
    parser.add_argument('--pg', '--perpetual_growth_rate', help='for perpetuity growth terminal value', type=float, default=0.05)
    parser.add_argument('--apikey', help='API key for financialmodelingprep.com', default=os.environ.get('APIKEY'))

    args = parser.parse_args()
    main(args)
