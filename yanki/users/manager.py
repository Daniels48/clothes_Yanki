from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
           Custom user model manager where email is the unique identifiers
           for authentication instead of usernames.
           """
    use_in_migration = True

    def _create_user(self, username=None, email=None, phone=None, password=None, **extra_fields):
        if not username:
            if not email and not phone:
                raise ValueError("The given email/phone must be set")

        if email:
            email = self.normalize_email(email)

            if not username:
                username = email

            user = self.model(email=email, username=username, **extra_fields)

        if phone:
            if not username:
                username = phone

            user = self.model(username=username, phone=phone, **extra_fields)

        user = self.model(username=username, **extra_fields)

        # yavlyaets9 polzovatel superuser
        if extra_fields.get("is_superuser"):
            user = self.model(username=username, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password, username=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username=username, password=password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
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
        return self.create_user(password, **extra_fields)


