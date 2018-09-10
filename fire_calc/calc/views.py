from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from . import apps

#temp helpers
import numpy as np
import matplotlib.pyplot as plt

parameters = {
    'annual_addition': 25000,
    'target_amount': 1000000,
    'stock_percentage': 60,
    'bond_percentage': 38,
    'cash_percentage': 2,
}

# Tab for pre-retirement calcs
def calc(request):
    params = None
    if 'params' in request.session:
        params = request.session['params']
    else:
        params = parameters.copy()
        request.session['params'] = params
    return render(request, 'calc/calc.html', {'params': params})

# About page for the calc
def about(request):
    return HttpResponse("Welcome to the about page")

def calc_pre(request):
    #set session params from POST
    params = request.session['params']
    params['annual_addition'] = int(request.POST['annual-addition'])
    params['target_amount'] = int(request.POST['target-amount'])
    params['stock_percentage'] = float(request.POST['stock-percentage'])
    params['bond_percentage'] = float(request.POST['bond-percentage'])
    params['cash_percentage'] = float(request.POST['cash-percentage'])
    request.session.modified = True
    print(params)

    print('starting simulations')
    end_vals = []
    sims_count = 10000
    failed = 0
    for i in range(sims_count):
        portfolio = apps.simulate_portfolio(params['target_amount'], params['annual_addition'], 40)
        end_vals.append(portfolio[-1])
        if portfolio[-1] < 0:
            failed += 1
        #plt.plot(portfolio)

    #plt.show()
    plt.hist(end_vals, 50, rwidth=0.8)
    #plt.show()
    print('mean:', np.mean(end_vals))
    print('fail rate: %f%%' % (failed/sims_count * 100))
    print("Done simulations")

    return HttpResponseRedirect(reverse('calc:calc'))
