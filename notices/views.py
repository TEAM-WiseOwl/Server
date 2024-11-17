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
from datetime import datetime
from .models import *
from django.db.models import Q



class NoticePage(APIView):
  def get(self, request):
    user = request.user
    response_data = None
    try:
      subscribe_instance = Subscribe.objects.get(user_id=user.user_id)
    except Subscribe.DoesNotExist:
      return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    try:
      profile_instance = Profile.objects.get(user_id=user.user_id)
    except Profile.DoesNotExist:
       return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    subscribe_data = {
            "major": subscribe_instance.subscribe_major,
            "double": subscribe_instance.subscribe_double,
            "ai": subscribe_instance.subscribe_ai,
            "foreign": subscribe_instance.subscribe_foreign,
            "cfl": subscribe_instance.subscribe_cfl,
            "special_foreign": subscribe_instance.subscribe_special_foreign,
            "flex": subscribe_instance.subscribe_flex,
            "foreign_edu": subscribe_instance.subscribe_foreign_edu,
        }
    organ_notices = {}
    major_department = Department.objects.get(department_id=profile_instance.major_id)
    double_major_department = Department.objects.get(department_id=profile_instance.double_or_minor_id) if profile_instance.double_or_minor_id else None
        
    major_department_name = major_department.department_name
    double_major_department_name = double_major_department.department_name if double_major_department else None
    subscribe_instance = Subscribe.objects.get(user_id=user.user_id)
    subscribe_data = {
            "major": subscribe_instance.subscribe_major,
            "double": subscribe_instance.subscribe_double,
            "ai": subscribe_instance.subscribe_ai,
            "foreign": subscribe_instance.subscribe_foreign,
            "cfl": subscribe_instance.subscribe_cfl,
            "special_foreign": subscribe_instance.subscribe_special_foreign,
            "flex": subscribe_instance.subscribe_flex,
            "foreign_edu": subscribe_instance.subscribe_foreign_edu,
        }
    if subscribe_data["major"]:
      crawled_data=crawl_notices_department(department_id=profile_instance.major_id)
      for post in crawled_data:
        title = post['title']
        link = post['url']
        published_date = post['date']
        try:
          published_date = datetime.strptime(published_date, "%Y.%m.%d").date()
        except ValueError:
          published_date = None
        if not Notice.objects.filter(notice_link=link, user_id=user.user_id).exists():
                Notice.objects.create(
                    notice_title=title,
                    notice_link=link,
                    notice_date=published_date,
                    user_id=user.user_id,
                    notice_read=False,
                    department_id=major_department.department_id,


                )

      organ_notices[major_department_name] = crawl_notices_department(department_id=profile_instance.major_id)  # 크롤링된 공지사항
    if subscribe_data["double"]:
      organ_notices[double_major_department_name] = crawl_notices_department(department_id=profile_instance.double_or_minor_id)  
      crawled_data=crawl_notices_department(department_id=profile_instance.double_or_minor_id)
      for post in crawled_data:
        title = post['title']
        link = post['url']
        published_date = post['date']
        try:
          published_date = datetime.strptime(published_date, "%Y.%m.%d").date()
        except ValueError:
          published_date = None
        if not Notice.objects.filter(notice_link=link).exists():
                Notice.objects.create(
                    notice_title=title,
                    notice_link=link,
                    notice_date=published_date,
                    user_id=user.user_id,
                    notice_read=False,
                    department_id=double_major_department.department_id,


                )

    if subscribe_data["ai"]:
      organ_name = "AI교육원" 
      organ_notices[organ_name] = crawl_notices()
      crawled_data=crawl_notices()
      for post in crawled_data:
        title = post['title']
        link = post['url']
        published_date = post['date']
        try:
          published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
        except ValueError:
          published_date = None
        if not Notice.objects.filter(notice_link=link, user_id=user.user_id).exists():
                Notice.objects.create(
                    notice_title=title,
                    notice_link=link,
                    notice_date=published_date,
                    user_id=user.user_id,
                    notice_read=False,
                    notice_organ_id=6,


                )
    if subscribe_data["foreign"]:
      organ_name = "국제교류원" 
      organ_notices[organ_name] = crawl_notices_foreign(url="https://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=135456840&siteId=oia3&menuType=T&uId=8&sortChar=A&menuFrame=left&linkUrl=7_1.html&mainFrame=right") 
      crawled_data=crawl_notices_foreign(url="https://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=135456840&siteId=oia3&menuType=T&uId=8&sortChar=A&menuFrame=left&linkUrl=7_1.html&mainFrame=right")
      for post in crawled_data:
        title = post['title']
        link = post['url']
        published_date = post['date']
        try:
          published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
        except ValueError:
          published_date = None
        if not Notice.objects.filter(notice_link=link, user_id=user.user_id).exists():
                Notice.objects.create(
                    notice_title=title,
                    notice_link=link,
                    notice_date=published_date,
                    user_id=user.user_id,
                    notice_read=False,
                    notice_organ_id=1,


                )
    if subscribe_data["cfl"]:
      organ_name = "진로취업센터" 
      organ_notices[organ_name] = crawl_notices_foreign_cfl()
      crawled_data=crawl_notices_foreign_cfl()
      for post in crawled_data:
        title = post['title']
        link = post['url']
        published_date = post['date']
        try:
          published_date = datetime.strptime(published_date,  "%Y.%m.%d").date()
        except ValueError:
          published_date = None
        if not Notice.objects.filter(notice_link=link, user_id=user.user_id).exists():
                Notice.objects.create(
                    notice_title=title,
                    notice_link=link,
                    notice_date=published_date,
                    user_id=user.user_id,
                    notice_read=False,
                    notice_organ_id=5,


                )
                
    if subscribe_data["special_foreign"]:
      organ_name = "특수외국어교육진흥원"  # 기관명은 창업지원센터로 예시
      organ_notices[organ_name] = crawl_notices_foreign_special()
      crawled_data=crawl_notices_foreign_special()
      for post in crawled_data:
        title = post['title']
        link = post['url']
        published_date = post['date']
        try:
          published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
        except ValueError:
          published_date = None
        if not Notice.objects.filter(notice_link=link, user_id=user.user_id).exists():
                Notice.objects.create(
                    notice_title=title,
                    notice_link=link,
                    notice_date=published_date,
                    user_id=user.user_id,
                    notice_read=False,
                    notice_organ_id=4,


                )
    if subscribe_data["flex"]:
      organ_name = "FLEX 센터"  # 기관명은 창업지원센터로 예시
      organ_notices[organ_name] = crawl_notices_foreign(url='https://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=84761504&siteId=flex2&menuType=T&uId=6&sortChar=A&linkUrl=4_1.html&mainFrame=right')
      crawled_data=crawl_notices_foreign(url='https://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=84761504&siteId=flex2&menuType=T&uId=6&sortChar=A&linkUrl=4_1.html&mainFrame=right')
      for post in crawled_data:
        title = post['title']
        link = post['url']
        published_date = post['date']
        try:
          published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
        except ValueError:
          published_date = None
        if not Notice.objects.filter(notice_link=link, user_id=user.user_id).exists():
                Notice.objects.create(
                    notice_title=title,
                    notice_link=link,
                    notice_date=published_date,
                    user_id=user.user_id,
                    notice_read=False,
                    notice_organ_id=3,


                )
    if subscribe_data["foreign_edu"]:
      organ_name = "외국어교육센터"  
      organ_notices[organ_name] = crawl_notices_foreign(url='https://builder.hufs.ac.kr/user/indexSub.action?framePath=unknownboard&siteId=flec2&dum=dum&boardId=98772159&page=1&command=list')
      crawled_data=crawl_notices_foreign(url='https://builder.hufs.ac.kr/user/indexSub.action?framePath=unknownboard&siteId=flec2&dum=dum&boardId=98772159&page=1&command=list')
      for post in crawled_data:
        title = post['title']
        link = post['url']
        published_date = post['date']
        try:
          published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
        except ValueError:
          published_date = None
        if not Notice.objects.filter(notice_link=link, user_id=user.user_id).exists():
                Notice.objects.create(
                    notice_title=title,
                    notice_link=link,
                    notice_date=published_date,
                    user_id=user.user_id,
                    notice_read=False,
                    notice_organ_id=2,


                )
    # 모든 구독 기관에서 읽지 않은 공지사항 갯수 집계
    new_sum = Notice.objects.filter(
        Q(user_id=user.user_id) & Q(notice_read=False)
    ).count()

      # 응답 데이터 준비
    response_data = {
            "subscribe_organ": organ_notices,
            "new_sum": new_sum
        }

    return Response(response_data, status=status.HTTP_200_OK)

