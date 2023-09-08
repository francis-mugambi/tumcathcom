from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from portal.models import User
from .serializers import membersSerializer
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
import requests

@api_view(['GET', 'PUT', 'DELETE'])
def getRoute(request):
     routes = [
        {"title":"This-is-a-bloglorem-ipsum-dolor-sit-amet-consectetur-adipisicing-el", "body":"This is a blogLorem, ipsum dolor sit amet consectetur adipisicing elit. Iusto veritatis incidunt unde, a vel ab quis, facilis expedita illum deserunt sit voluptatum repellendus quos optio mollitia asperiores … read more...", "author":"frankmugah97@gmail.com"},
        {"title":"This-is-a-bloglorem-ipsum-dolor-sit-amet-consectetur-adipisicing", "body":"To nature members spiritually, morally, physically, socially, economically and intellectually. To enlighten members on their roles in the society. To help members realize and develop their talents positively. Training leaders … read more...", "author":"francis97@gmail.com"},
        {"title":"Hail-marry-prayer", "body":"Lorem, ipsum dolor sit amet consectetur adipisicing elit. Iusto veritatis incidunt unde, a vel ab quis, facilis expedita illum deserunt sit voluptatum repellendus quos optio mollitia asperiores error magni debitis! … read more...", "author":"francis97@gmail.com"}
     ]
    
     return Response(routes)

@api_view(['GET','POST'])
def customers(request):
    if request.method == 'POST': 
        member_data = JSONParser().parse(request) 
        member_serializer = membersSerializer(member, data=member_data) 
        if member_serializer.is_valid(): 
            member_serializer.save() 
            return JsonResponse(member_serializer.data, status=status.HTTP_201_CREATED) 
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    else:
        customers = User.objects.filter().all()
        serialize = membersSerializer(customers, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH','POST'])
def customer(request, str):
    # member = User.objects.get(id=str)
    # serialize = membersSerializer(member, many=False)
    # return Response(serialize.data)

    try: 
        member = User.objects.get(id=str)
    except User.DoesNotExist: 
        return Response({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET': 
        member_serializer = membersSerializer(member) 
        return Response(member_serializer.data, status=status.HTTP_200_OK) 

    elif request.method == 'PUT': 
        member_data = JSONParser().parse(request) 
        member_serializer = membersSerializer(member, data=member_data) 
        if member_serializer.is_valid(): 
            member_serializer.save() 
            return JsonResponse(member_serializer.data, status=status.HTTP_201_CREATED) 
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'POST': 
        member_data = JSONParser().parse(request) 
        member_serializer = membersSerializer(member, data=member_data) 
        if member_serializer.is_valid(): 
            member_serializer.save() 
            return JsonResponse(member_serializer.data, status=status.HTTP_201_CREATED) 
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'PATCH': 
        member_data = JSONParser().parse(request) 
        member_serializer = membersSerializer(member, data=member_data) 
        if member_serializer.is_valid(): 
            context = {
                'user' : member_data,	
            }
            return render(request, 'api/member.html', context)
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE': 
        member.delete() 
        return Response({'message': 'Member was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    