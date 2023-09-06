import json
import random
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import DataPoint


def index(request):
    data_points = DataPoint.objects.all().order_by('date')

    interval_length = timedelta(hours=4)
    start_interval = data_points.first().date
    end_interval = start_interval + interval_length

    intervals = []

    while end_interval <= data_points.last().date:
        intervals.append((round(start_interval.timestamp()), round(end_interval.timestamp())))
        start_interval = end_interval
        end_interval = start_interval + interval_length

    context = {'intervals': intervals,
               'data_json': []}
    return render(request, 'index.html', context)

def update_interval(request):
    if request.method == 'POST':
        start_timestamp = int(request.POST['intervals[0][start_timestamp]'])
        end_timestamp = int(request.POST['intervals[0][end_timestamp]'])
        start_datetime = timezone.datetime.fromtimestamp(float(start_timestamp))
        end_datetime = timezone.datetime.fromtimestamp(float(end_timestamp))
        start_datetime = timezone.make_aware(start_datetime)
        end_datetime = timezone.make_aware(end_datetime)
        total_interval_seconds = (end_datetime - start_datetime).total_seconds()
        
        new_interval_data = []

        # Если интервал больше 60 секунд, разделим его на 60 интервалов
        if total_interval_seconds >= 60:
            desired_interval_count = 60
            interval_length = total_interval_seconds / desired_interval_count
            for i in range(desired_interval_count):
                start_interval = start_datetime + timedelta(seconds=interval_length * i)
                end_interval = start_datetime + timedelta(seconds=interval_length * (i + 1))

                interval_data_subset = DataPoint.objects.filter(date__gte=start_interval, date__lt=end_interval)

                min_value = min(interval_data_subset, key=lambda x: x.number).number
                max_value = max(interval_data_subset, key=lambda x: x.number).number

                new_interval_data.append([int(start_interval.timestamp()), int(end_interval.timestamp()), min_value, max_value])
        else:
            print('==== 30')
            desired_interval_count = 30
            finish = desired_interval_count - total_interval_seconds
            difference = finish // 2
            start_datetime = start_datetime - timedelta(seconds=difference)
            interval_length = 1
            for i in range(desired_interval_count):
                start_interval = start_datetime + timedelta(seconds=interval_length * i)
                end_interval = start_datetime + timedelta(seconds=interval_length * (i + 1))

                interval_data_subset = DataPoint.objects.filter(date__gte=start_interval, date__lt=end_interval)
                value = interval_data_subset[0].number
                if value > 0:
                    max_value = max(interval_data_subset, key=lambda x: x.number).number
                    min_value = 0
                else:
                    min_value = min(interval_data_subset, key=lambda x: x.number).number
                    max_value = 0
                new_interval_data.append([int(start_interval.timestamp()), int(end_interval.timestamp()), min_value, max_value])

        # Создаем интервалы
        new_data_json = json.dumps(new_interval_data)
        response_data = {'data_json': new_data_json}
        return JsonResponse(response_data)








def new_interval(request):
    if request.method == 'POST':
        start_timestamp = int(request.POST['start_timestamp'])
        end_timestamp = int(request.POST['end_timestamp'])

        print("start_timestamp:", start_timestamp)
        print("end_timestamp:", end_timestamp)
        
        start_datetime = timezone.datetime.fromtimestamp(start_timestamp)
        end_datetime = timezone.datetime.fromtimestamp(end_timestamp)
        
        total_interval_seconds = (end_datetime - start_datetime).total_seconds()
        
        if total_interval_seconds < 50:
            response_data = {'error': 'Interval is too short to be divided into 50 parts'}
            return JsonResponse(response_data, status=400)
        
        new_interval_data = []
        
        for i in range(0, 50):
            start_interval = start_datetime + timedelta(seconds=total_interval_seconds * i / 50)
            end_interval = start_datetime + timedelta(seconds=total_interval_seconds * (i + 1) / 50)
            
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
