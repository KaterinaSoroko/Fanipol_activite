from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager, timezone, send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name="username",
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
    name_organization = models.CharField(verbose_name="name of the organization", max_length=150, blank=True)
    licenses = models.CharField(verbose_name="number_license", blank=True)
    info = models.TextField(verbose_name="info", max_length=150, blank=True)
    logo = models.ImageField(verbose_name="logo", blank=True)
    phone = models.CharField(verbose_name="phone", max_length=20, blank=True)
    viber = models.CharField(verbose_name="viber", max_length=120, blank=True)
    telegram = models.CharField(verbose_name="telegram", max_length=120, blank=True)
    instagram = models.CharField(verbose_name="instagram", max_length=120, blank=True)
    vk = models.CharField(verbose_name="vk", max_length=120, blank=True)
    ok = models.CharField(verbose_name="ok", max_length=120, blank=True)
    site = models.CharField(verbose_name="site", max_length=120, blank=True)
    address = models.CharField(verbose_name="address", max_length=150, blank=True)
    email = models.EmailField(verbose_name="email address", blank=True)

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
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        abstract = False

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        """Return the short name for the user."""
        return self.name_organization

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
