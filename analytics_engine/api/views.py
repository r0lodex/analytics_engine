from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets
from ae_reflex.models import *
from rest_framework import status
from api.serializer import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import json


@api_view(['POST'])
@permission_classes((AllowAny,))
def store_events(request, external_id):
    project = get_object_or_404(Project, external_id=external_id)

    if request.method == 'POST':
        event = Event.objects.create(project=project, data=request.data)
        serializer = EventSerializer(event, context={'request': request})

        source_key = (request.META.get('HTTP_SOURCE_KEY', None))

        keys = Key.objects.filter(project=project)
        if keys.count():
            try:
                keys = keys.get(unique_id=source_key)
                event.source_key = keys
                event.save()
            except Key.DoesNotExist:
                return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((AllowAny,))
def count_queries(request, external_id):
    d = {}
    l = []
    query = {}
    today = datetime.date.today()
    source_key = None

    if request.method == 'POST':
        data = request.data
        if "source_key" in data:
            source_key = data["source_key"]

        if "query_param" in data:
            query = json.dumps(data["query_param"])

        if "date_range" in data:
            date_range = data["date_range"]
            if date_range == "today":
                start_date = today

                d["total"] = count_events(external_id, start_date, query=query, source_key=source_key)
                d["date"] = start_date

            elif date_range == "yesterday":
                end_date = today
                start_date = end_date - datetime.timedelta(1)

                d["total"] = count_events(external_id, start_date, end_date, query, source_key=source_key)
                d["date"] = start_date

            elif "days" in date_range:
                day = int(date_range["days"])
                end_date = datetime.datetime.now()
                start_date = today
                initial_date = today - datetime.timedelta(day)

                d['total'] = count_events(external_id, initial_date, end_date, query, source_key=source_key)

                for i in range(0, day):
                    di = {}
                    di['date'] = start_date
                    di['count'] = count_events(external_id, start_date, end_date, query, source_key=source_key)
                    l.append(di)

                    end_date = start_date
                    start_date = end_date - datetime.timedelta(1)

                d['results'] = l

            elif "weeks" in date_range:
                week = int(date_range["weeks"])
                year, weeknumber, weekday = today.isocalendar()
                day_diff = weekday - 1
                end_date = datetime.datetime.now()
                start_date = datetime.date.today() - datetime.timedelta(day_diff)  # start date set to first day of the current week
                initial_date = start_date - datetime.timedelta(7*(week-1))
                #initial date set to (first day of current week - (7 days * (total number of weeks being queried - 1(current week)))

                d["total"] = count_events(external_id, initial_date, end_date, query, source_key=source_key)

                for i in range(0, week):
                    di = {}
                    year, weeknumber, weekday = start_date.isocalendar()

                    di['week'] = weeknumber
                    di['count'] = count_events(external_id, start_date, end_date, query, source_key=source_key)
                    di['date'] = start_date
                    l.append(di)

                    end_date = start_date
                    start_date = end_date - datetime.timedelta(7)

                d["results"] = l

            elif "months" in date_range:
                month = int(date_range["months"])
                initial_date = today.replace(day=1)
                initial_date = initial_date - relativedelta(months=month-1)
                end_date = datetime.datetime.now()
                start_date = today.replace(day=1)

                d["total"] = count_events(external_id, initial_date, end_date, query, source_key=source_key)

                for i in range(0, month):
                    di = {}
                    di['count'] = count_events(external_id, start_date, end_date, query, source_key=source_key)
                    di['month'] = start_date.strftime("%b %Y")
                    l.append(di)

                    end_date = start_date
                    start_date = end_date - relativedelta(months=1)

                d["results"] = l

            elif "years" in date_range:
                year = int(date_range["years"])
                initial_date = today.replace(day=1, month=1)
                initial_date = initial_date - relativedelta(years=year-1)
                end_date = datetime.datetime.now()
                start_date = today.replace(day=1, month=1)

                d["total"] = count_events(external_id, initial_date, end_date, query, source_key=source_key)

                for i in range(0, year):
                    di = {}
                    di['count'] = count_events(external_id, start_date, end_date, query, source_key=source_key)
                    di['year'] = start_date.strftime("%Y")
                    l.append(di)

                    end_date = start_date
                    start_date = end_date - relativedelta(years=1)

                d["results"] = l

            elif date_range == "all":
                d["total"] = count_events(external_id, query=query)

        return Response(d, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
def raw_queries(request, external_id):
    project = Project.objects.get(external_id=external_id)
    count = 15
    events = Event.objects.filter(project=project)
    d = {}

    if request.method == 'POST':
        data = request.data

        if "source_key" in data:
            source_key = data["source_key"]
            events = events.filter(source_key__unique_id=source_key)

        if "query_param" in data:
            jsond = json.dumps(data["query_param"])
            events = events.filter(data__jcontains=jsond)

        if "count" in data:
            count = int(data["count"])

        events = events.order_by('-created')[:count]

    serializer = EventSerializer(events, many=True, context={'request': request})
    d['events'] = serializer.data

    return Response(d, status=status.HTTP_200_OK)


def count_events(external_id, start_date=None, end_date=None, query={}, source_key=None):
    project = Project.objects.get(external_id=external_id)
    events = Event.objects.filter(project=project)

    if start_date:
        events = events.filter(created__gte=start_date)
    if end_date:
        events = events.filter(created__lt=end_date)
    if source_key:
        events = events.filter(source_key__unique_id=source_key)

    events = events.filter(data__jcontains=query)

    return events.count()


