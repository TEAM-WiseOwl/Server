from django.utils import timezone
import requests
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from notices.models import Subscribe
from .models import User, Profile
from requirements.models import Department, College
from .serializers import StuNumberSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount, SocialLogin

class MypageUserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
		
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]    
    
    def get(self,request):
        user=User.objects.get(id=request.user.id)
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    def patch(self,request):
        user=User.objects.get(id=request.user.id)
        serializer=UserSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#[Info] 회원정보 조회 
class InfoUserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
		
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]    
    
    def get(self,request):
        user=User.objects.get(id=request.user.id)
        serializer=UserSerializer(user)
        return Response(serializer.data)


#BASE_URL = 'http://ec2-43-201-90-146.ap-northeast-2.compute.amazonaws.com:8000/'
#BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = 'https://wiseowlone.vercel.app/googleLogin'

def google_login(request):
    scope = "openid%20profile%20email"
    client_id = getattr(settings, "GOOGLE_CLIENT_ID")
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

def google_callback(request):
    state = 'random'
    client_id = getattr(settings, "GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "GOOGLE_SECRET")
    code = request.GET.get('code')
    redirect_uri = "https://wiseowlone.vercel.app/googleLogin"
    # 액세스 토큰 요청
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "state": state
        }
    )
    token_req_json = token_req.json()
    access_token = token_req_json.get('access_token')
    
    # 구글 API에서 이메일 정보 요청
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}"
    )
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    
    # 이메일로 유저 확인
    try:
        user = User.objects.get(email=email)
        social_login = SocialLogin(account=SocialAccount(user=user, provider='google', uid=email))

        merge_social_account(user, social_login)
        
        social_user = SocialAccount.objects.get(user=user)
        
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.last_login = timezone.now()  # 여기서 last_login을 갱신
        user.save()  
        
        # 이미 로그인된 유저인 경우 JWT 토큰 발급
        access_token, refresh_token = create_jwt_token(user)  # JWT 토큰 생성 함수
        user = request.user
        profile_created = False
        Profile.objects.create(
            user=user,
            profile_name="No Name",  # 직접 필드에 값을 전달
            profile_student_number=0
        )
        profile_created = created 
        print(f"[DEBUG] Profile created: {created}, Profile: {profile}")

        response = JsonResponse({
            'message': 'Login successful',
            'access_token':access_token,
            'refresh_token':refresh_token,
            'profile_created': profile_created
        })

        response["Authorization"] = f'Bearer {access_token}'
        response["Refresh-Token"] = refresh_token

        return response
    
    except User.DoesNotExist:
        # 신규 유저의 경우
        user = User.objects.create(email=email)
        social_user = SocialAccount.objects.create(user=user, provider='google', extra_data=email_req_json)
        user = request.user
        profile, created = Profile.objects.get_or_create(
            user=user,
            profile_name="No Name",  # 직접 필드에 값을 전달
            profile_student_number=0
        )
        print(created)
        access_token, refresh_token = create_jwt_token(user)  # JWT 토큰 생성 함수
        response = JsonResponse({'message': 'User created and logged in','profile_created': profile_created})
        response['Authorization'] = f'Bearer {access_token}'
        response['Refresh-Token'] = refresh_token
        return response
#리다이렉트 정해줘야함
def merge_social_account(user, social_login):
    try:
        existing_account = SocialAccount.objects.get(user=user, provider='google')
        if existing_account:
            # 기존 계정에 병합 처리
            existing_account.uid = social_login.account.uid
            existing_account.save()
    except SocialAccount.DoesNotExist:
        social_login.account.save()

def create_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return access_token, refresh_token

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client

class TokenRefreshAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({'message': 'No refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except TokenError as e:
            return Response({'message': f"Invalid token:{e}"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)
    
class AgreeMentAPIView(APIView):
    def post(self, request):
        user = request.user.user_id
        print(user)
        profile_agreement = request.data.get("profile_agreement", None)

        if profile_agreement is None:
            return Response({"message": "profile_agreement field is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found for the user."}, status=status.HTTP_404_NOT_FOUND)

        profile.profile_agreement = profile_agreement
        profile.save()

        return Response({"message": "Profile agreement updated successfully."}, status=status.HTTP_200_OK)

class ProfileCreateAPIView(APIView):
    def post(self, request):
        data = request.data
        user = request.user

        try:
            major_college = College.objects.get(college_id=data['major_college_id'])
            major = Department.objects.get(department_id=data['major_id'])
        except College.DoesNotExist:
            return Response({"error": "Major college not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Department.DoesNotExist:
            return Response({"error": "Major department not found."}, status=status.HTTP_400_BAD_REQUEST)

        double_or_minor_college = None
        double_or_minor = None
        profile_gubun = data['profile_gubun']

        if profile_gubun == "전공심화":
            double_or_minor_college = None
            double_or_minor = None

        elif profile_gubun in ["부전공", "이중전공", "전공심화+부전공"]:
            if 'double_or_minor_college_id' in data and 'double_or_minor_id' in data:
                try:
                    double_or_minor_college = College.objects.get(college_id=data['double_or_minor_college_id'])
                    double_or_minor = Department.objects.get(department_id=data['double_or_minor_id'])
                except College.DoesNotExist:
                    return Response({"error": "Double/Minor college not found."}, status=status.HTTP_400_BAD_REQUEST)
                except Department.DoesNotExist:
                    return Response({"error": "Double/Minor department not found."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": f"Double/Minor fields are required for {profile_gubun}."}, status=status.HTTP_400_BAD_REQUEST)

        # Profile 생성
        profile = Profile.objects.update_or_create(
            user=user,
            profile_name=data['profile_name'],
            profile_student_number=data['profile_student_number'],
            major_college=major_college,
            major=major,
            double_or_minor_college=double_or_minor_college,
            double_or_minor=double_or_minor,
            profile_gubun=profile_gubun,
        )

        # Subscribe 업데이트
        subscribe, created = Subscribe.objects.get_or_create(user=user)

        # 본전공 구독 추가
        subscribe.subscribe_major = True

        # 이중전공 또는 부전공 구독 추가
        if double_or_minor:
            subscribe.subscribe_double = True

        # 상태 저장
        subscribe.save()

        return Response({"message": "Profile and subscription created successfully."}, status=status.HTTP_201_CREATED)

class RequestStuNumAPIView(APIView):
    def post(self, request):
        serializer = StuNumberSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Request completed. After adding the relevant department's student number, we will notify you that it has been completed through a notification and email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
