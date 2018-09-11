from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
import json
from . import apps

#simulation helpers
import numpy as np
import matplotlib.pyplot as plt
import random

parameters = {
    'initial_amount': 400000,
    'annual_addition': 25000,
    'target_amount': 1000000,
    'stock_percentage': 60.0,
    'bond_percentage': 38.0,
    'cash_percentage': 2.0,
}

# Tab for pre-retirement calcs
def calc(request):
    params = parameters.copy()
    if 'params' in request.session:
        params = request.session['params']
        del request.session['params']
    else:
        request.session['params'] = params

    pre_graph_data = None
    if 'pre_dataset' in request.session:
        pre_graph_data = request.session['pre_dataset']
        del request.session['pre_dataset']
    #print(pre_graph_data)
    return render(request, 'calc/calc.html', {'params': params, 'pre_graph_data': pre_graph_data})

# About page for the calc
def about(request):
    return HttpResponse('Welcome to the about page')

def calc_pre(request):
    #set session params from POST
    params = None
    if 'params' in request.session:
        params = request.session['params']
    else:
        params = parameters.copy()
        request.session['params'] = params
    params['initial_amount'] = int(request.POST['initial-amount'])
    params['annual_addition'] = int(request.POST['annual-addition'])
    params['target_amount'] = int(request.POST['target-amount'])
    params['stock_percentage'] = float(request.POST['stock-percentage'])
    params['bond_percentage'] = float(request.POST['bond-percentage'])
    params['cash_percentage'] = float(request.POST['cash-percentage'])


    print('starting simulations')
    end_vals = []
    year_vals = []

    sims_count = 1000
    years_to_sim = 40

    dataset = {
        'portfolios': [],
    }
    for i in range(sims_count):
        stats = apps.simulate_pre_portfolio(
            params['initial_amount'],
            params['annual_addition'],
            params['target_amount'],
            years_to_sim,
            params['stock_percentage'],
            params['bond_percentage']
        )
        end_vals.append(stats['portfolio'][-1])
        dataset['portfolios'].append(stats['portfolio'])
        if stats['years_taken'] != float('inf'):
            year_vals.append(stats['years_taken'])

    request.session['pre_dataset'] = dataset
    #plt.show()
    #print(year_vals)
    #plt.hist(year_vals, 10, rwidth=0.8)
    #plt.show()
    print('mean years to target:', np.mean(year_vals))
    print('success rate:', len(year_vals)/len(end_vals) * 100)
    print('Done simulations')
    request.session.modified = True
    return HttpResponseRedirect(reverse('calc:calc'))
