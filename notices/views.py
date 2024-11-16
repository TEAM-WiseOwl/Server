from django.shortcuts import render
from notices.models import *
from rest_framework.views import APIView
from notices.crawler import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



class Notice(APIView):
  permission_classes = [AllowAny]
  authentication_classes = []
  def get(self, request):
    temp = "https://soft.hufs.ac.kr/"
    # subscribe = Subscribe.objects.get(user_id=request.user_id)
    crawl_notices_department()
    return Response({"message": "Notices fetched successfully"})
  

