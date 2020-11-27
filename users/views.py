from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from util.responseBuilder import Response_Builder
from rest_framework.response import Response
from rest_framework import status
from util.errorMessages import ErrorMsg
from rest_framework import permissions, authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from .models import OwnUser
from .serializers import UserSerializer
import pytz
import json

Resp = Response_Builder()
ErrorMSG = ErrorMsg()

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

# Create your views here.

class login(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
            if username is None or password is None:
                return Response({'error': 'Please provide both username and password'},
                                status=HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': 'Invalid Credentials'},
                                status=HTTP_404_NOT_FOUND)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key},
                            status=HTTP_200_OK)
        except Exception as e:
            print(3, 'Error, no se puede realizar login' + str(e))
            return Resp.send_response(_status=503, _msg=ErrorMSG.get_msg(5003), _data=e)


class userList(APIView):
    def get(self, request, format=None):
        try:
            user = OwnUser.objects.all()
            user_serializer = UserSerializer(user, many=True)

            return Resp.send_response(_status=200, _msg=ErrorMSG.get_msg(200), _data=user_serializer.data)
        except Exception as e:
            return Resp.send_response(_status=500, _msg=ErrorMSG.get_msg(500), _data=e)

    def post(self, request, format=None):
        try:
            #{"name": "nathalia"}
            user_name = request.data['name']
            if OwnUser.objects.filter(name=user_name).count() > 0:
                return Resp.send_response(_status=409, _msg=ErrorMSG.get_msg(409))
            else:
                user = OwnUser()
                user.name = user_name
                user.save()
                return Resp.send_response(_status=201, _msg=ErrorMSG.get_msg(201))
        except Exception as e:
            print(e)
            return Resp.send_response(_status=500, _msg=ErrorMSG.get_msg(500), _data=e)


class userDetail(APIView):
    def put(self, request, format=None):
        try:
            user_id = request.data['user']['id']
            user_name = request.data['user']['name']
            user = OwnUser.objects.get(id=user_id)
            user.name = user_name
            user.save()
            return Resp.send_response(_status=200, _msg=ErrorMSG.get_msg(200))
        except Exception as e:
            return Resp.send_response(_status=500, _msg=ErrorMSG.get_msg(500), _data=e)

    def delete(self, request, format=None):
        try:
            user_id = request.data['user']['id']
            user = OwnUser.objects.get(id=user_id)
            user.delete()
            return Response(_status=204, _msg=ErrorMSG.get_msg(204))
        except Exception as e:
            return Resp.send_response(_status=500, _msg=ErrorMSG.get_msg(500), _data=e)

