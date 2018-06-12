import imghdr

from django import forms

from vqapps.mediamanager.models import Media


class MediaForm(forms.ModelForm):

    file_ = forms.FileField()

    def clean(self):
        # http://django.readthedocs.io/en/latest/topics/forms/modelforms.html#s-overriding-clean-on-a-modelformset
        cleaned_data = super(MediaForm, self).clean()
        file_ = cleaned_data['file_']
        if imghdr.what(file_):
            cleaned_data['image'] = file_
            # update the instance value.
            self.instance.image = file_
        else:
            cleaned_data['attachment'] = file_
            # update the instance value.
            self.instance.attachment = file_
        return cleaned_data

    class Meta:
        model = Media
        exclude = ['attachment', 'image']