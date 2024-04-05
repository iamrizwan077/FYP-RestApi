from django.shortcuts import render
import pickle
from rest_framework import status
import pandas as pd
import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from myapp import serializers, models
from rest_framework import generics
from rest_framework import filters
from ml_pipeline import missing_invoice, run_pipeline
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
import psycopg
from psycopg.rows import dict_row
# from django_filters import rest_framework as filters
# from . import filters

def time_to_sec(time):
    return time.hour * 3600 + time.minute * 60 + time.second

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, AllowAny])
@api_view(['GET'])
def get_user_role(request):
    # print(request.user.is_staff)
    # print(request.user.is_superuser)
    return Response({'is_admin': request.user.is_superuser, 'is_staff':request.user.is_staff})

# from rest_framework import generics, filters
# from django_filters import rest_framework as django_filters
# from . import models, serializers

# class NTNFilter(django_filters.FilterSet):
#     ntn = filters.BaseInFilter(field_name='ntn')

#     class Meta:
#         model = models.NTN
#         fields = ['ntn', 'name']

# class NTNListView(generics.ListAPIView):
#     queryset = models.NTN.objects.all()
#     serializer_class = serializers.NTNSerializer
#     filter_backends = [django_filters.DjangoFilterBackend]
#     filterset_class = NTNFilter
#     filterset_fields = ['ntn']


