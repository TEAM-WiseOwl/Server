from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from config import settings
from requirements.models import College, Department

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            email= email,
            password= password
        )

        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.save(using=self._db)
        return superuser
    
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    major_college = models.ForeignKey(College, verbose_name='대학', on_delete=models.CASCADE, related_name='major_college')
    double_or_minor_college = models.ForeignKey(College, verbose_name='이중/부전공 대학', on_delete=models.CASCADE, related_name='double_minor_college', null=True, blank=True)
    major = models.ForeignKey(Department, verbose_name='학과', on_delete=models.CASCADE, related_name='major')
    double_or_minor = models.ForeignKey(Department, verbose_name='이중/부전공 학과', on_delete=models.CASCADE, related_name='double_minor', null=True, blank=True)
    profile_name = models.CharField(max_length=20, unique=True)
    profile_student_number = models.PositiveIntegerField(verbose_name='학번')
    profile_gubun = models.CharField(max_length=20, verbose_name="이중전공, 부전공, 전공심화, 전공심화+부전공")
    profile_agreement = models.BooleanField(default=False)
    profile_img = models.ImageField(upload_to="profiles/%Y/%m/%d/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    profile_grade = models.FloatField(default=0)
    grad_research = models.BooleanField(default=False)
    grad_exam = models.BooleanField(default=False)
    grad_pro = models.BooleanField(default=False)
    grad_certificate = models.BooleanField(default=False)
    for_language = models.BooleanField(default=False)
    for_language_name = models.CharField(max_length=50, verbose_name='외국어 시험명', blank=True, null=True)
    for_language_score = models.PositiveBigIntegerField(verbose_name='외국어 시험점수', blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - Profile"
    
class RequestStuNumber(models.Model):
    request_id = models.BigAutoField(primary_key=True)
    request_number = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_user_id')
    department = models.ForeignKey(Department, verbose_name= '학과 아이디', on_delete=models.CASCADE, related_name='request_department_id')