from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, RequestStuNumber, College, Department

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user
    
class StuNumberSerializer(serializers.ModelSerializer):
    request_college = serializers.CharField(write_only=True)
    request_department = serializers.CharField(write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RequestStuNumber
        fields = ['request_number', 'request_college', 'request_department', 'user']

    def create(self, validated_data):
        college_name = validated_data.pop('request_college')
        department_name = validated_data.pop('request_department')
        try:
            college = College.objects.get(college_name=college_name)
        except College.DoesNotExist:
            raise serializers.ValidationError(f"College with name {college_name} not found.")
        try:
            department = Department.objects.get(department_name=department_name)
        except Department.DoesNotExist:
            raise serializers.ValidationError(f"Department with name {department_name} not found.")

        user = self.context['request'].user

        request_stu_number = RequestStuNumber.objects.create(
            request_number=validated_data['request_number'],
            college=college,
            department=department,
            user=user
        )

        return request_stu_number
