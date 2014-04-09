from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field



from .models import Complaint


class ComplaintForm(forms.ModelForm):

  class Meta:
    model = Complaint
    fields = ["quiz", "subject", "message", "email"]


  def __init__(self, *args, **kwargs):
    super(ComplaintForm, self).__init__(*args, **kwargs)

    self.helper = FormHelper()

    self.helper.add_input(Submit('submit', "Submit"))
    self.helper.form_method =  "POST"
