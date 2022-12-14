import datetime

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField

from .models import JobVacancy, Comment, EmployeeType, Location, ExperienceLevel, Employer


class CreateJobForm(forms.Form):
    # employer = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'hidden': True}))
    position = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    company_logo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=CKEditorUploadingWidget())
    apply_url = forms.URLField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter the url to the application site...'}))
    location = forms.ModelChoiceField(queryset=Location.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    employee_type = forms.ModelChoiceField(queryset=EmployeeType.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    experience_level = forms.ModelChoiceField(queryset=ExperienceLevel.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={
        'format': 'yyyy-MM-dd',
        'class': 'form-control',
        'placeholder': 'yyyy-MM-dd'
    }))

    # def clean_expiry_date(self):
    #     data = self.cleaned_data['expiry_date']
    #     if data < datetime.date.today():
    #         raise ValidationError(_('Invalid date - expiry date in past'))
    #     return data

    class Meta:
        model = JobVacancy

    def save(self):
        pass


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('job_vacancy', 'is_hidden',)

        widgets = {
            'comment_author': forms.TextInput(attrs={"class": "form-control"}),
            'comment_message': forms.Textarea(attrs={"class": "form-control"})
        }


class EmployerForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control", "autocomplete": "new-password"}), label="Password:")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'new-password'}), label="Password Confirmation:")

    class Meta:
        model = Employer
        fields = ['username', 'email', 'password1', 'password2', 'job_position', 'company']

        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control", 'type': 'text'}),
            'email': forms.EmailInput(attrs={"class": "form-control", 'type': 'email'}),
            'password1': forms.PasswordInput(attrs={"class": "form-control", 'type': 'password'}),
            'password2': forms.PasswordInput(attrs={"class": "form-control", 'type': 'password'}),
            'job_position': forms.TextInput(attrs={"class": "form-control", 'type': 'text'}),
            'company': forms.TextInput(attrs={"class": "form-control", 'type': 'text'}),
        }


class ApplicantForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control", "autocomplete": "new-password"}), label="Password:")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'new-password'}), label="Password Confirmation:")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control", 'type': 'text'}),
            'email': forms.EmailInput(attrs={"class": "form-control", 'type': 'email'}),
            'password1': forms.PasswordInput(attrs={"class": "form-control", 'type': 'password'}),
            'password2': forms.PasswordInput(attrs={"class": "form-control", 'type': 'password'})
        }