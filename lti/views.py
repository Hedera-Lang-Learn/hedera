from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.generic import RedirectView
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm


from account.models import EmailAddress

from .forms import LtiUsernameForm

import random
import string

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

class LtiInitializerView(RedirectView):
    
    pattern_name = 'home'
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        # canvas_course ----> group
        # canvase_user_roles ----> group role
        return super(LtiInitializerView, self).dispatch(request, *args, **kwargs)

    
class LtiRegistrationView(FormView):
    
    template_name = 'lti_registration.html'
    form_class = LtiUsernameForm
    success_url = 'lti_initializer'
    
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        
        username = form.cleaned_data['username']
        unique_username = form.unique_username(username)
        if unique_username is False:
            msg = "Sorry, that username is taken."
            form.add_error('username', msg)
            return super().form_invalid(form)
             
        """
        JOSH!!
        Below where there is still work to be done on this section.
        I wasn't able to successfully get the email in the method I used below.
        So there will need to be another way to seed the email.
        
        Also, I haven't tested whether get_random_alphanumeric_string produces a 
        valid password.
        
        If you can get the email, and a valid password, it should work.
        
        Sorry I wasn't able to write tests for all of this, I'm in a bit of a rush before
        I head out tonight.
        """
        email = self.request.POST.get('lis_person_contact_email_primary', False)  
        password = get_random_alphanumeric_string(10)
            
        new_user = User.objects.create_user(username, email=email, password=password)
        return super().form_valid(form)
        
        
        
        
        
        
