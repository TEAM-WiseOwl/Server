from django.shortcuts import render
from notices.models import *
from rest_framework.views import APIView
from notices.crawler import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import *
from .serializers import *
from rest_framework import status



class Notice(APIView):
  permission_classes = [AllowAny]
  authentication_classes = []
  def get(self, request):
    temp = "https://soft.hufs.ac.kr/"
    # subscribe = Subscribe.objects.get(user_id=request.user_id)
    crawl_notices_department()
    return Response({"message": "Notices fetched successfully"})

class Mypage(APIView):
  permission_classes = [AllowAny]
  authentication_classes = []
  def get(self,request, user_id):
    print(Profile.objects.all())
    profile = Profile.objects.get(user=user_id)
    serializer = MypageSerializer(profile)
    return Response(serializer.data)

class MyinfoEdit(APIView):
  def get(self, request, user_id):
    profile = Profile.objects.get(user=user_id)
    serializer = MypageSerializer(profile)
    return Response(serializer.data)
  
class MyCourseEdit(APIView):
  def get(self, request, user_id):
    profile=Profile.objects.get(user=user_id)
    serializers=CourseCompleteSerializer(profile)
    return Response(serializers.data)
  def delete(self, request):
    complete_year = request.data.get("complete_year")
    school_year = request.data.get("school_year")
    subject_name = request.data.get("subject_name")
    #major 테이블에서 찾음
    subject_department = SubjectDepartment.objects.filter(subject_name=subject_name).first()
    if subject_department:
      major_subject = MajorSubjectCompleted.objects.filter(
        user=request.user,
        subject_department=subject_department,
        completed_year=complete_year,
        school_year=school_year
        ).first()

        # 과목이 존재하면 삭제
      if major_subject:
        major_subject.delete()
        return Response({
                    "message": "Resource deleted successfully"
                }, status=status.HTTP_204_NO_CONTENT)
    #교양 테이블
    subject_gened = SubjectGened.objects.filter(subject_name=subject_name).first()
    if subject_gened:
      general_subject = GeneralSubjectCompleted.objects.filter(
                user=request.user,
                subject_gened=subject_gened,
                completed_year=complete_year,
                school_year=school_year
            ).first()

            # 과목이 존재하면 삭제
      if general_subject:
                general_subject.delete()
                return Response({
                    "message": "Resource deleted successfully"
                }, status=status.HTTP_204_NO_CONTENT)


  def patch(self, request):
    complete_year = request.data.get("complete_year")
    school_year = request.data.get("school_year")
    subject_name = request.data.get("subject_name")
    grade = request.data.get("grade")
    retry_yn = request.data.get("retry_yn")

    #전공테이블 찾음
    subject_department = SubjectDepartment.objects.filter(subject_name=subject_name).first()
    if subject_department:
      major_subject = MajorSubjectCompleted.objects.filter(
      user=request.user,
      subject_department=subject_department,
      completed_year=complete_year,
      school_year=school_year
        ).first()
      if major_subject:
        major_subject.grade = grade
        major_subject.retry_yn = retry_yn
        major_subject.save()
        return Response({
                        "message": "Resource updated successfully"
                    }, status=status.HTTP_200_OK)
    subject_gened = SubjectGened.objects.filter(subject_name=subject_name).first()
    if subject_gened:
      general_subject = GeneralSubjectCompleted.objects.filter(
        user=request.user,
        subject_gened=subject_gened,
        completed_year=complete_year,
        school_year=school_year
          ).first()
      if general_subject:
        general_subject.grade = grade
        general_subject.retry_yn = retry_yn
        general_subject.save()
        return Response({
                    "message": "Resource updated successfully"
                }, status=status.HTTP_200_OK)
    # 과목이 존재하지 않으면 오류 반환
      return Response({"detail": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)
    