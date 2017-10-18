from django import forms
from django.utils.translation import ugettext_lazy as _
from userena.forms import AuthenticationForm

username_style = {'class': 'required','style':"width:900px"}

password_style = {'class': 'required','style':"width:900px"}

class SigninFormExtra(AuthenticationForm):
	identification = forms.CharField(label="userName by WuNL",
                           widget=forms.TextInput(attrs=username_style),
                           max_length=75,
                           error_messages={'required': "Either supply us with your email or username."})
	password = forms.CharField(label=_("Password"),widget=forms.PasswordInput(attrs=password_style, render_value=False))
	remember_me = forms.BooleanField(widget=forms.CheckboxInput(),required=False,label=_('Remember me for %(days)s') % {'days': 30} )
