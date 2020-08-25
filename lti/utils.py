from django.contrib.auth import get_user_model, login

from account.models import EmailAddress


def login_existing_user(request):
    """
    Takes the request from the authentaction middleware.
    It expects there to be lis_person_contact_email_primary in the POST.
    Returns the login function.
    """

    lti_user_email = request.POST.get("lis_person_contact_email_primary", None)
    if lti_user_email is None:
        return False
    account_email = EmailAddress.objects.get(email=lti_user_email)
    user = get_user_model().objects.get(username=account_email.user.username)
    login(request, user, backend="hedera.backends.UsernameAuthenticationBackend")
    return True
