from django.shortcuts import render
import pickle
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
# single_data_point = pd.DataFrame({
#     'pos_id': [387],
#     'ntn': [55],
#     'rate_value': [0.0],
#     'sales_value': [0.0],
#     'consumer_name': [0],
#     'consumer_ntn': [0],
#     'consumer_address': [0],
#     'extra_info': [0.0],
#     'is_active': [1],
#     'invoice_type': [1.0],
#     'consider_for_Annex': [1],
#     'month': [11],
#     'weekday': [3],
#     'day': [16],
#     'time_seconds': [22596]
# })
# Create your views here.
@api_view(['GET'])
def anomaly(request):
    with open('/workspaces/FYP-RestApi/main_app/myapp/single_invoice.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
        new_data = pd.DataFrame([[3.8700e+02, 5.5000e+01, 0.0000e+00, 0.0000e+00, 0.0000e+00,
       0.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00, 1.0000e+00,
       1.0000e+00, 1.1000e+01, 3.0000e+00, 1.6000e+01, 2.2596e+04]])

        prediction = loaded_model.predict(new_data)

        print("Anomaly Prediction:", prediction[0])
    return Response(prediction)