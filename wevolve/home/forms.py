import re

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django import forms

from wevolve.libs.utils import generate_hash, verify_user_route
from wevolve.users.models import Profile


class RegisterForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    first_name = forms.CharField(label=_("Firstname"))
    last_name = forms.CharField(label=_("Lastname"))
    username = forms.CharField(label=_("Username"))
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirm"), widget=forms.PasswordInput)
    accept_terms = forms.BooleanField(label=_("I accept"),
                                      help_text=_('You should accept '
                                      'the <a href="/terms">terms of use</a> '
                                      'and the <a href="/privacy">privacy policy</a> '
                                      'to join to wevolve'),
                                      error_messages={'required': _("You should accept the terms of use and the privacy policy")},
                                      required=True)

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not re.match("^\w+$", username):
            raise forms.ValidationError(_("Username isn't valid, use only letters, numbers or _"))

        if User.objects.filter(username=username).count():
            raise forms.ValidationError(_("Username exists"))

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")

        if not re.match("^(\w|\s)+\w$", first_name):
            raise forms.ValidationError(_("Firstname isn't valid, use only letters, numbers or _"))

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")

        if not re.match("^(\w|\s)+\w$", last_name):
            raise forms.ValidationError(_("Lastname isn't valid, use only letters, numbers or _"))

        return last_name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).count():
            raise forms.ValidationError(_("User exists with the same email"))

        return email

    def clean(self):
        cleaned_data = self.cleaned_data
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password2")

        if p1 != p2:
            raise forms.ValidationError(_("Password and password confirm didn't match"))

        return cleaned_data

    def save(self, request, group=None):
        data = self.cleaned_data
        u = User(username=data["username"], email=data["email"],
                 is_active=False,
                 first_name=data['first_name'],
                 last_name=data['last_name'])
        u.set_password(data["password"])
        u.save()
        token = generate_hash()
        Profile(user=u,
                token=token,
                country='None',
                city='None').save()
        token_url = verify_user_route(request, token)

        if group:
            group.user_set.add(u)

        self.verify_user(u, token_url)

        return u

    def verify_user(self, user, token_url):
        text_content = '''Hey there %(username)s,

We're ready to activate your account. All we need to do is make sure this is your email address.
Please click the link below to verify your account:
<a href="%(token_url)s">%(token_url)s</a>
(you can copy link to your browser if it doesn't work)

If you are having trouble verifying your email address,
just get in touch with us - support@wevolver.net''' % {'token_url': token_url,
                                                       'username': user.first_name
                                                       }
        email = EmailMultiAlternatives('Wevolve account activation',
                                       text_content,
                                       'info@wevolver.net',
                                       [user.email]
                                       )
        email.attach_alternative(text_content, "text/html")
        email.send()
