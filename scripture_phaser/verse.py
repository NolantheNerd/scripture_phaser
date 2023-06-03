class Verse:
    def __init__(self, reference, text):
        self.reference = reference
        self.text = text
        self.length = len(self.text)
        self.n_words = len(self.text.split())
