from django.shortcuts import render
from rest_framework.views import APIView
from users.models import OwnUser
from .models import User_Tasks
from .serializers import User_TasksSerializer
from util.responseBuilder import Response_Builder
from rest_framework.response import Response
from util.errorMessages import ErrorMsg

Resp = Response_Builder()
ErrorMSG = ErrorMsg()
# Create your views here.
class taskList(APIView):
    def get(self, request, format=None):
        try:
            print('hola')
            print(User_Tasks.objects.all())
            task = User_Tasks.objects.all()
            print(task)
            task_serializer = User_TasksSerializer(task, many=True)
            print(task_serializer)
            return Resp.send_response(_status=200, _msg=ErrorMSG.get_msg(200), _data=task_serializer.data)
        except Exception as e:
            print(e)
            return Resp.send_response(_status=500, _msg=ErrorMSG.get_msg(500), _data=e)

    def post(self, request, format=None):
        try:
            #{"name": "descreipcion de tarea 1"}
            taskInfo = request.data['task']
            user_id = taskInfo['user_id']
            print(taskInfo)
            task = User_Tasks()
            task.description = taskInfo['description']
            if(taskInfo['state'] == 'To Do' or taskInfo['state'] == 'To Done'):
                task.state = taskInfo['state']
            else:
                return Resp.send_response(_status=400, _msg=ErrorMSG.get_msg(400), _data="Task status is not formatted correctly")
            try:
                user = OwnUser.objects.get(id=user_id)
            except Exception as e:
                return Resp.send_response(_status=400, _msg=ErrorMSG.get_msg(400), _data="User not found")
            task.user_id = user
            task.save()
            return Resp.send_response(_status=201, _msg=ErrorMSG.get_msg(201))
        except Exception as e:
            print(e)
            return Resp.send_response(_status=400, _msg=ErrorMSG.get_msg(400), _data=e)


class taskDetail(APIView):
    def get(self, request, format=None):
        try:
            taskInfo = request.data['task']
            user_id = taskInfo['user_id']
            try:
                user = OwnUser.objects.get(id=user_id)
            except Exception as e:
                return Resp.send_response(_status=400, _msg=ErrorMSG.get_msg(400), _data="User not found")
                
            task = User_Tasks.objects.filter(user_id=user)
            print(task)
            task_serializer = User_TasksSerializer(task, many=True)
            print(task_serializer)
            return Resp.send_response(_status=200, _msg=ErrorMSG.get_msg(200), _data=task_serializer.data)
        except Exception as e:
            print(e)
            return Resp.send_response(_status=500, _msg=ErrorMSG.get_msg(500), _data=e)

    def put(self, request, format=None):
        try:
            taskInfo = request.data['task']
            print(taskInfo)
            task_id = taskInfo['id']
            task = User_Tasks.objects.get(id=task_id)
            task.description = taskInfo['description']
            task.state = taskInfo['state']
            user_id = taskInfo['user_id']
            try:
                user = OwnUser.objects.get(id=user_id)
            except Exception as e:
                return Resp.send_response(_status=400, _msg=ErrorMSG.get_msg(400), _data="User not found")
            task.user_id = user
            task.save()
            return Resp.send_response(_status=200, _msg=ErrorMSG.get_msg(200))
        except Exception as e:
            print(e)
            return Resp.send_response(_status=400, _msg=ErrorMSG.get_msg(400))

    def delete(self, request, format=None):
        try:
            task_id = request.data['task']['id']
            print(task_id)
            try:
                task = User_Tasks.objects.get(id=task_id)
            except Exception as e:
                return Resp.send_response(_status=400, _msg=ErrorMSG.get_msg(400), _data="Task not found")
            task.delete()
            return Resp.send_response(_status=200, _msg=ErrorMSG.get_msg(200))
        except Exception as e:
            print(e)
            return Resp.send_response(_status=500, _msg=ErrorMSG.get_msg(500), _data=e)
