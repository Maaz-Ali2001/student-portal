from django import forms

class TeacherForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone_no = forms.CharField(max_length=11)
    email= forms.EmailField(required=False)    
    Class = forms.CharField()
    section= forms.CharField()
    subject= forms.CharField()

    

class MyCustomForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    address = forms.CharField(max_length=100, label="Address", widget=forms.TextInput(attrs={'placeholder': '1234 Main St'}))
    address2 = forms.CharField(max_length=100, label="Address 2", widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'}))
    city = forms.CharField(max_length=100, label="City")
    state = forms.CharField(max_length=100, label="State")
    zip = forms.CharField(max_length=10, label="Zip")
    check_me_out = forms.BooleanField(required=False, label="Check me out")

