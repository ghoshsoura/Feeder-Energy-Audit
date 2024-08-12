from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Project
import requests
import re
from django.http import JsonResponse
import oracledb
import pandas as pd

d = r'C:\Users\met.officer4\Downloads\instantclient-basic-windows.x64-21.13.0.0.0dbru\instantclient_21_13'
oracledb.init_oracle_client(d)
DB_URL = "safetd/safetd@//itsc-c2-scan:1521/SCTDDB"


# Function to establish a database connection
def connect_to_database():
    connection = oracledb.connect(DB_URL)
    return connection

@api_view(['GET'])
def fetch_all_details(request):
    if request.method == "GET":
        detail = Project.fetch_all()
        return Response(detail)


@api_view(['GET'])
def fetch_by_category(request, station):
    if request.method == "GET":
        details = Project.fetch_details_by_category(station)
        return Response(details)


@api_view(['GET'])
def fetch_by_station(request):
    if request.method == "GET":
        details = Project.fetch_details_by_station()
        return Response(details)


@api_view(['GET'])
def fetch_by_feeder(request, station_name):
    if request.method == "GET":
        details = Project.fetch_details_by_feeder(station_name)
        return Response(details)


@api_view(['GET'])
def fetch_by_options(request, st_name, fd_name):
    if request.method == "GET":
        details = Project.fetch_details_by_option(st_name, fd_name)
        return Response(details)
    

@api_view(['GET'])
def fetch_station_by_dtr(request, sname):
    if request.method == "GET":
        details = Project.fetch_station_by_dtr(sname)
        return Response(details)
    

@api_view(['GET'])
def fetch_by_all_dtr(request):
    df = pd.read_csv('D:/dtrList.csv')
    dtr_list = df[['SCODE', 'SNAME']].to_dict('records')
    return JsonResponse(dtr_list, safe=False)


@api_view(['GET'])
def fetch_overall_info(request):
    if request.method == "GET":
        details = Project.fetch_overall()
        return Response(details)
    
@api_view(['GET'])
def fetch_overall_consumption(request,feeder_code,date):
    if request.method == "GET":
        details = Project.fetch_overall_consumption(feeder_code,date)
        return Response(details)
    
@api_view(['GET'])
def fetch_by_dtr(request, station):
    if request.method == "GET":
        details = Project.fetch_details_by_dtr(station)
        details_2 = Project.fetch_details_by_feeder(station)
        details_3 = Project.fetch_details_by_station()

        specific_record = details
        ans = []

        try:
            for data in details_2:
                for sta in details_3:

                    modified = re.sub(r'[^a-zA-Z0-9\s]', ' ', data.get('FEEDER_NAME')) # type: ignore
                    res = modified.split(' ')
                    
                    for info in res:
                        if info==sta.get('STATION') :
                            result = Project.fetch_details_by_dtr(info)
                            ans = ans + result

            specific_record = ans
            if specific_record:
                return Response(specific_record)
            else:
                return Response({'error': 'Record not found'}, status=404)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=500)
        except ValueError as e:
            return Response({'error': 'Invalid JSON response'}, status=500)


@api_view(['GET'])
def fetch_by_dtr_by_station(request, dtr_id):
    if request.method == "GET":
        details = Project.fetch_details_by_dtr_category(dtr_id)
        return Response(details)


@api_view(['GET'])
def fetch_by_HT(request):
    df = pd.read_csv('D:/ht-cons.csv')
    dtr_list = df[['EN1', 'CONS_NUM']].to_dict('records')
    return JsonResponse(dtr_list, safe=False)

    
@api_view(['GET'])
def fetch_by_HT_ID(request, consumer_id):
    if request.method == 'GET':
        url = 'http://itgfscn2z1:38772/tdamr/service_get_masdreg_cinf.jsp'
        params = {
            'handshake': 'cHPo7dbRyoc0wrxs2Luc9SD1a30ji01s67a',
            'consumer_id': consumer_id
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json() # Assuming the response is in JSON format

            specific_record = None
            
            for record in data[0]['DATA']:
                if not record.get('EN2'):
                    result = re.sub(r'[^a-zA-Z0-9]', ' ',record.get('EN1'))
                else:
                    result = re.sub(r'[^a-zA-Z0-9]', ' ',record.get('EN1')+record.get('EN2'))


                if result == consumer_id:
                    specific_record = record
        
            if specific_record:
                return Response(specific_record)
            else:
                return Response({'error': 'Record not found'}, status=404)
            
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=500)
        except ValueError as e:
            return Response({'error': 'Invalid JSON response'}, status=500)
        
        
