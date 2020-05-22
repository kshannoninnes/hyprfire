from django import forms
import os
from pathlib import Path
from hyprfire.settings import BASE_DIR

WINDOW_SIZES = [
    (1000, '1000'),
    (2000, '2000'),
]

ALGORITHMS = [
    ('Benford', 'Benford'),
    ('Zipf', 'Zipf'),
]

ANALYSIS = [
    ('Length', 'Length'),
    ('Time', 'Time'),
]


class AnalyseForm(forms.Form):

    path = str(Path(BASE_DIR) / 'pcaps') 
    filenames = forms.FilePathField(label='Files', path=path, recursive=False, allow_files=True)
    window = forms.CharField(label="Window Size ", widget=forms.Select(choices=WINDOW_SIZES))
    algorithm = forms.CharField(label="Algorithm ", widget=forms.Select(choices=ALGORITHMS))
    analysis = forms.CharField(label="Analysis ", widget=forms.Select(choices=ANALYSIS))
