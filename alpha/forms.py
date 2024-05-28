# forms.py

from django import forms
from django.contrib.auth import authenticate
from .models import Department, Course, HashTag, CustomUser, Questions, Answers, Replies, PaymentSwitch

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'  # Include all fields

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course', 'department')  # Explicit field selection

class HashTagForm(forms.ModelForm):
    class Meta:
        model = HashTag
        fields = '__all__'  # Include all fields

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["phone_number", "status",'first_name', 'last_name','profile_pic'] # Customize user fields

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [ 'password', 'first_name', 'last_name', 'phone_number', 'department']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Perform custom validation for phone number format
        if not phone_number.startswith('+251') or len(phone_number) != 13:
            raise forms.ValidationError("Phone number should start with +251 followed by 9 digits.")
        return phone_number
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = (  'course', 'question', 'hashtags')
        widgets = {
            'question': forms.Textarea(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'hashtags': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'course': forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ('user', 'answer', 'verified')
        exclude = ['date'] 

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Replies
        fields = ('user', 'reply', 'date')
        exclude = ['date'] 
        
        
        
        
class PaymentSwitchForm(forms.ModelForm):
    class Meta:
        model = PaymentSwitch
        fields = ['is_on']