class FilterView(generics.ListAPIView):
    # 
    # try:
    missing_data_serializer_class = serializers.MissingInvoiceSerializer
    missing_data_queryset = models.MissingInvoice.objects.all()

    anomaly_serializer_class = serializers.AnomalySerializer
    anomaly_data_queryset = models.Anomaly.objects.all()

    anomaly_info_serializer_class = serializers.AnomalyInfoSerializer
    anomaly_info_data_queryset = models.AnomalyInfo.objects.all()

    ntn_serializer_class = serializers.NTNSerializer
    ntn_data_queryset = models.NTN.objects.all()

    location_serializer_class = serializers.LocationSerializer
    location_data_queryset = models.Location.objects.all()


    # pos_serializer_class = serializers.POSSerializer
    # pos_data_queryset = models.POS.objects.all()

    filter_backends = [filters.OrderingFilter]


    def get_queryset(self):
        # try:
        if any(param in self.request.query_params for param in ['missing_invoice_by_ntn', 'missing_invoice_by_date','missing_invoice_by_pos','missing_invoice_by_location']):
            queryset = self.missing_data_queryset
        elif "ntn" in self.request.query_params:
            queryset = self.ntn_data_queryset
        elif "anomaly_info" in self.request.query_params:
            queryset = self.anomaly_info_data_queryset
        elif "location" in self.request.query_params:
            queryset = self.location_data_queryset
        else:
            queryset = self.anomaly_data_queryset


        anomaly = self.request.query_params.get('anomaly')
        anomaly_by_pos = self.request.query_params.get('anomaly_by_pos')
        anomaly_by_ntn = self.request.query_params.get('anomaly_by_ntn')
        anomaly_by_srb_invoice_id = self.request.query_params.get('anomaly_by_srb_invoice_id')
        anomaly_by_date = self.request.query_params.get('anomaly_by_date')
        anomaly_by_location = self.request.query_params.get('anomaly_by_location')

        missing_invoice_by_date = self.request.query_params.get('missing_invoice_by_date')
        missing_invoice_by_ntn = self.request.query_params.get('missing_invoice_by_ntn')
        missing_invoice_by_pos = self.request.query_params.get('missing_invoice_by_pos')
        missing_invoice_by_location = self.request.query_params.get('missing_invoice_by_location')

        anomaly_info = self.request.query_params.get('anomaly_info')

        ntn = self.request.query_params.get('ntn')
        
        location = self.request.query_params.get('location')

        # pos_in_ntn = self.request.query_params.get('pos_in_ntn')
        # print(ntn)        
        # print(anomaly is not None, isinstance(anomaly, str))
        if anomaly is not None:
            # print(anomaly)
            
            anomaly_values = anomaly.split(',')
            if '10' not in anomaly_values:
            # print(anomaly_values)
            # correct_anomaly_ids = []
            
            # for i in anomaly_values:
            #     correct_anomaly_ids.push(i)
            # if correct_anomaly_ids:
                queryset = queryset.filter(anomaly__in=anomaly_values)
            
            else:
                # print(anomaly)
                queryset = queryset.exclude(anomaly=0)
                # print(queryset)
            # queryset = queryset.filter(anomaly=0)
        # print(anomaly_by_pos,anomaly_by_pos=='None')
        if anomaly_by_pos is not None and anomaly_by_pos != 'None':
            anomaly_by_pos_values = anomaly_by_pos.split(',')
            queryset = queryset.filter(pos_id__in=anomaly_by_pos_values)
        if anomaly_by_ntn is not None and anomaly_by_ntn != 'None':
            anomaly_by_ntn_values = anomaly_by_ntn.split(',')
            queryset = queryset.filter(ntn__in=anomaly_by_ntn_values)
        if anomaly_by_date is not None and anomaly_by_date != 'None':
            anomaly_by_date_values = anomaly_by_date.split(',')
            queryset = queryset.filter(created_date_time__date__in=anomaly_by_date_values)
        if anomaly_by_srb_invoice_id is not None and isinstance(anomaly_by_srb_invoice_id, str):
            anomaly_by_srb_invoice_id_values = anomaly_by_srb_invoice_id.split(',')
            queryset = queryset.filter(srb_invoice_id__in=anomaly_by_srb_invoice_id_values)
        if anomaly_by_location is not None and anomaly_by_location != 'None':
            anomaly_by_location_values = anomaly_by_location.split(',')
            queryset = queryset.filter(location__location__in=anomaly_by_location_values)

        
        if missing_invoice_by_date is not None and missing_invoice_by_date != 'None':
            missing_invoice_by_date_values = missing_invoice_by_date.split(',')
            queryset = queryset.filter(date__in=missing_invoice_by_date_values)
        if missing_invoice_by_ntn is not None  and missing_invoice_by_ntn != 'None':
            if missing_invoice_by_ntn == "all":
                queryset = queryset.all()
            else:
                missing_invoice_by_ntn_values = missing_invoice_by_ntn.split(',')
                queryset = queryset.filter(ntn__in=missing_invoice_by_ntn_values)
        if missing_invoice_by_pos is not None and missing_invoice_by_pos != 'None':
            missing_invoice_by_pos_values = missing_invoice_by_pos.split(',')
            queryset = queryset.filter(pos_id__in=missing_invoice_by_pos_values)
        if missing_invoice_by_location is not None and missing_invoice_by_location != 'None':
            missing_invoice_by_location_values = missing_invoice_by_location.split(',')
            queryset = queryset.filter(location__location__in=missing_invoice_by_location_values)
        if anomaly_info is not None:
            if anomaly_info == "all":
                queryset = queryset.all()
            else:
                anomaly_info_values = anomaly_info.split(',')
                queryset = queryset.filter(id__in=anomaly_info_values)

        if ntn is not None:
            if ntn == "all":
                queryset = queryset.all()
            else:
                ntn_values = ntn.split(',')
                queryset = queryset.filter(ntn__in=ntn_values)

        if location is not None:
            if location == "all":
                queryset = queryset.all()
            else:
                location_values = location.split(',')
                queryset = queryset.filter(location__in=location_values)

        # if pos_in_ntn is not None:
        #     # print(ntn)
        #     # if ntn == "all":

        #         # print("all")
        #         # queryset = queryset.all()
        #     # else:
        #         # print(ntn)
        #     queryset = queryset.filter(ntn=pos_in_ntn)


        return queryset
    # except Exception as e:
        # return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_serializer_class(self):
        if any(param in self.request.query_params for param in ['missing_invoice_by_ntn', 'missing_invoice_by_date','missing_invoice_by_pos','missing_invoice_by_location']):
            return self.missing_data_serializer_class
        elif "ntn" in self.request.query_params:
            return self.ntn_serializer_class
        elif "anomaly_info" in self.request.query_params:
            return self.anomaly_info_serializer_class
        elif "location" in self.request.query_params:
            return self.location_serializer_class
        # elif "pos_in_ntn" in self.request.query_params:
        #     return self.pos_serializer_class
        else:
            return self.anomaly_serializer_class
        
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(['POST'])
def add_location(request):
    try:
        data = request.data['data']
        serializer = serializers.LocationSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_ntn(request):
    try:
        data = request.data['data']
        serializer = serializers.NTNSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @api_view(['GET'])
# def connect_to_db(dbname, user, password, host, query):
#     try:
#         connection = psycopg.connect(dbname=dbname,
#                                     user=user,
#                                     password= password,
#                                     host=host,
#                                     row_factory=dict_row)
        
#         # Create a cursor object to execute SQL queries
#         cursor = connection.cursor()
#         # Example: Execute a SQL query
#         cursor.execute(query)

#         # Fetch the results, if any
#         rows = cursor.fetchall()
#         # print(rows, type(rows))
#         # for row in rows:
#             # print(row)

