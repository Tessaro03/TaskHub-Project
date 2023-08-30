from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Relationship
from django.contrib.auth.admin import UserAdmin

admin.site.register(UserProfile)
admin.site.register(Relationship)