class AlarmOrgan(APIView):
  def get(self,request):
    user = request.user
    subscribe = Subscribe.objects.filter(user_id=user.user_id).first()
        
    if subscribe:
      serializer = SubscribeOrganSerializer(subscribe)
      return Response(serializer.data)
    else:
      return Response({"message": "No subscription found for this user."}, status=404)
  def patch(self,request):
    user = request.user
    try:
      subscribe_instance = Subscribe.objects.get(user_id=user.user_id)
    except Subscribe.DoesNotExist:
      return Response({"detail": "Subscribe record not found."}, status=status.HTTP_404_NOT_FOUND)

    # 요청 데이터에서 전달된 구독 정보를 가져옴
    subscribe_data = request.data

    # 기존 Subscribe 객체에서 변경할 필드만 업데이트
    for field in subscribe_data:
      if hasattr(subscribe_instance, field):
        setattr(subscribe_instance, field, subscribe_data[field])

    # 변경된 데이터를 저장
    subscribe_instance.save()

    # 수정된 구독 정보를 반환
    return Response({"detail": "Resource updated successfully"}, status=status.HTTP_200_OK)

class Mypage(APIView):
  def get(self,request):
    user = request.user
    profile = Profile.objects.get(user_id=user.user_id)
    serializer = MypageSerializer(profile)
    return Response(serializer.data)