#         # submit_data(rows)
#         # Close cursor and connection
#         cursor.close()
#         connection.close()
#         print("Connection closed.")
#         return rows
#         # return "Connected to database."
#     except psycopg.Error as e:
#         print("Error connecting to database:", e)
#         return str(e)

# # {
# # "dbname":"fyp",
# # "user":"postgres",
# # "password":"postgres",
# # "host":"localhost",
# # "query":"select * from myapp_anomaly limit 5"
# # }

# def submit_data(data):
    
#     try:
#         print(data)
#         # for i in data:
#         #     i['ntn'] = i['ntn_id']
#         serializer = serializers.AnomalySerializer(data=data, many=True)
#         print(serializer.is_valid())
#         if serializer.is_valid():
            
#             df = pd.DataFrame.from_dict(data)
#             prediction = run_pipeline.main(df)
            
#             df['anomaly'] = prediction
#             df.rename(columns={'consider_for_Annex': 'consider_for_annex'}, inplace=True)
            
#             data = df.to_dict(orient='records')
            
#             for i in data:
#                 i['ntn'] = models.NTN.objects.get(ntn=i['ntn'])
#                 i['location'] = models.Location.objects.get(location=i['location'])
#                 i['anomaly'] = models.AnomalyInfo.objects.get(pk=i['anomaly'])
#                 i['created_date_time'] = datetime.datetime.fromisoformat(i['created_date_time'])
#                 del i['name']
            
#             models.Anomaly.objects.bulk_create([models.Anomaly(**record) for record in data])
#             return "OK"
#         else:    
#             print(serializer.errors)
#             return serializer.errors
        
#     except Exception as e:
#         return str(e)
    
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @api_view(['POST'])
# def anomaly_check(request):
#     try:
#         dbname = request.data['dbname']
#         user = request.data['user']
#         password = request.data['password']
#         host = request.data['host']
#         query = request.data['query']
#         db_output = connect_to_db(dbname, user, password, host, query)
#         anomaly = submit_data(db_output)
#         if anomaly == "OK":
#             return Response("OK", status=status.HTTP_200_OK)
#         else:
#             return Response(anomaly, status=status.HTTP_400_BAD_REQUEST)
#         # return Response(anomaly, status=status.HTTP_200_OK)
#     except Exception as e: 
#         return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)






@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(['POST'])
def missing_invoices(request):
    if request.method == "POST":
        # print(request.data)
        try:
            df2 = pd.DataFrame.from_dict(request.data['data'], orient="columns")
            # print(df2)
            result = missing_invoice.main(df2)
            # print(result)
            for i in result:
                i['location'] = models.Location.objects.get(location=i['location']).pk
            # result['invoices'] = ','.join(map(str, result['invoices']))
            serializer = serializers.MissingInvoiceSerializer(data=result, many=True)
            if serializer.is_valid():
                # print(serializer.data)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                # print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        # print(request.data)
# def missing_invoices(request):
#     if request.method == "POST":
#         try:
#             data = request.data
#             if not data:
#                 raise ValueError("Data not found in the request.")

#             # Perform type validation for specific fields
#             if not isinstance(data.get('date'), datetime.date):
#                 raise ValueError("Field 'date' should be a valid date.")
            
#             if not isinstance(data.get('ntn'), int):
#                 raise ValueError("Field 'ntn' should be a string.")

#             # Proceed with processing the data
#             df2 = pd.DataFrame.from_dict(data, orient="columns")
#             result = missing_invoice.main(df2)
#             serializer = serializers.MissingInvoiceSerializer(data=result, many=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response("OK", status=status.HTTP_202_ACCEPTED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


































@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(['POST'])
def submit_data(request):
    if request.method == "POST":
        try:
            serializer = serializers.AnomalySerializer(data=request.data['data'], many=True)
            
            if serializer.is_valid():
                
                df = pd.DataFrame.from_dict(request.data['data'])
                prediction = run_pipeline.main(df)
                
                df['anomaly'] = prediction
                df.rename(columns={'consider_for_Annex': 'consider_for_annex'}, inplace=True)
                
                data = df.to_dict(orient='records')
                
                for i in data:
                    i['ntn'] = models.NTN.objects.get(ntn=i['ntn'])
                    i['location'] = models.Location.objects.get(location=i['location'])
                    i['anomaly'] = models.AnomalyInfo.objects.get(pk=i['anomaly'])
                    i['created_date_time'] = datetime.datetime.fromisoformat(i['created_date_time'])
                    del i['name']
                
                models.Anomaly.objects.bulk_create([models.Anomaly(**record) for record in data])
                return Response("OK", status=status.HTTP_200_OK)
            else:    
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
