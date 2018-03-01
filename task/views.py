"""
Views module
===========
"""
import json
from django.http import JsonResponse
from django.views import View
from utils.validators import task_data_validate_update, task_data_validate_create
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_200_DELETED,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_404_OBJECT_NOT_FOUND,
                                  RESPONSE_400_EMPTY_JSON)
from .models import Task



class TaskView(View):
    """Task view handles GET, POST, PUT, DELETE requests"""

    def get(self, request, task_id=None):
        """
        Method that handles GET request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param task_id: ID of the certain event.
        :type task_id: `int`

        :return: the response with the certain task information.
                 If task does not exist returns the 404 failed status code response.
            E.G.
            |    {
            |        "id": 4,
            |        "title": "Hello",
            |        "description": "i`m description",
            |        "status": 1,
            |        "created_at": 1510669962,
            |        "updated_at": 1510669962
            |    }
        :rtype: `HttpResponse object.
        """

        print(task_id)
        if task_id:
            task = Task.get_by_id(task_id)
            if not task:
                return RESPONSE_404_OBJECT_NOT_FOUND
            data = task.to_dict()
            return JsonResponse(data, status=200)

        tasks = Task.objects.all().exclude(status=2)
        data = {'tasks': [task.to_dict() for task in tasks]}
        return JsonResponse(data, status=200)


    def post(self, request):
        """
        Method that handles POST request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :return: the response with certain task information when the task was successfully
                 created or response with 400 or 404 failed status code.
        :rtype: `HttpResponse object.
        """

        data = json.loads(request.body)

        if not data:
            return RESPONSE_400_EMPTY_JSON


        if not task_data_validate_create(data):
            return RESPONSE_400_INVALID_DATA

        data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'status': data.get('status'),
        }
        task = Task.create(**data)
        if task:
            task = task.to_dict()
            return JsonResponse(task, status=201)

        return RESPONSE_400_DB_OPERATION_FAILED


    def put(self, request, task_id=None):
        """
        Method that handles PUT request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param task_id_id: ID of the certain task.
        :type task_id: `int`

        :return: response with status code 204 when event was successfully updated or response with
                 400, 403 or 404 failed status code.
        :rtype: `HttpResponse object.
        """


        task = Task.get_by_id(task_id)
        if not task:
            return RESPONSE_404_OBJECT_NOT_FOUND

        data = json.loads(request.body)

        if not task_data_validate_update(data):
            return RESPONSE_400_INVALID_DATA

        data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'status': data.get('status')
        }

        task.update(**data)
        return RESPONSE_200_UPDATED


    def delete(self, request, task_id=None):
        """
        Method that handles DELETE request.

        :param request: the accepted HTTP request.
        :type request: `HttpRequest object`

        :param task_id: ID of the certain task.
        :type task_id `int`

        :return: response with status code 200 when task was successfully deleted or response with
                 400 failed status code.
        :rtype: `HttpResponse object."""


        if task_id:
            Task.delete_by_id(task_id)
            return RESPONSE_200_DELETED

        return RESPONSE_400_DB_OPERATION_FAILED
