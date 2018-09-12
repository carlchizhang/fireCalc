from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
import json
from . import apps

#simulation helpers
import numpy as np
import random

parameters = {
    'initial_amount': 0,
    'annual_addition': 40000,
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

    pre_simulation_stats = None
    if 'pre_stats' in request.session:
        pre_simulation_stats = request.session['pre_stats']
        del request.session['pre_stats']

    return render(request, 'calc/calc.html', {'params': params, 'pre_graph_data': pre_graph_data, 'pre_simulation_stats': pre_simulation_stats})

# About page for the calc
def about(request):
    return HttpResponse('Welcome to the about page')

def calc_pre(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('calc:calc'))
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
    portfolios_store = []

    sims_count = 10000
    years_to_sim = 40
    stats_period = 5

    dataset = {
        'portfolios': [],
        'stats': {
            'target': params['target_amount'],
            'success_rates': [],
            'means': [],
        },
        'histogram': {
            'years': [],
            'bins': [],
        }
    }
    for i in range(sims_count):
        results = apps.simulate_pre_portfolio(
            params['initial_amount'],
            params['annual_addition'],
            params['target_amount'],
            years_to_sim,
            params['stock_percentage'],
            params['bond_percentage']
        )
        end_vals.append(results['portfolio'][-1])
        if i % 100 == 0:
            dataset['portfolios'].append(results['portfolio'])
        portfolios_store.append(results['portfolio'])

        if results['years_taken'] != float('inf'):
            year_vals.append(results['years_taken'])

    request.session['pre_dataset'] = dataset

    #process stats
    dataset['stats']['means'] = [round(np.mean(i), 0) for i in zip(*portfolios_store)]
    def calc_success_rate(i):
        return round(sum(k > params['target_amount'] for k in i)/sims_count * 100, 2)
    dataset['stats']['success_rates'] = [calc_success_rate(i) for i in zip(*portfolios_store)]

    hist, bins = np.histogram(year_vals, (max(year_vals) - min(year_vals)))
    dataset['histogram']['years'] = hist.tolist()
    dataset['histogram']['bins'] = bins.tolist()

    simu_stats = {
        'mean_years': round(np.mean(year_vals), 2),
        'simulation_count': sims_count,
    }
    request.session['pre_stats'] = simu_stats
    #print(type(bins))

    print('Done simulations')
    request.session.modified = True
    return HttpResponseRedirect(reverse('calc:calc'))
