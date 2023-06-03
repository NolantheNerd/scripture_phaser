from scripture_phaser.enums import Bible
from scripture_phaser.agents import ESVAPIAgent
from scripture_phaser.exceptions import InvalidReference

class Passage:
    def __init__(self, reference, translation):
        self.translation = translation
        self.reference = reference
        #self.text = self.translation.agent.get()
