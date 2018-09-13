from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
import json
from . import apps

#simulation helpers
import numpy as np
import random

pre_parameters = {
    'starting': 0,
    'addition': 40000,
    'target': 1000000,
    'stock': 60.0,
    'bond': 38.0,
}

post_parameters = {
    'starting': 1000000,
    'withdrawal': 40000,
    'period': 40,
    'stock': 60.0,
    'bond': 38.0,
}

# Tab for pre-retirement calcs
def calc(request):
    if 'error' in request.session:
        messages.error(request, request.session['error'])
        print('error: ', request.session['error'])
        request.session.flush()

    view = 'pre'
    if 'view' in request.session:
        view = request.session['view']

    pre_params = pre_parameters.copy()
    if 'pre_params' in request.session:
        pre_params = request.session['pre_params']

    post_params = post_parameters.copy()
    if 'post_params' in request.session:
        post_params = request.session['post_params']

    pre_graph_data = None
    if 'pre_dataset' in request.session:
        pre_graph_data = request.session['pre_dataset']
    #print(pre_graph_data)

    pre_simulation_stats = None
    if 'pre_stats' in request.session:
        pre_simulation_stats = request.session['pre_stats']

    post_graph_data = None
    if 'post_dataset' in request.session:
        post_graph_data = request.session['post_dataset']
    #print(pre_graph_data)

    post_simulation_stats = None
    if 'post_stats' in request.session:
        post_simulation_stats = request.session['post_stats']

    request.session.flush()

    return render(
            request,
            'calc/calc.html',
            {
                'view': view,
                'pre_params': pre_params,
                'pre_graph_data': pre_graph_data,
                'pre_simulation_stats': pre_simulation_stats,
                'post_params': post_params,
                'post_graph_data': post_graph_data,
                'post_simulation_stats': post_simulation_stats,
            }
        )

# About page for the calc
def about(request):
    return HttpResponse('Welcome to the about page')

def pre_form_validate_input(request):
    if request.method != 'POST':
        return 'wrong request method'
    data = request.POST
    if float(request.POST['stock']) + float(request.POST['bond']) > 100:
        return "sum of asset allocation is greater than 100%"
    return 'valid'

def calc_pre(request):
    validate = pre_form_validate_input(request)
    if validate != 'valid':
        request.session['error'] = validate
        return HttpResponseRedirect(reverse('calc:calc'))
    #set session params from POST
    pre_params = pre_parameters.copy()
    request.session['pre_params'] = pre_params
    pre_params['starting'] = int(request.POST['starting'])
    pre_params['addition'] = int(request.POST['addition'])
    pre_params['target'] = int(request.POST['target'])
    pre_params['stock'] = float(request.POST['stock'])
    pre_params['bond'] = float(request.POST['bond'])

    print('Starting pre-retirement simulations')
    end_vals = []
    year_vals = []
    portfolios_store = []

    sims_count = 10000
    years_to_sim = 40

    dataset = {
        'portfolios': [],
        'stats': {
            'target': pre_params['target'],
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
            pre_params['starting'],
            pre_params['addition'],
            pre_params['target'],
            years_to_sim,
            pre_params['stock'],
            pre_params['bond']
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
        return round(sum(k > pre_params['target'] for k in i)/sims_count * 100, 2)
    dataset['stats']['success_rates'] = [calc_success_rate(i) for i in zip(*portfolios_store)]

    simu_stats = {
        'mean_years': None,
        'simulation_count': sims_count,
        'simulation_years': years_to_sim,
    }
    request.session['pre_stats'] = simu_stats
    if year_vals:
        hist, bins = np.histogram(year_vals, (max(year_vals) - min(year_vals)))
        dataset['histogram']['years'] = hist.tolist()
        dataset['histogram']['bins'] = bins.tolist()
        simu_stats['mean_years'] = round(np.mean(year_vals), 2)

    #print(type(bins))

    print('Done simulations')
    request.session['view'] = 'pre'
    request.session.modified = True
    return HttpResponseRedirect(reverse('calc:calc'))

def post_form_validate_input(request):
    if request.method != 'POST':
        return 'wrong request method'
    data = request.POST
    if float(request.POST['stock']) + float(request.POST['bond']) > 100:
        return "sum of asset allocation is greater than 100%"
    return 'valid'

def calc_post(request):
    validate = pre_form_validate_input(request)
    if validate != 'valid':
        request.session['error'] = validate
        request.session['view'] = 'post'
        return HttpResponseRedirect(reverse('calc:calc'))

    post_params = post_parameters.copy()
    request.session['post_params'] = post_params
    post_params['starting'] = int(request.POST['starting'])
    post_params['withdrawal'] = int(request.POST['withdrawal'])
    post_params['period'] = int(request.POST['period'])
    post_params['stock'] = float(request.POST['stock'])
    post_params['bond'] = float(request.POST['bond'])

    print('Starting post-retirement simulations')
    end_vals = []
    year_vals = []
    portfolios_store = []

    sims_count = 10000
    years_to_sim = post_params['period']

    dataset = {
        'portfolios': [],
        'stats': {
            'failure_rates': [],
            'means': [],
        },
        'histogram': {
            'years': [],
            'bins': [],
        }
    }
    for i in range(sims_count):
        results = apps.simulate_post_portfolio(
            post_params['starting'],
            post_params['withdrawal'],
            years_to_sim,
            post_params['stock'],
            post_params['bond']
        )
        end_vals.append(results['portfolio'][-1])
        if i % 100 == 0:
            dataset['portfolios'].append(results['portfolio'])
        portfolios_store.append(results['portfolio'])

        if results['years_survived'] != float('inf'):
            year_vals.append(results['years_survived'])

    request.session['post_dataset'] = dataset

    #process stats
    dataset['stats']['means'] = [round(np.mean(i), 0) for i in zip(*portfolios_store)]
    def calc_failure_rate(i):
        return round(sum(k <= 0 for k in i)/sims_count * 100, 2)
    dataset['stats']['failure_rates'] = [calc_failure_rate(i) for i in zip(*portfolios_store)]

    simu_stats = {
        'mean_years': None,
        'simulation_count': sims_count,
        'simulation_years': years_to_sim,
        'final_failure_rate': dataset['stats']['failure_rates'][-1],
    }
    request.session['post_stats'] = simu_stats

    if year_vals:
        hist, bins = np.histogram(year_vals, (max(year_vals) - min(year_vals)))
        dataset['histogram']['years'] = hist.tolist()
        dataset['histogram']['bins'] = bins.tolist()
        simu_stats['mean_years'] = round(np.mean(year_vals), 2)

    print('Done simulations')
    #print('data: ', request.session['post_dataset'])
    #print('stats: ', request.session['post_stats'])
    request.session['view'] = 'post'
    request.session.modified = True
    return HttpResponseRedirect(reverse('calc:calc'))
