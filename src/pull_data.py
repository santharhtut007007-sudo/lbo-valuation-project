#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 08:34:54 2026

@author: santharhtut
"""

import yfinance as yf

gtx = yf.Ticker("GTX")
folder = "/Users/santharhtut/Desktop/Finance Projects/lbo-valuation-project/data/"

gtx.income_stmt.to_csv(folder + "gtx_income_statement.csv")
gtx.balance_sheet.to_csv(folder + "gtx_balance_sheet.csv")
gtx.cashflow.to_csv(folder + "gtx_cash_flow.csv")