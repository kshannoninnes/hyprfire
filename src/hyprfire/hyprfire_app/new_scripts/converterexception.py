# converterexception.py: used for exceptions occurring in the converters
# Author: Dean Quaife
# Last edited: 2020/04/30

class ConverterException(Exception):
    def __init__(self, message="Something went wrong"):
        self.message = message

    def __str__(self):
        return f'{self.message}'