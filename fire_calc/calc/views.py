from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from . import apps

#simulation helpers
import numpy as np
import matplotlib.pyplot as plt
import random

parameters = {
    'initial-amount': 400000,
    'annual-addition': 25000,
    'target-amount': 1000000,
    'stock-percentage': 60,
    'bond-percentage': 38,
    'cash-percentage': 2,
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
    params['initial-amount'] = int(request.POST['initial-amount'])
    params['annual-addition'] = int(request.POST['annual-addition'])
    params['target-amount'] = int(request.POST['target-amount'])
    params['stock-percentage'] = float(request.POST['stock-percentage'])
    params['bond-percentage'] = float(request.POST['bond-percentage'])
    params['cash-percentage'] = float(request.POST['cash-percentage'])
    request.session.modified = True
    print(params)

    print('starting simulations')
    end_vals = []
    year_vals = []

    sims_count = 10000
    succeeded = 0
    for i in range(sims_count):
        stats = apps.simulate_pre_portfolio(params['initial-amount'], params['annual-addition'], params['target-amount'], params['stock-percentage'], params['bond-percentage'])
        end_vals.append(stats['portfolio'][-1])
        if stats['years_taken'] != float('inf'):
            year_vals.append(stats['years_taken'])
        #if random.randint(0, 10) == 5:
            #plt.plot(stats['portfolio'])

    #plt.show()
    #print(year_vals)
    plt.hist(year_vals, 10, rwidth=0.8)
    plt.show()
    print('mean years to target:', np.mean(year_vals))
    print('success rate:', len(year_vals)/len(end_vals) * 100)
    print("Done simulations")

    return HttpResponseRedirect(reverse('calc:calc'))
