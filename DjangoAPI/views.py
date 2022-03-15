from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.core import serializers 
from django.http import JsonResponse 

from isort import Config
from .forms import CustomerForm 
from .models import Customer 

from rest_framework import viewsets 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.parsers import JSONParser 

from .serializer import CustomerSerializers 

import pickle
import json 
import numpy as np 
from sklearn import preprocessing 
import pandas as pd 


import custom_config

# Create your views here.



class CustomerView(viewsets.ModelViewSet): 
    queryset = Customer.objects.all() 
    serializer_class = CustomerSerializers 

def status(df):
    try:
        scaler=pickle.load(open(custom_config.SCALER_PATH, 'rb'))
        model=pickle.load(open(custom_config.MODEL_PATH, 'rb'))
        X = scaler.transform(df) 
        y_pred = model.predict(X) 
        y_pred=(y_pred>0.80) 
        result = "Yes" if y_pred else "No"
        return result 
    except ValueError as e: 
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST) 

def FormView(request):
    if request.method=='POST':
        form=CustomerForm(request.POST or None)

        if form.is_valid():
            Gender = form.cleaned_data['gender']
            Age = form.cleaned_data['age']
            EstimatedSalary = form.cleaned_data['salary']
            df=pd.DataFrame({'gender':[Gender], 'age':[Age], 'salary':[EstimatedSalary]})
            df["gender"] = 1 if "male" else 2
            result = status(df)
            return render(request, 'status.html', {"data": result}) 
            
    form=CustomerForm()
    return render(request, 'form.html', {'form':form})

