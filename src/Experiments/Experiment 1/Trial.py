'''
Created by Hsuan-Yu Lin @ 09.08.2017
'''

def getText(word_ind):
    pass

class Stimulus(object):
    def __init__(self, word_ind, present_position, cue_color):
        self.word_ind = word_ind
        self.present_position = present_position
        self.cue_color = cue_color

    def draw(self, display):
        output_pos = display.getStimulusPos(self.present_position)
        output_text = getText(self.word_ind)
        
        display.drawText(output_text, output_pos)