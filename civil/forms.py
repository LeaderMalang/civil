from django import forms
# from civil.models import AddHazard
from civil.models import AddNewHazard
from civil.models import AddDesignElement
from civil.models import AddActivity
from civil.models import AddSignup
from civil.models import AddProject


# class AddHazardForm(forms.ModelForm):
#     class Meta:
#         model = AddHazard
#         fields = "__all__"
        
class AddNewHazardForm(forms.ModelForm):
    class Meta:
        model = AddNewHazard
        fields = "__all__"
        
class AddDesignElementForm(forms.ModelForm):
    class Meta:
        model = AddDesignElement
        fields = "__all__"

class AddActivityForm(forms.ModelForm):
    class Meta:
        model = AddActivity
        fields = "__all__"
        
        
class AddSignupForm(forms.ModelForm):
    class Meta:
        model = AddSignup
        fields = "__all__"

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = AddProject
        fields = "__all__"
        
        
