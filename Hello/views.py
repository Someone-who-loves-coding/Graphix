import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import UploadFileForm
from .utils import process_and_visualize_excel
# Create your views here.

def index(request):
    return render(request,"Hello/index.html")
'''
def upload(request):
    return render(request,"Hello/upload.html")
    # return HttpResponse("yoyoyoyo")
'''


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Store the uploaded file in the session
            request.session['uploaded_file'] = uploaded_file

            charts = process_and_visualize_excel(uploaded_file)
            if charts:
                return render(request, 'Hello/upload.html', {'form': form, 'charts': charts})
            else:
                return HttpResponse("Unable to identify 'Category' and 'Values' columns. Please check the data structure.")
    else:
        form = UploadFileForm()

    return render(request, 'Hello/upload.html', {'form': form})

def pie_chart(request):
    # Retrieve the uploaded file from the session
    uploaded_file = request.session.get('uploaded_file')

    if uploaded_file:
        chart_data = process_and_visualize_excel(uploaded_file, 'Pie Chart')

        if chart_data:
            # Pass the chart data to the template
            return render(request, 'Hello/pie_chart.html', {'chart_data': chart_data})
        else:
            return render(request, 'Hello/result.html', {'message': 'Unable to generate the pie chart.'})
    else:
        return HttpResponse("No uploaded file found in the session. Please upload a file first.")


def result(request):
    return render(request, 'Hello/result.html')