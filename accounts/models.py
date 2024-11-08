from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
    major_college = models.ForeignKey(College, verbose_name='대학', on_delete= models.CASCADE, related_name='major_college_id')
    double_or_minor_college = models.ForeignKey(College, verbose_name='대학', on_delete= models.CASCADE, related_name='double_or_minor_college_id')
    major = models.ForeignKey(Department, verbose_name='학과', on_delete= models.CASCADE, related_name='major_id')
    double_or_minor = models.ForeignKey(Department, verbose_name='학과', on_delete= models.CASCADE, related_name='double_or_minor_id')
    profile_name = models.CharField(max_length=20, unique=True)
    profile_student_number = models.PositiveIntegerField(verbose_name='학번')
    profile_gubun = models.CharField(max_length=20)
    profile_agreement = models.BooleanField(default=False)
    profile_img = models.ImageField(upload_to="profiles/%Y/%m/%d/")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    profile_grade = models.FloatField(default=0)
    grad_research = models.BooleanField(default=False)
    grad_exam = models.BooleanField(default=False)
    grad_pro = models.BooleanField(default=False)
    grad_certificate = models.BooleanField(default=False)
    for_language = models.BooleanField(default=False)
    for_language_name = models.CharField(max_length=50, verbose_name='외국어 시험명', blank=True, null=True)
    for_language_score = models.PositiveBigIntegerField(verbose_name='외국어 시험점수', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email