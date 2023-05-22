class InvalidReference(Exception):
    def __init__(self, ref_string):
        Exception.__init__(self, f"{ref_string} is not a valid Bible reference")