# @api_view(['GET'])
# def fetch_as_whole(request, station_id, feeder_id, dt_id, ht_id):
#     if request.method == 'GET':
#         details = Project.fetch_overall_details(station_id, feeder_id, dt_id)
#         try:
#             for info in details:
#                 val = info['SNAME'].split(' ')
#                 ht_id_m = ht_id.split(' ')
#                 if val[0] in ht_id_m:
#                     details[0]['HT_CONS'] = ht_id

#             return Response(details)

#         except requests.exceptions.RequestException as e:
#             return Response({'error': str(e)}, status=500)
#         except ValueError as e:
#             return Response({'error': 'Invalid JSON response'}, status=500)


# class ValidateDatesView(View):
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             station = data.get('station')
#             feeder_name = data.get('feeder_name')
#             child_type = data.get('child_type')
#             from_date = data.get('from_date')
#             to_date = data.get('to_date')

#             if not from_date or not to_date:
#                 return JsonResponse({'message': 'Please provide both From Date and To Date.'}, status=400)

#             message = (
#                 f"Station: {station}, Feeder Name: {feeder_name}, "
#                 f"DTR: {child_type}, HT Consumer: {child_type}, "
#                 f"Records from {from_date} to {to_date}"
#             )
#             return JsonResponse({'message': message}, status=200)
        
#         except json.JSONDecodeError:
#             return JsonResponse({'message': 'Invalid JSON data.'}, status=400)
        
@api_view(['POST'])
def insert_overall_details(request):
        try:
        # Extract data from the request
            connection = connect_to_database()
            data = request.data
            station = data.get('station')
            feeder_name = data.get('feeder_name')
            dtrs = data.get('dtrs')  # List of DTRs/HTs
            hts = data.get('hts')
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            
            cursor = connection.cursor()

            for i in range(len(feeder_name)-1,-1,-1):
                if feeder_name[i]=='(':
                    idx = i
                    break
            feeder_l = feeder_name[:idx-1]

            if not station:
                return Response({"error": "Please select a station"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not feeder_name:
                return Response({"error": "Please select a feeder name"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not from_date:
                return Response({"error": "Please select a from date"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not to_date:
                return Response({"error": "Please select a to date"}, status=status.HTTP_400_BAD_REQUEST)

            if not dtrs or not isinstance(dtrs, list):
                return Response({"error": "Please select one or more DTR details"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not hts or not isinstance(hts, list):
                return Response({"error": "Please select one or more HT details"}, status=status.HTTP_400_BAD_REQUEST)

            # Prepare and execute the SQL query for each DTR or HT
            for dtr in dtrs:
                child_name = 'D'

                child_code = dtr['SCODE']
                

                sql_query = """INSERT INTO TD_AMR.FDR_AUD_MATRIX (station, feeder_code, feeder_name, child_code, child_type, dt1, dt2)
                            VALUES (:STATION, (SELECT FEEDER_CODE FROM TD_AMR.FDR_INFO WHERE FEEDER_NAME = :FEEDER_NAME),
                            :FEEDER_NAME, :child_code, :child_type, to_date(:from_date,'YYYY-MM-DD'), to_date(:to_date,'YYYY-MM-DD'))
                            """
                cursor.execute(sql_query, {'STATION':station, 'FEEDER_NAME':feeder_l, 'child_code': child_code, 'child_type': child_name, 'from_date':from_date, 'to_date':to_date})
 
            for ht in hts:
                child_name = 'H'

                child_code = ht['CONS_NUM']

                sql_query = """INSERT INTO TD_AMR.FDR_AUD_MATRIX (station, feeder_code, feeder_name, child_code, child_type, dt1, dt2)
                            VALUES (:STATION, (SELECT FEEDER_CODE FROM TD_AMR.FDR_INFO WHERE FEEDER_NAME = :FEEDER_NAME),
                            :FEEDER_NAME, :child_code, :child_type, to_date(:from_date,'YYYY-MM-DD'), to_date(:to_date,'YYYY-MM-DD'))
                            """
                cursor.execute(sql_query, {'STATION':station, 'FEEDER_NAME':feeder_l, 'child_code': child_code, 'child_type': child_name, 'from_date':from_date, 'to_date':to_date})

            connection.commit()
            return Response({"message": "Records inserted successfully"}, status=status.HTTP_201_CREATED)

        except oracledb.DatabaseError as e:
            error, = e.args
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# @api_view(['POST'])
# def register_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     if not username or not password:
#         return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         user = User.objects.create_user(username=username, password=password)
#         user.save()
#         return Response({'success': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(username=username, password=password)
    
#     if user is not None:
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token), # type: ignore
#         })
#     else:
#         return Response({'error': 'Invalid Credentials'}, status=400)
    