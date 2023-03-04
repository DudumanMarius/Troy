from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

ADMIN = 0
USER = 1

USER_ROLES = (
    (ADMIN, "Admin"),
    (USER, "User")
)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


def avatars_directory_path(instance, filename):
    return f"avatars/avatar_{instance.pk}"


class User(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(
        verbose_name="Profile Image", upload_to=avatars_directory_path,
        default='avatars/default.png')
    email = models.EmailField(verbose_name="Email address", unique=True)
    first_name = models.CharField(verbose_name="First Name", max_length=256)
    last_name = models.CharField(verbose_name="Last Name", max_length=256)
    is_staff = models.BooleanField(verbose_name="Is staff", default=False)
    is_active = models.BooleanField(verbose_name="Is active", default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.IntegerField(choices=USER_ROLES, default=USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
