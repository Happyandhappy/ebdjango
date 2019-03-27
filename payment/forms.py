from django.forms import ModelForm, forms, fields
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS


class StripeCoreForm(forms.Form):

  def addError(self, message):
    self._errors[NON_FIELD_ERRORS] = self.error_class([message])


class CardForm(StripeCoreForm):

    last_4_digits = fields.CharField(
        required = True,
        min_length = 4,
        max_length = 4,
        widget = fields.HiddenInput()
    )

    stripe_token = fields.CharField(
        required = True,
        widget = fields.HiddenInput()
    )
    email = fields.EmailField(
        required = True,
        widget = fields.HiddenInput()
    )
    name = fields.CharField(
        required = True,
        widget = fields.HiddenInput()
    )
