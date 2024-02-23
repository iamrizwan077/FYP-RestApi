# from django.shortcuts import render
# import pickle
# import pandas as pd
# import datetime
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# # single_data_point = pd.DataFrame({
# #     'pos_id': [387],
# #     'ntn': [55],
# #     'rate_value': [0.0],
# #     'sales_value': [0.0],
# #     'consumer_name': [0],
# #     'consumer_ntn': [0],
# #     'consumer_address': [0],
# #     'extra_info': [0.0],
# #     'is_active': [1],
# #     'invoice_type': [1.0],
# #     'consider_for_Annex': [1],
# #     'month': [11],
# #     'weekday': [3],
# #     'day': [16],
# #     'time_seconds': [22596]
# # })
# # Create your views here.
# @api_view(['GET', 'POST'])
# def anomaly(request):
#     if request.method == "POST":
#         data = {
#     'pos_id': request.data['pos_id'],
#     'ntn': request.data['ntn'],
#     'rate_value': request.data['rate_value'],
#     'sales_value': request.data['sales_value'],
#     'consumer_name': request.data['consumer_name'] | 0.0,
#     'consumer_ntn': request.data['consumer_ntn'] | 0.0,
#     'consumer_address': request.data['consumer_address'] | 0.0,
#     'extra_info': request.data['extra_info'] | 0.0,
#     'is_active': request.data['is_active'],
#     'invoice_type': request.data['invoice_type'],
#     'consider_for_Annex': request.data['consider_for_Annex'],
#     'month': datetime.datetime(request.data['created_date_time']).month(),
#     'weekday': datetime.datetime(request.data['created_date_time']).weekday(),
#     'day': datetime.datetime(request.data['created_date_time']).day(),
#     'time_seconds': time_to_sec(request.data['created_date_time'])
#         }
#         with open('/workspaces/FYP-RestApi/main_app/myapp/single_invoice.pkl', 'rb') as file:
#             loaded_model = pickle.load(file)
#         #     new_data = pd.DataFrame([[3.8700e+02, 5.5000e+01, 0.0000e+00, 0.0000e+00, 0.0000e+00,
#         # 0.0000e+00, 0.0000e+00, 0.0000e+00, 1.0000e+00, 1.0000e+00,
#         # 1.0000e+00, 1.1000e+01, 3.0000e+00, 1.6000e+01, 2.2596e+04]])
#             prediction = loaded_model.predict(data)
#             # prediction = loaded_model.predict(new_data)

#             print("Anomaly Prediction:", prediction[0])
#         return Response(prediction)

# def time_to_sec(time):
#     # datetime.datetime(time).
#     return datetime.datetime(time).hour()*3600 + datetime.datetime(time).minute()*60 + datetime.datetime(time).second()

from django.shortcuts import render
import pickle
import pandas as pd
import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from myapp import serializers, models
from rest_framework import generics
from rest_framework import filters
from ml_pipeline import missing_invoice

# Create your views here.
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @api_view(['GET', 'POST'])
# def submit_data(request):
#     if request.method == "POST":
#         created_date_time = datetime.datetime.fromisoformat(request.data['created_date_time'])
#         data = {
#             'pos_id': request.data.get('pos_id'),
#             'ntn': request.data.get('ntn_id'),
#             'rate_value': request.data.get('rate_value'),
#             'sales_value': request.data.get('sales_value'),
#             'consumer_name': request.data.get('consumer_name', 0.0),
#             'consumer_ntn': request.data.get('consumer_ntn', 0.0),
#             'consumer_address': request.data.get('consumer_address', 0.0),
#             'extra_info': request.data.get('extra_info', 0.0),
#             'is_active': request.data.get('is_active'),
#             'invoice_type': request.data.get('invoice_type'),
#             'consider_for_Annex': request.data.get('consider_for_annex'),
#             'month': created_date_time.month,
#             'weekday': created_date_time.weekday(),
#             'day': created_date_time.day,
#             'time_seconds': time_to_sec(created_date_time)
#         }
#         # data = []

