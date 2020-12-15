from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import getSettings, getTransformationParameters
from .converter import Converter, Geographic, Cassini
import json
from .utm import from_latlon

def index(request):
	return render(request, 'convert/index.html')


def upload(request):
	data = []
	if "GET" == request.method:
		return render(request, "convert/index.html")

	csv_file = request.FILES["csv_file"]

	#if file is too large, return
	if csv_file.multiple_chunks():
		return JsonResponse({'success': False, 'reason': 'File is too large'})

	file_data = csv_file.read().decode("utf-8")
	lines = file_data.split("\n")
	#loop over the lines and then display
	for line in lines:
		fields = line.split(",")
		if len(fields) == 5:
			data_dict = {}
			data_dict["index"] = fields[0]
			data_dict["lat"] = fields[1]
			data_dict["long"] = fields[2]
			data_dict["height"] = fields[3]
			data_dict["point_id"] = fields[4]
			data.append(data_dict)

	return JsonResponse({'success': True, 'points': data})

def convert(request):
	results = []
	if "GET" == request.method:
		return render(request, "convert/index.html")

	configuration = json.loads(request.POST.get('configs'))
	points = json.loads(request.POST.get('points'))

	conversion = Converter(points, getSettings(), configuration)
	results = conversion.convert()

	return JsonResponse({'success': True, 'cartesian': results})

def transform(request):
	results = []
	if "GET" == request.method:
		return render(request, "convert/index.html")

	configuration = json.loads(request.POST.get('configs'))
	points = json.loads(request.POST.get('points'))
	cartesian = json.loads(request.POST.get('cartesian'))

	conversion = Converter(points, getSettings(), configuration, cartesian)
	results = conversion.transform()

	return JsonResponse({'success': True, 'clarke': results})

def geographic(request):
	results = []
	if "GET" == request.method:
		return render(request, "convert/index.html")
	
	clarke = json.loads(request.POST.get('clarke'))

	conversion = Geographic(clarke, getSettings())
	results = conversion.geographic()

	return JsonResponse({'success': True, 'geographic': results})

def utm(request):
	results = []
	if "GET" == request.method:
		return render(request, "convert/index.html")
	
	geographic = json.loads(request.POST.get('geographic'))
	results = []
	for p in geographic:
		utm = from_latlon(p['x'], p['y'])
		results.append({'index':p['index'], 'x': utm[0], 'y': utm[1], 'point_id': p['point_id']})

	return JsonResponse({'success': True, 'utm': results})

def cassini(request):
	results = []
	if "GET" == request.method:
		return render(request, "convert/index.html")
	
	utm = json.loads(request.POST.get('utm'))
	config = json.loads(request.POST.get('config'))

	conversion = Cassini(utm, config, getTransformationParameters())
	results = conversion.cassini()

	return JsonResponse({'success': True, 'cassini': results})
