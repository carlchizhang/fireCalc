from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect

class Parameters:
    annual_addition = 25000
    target_amount = 1000000
    stock_percentage = 60
    bond_percentage = 38
    cash_percentage = 2
parameters = Parameters()

# Tab for pre-retirement calcs
def calc(request):
    return render(request, 'calc/calc.html', {'params': parameters})

# About page for the calc
def about(request):
    return HttpResponse("Welcome to the about page")

def calc_pre(request):
    val = request.POST['annual-addition']
    parameters.annual_addition = request.POST['annual-addition']
    parameters.target_amount = request.POST['target-amount']
    parameters.stock_percentage = request.POST['stock-percentage']
    parameters.bond_percentage = request.POST['bond-percentage']
    parameters.cash_percentage = request.POST['cash-percentage']
    print(val)
    return HttpResponseRedirect(reverse('calc:calc'))
