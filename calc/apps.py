from django.apps import AppConfig
from . import views
import csv, os

#data related packages
import numpy as np
import math, random

SP500_BIN_START = -50.0
SP500_BIN_RANGE = 10.0
sp500_rand_percent = []
bonds_rand_percent = []
class CalcConfig(AppConfig):
    name = 'calc'
    def ready(self):
        print("Hello World")
        ready_data()

def ready_data():
    file_dir = os.path.dirname(__file__)

    #process stock historical prices
    sp500_path = os.path.join(file_dir, "data/sp500.csv")
    with open(sp500_path, newline='') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        sp500 = []
        for row in read_csv:
            sp500.append(float(row[1]))
        sp500.reverse()

        sp500_percent = [0]
        for i in range(len(sp500)):
            if i != 0:
                percent_change = (sp500[i]/sp500[i-1] - 1) * 100
                sp500_percent.append(percent_change)

        #print(min(sp500_percent), max(sp500_percent), np.mean(sp500_percent))
        hist, bins = np.histogram(sp500_percent, bins=10)
        sp500_rand_percent.clear()
        for i in range(50000):
            gen = random.randint(1, len(sp500))
            bin_num = 0
            while gen > 0:
                gen -= hist[bin_num]
                bin_num += 1
            bin_num -= 1
            bin_start = bins[bin_num]
            bin_end = bins[bin_num + 1]
            percent = bin_start + random.random() * (bin_end - bin_start)
            #print(percent)
            sp500_rand_percent.append(percent)
        print(min(sp500_rand_percent), max(sp500_rand_percent), np.mean(sp500_rand_percent))

    bonds_path = os.path.join(file_dir, "data/bonds.csv")
    with open(bonds_path, newline='') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        bonds_yield = []
        for row in read_csv:
            bonds_yield.append(float(row[1]))
        bonds_yield.reverse()
        #print(min(bonds_yield), max(bonds_yield), np.mean(bonds_yield))
        hist, bins = np.histogram(bonds_yield, bins=10)
        # plt.hist(bonds_yield, bins=10)
        # plt.show()
        bonds_rand_percent.clear()
        for i in range(50000):
            gen = random.randint(1, len(bonds_yield))
            bin_num = 0
            while gen > 0:
                gen -= hist[bin_num]
                bin_num += 1
            bin_num -= 1
            bin_start = bins[bin_num]
            bin_end = bins[bin_num + 1]
            percent = bin_start + random.random() * (bin_end - bin_start)
            bonds_rand_percent.append(percent)
        print(min(bonds_rand_percent), max(bonds_rand_percent), np.mean(bonds_rand_percent))

    print("Finished setting up s&p500 data")


def generate_stock_percent():
    gen = random.randint(0, len(sp500_rand_percent) - 1)
    return sp500_rand_percent[gen]

def generate_bond_percent():
    gen = random.randint(0, len(bonds_rand_percent) - 1)
    return bonds_rand_percent[gen]

def simulate_pre_portfolio(starting, addition, target, period, stock, bond):
    cash = 100 - stock - bond
    portfolio = [starting]
    stats = {}
    years_taken = float("inf")
    for i in range(period):
        stock_change = generate_stock_percent()
        bond_change = generate_bond_percent()
        cur_portfolio = portfolio[-1]
        next_portfolio = cur_portfolio * stock/100 * (1 + stock_change/100) + \
                        cur_portfolio * bond/100 * (1 + bond_change/100) + \
                        cur_portfolio * cash/100 + addition

        next_portfolio = int(round(next_portfolio))
        #print(next_portfolio)
        if years_taken > period and next_portfolio > target:
            years_taken = i
        portfolio.append(next_portfolio)

    stats['years_taken'] = years_taken
    stats['portfolio'] = portfolio
    return stats

def simulate_post_portfolio(starting, withdrawal, period, stock, bond):
    cash = 100 - stock - bond
    portfolio = [starting]
    stats = {}
    years_survived = float("inf")
    for i in range(period):
        stock_change = generate_stock_percent()
        bond_change = generate_bond_percent()
        cur_portfolio = portfolio[-1]
        next_portfolio = cur_portfolio * stock/100 * (1 + stock_change/100) + \
                        cur_portfolio * bond/100 * (1 + bond_change/100) + \
                        cur_portfolio * cash/100 - withdrawal
        next_portfolio = int(round(next_portfolio))
        if years_survived > period and next_portfolio <= 0:
            years_survived = i
        if next_portfolio < 0:
            next_portfolio = 0
        portfolio.append(next_portfolio)

    stats['years_survived'] = years_survived
    stats['portfolio'] = portfolio
    return stats
