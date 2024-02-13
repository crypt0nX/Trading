#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# @Author  : 
# @Time    : 2024/2/5 07:24
# @File    : positionHelper.py
# @annotation    :
import argparse
import ast
import logging
import sys

unit = "usdt"


# transactions = [(0.1974, 200), (0.1944, 800)]


def calculate_average_price(_transactions):
    total_amount = 0
    total_spent = 0

    for price, spent in _transactions:
        total_amount += spent / price
        total_spent += spent
    average_price = total_spent / total_amount
    return total_spent, average_price


def calculate_profit_loss(_size, entry, _tp, _sl):
    _loss = _size * abs(entry - _sl) / entry
    _profit = _size * abs(_tp - entry) / entry
    return round(_profit, 3), round(_loss, 3), round(_profit / _loss, 3)


def check_arguments(_tp, _sl, _transactions):
    if _tp > _sl:
        for _transaction in _transactions:
            if not (_sl < _transaction[0] < _tp):
                logging.error("entry price is wrong!!")
                sys.exit()
    elif _tp < _sl:
        for _transaction in _transactions:
            if not (_tp < _transaction[0] < _sl):
                logging.error("entry price is wrong!!")
                sys.exit()
    else:
        logging.error("tp or sl is wrong!!")
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate average price from transactions")
    # parser.add_argument("--size", type=float, help="Specify size.")
    parser.add_argument("--tp", type=float, help="Specify tp.", required=True)
    parser.add_argument("--sl", type=float, help="Specify sl.", required=True)
    parser.add_argument("--transactions", type=str,
                        help="Specify transactions as a list. like [(0.1974, 200), (0.1944, 800)]", required=True)

    args = parser.parse_args()
    # size = args.size
    tp = args.tp
    sl = args.sl
    transactions = ast.literal_eval(args.transactions)
    check_arguments(tp, sl, transactions)
    side = "long📈" if tp > sl else "short📉"
    size, entry_price = calculate_average_price(transactions)

    profit, loss, RR = calculate_profit_loss(size, entry_price, tp, sl)

    print(f"\033[33maverage price: {str(round(entry_price, 5))} {unit}\033[0m\n"
          f"side: {str(side)}\n"
          f"size: {str(size)} {unit}\n"
          f"\033[32mprofit🤑: {str(profit)} {unit}\033[0m\n"
          f"\033[31mloss🤮: {str(loss)} {unit}\033[0m\n"
          f"RR : {str(RR)}")
