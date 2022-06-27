from django.http import JsonResponse, QueryDict, HttpResponse
from rest_framework.utils import json
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .client import get_external_data, get_user_id

class API (GenericAPIView):
    @api_view(['DELETE', 'PUT'])
    def delete_or_put(request, id):
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            zaznam_neexistuje = {
                "message": "The post does not exist"
            };

            error = {
                "error": zaznam_neexistuje
            };

            json_object = json.dumps(error, ensure_ascii=False, indent=4, separators=(',', ':'))
            return HttpResponse(json_object, status=404, content_type="application/json")

        if request.method == 'DELETE':
            post.delete()
            return HttpResponse(status=204, content_type="application/json")

        elif request.method == 'PUT':
            body = request.body
            serializer = PostSerializer(post, data=body)
            if body:
                body_json = json.loads(body)
                for edit in body_json:
                    if edit == 'title':
                        new_title = body_json[edit]
                        Post.objects.filter(pk=id).update(title=new_title)

                    if edit == 'body':
                        new_body = body_json[edit]
                        Post.objects.filter(pk=id).update(body=new_body)

                serializer = PostSerializer(Post.objects.get(pk=id))
                json_object = json.dumps(serializer.data, ensure_ascii=False, indent=4, separators=(',', ':'))
                return HttpResponse(json_object, status=200, content_type="application/json")

            elif not serializer.is_valid():
                return HttpResponse(serializer.errors, status=400, content_type="application/json")


    @api_view(['GET', 'POST'])
    def get_post(request):
        if request.method == 'POST':
            serializer = PostSerializer(data=request.data)
            errors = []
            if not serializer.initial_data['title']:
               error = {
                    "field": "title",
                    "reasons": "is_blank"
                    }
               errors.append(error)

            if not serializer.initial_data['body']:
                    error = {
                        "field": "body",
                        "reasons": "is_blank"
                    }
                    errors.append(error)

            if not serializer.initial_data['userID']:
                    error = {
                        "field": "userID",
                        "reasons": "is_blank"
                    }
                    errors.append(error)

            if not get_user_id(serializer.initial_data['userID']):
                    error = {
                        "field": "userID",
                        "reasons": "Unknown"
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
                    errors = []
                    error = {
                        "field": "userID",
                        "reasons": "Unknown"
                    }
                    errors.append(error)
                    found_errors = {
                        "errors": errors
                    };
                    json_object = json.dumps(found_errors, ensure_ascii=False, indent=4, separators=(',', ':'))
                    return HttpResponse(json_object, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)


        if request.method == 'GET':
            id = request.GET.get('id')
            userid = request.GET.get('userid')
            if id is not None:
                try:
                    post = Post.objects.get(id=id)

                except ValueError as v:
                    errors = []
                    error = {
                        "field": "ID",
                        "reasons": "Is not an integer"
                    }

                    errors.append(error)
                    found_errors = {
                        "errors": errors
                    };

                    json_object = json.dumps(found_errors, ensure_ascii=False, indent=4, separators=(',', ':'))
                    return HttpResponse(json_object, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

                except Post.DoesNotExist:
                    if get_external_data(id):
                        post = Post.objects.last()

                    else:
                        errors = []
                        error = {
                            "field": "ID",
                            "reasons": "Invalid ID"
                        }
                        errors.append(error)
                        found_errors = {
                            "errors": errors
                        };
                        json_object = json.dumps(found_errors, ensure_ascii=False, indent=4, separators=(',', ':'))
                        return HttpResponse(json_object, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
                serializer = PostSerializer(post)
                return JsonResponse(serializer.data)

            if userid is not None:
                try:
                    post = Post.objects.filter(userID=userid)
                    if post.count() == 0:
                        errors = []
                        error = {
                            "field": "userID",
                            "reasons": "Unknown userID"
                        }
                        errors.append(error)
                        found_errors = {
                            "errors": errors
                        };
                        json_object = json.dumps(found_errors, ensure_ascii=False, indent=4, separators=(',', ':'))
                        return HttpResponse(json_object, content_type="application/json",
                                            status=status.HTTP_400_BAD_REQUEST)

                except ValueError as v:
                    errors = []
                    error = {
                        "field": "UserID",
                        "reasons": "Is not an integer"
                    }

                    errors.append(error)
                    found_errors = {
                        "errors": errors
                    };

                    json_object = json.dumps(found_errors, ensure_ascii=False, indent=4, separators=(',', ':'))
                    return HttpResponse(json_object, content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

                else:
                    serializer = PostSerializer(post, many=True)
                    return Response(serializer.data)
