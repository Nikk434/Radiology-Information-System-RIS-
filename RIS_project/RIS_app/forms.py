from django import forms
from .models import Document
import os 
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['uploaded_file']

    def save(self, commit=True):
        instance = super(DocumentForm, self).save(commit=False)
        # Get the uploaded file from the form
        uploaded_file = self.cleaned_data['uploaded_file']
        # Define the new file name
        # original_extension = os.path.splitext(uploaded_file.name)[1]
        new_file_name = "xray.png"
        # new_file_name = f"xray{original_extension}"
        # Save the file with the new name
        instance.uploaded_file.save(new_file_name, uploaded_file, save=False)
        if commit:
            instance.save()
        return instance