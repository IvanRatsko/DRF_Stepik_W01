# Create your views here.
import logging

import requests
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

recipients_url = 'https://stepik.org/media/attachments/course/73594/recipients.json'
product_sets_url = 'https://stepik.org/media/attachments/course/73594/beautyboxes.json'


class MainView(TemplateView):
    template_name = 'index.html'


@api_view(http_method_names=['GET'])
def recipients_list(request):
    shortdata = {}
    shortdatalist = []
    try:
        responce = requests.get(url=recipients_url, timeout=5)
    except requests.exceptions.Timeout as ex:
        logging.error(ex)
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    if responce.status_code != 200:
        return Response(status=status.HTTP_409_CONFLICT)

    try:
        recipients = responce.json()
        for item in recipients:
            shortdata.update(item['info'])
            shortdata.update(item['contacts'])
            shortdatalist.append(shortdata)
            shortdata = {}
        recipients = shortdatalist

    except Exception as ex:
        logging.error(ex)
        pass
    else:
        return Response(recipients)


@api_view(http_method_names=['GET'])
def recipients_detail(request, pk):
    shortdata = {}
    shortdatalist = []
    try:
        response = requests.get(url=recipients_url, timeout=5)
    except requests.exceptions.Timeout as ex:
        logging.error(ex)
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    if response.status_code != 200:
        return Response(status=status.HTTP_409_CONFLICT)

    try:
        recipients = response.json()
        for item in recipients:
            shortdata.update(item['info'])
            shortdata.update(item['contacts'])
            shortdatalist.append(shortdata)
            shortdata = {}
        recipients = shortdatalist



        result = next(recipient_item for index, recipient_item in enumerate(recipients) if index + 1 == pk)

        if result:
            return Response(result)

    except Exception as ex:
        logging.error(ex)
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['GET'])
def product_sets_list(request):
    result = []
    try:
        response = requests.get(url=product_sets_url, timeout=5)
    except requests.exceptions.Timeout as ex:
        logging.error(ex)
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    if response.status_code != 200:
        return Response(status=status.HTTP_409_CONFLICT)

    try:
        product_sets = response.json()

        if request.query_params:
            min_price = request.query_params.get('min_price')
            min_weight = request.query_params.get('min_weight')
            if min_price:
                for product_set in product_sets:
                    if int(product_set['price']) >= int(min_price):
                        result.append(product_set)
            elif min_weight:
                for product_set in product_sets:
                    if int(product_set['weight_grams']) >= int(min_weight):
                        result.append(product_set)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            result = product_sets

    except Exception as ex:
        logging.error(ex)
        pass
    else:
        return Response(result)


@api_view(http_method_names=['GET'])
def product_sets_detail(request, pk):
    try:
        response = requests.get(url=product_sets_url, timeout=5)
    except requests.exceptions.Timeout as ex:
        logging.error(ex)
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

    if response.status_code != 200:
        return Response(status=status.HTTP_409_CONFLICT)

    try:
        product_sets = response.json()
        result = next(product_set_item for index, product_set_item in enumerate(product_sets) if index + 1 == pk)

        if result:
            return Response(result)

    except Exception as ex:
        logging.error(ex)
        return Response(status=status.HTTP_404_NOT_FOUND)


def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1 align="center">Ошибка 404 </h1>')


def custom_handler500(request):
    return HttpResponseNotFound('<h1 align="center">Ошибка 500</h1>')
