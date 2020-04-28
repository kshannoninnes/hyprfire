from django import forms
import os
from pathlib import Path

WINDOW_SIZES = [
    (1000, '1000'),
    (2000, '2000'),
]

ALGORITHMS = [
    ('Benford', 'Benford'),
    ('Zipf', 'Zipf'),
]


class AnalyseForm(forms.Form):
    project_root = os.path.dirname(os.path.abspath(__file__))
    pcaps_path = os.path.join(project_root, '..\\pcaps')

    path = Path(pcaps_path)

    filenames = forms.FilePathField(label='Files', path=path, recursive=False, allow_files=True)
    window = forms.CharField(label="Window Size ", widget=forms.Select(choices=WINDOW_SIZES))
    algorithm = forms.CharField(label="Algorithm ", widget=forms.Select(choices=ALGORITHMS))
    length = forms.CharField(label="Length ", widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': 'Enter numbers Only '}))
