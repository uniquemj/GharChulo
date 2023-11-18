from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password = None):
        if not email:
            ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email = email,)
        user.set_password(password)
        user.save(using = self.db)

        return user

    def create_superuser(self,email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self.db)
        return user