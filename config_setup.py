import json
import os

from Automaton.logger import Logger
LOGGER = Logger()
source: str = 'BabelConfigSetup'

def YesOrNoQuestionCheck(answer: str, default: bool) -> bool:
    answer.lower()

    if answer in ('y', 'yes'):
        return True
    elif answer in ('n', 'no'):
        return False
    elif answer == '':
        return default

    LOGGER.log('error', 'config_setup.YesOrNoQuestionCheck', 'Invalid answer passed to final check')
    raise ValueError


class ConfigSetup:
    def __init__(self):
        self.CONFIG_LOCATION: str = f'Automaton/config.json'
        self.DEFAULT_SETTINGS: dict = \
            {
                'auto_sync'       : False,
                'reconnect'       : False,
                'prefix'          : ''
            }

        self.settings_to_write: dict = self.DEFAULT_SETTINGS

        if os.path.isfile(self.CONFIG_LOCATION):
            LOGGER.log('warn', source, 'Config File Already Exists')
            wipe_config_question: bool = YesOrNoQuestionCheck(str(input(f'<BabelConfigSetup--> Would you like to wipe the old config file and make a new one? (y/N): ')), False)
            if wipe_config_question:

                wipe_config_double_check: bool = YesOrNoQuestionCheck(str(input(f'<BabelConfigSetup--> Are you CERTAIN you want to delete the old config? (y/N): ')),False)
                if wipe_config_double_check:
                    LOGGER.log('info', source, 'Deleting Old Config...')
                    self.Delete_Old_Config()
                    LOGGER.log('success', source, 'Old Config Deleted...')
                elif not wipe_config_double_check:
                    LOGGER.log('info', source, 'Keeping Old Config...')
                    return

            elif not wipe_config_question:
                LOGGER.log('info', source, 'Keeping Old Config...')
                return


        auto_sync_question: bool = YesOrNoQuestionCheck(str(input(f'<BabelConfigSetup--> Should the automaton sync on launch? (y/N): ')), False)
        if auto_sync_question:
            self.settings_to_write['auto_sync'] = True
            LOGGER.log('info', source, 'Auto-sync: Enabled...')
        elif not auto_sync_question:
            LOGGER.log('info', source, 'Auto-sync: Disabled...')


        reconnect_question: bool = YesOrNoQuestionCheck(str(input(f'<BabelConfigSetup--> Should the automaton attempt to reconnect if it loses connection? (Y/n): ')), True)
        if reconnect_question:
            self.settings_to_write['reconnect'] = True
            LOGGER.log('info', source, 'Reconnect: Enabled...')
        elif not reconnect_question:
            LOGGER.log('info', source, 'Reconnect: Disabled...')

        self.settings_to_write['prefix'] = str(input(f'<BabelConfigSetup--> Please Input The Automaton\'s prefix: '))

        LOGGER.log('info', source, 'Please ensure the settings above are to your preference.')
        double_check_question: bool = YesOrNoQuestionCheck(str(input(f'<BabelConfigSetup--> Are you sure you want to write these settings to the config? (y/N): ')), False)
        if double_check_question:
            LOGGER.log('info', source, 'Writing Config...')
            self.Write_Config()
            LOGGER.log('success', source, f'Config Written to {self.CONFIG_LOCATION}, Enjoy Babel_Automaton!')
        else:
            LOGGER.log('info', source, 'Not Writing Config File')
            return

    def Write_Config(self) -> None:
        with open(self.CONFIG_LOCATION, "w") as opened_file:
            json.dump(self.settings_to_write, opened_file)
        return None

    def Delete_Old_Config(self) -> None:
        if os.path.isfile(self.CONFIG_LOCATION):
            os.remove(self.CONFIG_LOCATION)
        return None

if __name__ == '__main__':
    ConfigSetup: ConfigSetup = ConfigSetup()
