from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
import time



FOUNDATION = 1
NONGOVERORG = 2
LOCAL = 3

TYPE = [
    (FOUNDATION, 'fundacja'),
    (NONGOVERORG, 'organizacja pozarządowa'),
    (LOCAL, 'zbiórka lokalna'),
]


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Institution(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    type = models.IntegerField(default=FOUNDATION, choices=TYPE)
    category = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)


def add_category():
    c = Category(name="test")
    c.save()


def add_institution():
    i = Institution(name="Kosciol Polski", description="test instition",
                    type=1)
    i.save()
    i.category.add(1)


def add_donation():
    u = User.objects.get(pk=1)
    i = Institution.objects.get(pk=1)
    d = Donation(quantity=3, institution=i, address="Narutowicza", phone_number="509-214-447", city="Szczecinek",
                 zip_code="78-400", pick_up_date=datetime.datetime.now(), pick_up_time=datetime.time(),
                 pick_up_comment="test test", user=u)
    d.save()