class MyinfoEdit(APIView):
  def get(self, request):
    user = request.user
    profile = Profile.objects.get(user=user.user_id)
    serializer = MyInfoSerializer(profile)
    return Response(serializer.data)
  
class MyCourseEdit(APIView):
  def get(self, request):
    user = request.user
    profile=Profile.objects.get(user=user.user_id)
    serializers=CourseCompleteSerializer(profile)
    return Response(serializers.data)
  def delete(self, request):
    user = request.user
    complete_year = request.data.get("complete_year")
    school_year = request.data.get("school_year")
    subject_name = request.data.get("subject_name")
    #major 테이블에서 찾음
    subject_department = SubjectDepartment.objects.filter(subject_department_name=subject_name).first()
    if subject_department:
      major_subject = MajorSubjectCompleted.objects.filter(
        # user=request.user,
        user_id=user.user_id,
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
    subject_gened = SubjectGened.objects.filter(subject_gened_name=subject_name).first()
    if subject_gened:
      general_subject = GeneralSubjectCompleted.objects.filter(
                user_id=user.user_id,
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
    return Response({"detail": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)


  def patch(self, request):
    user = request.user
    complete_year = request.data.get("complete_year")
    school_year = request.data.get("school_year")
    subject_name = request.data.get("subject_name")
    grade = request.data.get("grade")
    retry_yn = request.data.get("retry_yn")

    #전공테이블 찾음
    subject_department = SubjectDepartment.objects.filter(subject_department_name=subject_name).first()
    if subject_department:
      major_subject = MajorSubjectCompleted.objects.filter(
      user_id=user.user_id,
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
    subject_gened = SubjectGened.objects.filter(subject_gened_name=subject_name).first()
    if subject_gened:
      general_subject = GeneralSubjectCompleted.objects.filter(
        user_id=user.user_id,
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
    