'''
Created by Hsuan-Yu Lin @ 09.08.2017
'''
import numpy

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

    def __str__(self):
        return '{}\t{}\t{}'.format(self.word_ind, self.present_position, self.cue_color)

class Cue(object):
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def draw(self, display):
        cue_pos = display.getCuePos(self.position)

        if self.color == 'green':
            color = (0, 255, 0)
        elif self.color == 'red':
            color = (255, 0, 0)

        display.drawThickFrame(
            cue_pos[0],
            cue_pos[1],
            cue_pos[2],
            cue_pos[3],
            4,
            color
        )

    def __str__(self):
        return '{}\t{}'.format(
            self.color,
            self.position
        )

class OSQuestion(object):
    def __init__(self):
        self.question = ''
        self.correctness = 1 # 1 as correct, 0 as incorrect

        self._generateQuestion()

    def _generateQuestion(self):
        illegal = True

        while illegal:
            first_number = numpy.random.randint(1, 10)
            second_number = numpy.random.randint(1, 10)
            operation = numpy.random.choice(['+', '-'])

            if operation == '+':
                correct_answer = first_number + second_number
            elif operation == '-':
                correct_answer = first_number - second_number

            correctness = numpy.random.randint(0, 2)
            if correctness == 1:
                answer = correct_answer
            else:
                answer = correct_answer + numpy.random.choice([-1, +1])

            illegal = not(self._checkLegalness(answer) and self._checkLegalness(correct_answer))

        self.question = '{} {} {} = {}'.format(first_number, operation, second_number, answer)
        self.correctness = correctness

    def _checkLegalness(self, answer):
        if answer <= 0:
            return False

        return True

    def __str__(self):
        return '{}\t{}'.format(self.question, self.correctness)


class Trial(object):
    def __init__(self, stimuli, CSI, CL_manipulation, relevent_cue, probe, exp_setting):
        self.stimuli = stimuli
        self.exp_setting = exp_setting

        self.cues = [Cue('green', 'top'), Cue('red', 'botton')]
        self.CSI = CSI
        self.CL_manipulation = CL_manipulation
        self.relevent_cue = relevent_cue
        self.probe = probe

        self._getOSQuestions()

    def run(self, display, recorder):
        display.clear()

        for stimulus in self.stimuli:
            stimulus.draw(display)

        for cue in self.cues:
            cue.draw(display)

        display.wait(self.exp_setting.stimulus_onset_duration)

        display.clear()

    def _getOSQuestions(self):
        OS = []
        for OS_index in range(self.CL_manipulation):
            pass