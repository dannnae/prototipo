from django.contrib.auth.backends import ModelBackend


class MultiUserBackend(ModelBackend):
    def authenticate(self, request, username, password, **kwargs):
        UserModel = kwargs.get('UserModel')
        if username is None:
            username = kwargs.get('rut')
        
        if username is None or password is None:
            return
        
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            