#         print(data)
#         serializer = serializers.AnomalySerializer(data=request.data)
#         if serializer.is_valid():
#             with open('/workspaces/FYP-RestApi/main_app/myapp/single_invoice.pkl', 'rb') as file:
#                 loaded_model = pickle.load(file)
#                 # print("1")
#                 prediction = loaded_model.predict([[i for i in data.values()]])
#                 # print("2")
#                 print("Anomaly Prediction:", prediction[0])
#                 serializer.validated_data['anomaly'] = prediction[0]
#                 serializer.save()
#             return Response(prediction)
#         else:
#             return Response(serializer.errors)
import json
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def submit_data(request):
    if request.method == "POST":
        print(request.data)
        # data = json.loads(request.data)
        # df = pd.read_json(request.data['data'])
        df2 = pd.DataFrame.from_dict(request.data['data'], orient="columns")
        print(df2)
        print(missing_invoice.main(df2))
        return Response(request.data)
        # print(request.data)

        data = {
            'pos_id': request.data.get('pos_id'),
            'ntn': request.data.get('ntn_id'),
            'rate_value': request.data.get('rate_value'),
            'sales_value': request.data.get('sales_value'),
            'consumer_name': request.data.get('consumer_name', 0.0),
            'consumer_ntn': request.data.get('consumer_ntn', 0.0),
            'consumer_address': request.data.get('consumer_address', 0.0),
            'extra_info': request.data.get('extra_info', 0.0),
            'is_active': request.data.get('is_active'),
            'invoice_type': request.data.get('invoice_type'),
            'consider_for_Annex': request.data.get('consider_for_annex'),
            'month': created_date_time.month,
            'weekday': created_date_time.weekday(),
            'day': created_date_time.day,
            'time_seconds': time_to_sec(created_date_time)
        }
        created_date_time = datetime.datetime.fromisoformat(request.data['created_date_time'])
        data = {
            'pos_id': request.data.get('pos_id'),
            'ntn': request.data.get('ntn_id'),
            'rate_value': request.data.get('rate_value'),
            'sales_value': request.data.get('sales_value'),
            'consumer_name': request.data.get('consumer_name', 0.0),
            'consumer_ntn': request.data.get('consumer_ntn', 0.0),
            'consumer_address': request.data.get('consumer_address', 0.0),
            'extra_info': request.data.get('extra_info', 0.0),
            'is_active': request.data.get('is_active'),
            'invoice_type': request.data.get('invoice_type'),
            'consider_for_Annex': request.data.get('consider_for_annex'),
            'month': created_date_time.month,
            'weekday': created_date_time.weekday(),
            'day': created_date_time.day,
            'time_seconds': time_to_sec(created_date_time)
        }
        # data = []
        print(data)
        serializer = serializers.AnomalySerializer(data=request.data)
        if serializer.is_valid():
            with open('/workspaces/FYP-RestApi/main_app/myapp/single_invoice.pkl', 'rb') as file:
                loaded_model = pickle.load(file)
                # print("1")
                prediction = loaded_model.predict([[i for i in data.values()]])
                # print("2")
                print("Anomaly Prediction:", prediction[0])
                serializer.validated_data['anomaly'] = prediction[0]
                serializer.save()
            return Response(prediction)
        else:
            return Response(serializer.errors)

# class 

def time_to_sec(time):
    return time.hour * 3600 + time.minute * 60 + time.second

class FilterView(generics.ListAPIView):
    serializer_class = serializers.AnomalySerializer
    queryset = models.Anomaly.objects.all()
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        anomaly = self.request.query_params.get('anomaly')
        pos_id = self.request.query_params.get('pos')
        ntn_id = self.request.query_params.get('ntn')
        srb_invoice_id = self.request.query_params.get('srb_invoice_id')
        
        if anomaly is not None and anomaly == True or False:
            queryset = queryset.filter(anomaly=anomaly)
        if pos_id is not None:
            queryset = queryset.filter(pos_id=pos_id)
        if ntn_id is not None:
            queryset = queryset.filter(ntn_id=ntn_id)
        if srb_invoice_id is not None:
            queryset = queryset.filter(srb_invoice_id=srb_invoice_id)
        return queryset