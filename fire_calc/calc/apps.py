from django.apps import AppConfig
from . import views
import csv, os

#data related packages
import numpy as np
import math, random
import matplotlib.pyplot as plt
from scipy.stats import norm

class CalcConfig(AppConfig):
    name = 'calc'
    def ready(self):
        print("Hello World")
        ready_data()

sp500_data = {}
SP500_BIN_START = -50.0
SP500_BIN_RANGE = 10.0
def ready_data():
    file_dir = os.path.dirname(__file__)

    sp500path = os.path.join(file_dir, "data/sp500.csv")
    with open(sp500path, newline='') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')

        sp500_start = 0
        sp500 = []
        sp500_percent = [0]

        for row in read_csv:
            sp500.append(float(row[1]))
            sp500_start = row[0]
        sp500.reverse()
        sp500_data['years'] = len(sp500)

        for i in range(len(sp500)):
            if i != 0:
                percent_change = (sp500[i]/sp500[i-1] - 1) * 100
                sp500_percent.append(percent_change)

        # print(sp500)
        #print(sp500_percent)
        # print(sp500_start)
        # print(len(sp500))

        #generate histogram
        #print(min(sp500_percent), max(sp500_percent))
        hist, bins = np.histogram(sp500_percent, bins=10, range=(-50, 50))
        sp500_data['hist'] = hist
        #print(hist)
        #print(bins)
        sp500_rand_percent = []
        for i in range(10000):
            gen = random.randint(1, sp500_data['years'])
            bin_num = 0
            hist = sp500_data['hist']
            while gen > 0:
                gen -= hist[bin_num]
                bin_num += 1
            bin_num -= 1
            bin_start = bin_num * 10 - 50
            percent = bin_start + random.random() * 10
            sp500_rand_percent.append(percent)
        # plt.hist(sp500_rand_percent, 50)
        # plt.show()
        sp500_data['percents'] = sp500_rand_percent
        print("Finished setting up s&p500 data")

def generate_sp500_percent(inflation=False):
    gen = random.randint(0, len(sp500_data['percents']) - 1)
    return sp500_data['percents'][gen]

def simulate_portfolio(start_amount, change, period):
    S = start_amount
    T = period
    C = change
    portfolio = [S]
    percents = [0]
    for i in range(T):
        year_change = generate_sp500_percent()
        portfolio.append(portfolio[-1] * (1 + year_change/100) + change)
        percents.append(year_change)

    return portfolio
