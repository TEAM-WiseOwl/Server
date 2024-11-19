from rest_framework.views import APIView
from rest_framework.response import Response
from .models import College
from .serializers import CollegeSerializer

class CollegeListAPIView(APIView):
    def get(self, request):
        colleges = College.objects.prefetch_related('department_set')  # 관련 학과 데이터 미리 로드
        serializer = CollegeSerializer(colleges, many=True)
        return Response({"colleges": serializer.data}, status=200)
