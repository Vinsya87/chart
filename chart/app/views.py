import json
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse
import random
from .models import DataPoint


def index(request):
    data_points = DataPoint.objects.all().order_by('date')

    total_time_range = data_points.last().date - data_points.first().date
    session_selected_interval = request.session.get('selected_interval')
    
    if session_selected_interval:
        interval_duration = session_selected_interval / 10
    else:
        interval_duration = total_time_range.total_seconds() / 10
    
    title = f'{data_points.last().date.strftime("%Y-%m-%d %H:%M:%S")} - {data_points.first().date.strftime("%Y-%m-%d %H:%M:%S")}'

    data = []
    for i in range(0, 10):
        start_datetime = data_points.first().date + timedelta(seconds=interval_duration * i)
        end_datetime = start_datetime + timedelta(seconds=interval_duration)

        interval_data = data_points.filter(date__gte=start_datetime, date__lt=end_datetime)

        min_value = min(interval_data, key=lambda x: x.number).number
        max_value = max(interval_data, key=lambda x: x.number).number

        data.append([int(start_datetime.timestamp()), int(end_datetime.timestamp()), min_value, max_value])

    data_json = json.dumps(data)
    context = {
        'data_json': data_json,
        'title': title
    }

    return render(request, 'index.html', context)


def update_interval(request):
    if request.method == 'POST':
        start_timestamp = float(request.POST.get('start_timestamp'))
        end_timestamp = float(request.POST.get('end_timestamp'))
        start_datetime = timezone.datetime.fromtimestamp(float(start_timestamp))
        end_datetime = timezone.datetime.fromtimestamp(float(end_timestamp))
        start_datetime = timezone.make_aware(start_datetime)
        end_datetime = timezone.make_aware(end_datetime)
        total_interval_seconds = (end_datetime - start_datetime).total_seconds()
        if total_interval_seconds < 10:
            response_data = {'error': 'Interval is too short to be divided into 10 parts'}
            return JsonResponse(response_data, status=400)
        new_interval_data = []
        for i in range(0, 10):
            start_interval = start_datetime + timedelta(seconds=total_interval_seconds * i / 10)
            end_interval = start_datetime + timedelta(seconds=total_interval_seconds * (i + 1) / 10)

            interval_data_subset = DataPoint.objects.filter(date__gte=start_interval, date__lt=end_interval)

            min_value = min(interval_data_subset, key=lambda x: x.number).number
            max_value = max(interval_data_subset, key=lambda x: x.number).number

            new_interval_data.append([int(start_interval.timestamp()), int(end_interval.timestamp()), min_value, max_value])

        new_data_json = json.dumps(new_interval_data)
        response_data = {'data_json': new_data_json}
        return JsonResponse(response_data)


def populate_database(request):
    if DataPoint.objects.exists():
        return redirect('app:index')

    end_date = timezone.now()
    start_date = end_date - timedelta(days=1)
    current_date = start_date
    unique_numbers = list(range(-1000000, 1000001))
    random.shuffle(unique_numbers)

    while current_date <= end_date and unique_numbers:
        number = unique_numbers.pop()
        data_point = DataPoint(date=current_date, number=number)
        data_point.save()

        current_date += timedelta(seconds=1)

    return redirect('app:index')


def clear_data(request):
    DataPoint.objects.all().delete()
    return redirect('app:index')


def clear_cache(request):
    if 'selected_interval' in request.session:
        del request.session['selected_interval']
    return redirect('app:index')
