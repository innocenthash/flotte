from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator 
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# pour envoyer l'email
from django.core.mail import send_mail

from .manager import UserManager

# permissions 

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    post = models.CharField(_("post"), max_length=150, blank=True , null=True)
    email = models.EmailField(_("email address"), blank=True , unique=True , null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_members = models.BooleanField(
        _("members status"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as members. "
           
        ),
    )
    
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
#     a la place de username  name on utilisera email
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        # abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the  user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
        
    def get_admin_url(self):
        return reverse('admin:compte_user_change', args=[self.pk])
class CustomPermission(models.Model):
    class Meta:
        
        managed = True
        permissions = (
            ('view_user_info','can view user'),
            ('view_group', 'can view group')
        )

class ImageUser(models.Model):
    '''Model definition for ImageUser.'''
    user=models.OneToOneField("compte.User", on_delete=models.SET_NULL , null=True)
    profil=models.ImageField( upload_to='profil_user', height_field=None, width_field=None, max_length=None , null=True)
    class Meta:
        '''Meta definition for ImageUser.'''

        verbose_name = 'ImageUser'
        verbose_name_plural = 'ImageUsers'

    def __str__(self):
        return str(self.profil)