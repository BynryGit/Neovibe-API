import uuid
from datetime import datetime
from django.utils import timezone  # importing package for datetime
from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

import fsm
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.department import get_department_by_id
from v1.commonapp.models.document import get_documents_by_user_id
from v1.commonapp.models.form_factor import get_form_factor_by_id
from v1.commonapp.models.notes import get_notes_by_userid
from v1.supplier.models.supplier import get_supplier_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.userapp.models.role import get_role_by_id
from v1.userapp.models.user_area import get_area_by_user_id
from v1.userapp.models.user_skill import get_skill_by_user_id
from v1.userapp.models.user_status import get_user_status_by_id
from v1.userapp.models.user_sub_type import get_user_sub_type_by_id
from v1.userapp.models.user_type import get_user_type_by_id
from v1.userapp.models.role_type import get_role_type_by_id
from v1.userapp.models.role_sub_type import get_role_sub_type_by_id
from v1.userapp.models.user_utility import get_utility_by_user


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MasterUser(AbstractBaseUser, PermissionsMixin):
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    username = None
    email = models.CharField(max_length=200, blank=False)
    USERNAME_FIELD = ('email')
    password = models.CharField(max_length=200, verbose_name='password')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    objects = MyUserManager()
    REQUIRED_FIELDS = []



# *********** USER CONSTANTS **************
USER_DICT = {
    "CREATED": 0,
    "ACTIVE": 1,
    "INACTIVE": 2,
    "ARCHIVED": 3,
}


# Create USER Master table start.
class User(MasterUser, PermissionsMixin, fsm.FiniteStateMachineMixin):
    CHOICES = (
        (0, 'CREATED'),
        (1, 'ACTIVE'),
        (2, 'INACTIVE'),
        (3, 'ARCHIVED'),
    )

    state_machine = {
        USER_DICT['CREATED']: (USER_DICT['ACTIVE'],),
        USER_DICT['ACTIVE']: (USER_DICT['INACTIVE'],),
        USER_DICT['INACTIVE']: (USER_DICT['ACTIVE'],),
        USER_DICT['INACTIVE']: (USER_DICT['ARCHIVED'],),
    }

    # username = None
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_id = models.CharField(max_length=200, blank=True, null=True)
    city_id = models.BigIntegerField(blank=True, null=True)
    user_type_id = models.BigIntegerField(null=True, blank=True)  # Tenant, Utility
    user_subtype_id = models.BigIntegerField(null=True, blank=True)  # employee, vendor, supplier
    form_factor_id = models.BigIntegerField(null=True, blank=True)  # Web, Mobile
    department_id = models.BigIntegerField(null=True, blank=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    state = models.BigIntegerField(choices=CHOICES, default=0)
    # password = models.CharField(max_length=200, verbose_name='password')
    first_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    # email = models.CharField(max_length=200, blank=False, unique=True)
    # USERNAME_FIELD = 'email'
    user_image = models.URLField(null=True, blank=True)
    phone_mobile = models.CharField(max_length=200, null=True, blank=True)
    phone_landline = models.CharField(max_length=200, null=True, blank=True)
    supplier_id = models.BigIntegerField(null=True, blank=True)
    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    # last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    # objects = MyUserManager()
    # REQUIRED_FIELDS = []

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

    @property
    def get_user_status(self):
        return get_user_status_by_id(self.status_id)

    @property
    def get_city(self):
        return get_city_by_id(self.city_id)

    @property
    def get_user_type(self):
        return get_user_type_by_id(self.user_type_id)

    @property
    def get_role_type(self):
        return get_role_type_by_id(self.user_type_id)

    @property
    def get_user_sub_type(self):
        return get_user_sub_type_by_id(self.user_subtype_id)

    @property
    def get_role_sub_type(self):
        return get_role_sub_type_by_id(self.user_subtype_id)

    @property
    def get_department(self):
        return get_department_by_id(self.department_id)

    @property
    def get_form_factor(self):
        return get_form_factor_by_id(self.form_factor_id)

    @property
    def get_user_role(self):
        return get_role_by_id(self.role_id)

    @property
    def get_user_bank(self):
        return get_bank_by_id(self.bank_detail_id)

    @property
    def get_user_utility(self):
        return get_utility_by_user(self.id)

    @property
    def get_user_area(self):
        return get_area_by_user_id(self.id)

    @property
    def get_user_skill(self):
        return get_skill_by_user_id(self.id)

    @property
    def get_supplier(self):
        return get_supplier_by_id(self.supplier_id)


def get_user_by_email(email):
    return User.objects.get(email=email, is_active=True)


def get_all_users():
    return User.objects.filter(is_active=True)


def is_email_exists(email):
    return User.objects.filter(email=email, is_active=True).exists()


def is_contact_exists(phone_mobile, tenant_id):
    return User.objects.filter(phone_mobile=phone_mobile, tenant_id=tenant_id, is_active=True).exists()


def get_user_by_id_string(id_string):
    try:
        return User.objects.get(id_string=id_string)
    except:
        return False


def get_user_by_id(id):
    try:
        return User.objects.get(id=id)
    except:
        return False




def get_user_by_username_password(email, password):
    return User.objects.get(email=email, password=password, is_active=True)


def get_users_by_tenant_id_string(id_string):
    return User.objects.filter(tenant__id_string=id_string, is_active=True)


def get_bank_by_user_id_string(id_string):
    user = User.objects.filter(id_string=id_string, is_active=True).last()
    return get_bank_by_id(user.bank_detail_id)


def get_documents_by_user_id_string(id_string):
    user = User.objects.filter(id_string=id_string, is_active=True).last()
    return get_documents_by_user_id(user.id)


def get_notes_by_user_id_string(id_string):
    user = User.objects.filter(id_string=id_string, is_active=True).last()
    return get_notes_by_userid(user.id)


def check_user_id_string_exists(id_string):
    return User.objects.filter(id_string=id_string, is_active=True).exists()
