from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib import auth
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
# Create your views here.
def test(request: Request):
    print('*'*20)
    print(request.method, request._request.COOKIES, request.headers)
    print(request.data)
    print(request.user, request.user.is_authenticated)
    print(request.auth)
    print('*'*20)
    return Response({'view', 'test'})


