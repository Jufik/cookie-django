import imghdr

from django import forms

from vqapps.mediamanager.models import Media


class MediaForm(forms.ModelForm):

    file_ = forms.FileField(required=True)

    def clean_file_(self):
        # http://django.readthedocs.io/en/latest/topics/forms/modelforms.html#s-overriding-clean-on-a-modelformset
        file_ = self.cleaned_data.get('file_')
        if imghdr.what(file_):
            self.cleaned_data['image'] = file_
            # update the instance value.
            self.instance.image = file_
        else:
            self.cleaned_data['attachment'] = file_
            # update the instance value.
            self.instance.attachment = file_
        return file_

    class Meta:
        model = Media
        exclude = ['attachment', 'image']