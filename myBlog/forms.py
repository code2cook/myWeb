from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django.forms import FileField, Form, ModelForm
# from .models import Product
from .models import UserProfile

    
class UserRegistrationForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    # confirm_password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(label=("Password"),widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),widget=forms.PasswordInput,
        help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ['username']
        
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        # if not any(char.isdigit() for char in password):
        #     raise forms.ValidationError("Password must contain at least one digit.")
        # if not any(char.isalpha() for char in password):
        #     raise forms.ValidationError("Password must contain at least one letter.")
        # if not re.search(r'[!@#$%^&*]', password):
        #     raise forms.ValidationError("Password must contain at least one special character (!@#$%^&*).")
        return password
    
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender']
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)