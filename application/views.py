from django.shortcuts import render
from django.http import JsonResponse, QueryDict, HttpResponse
from rest_framework.utils import json

from .models import Drink, Post, User
from .serializers import DrinkSerializer, PostSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .client import get_external_data, get_user_id


@api_view(['DELETE', 'PUT'])
def delete_post(request, id):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        body = request.body
        body_json = json.loads(body)
        for edit in body_json:
            if edit == 'title':
               new_title = body_json[edit]
               Post.objects.filter(pk=id).update(title=new_title)

            if edit == 'body':
               new_body = body_json[edit]
               Post.objects.filter(pk=id).update(body=new_body)

        serializer = PostSerializer(Post.objects.filter(pk=id), data=request.data)
        if body is not None:
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        try:
            serializer.initial_data['title']
        except Exception as e:
            print('exception')
            print(e)

        if not serializer.is_valid():
            errors=[]
            if not serializer.data['title']:
                error = {
                    "field": "title",
                    "reasons": "is_blank"
                }
                errors.append(error)

            if not serializer.data['body']:
                error = {
                    "field": "body",
                    "reasons": "is_blank"
                }
                errors.append(error)

            if not serializer.data['userID']:
                error = {
                    "field": "userID",
                    "reasons": "is_blank"
                }
                errors.append(error)

            if errors:
                found_errors = {
                    "errors": errors
                };

                json_object = json.dumps(found_errors, ensure_ascii=False, indent=4, separators=(',', ':'))
                return HttpResponse(json_object, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)



        if serializer.is_valid():
            if get_user_id(serializer.validated_data['userID']):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("invalid userID", status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'GET':
        id = request.GET.get('id')
        userid = request.GET.get('userid')
        if id is not None:
            print("id not none")
            try:
                post = Post.objects.get(id=id)
                print(post)
            except ValueError as v:
                return Response("Id neobsahuje cislo")
            except Post.DoesNotExist:
                print("Som except")
                if get_external_data(id):
                    post = Post.objects.last()  #externe je 3. ale ulozeny ako 2., chcem 2., ale uz sa neviem dostat k
                                                    #druhemu, ktory je ulozeny v externej api
                else:
                    return Response("neexistujuce ID", status=status.HTTP_400_BAD_REQUEST)
            serializer = PostSerializer(post)
            return JsonResponse(serializer.data)

        if userid is not None:
            post = Post.objects.filter(userID=userid)
            if post.count() == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = PostSerializer(post, many=True)
                return Response(serializer.data)


@api_view(['GET', 'POST'])
def drink_list(request, format = None):

    #get all drinks
    #serialize them
    #return json
    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return JsonResponse({'drinks': serializer.data})

    if request.method == 'POST':
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id, format = None):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DrinkSerializer(drink, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)