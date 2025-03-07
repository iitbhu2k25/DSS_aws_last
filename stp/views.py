from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import json
import os 
import geopandas as gpd
from .models import Village,District,SubDistrict,State
from shapely.geometry import mapping
from .service import weight_redisturb,normalize_data,rank_process,process_geometries
def stp_home(request):
    return render(request, 'stp/prediction.html')

@csrf_exempt
def GetStatesView(request):
    states=State.objects.values('state_code','state_name')
    states=[{'id': state['state_code'],'name':state['state_name']} for state in states]
    return JsonResponse(list(states),safe=False)

@csrf_exempt
def GetDistrictView(request):
    if request.method == 'POST':
        state_id=int(json.loads(request.body).get('state'))
        print("state id is ",state_id)
        districts=District.objects.values('district_code','district_name').filter(state_id=state_id).order_by('district_name')
        districts=[{'id': district['district_code'],'name':district['district_name']} for district in districts]
        return JsonResponse(list(districts),safe=False)

@csrf_exempt
def GetSubDistrictView(request):
    if request.method == 'POST':
        district_id=(json.loads(request.body).get('districts'))
        SubDistricts=list(SubDistrict.objects.values('subdistrict_code','subdistrict_name').filter(district_id__in=district_id).order_by('subdistrict_name'))
        SubDistricts=[{'id': SubDistrict['subdistrict_code'],'name':SubDistrict['subdistrict_name']} for SubDistrict in SubDistricts]
        return JsonResponse(list(SubDistricts),safe=False)

@csrf_exempt
def  GetVillageView(request):
    if request.method == 'POST':
        SubDistrict_id=(json.loads(request.body).get('subDistricts'))
        villages=list(Village.objects.values('village_id','village_name').filter(subdistrict_id_id__in=SubDistrict_id))
        villages=[{'id': village['village_id'],'name':village['village_name']} for village in villages]
        return JsonResponse(list(villages),safe=False)


@csrf_exempt
def GetBoundry(request):
    if request.method == 'GET':
        try:
            print("try to get all the polygon")
            shapefile_path = os.path.join(settings.BASE_DIR, 'media','Rajat_data','shape_stp','state','state.shp')
            gdf = gpd.read_file(shapefile_path)
            if gdf.crs is None or gdf.crs.to_epsg() != 4326:
                gdf = gdf.to_crs(epsg=4326) 
            geojson_data = json.loads(gdf.to_json())
            print("staring sedn bakcen shpe file")
            return JsonResponse(geojson_data, safe=False)
            
        except Exception as e:
            print("error is", str(e))
            return JsonResponse({'error': str(e)}, status=500)
        
    if request.method == 'POST':
        try:
            # Read the shapefile
            request_data = json.loads(request.body)
            print(request_data)
            try:
                if request_data.get('subDistricts'):            
                    subDistricts=request_data.get('subDistricts')
                    print("getting District_Id is ",subDistricts)
                    subDistricts=list(map(int,subDistricts))
                    shapefile_path = os.path.join(settings.BASE_DIR, 'media', 'Rajat_data', 'shape_stp', 'subdistrict', 'subdistrict_updated.shp')
                    gdf = gpd.read_file(shapefile_path)
                    if gdf.crs is None or gdf.crs.to_epsg() != 4326:
                        gdf = gdf.to_crs(epsg=4326)
                    filtered_gdf = gdf[gdf['subdis_cod'].isin(subDistricts)]
                    geojson_data = json.loads(filtered_gdf.to_json())
                    return JsonResponse(geojson_data, safe=False)
                
                elif request_data.get('districts'):
                    District_Id=request_data.get('districts')
                    shapefile_path = os.path.join(settings.BASE_DIR, 'media', 'Rajat_data', 'shape_stp', 'district', 'district.shp')
                    gdf = gpd.read_file(shapefile_path)
                    if gdf.crs is None or gdf.crs.to_epsg() != 4326:
                        gdf = gdf.to_crs(epsg=4326)
                    filtered_gdf = gdf[gdf['district_c'].isin(District_Id)]
                    geojson_data = json.loads(filtered_gdf.to_json())
                    return JsonResponse(geojson_data, safe=False)
                
                else :
                    stateId=request_data.get('stateId')
                    if int(stateId)<10:
                        stateId='0'+stateId
                    shapefile_path = os.path.join(settings.BASE_DIR, 'media', 'Rajat_data', 'shape_stp', 'state', 'state.shp')
                    gdf = gpd.read_file(shapefile_path)
                    if gdf.crs is None or gdf.crs.to_epsg() != 4326:
                        gdf = gdf.to_crs(epsg=4326)
                    filtered_gdf = gdf[gdf['state_code'] == stateId]  
                    geojson_data = json.loads(filtered_gdf.to_json())
                    return JsonResponse(geojson_data, safe=False)
                
            except Exception as e:
                print(f"Error filtering or processing data: {str(e)}")
                return JsonResponse({'error': 'Error processing geographic data'}, status=500)
                
        except Exception as e:
            print(f"Error reading shapefile or processing request: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
def GetVillage_UP(request):
    try:
        try:
            request_data = json.loads(request.body)
            villages_list=request_data.get('village_name')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        try:
            gdf = gpd.read_file('media/shapefile/villages/Basin_Villages.shp')

        except Exception as e:
            print('erris is ',str(e))
            return JsonResponse({'error': 'Error reading geographic data'}, status=500)

        # Filter geodataframe
        print("village_list",villages_list)
        filtered_gdf = gdf[gdf['NAME_1'].isin(villages_list)]
        print("filtered_gdf",filtered_gdf)
        coordinates = process_geometries(filtered_gdf)
        print("coor",coordinates)
        if not coordinates:
            return JsonResponse({'error': 'Failed to extract valid coordinates'}, status=500)

        if len(coordinates) > 1:
            coordinates = [coordinates]

        return JsonResponse({'coordinates': coordinates})

    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)


@csrf_exempt
def GetTableView(request):
    if request.method == 'POST':
        request=json.loads(request.body)
        main_data=request.get('main_data')
        vig_data=main_data['villages']
        table_id=[]
        for i in vig_data:
            table_id.append(int(i[8:]))
        categories=request.get('categories')
        ans=Data.objects.values('name',*categories).filter(id__in=table_id)
        ans=list(ans)
        for i in ans:
            print(i)
        return JsonResponse(ans,safe=False)
    
@csrf_exempt
def GetRankView(request):
    if request.method == 'POST':
        request=json.loads(request.body)
        table_data=request.get('tableData')
        headings=[]
        for i in table_data[0]:
            headings.append(i)        
        headings.remove('name')
        weight_key=weight_redisturb(headings)
        table_data=normalize_data(table_data)
        ans=rank_process(table_data,weight_key,headings)
        print('main ans',ans)
        return JsonResponse(ans,safe=False)
