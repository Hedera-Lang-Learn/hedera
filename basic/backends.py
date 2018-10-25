from account.auth_backends import UsernameAuthenticationBackend as UAB


class UsernameAuthenticationBackend(UAB):

    def authenticate(self, request, **credentials):
        return super().authenticate(**credentials)
