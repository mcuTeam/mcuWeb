# -*- coding: UTF-8 -*-
from system.models import *
from django.forms import ModelForm,ValidationError,TextInput
from django import forms

class terminalForm(ModelForm):
	class Meta:
		model = terminal
		fields = ['name','terminalIP',]
		widgets = {
		'name':TextInput(attrs={'class':'text-input small-input',}),
		'terminalIP':TextInput(attrs={'class':'text-input small-input',}),
		}