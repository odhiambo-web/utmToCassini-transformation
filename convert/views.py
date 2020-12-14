from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import getSettings
from .converter import Converter
import json

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
