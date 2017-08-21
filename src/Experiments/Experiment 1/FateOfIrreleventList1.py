import os
os.environ['PYSDL2_DLL_PATH'] = 'sdl_dll\\'
import sdl2.ext

import datetime
import random
import numpy

import Trial
import Display
import Recorder
import ExpSetting

class Experiment(object):
    def __init__(self):
        self.data_file = open('Data\\irrelevent_list.dat', 'a')
        self.data_log = open('Data\\log.dat', 'a')

        self.exp_setting = ExpSetting.ExpSetting()
        self.resource = sdl2.ext.Resources('.', 'resources')
        self.display = Display.Display(self.resource, self.exp_setting)
        self.recorder = Recorder.Recorder(self.exp_setting)
        self.exp_setting.updateDisplayScale(self.display)
        self.pID = 999
        self.session = 1

        self.recorder.hideCursor()

        self._getWordList()
        self._setupPracticeTrials()
        self._setupExpTrials()

        self.log('experiment created.')

        self.pID, self.session = self._getPIDNSession()

    def log(self, msg):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%d-%b-%Y %I-%M-%S')
        
        self.data_log.write('{}\t{}\t{}\t{}\n'.format(time_str, self.pID, self.session, msg))

    def _getWordList(self):
        list_file = open('resources\\WordList.txt', 'r')

        self.word_list = []
        self.word_index_list = []
        self.current_word_index = 0
        for word in list_file:
            self.word_list.append(word.replace('\n', ''))

        list_file.close()

    def getWord(self, word_index):
        return self.word_list[word_index]

    def _getPIDNSession(self):
        pID = self.display.getString(self.recorder, 'Participant ID: ', 20, 20)
        session = self.display.getString(self.recorder, 'Session: ', 20, 20)
        
        return pID, session

    def _setupPracticeTrials(self):
        self.display.clear()
        self.display.drawText('Please stand by, the first hamster is running as fast as it can.')
        self.display.refresh()

        self.p_trials = []
        cond_list = numpy.arange(self.exp_setting.n_practice)
        numpy.random.shuffle(cond_list)        
        for trial_index in range(self.exp_setting.n_practice):
            self.p_trials.append(self._getTrial(cond_list[trial_index]))

    def _setupExpTrials(self):
        self.display.clear()
        self.display.drawText('Please stand by, the second hamster is running as fast as it can.')
        self.display.refresh()

        self.trials = []
        cond_list = numpy.arange(self.exp_setting.n_trials)
        numpy.random.shuffle(cond_list)
        for trial_index in range(self.exp_setting.n_trials):
            self.trials.append(self._getTrial(cond_list[trial_index]))

    def _getTrial(self, trial_index):
        probe_type, cue_color, CL_manipulation = self._getConditions(trial_index)


        words = self._getWordIndex(7)
        relevent_stimulus = []
        for i in range(3):
            word_ind = words[i]
            if cue_color == 'green':
                relevent_stimulus.append(Trial.Stimulus(word_ind, i+1))
            else:
                relevent_stimulus.append(Trial.Stimulus(word_ind, i+4))

        irrelevent_stimulus = []
        for i in range(3):
            word_ind = words[i+3]
            if cue_color == 'green':
                irrelevent_stimulus.append(Trial.Stimulus(word_ind, i+4))
            else:
                irrelevent_stimulus.append(Trial.Stimulus(word_ind, i+1))

        if probe_type == 'positive':
            word_ind = words[numpy.random.randint(0, 3)]
        elif probe_type == 'intrusion':
            word_ind = words[numpy.random.randint(3, 6)]
        else:
            word_ind = words[6]

        probe = Trial.Stimulus(word_ind, 0)
        relevent_cue = Trial.Cue(cue_color, 'middle')

        return Trial.Trial(
            relevent_stimulus,
            irrelevent_stimulus,
            CL_manipulation,
            relevent_cue, 
            probe_type,
            probe,
            self.exp_setting
        )

    def _getConditions(self, trial_index):
        cond = trial_index % 24

        if cond // 6 == 0:
            probe_type = 'intrusion'
        elif cond // 6 == 1:
            probe_type = 'new'
        else:
            probe_type = 'positive'

        cond = cond % 6

        if cond // 3 == 0:
            cue_color = 'green'
        else:
            cue_color = 'red'

        cond = cond % 3

        if cond == 0:
            CL_manipulation = 2
        elif cond == 1:
            CL_manipulation = 3
        else:
            CL_manipulation = 4
        return probe_type, cue_color, CL_manipulation
        
    def _getWordIndex(self, n_words):
        if len(self.word_index_list) - self.current_word_index <= n_words:
            self.word_index_list = numpy.arange(len(self.word_list))
            numpy.random.shuffle(self.word_index_list)
            self.current_word_index = 0

        word_index = []
        for i in range(n_words):
            word_index.append(self.word_index_list[self.current_word_index])
            self.current_word_index += 1

        return word_index

    def run(self):
        self.showPracticeMessage()
        self.log('beginning practice:')
        for trial in self.p_trials:
            trial.run(self.display, self.recorder, self.getWord, self.log)
            self.log(trial)

        self.showExperimentMessage()
        self.log('beginning trials:')
        for t_ind, trial in enumerate(self.trials):
            trial.run(self.display, self.recorder, self.getWord, self.log)
            self.log(trial)
            self.save2file(trial)

            if t_ind % int(self.exp_setting.n_trials / 10) == 0 and t_ind != 0:
                self.doBreak(t_ind / int(self.exp_setting.n_trials / 10))

        self._endofExperiment()

    def showPracticeMessage(self):
        self.display.clear(True)
        self.display.drawText('Mit Leertaste weiter zu den Ubungsaufgaben')
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        self.display.clear(refresh = True)
        self.display.wait(500)

    def showExperimentMessage(self):
        self.display.drawText('Mit Leertaste weiter zu den Testaufgaben')
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        self.display.clear(refresh = True)
        self.display.wait(500)
        
    def doBreak(self, n_block):
        self.log('taking a break')

        self.display.drawText('Das war Block {} von 10.'.format(n_block))

        self.display.drawText('Gelegenheit fur kurze Pause. Weiter mit Leertaste.',
        y = self.display.window_surface.h/2 + 100)
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        self.display.clear(refresh = True)
        self.display.wait(500)

    def _endofExperiment(self):
        self.log('experiment finished, closing files.')
        self.data_file.close()
        
        self.display.clear()
        self.display.drawText(u'Ende des Experiments: Bitte Versuchsleiter rufen')
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        
        self.log('exiting program.')
        self.data_log.close()

    def save2file(self, trial):
        self.data_file.write(
            '{}\t{}\t{}\n'.format(
                self.pID,
                self.session,
                trial
            )
        )

if __name__ == '__main__':
    exp = Experiment()
    exp.run()