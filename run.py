import argparse

import togglore
from togglore import utils


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for toggle to calculate over/undertime.')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    parser_range = subparsers.add_parser('range', help='range help')
    parser_range.add_argument('from_date', help='startdate, e.g. 30.08.2016')
    parser_range.add_argument('to_date', help='enddate, e.g. 12.10.2016')

    parser_year = subparsers.add_parser('thisyear', help='today help')
    parser_thismonth = subparsers.add_parser('thismonth', help='month help')
    parser_week = subparsers.add_parser('thisweek', help='week help')
    parser_today = subparsers.add_parser('today', help='day help')
    parser_month = subparsers.add_parser('month', help='month help')
    parser_month.add_argument('month', help='month e.g. 08')
    parser_since = subparsers.add_parser('since', help='since help')
    parser_since.add_argument('since', help='since e.g. 2016.08.01')

    args = parser.parse_args()

    client = togglore.Togglore()

    expected = 0
    actual = 0

    if args.command == 'range':
        actual, expected = client.diff(utils.DateRange.parse_from_iso_strings(args.from_date, args.to_date))
    elif args.command == 'thisyear':
        actual, expected = client.diff(utils.DateRange.this_year())
    elif args.command == 'thismonth':
        actual, expected = client.diff(utils.DateRange.this_month())
    elif args.command == 'thisweek':
        actual, expected = client.diff(utils.DateRange.this_week())
    elif args.command == 'today':
        actual, expected = client.diff(utils.DateRange.today())
    elif args.command == 'month':
        actual, expected = client.diff(utils.DateRange.month(int(args.month)))
    elif args.command == 'since':
        actual, expected = client.diff(utils.DateRange.since(args.since))

    print("Hours to do: {0:.2f}h ({1:.2f} days)".format(expected, expected/client.cfg.work_hours_per_day))
    print("Hours worked: {0:.2f}h ({1:.2f} days)".format(actual, actual/client.cfg.work_hours_per_day))

    difference = actual-expected
    print("Difference: {0:.2f}h ({1:.2f} days)".format(difference, difference/client.cfg.work_hours_per_day))

    vacation_days_used = client.cfg.vacation_days
    vacation_days_per_year = client.cfg.vacation_days_per_year
    started_on = client.cfg.started_on
    demand = utils.calculate_vacation_demand(started_on, vacation_days_per_year)

    print("Difference Worktime: {0:.2f}h ({1:.2f} days)".format(
        difference, difference / client.cfg.work_hours_per_day)
    )
    print("Difference Vacation: {}d of {}d used".format(
        len(vacation_days_used), demand)
    )
