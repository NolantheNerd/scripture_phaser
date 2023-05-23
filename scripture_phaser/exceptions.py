class InvalidReference(Exception):
    def __init__(self, ref_string):
        Exception.__init__(self, f"{ref_string} is not a valid Bible reference")

class InvalidReferenceFormat(Exception):
    def __init__(self, ref_string):
        Exception.__init__(self, "Invalid reference format; make sure there is a space between the book name and chapter number")
