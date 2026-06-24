from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        # Password restrictions
        self.fields['password1'].widget.attrs.update({
            'maxlength': 20,
            'minlength': 8
        })

        self.fields['password2'].widget.attrs.update({
            'maxlength': 20,
            'minlength': 8
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']
        if commit:
            user.save()
        return user
    
    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if not password:
            return password

        if len(password) > 20:
            raise forms.ValidationError(
                "Password cannot be more than 20 characters."
            )

        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters."
            )

        return password