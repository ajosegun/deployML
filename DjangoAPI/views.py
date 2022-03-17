from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.core import serializers 
from django.http import JsonResponse 

from isort import Config
from .forms import CustomerForm, DiabetesForm
from .models import Customer 

from rest_framework import viewsets 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.parsers import JSONParser 

from .serializer import CustomerSerializers 

import pickle
import joblib
import json 
import numpy as np 
from sklearn import preprocessing 
import pandas as pd 


import custom_config

# Create your views here.



class CustomerView(viewsets.ModelViewSet): 
    queryset = Customer.objects.all() 
    serializer_class = CustomerSerializers 

def status_car(df):
    try:

        scaler=pickle.load(open(custom_config.SCALER_PATH, 'rb'))
        model=pickle.load(open(custom_config.MODEL_PATH, 'rb'))

        X = scaler.transform(df) 
        y_pred = model.predict(X) 
        y_pred = (y_pred > 0.80) 

        result = "Yes" if y_pred else "No"
        return result 

    except ValueError as e: 
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST) 

def status_diabetes(df):
    try:

        # Load the model from the file
        scaler = joblib.load(open(custom_config.DIABETES_CLASSIFIER_SCALER_PATH, 'rb'))
        model = joblib.load(open(custom_config.DIABETES_CLASSIFIER_PATH, 'rb'))

        X = scaler.transform(df) 
        y_pred = model.predict(X) 
        y_pred = (y_pred == 1) 

        result = "Oops! You have diabetes." if y_pred else "Great! You don't have diabetes."
        return result 

    except ValueError as e: 
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST) 

def BuyCarView(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST or None)

        if form.is_valid():
            Gender = form.cleaned_data['gender']
            Age = form.cleaned_data['age']
            EstimatedSalary = form.cleaned_data['salary']
            df=pd.DataFrame({'gender':[Gender], 'age':[Age], 'salary':[EstimatedSalary]})
            df["gender"] = 1 if "male" else 2
            
            result = status_car(df)
            return render(request, 'status.html', {"car_buying_data": result}) 
            
    form = CustomerForm()
    return render(request, 'form.html', {'form':form})

def DiabetesView(request):
    if request.method == 'POST':
        form = DiabetesForm(request.POST or None)

        if form.is_valid():
            Pregnancies = form.cleaned_data['pregnancies']
            Glucose = form.cleaned_data['glucose']
            BloodPressure = form.cleaned_data['bloodPressure']
            SkinThickness = form.cleaned_data['skinThickness']
            Insulin = form.cleaned_data['insulin']
            BMI = form.cleaned_data['bmi']
            DiabetesPedigreeFunction = form.cleaned_data['diabetesPedigreeFunction']
            Age = form.cleaned_data['age']
            
            df = pd.DataFrame(
                    {
                        'pregnancies':[Pregnancies], 
                        'glucose':[Glucose], 
                        'bloodPressure':[BloodPressure],
                        'skinThickness':[SkinThickness], 
                        'insulin':[Insulin], 
                        'bmi':[BMI],
                        'diabetesPedigreeFunction':[DiabetesPedigreeFunction], 
                        'age':[Age],                    
                    }
                )
            
            result = status_diabetes(df)
            
            return render(request, 'status.html', {"diabetes_data": result}) 
            
    form = DiabetesForm()
    return render(request, 'diabetes_form.html', {'diabetes_form': form})

