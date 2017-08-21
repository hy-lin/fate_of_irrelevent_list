'''
Created by Hsuan-Yu Lin @ 09.08.2017
'''
import numpy

class Stimulus(object):
    def __init__(self, word_ind, present_position):
        self.word_ind = word_ind
        self.present_position = present_position

    def draw(self, display, getText):
        output_pos = display.getStimulusPos(self.present_position)
        output_text = getText(self.word_ind)
        
        display.drawText(output_text, output_pos[0], output_pos[1])

    def __str__(self):
        return '{}\t{}\t'.format(self.word_ind, self.present_position)

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

    def draw(self, display):
        display.drawText(self.question)

    def __str__(self):
        return '{}\t{}'.format(self.question, self.correctness)

    def __eq__(self, target):
        return str(self) == str(target)


class Trial(object):
    def __init__(self, relevent_stimuli, irrelevent_stimuli, CL_manipulation, relevent_cue, probe_type, probe, exp_setting):
        self.relevent_stimuli = relevent_stimuli
        self.irrelevent_stimuli = irrelevent_stimuli
        self.exp_setting = exp_setting

        self.cues = [Cue('green', 'top'), Cue('red', 'bottom')]
        self.CL_manipulation = CL_manipulation
        self.relevent_cue = relevent_cue
        self.probe_type = probe_type
        self.probe = probe
            
        self._getOSQuestions()

    def run(self, display, recorder, getText, logger):
        display.clear()

        for relevent_stimulus in self.relevent_stimuli:
            relevent_stimulus.draw(display, getText)

        for irrelevent_stimulus in self.irrelevent_stimuli:
            irrelevent_stimulus.draw(display, getText)

        for cue in self.cues:
            cue.draw(display)

        display.refresh()
        logger('Displaying stimuli')
        display.wait(self.exp_setting.stimulus_onset_duration)

        logger('Begin CSI')
        t0 = display.getTicks()
        ct = display.getTicks() - t0

        OS_index = 0
        while ct < self.exp_setting.CSI:
            display.clear()
            self.relevent_cue.draw(display)

            ct = display.getTicks() - t0
            if ct >= self.OS_schedule[OS_index] + self.exp_setting.max_os_response_time:
                logger('Participant failed to make a response for OS')
                self.OS_responses.append(False)
                OS_index += 1
                display.drawText('Zu langsam!')
                display.refresh()
                display.wait(200)

            elif ct >= self.OS_schedule[OS_index]:
                self.OSs[OS_index].draw(display)

                OS_response = recorder.getKeyboard(self.exp_setting.response_keys)
                if OS_response is not None:
                    logger('Participant made a response for OS')
                    correctness = int(OS_response == 'right') == self.OSs[OS_index].correctness
                    self.OS_responses.append(correctness)
                    OS_index += 1


            keys = recorder.getKeyboard(self.exp_setting.escape_key)
            if keys is not None:
                logger('Because Danielle demands it')
                raise KeyboardInterrupt('Because Danielle demands it')
  

            display.refresh()
            display.waitFPS()

        display.clear()
        self.relevent_cue.draw(display)
        self.probe.draw(display, getText)
        display.refresh()

        logger('Probe displayed')
        self.response, self.rt = recorder.recordKeyboard(self.exp_setting.response_keys)
        logger('Recognition response made')
        display.clear()
        display.refresh()
        display.wait(self.exp_setting.inter_trial_interval)
        logger('Exiting trial, gooodbye.')

    def _getOSQuestions(self):
        self.OS_schedule = numpy.linspace(0, self.exp_setting.CSI, self.CL_manipulation+1)
        self.OS_schedule[-1] = self.exp_setting.CSI + 8000

        self.OSs = []
        self.OS_responses = []
        for OS_index in range(self.CL_manipulation):
            self.OSs.append(OSQuestion())
            try:
                if self.OSs[OS_index] == self.OSs[OS_index-1]:
                    self.OSs[OS_index] = OSQuestion()
            except:
                pass

    def __str__(self):
        output_string = ''
        output_string += '{}\t{}\t{}\t'.format(self.exp_setting.CSI, self.CL_manipulation, self.probe_type)
        output_string += '{}\t'.format(self.relevent_cue)

        for relelvent_stimulus in self.relevent_stimuli:
            output_string += '{}\t'.format(relelvent_stimulus)

        for irrelelvent_stimulus in self.irrelevent_stimuli:
            output_string += '{}\t'.format(irrelelvent_stimulus)

        output_string += '{}\t'.format(self.probe)
        output_string += '{}\t{}\t{}'.format(
            self.response,
            self.rt,
            sum(self.OS_responses)
        )

        return output_string


