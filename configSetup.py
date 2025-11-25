import json
import os

from Automaton.logger import Logger
logger = Logger()

def yesOrNoQuestion(answer: str, default: bool) -> bool:
    answer.lower()

    if answer in ('y', 'yes'):
        return True
    elif answer in ('n', 'no'):
        return False
    elif answer == '':
        return default

    logger.log('warn', 'Invalid Answer Given', 'configSetup', '.yesOrNoQuestion()')
    raise ValueError


class ConfigSetup:
    def __init__(self):
        self.CONFIG_LOCATION: str = f'Automaton/config.json'
        self.DEFAULT_SETTINGS: dict = \
            {
                'auto_sync'          : False,
                'reconnect'          : False,
                'terminal_log_level' : '',
                'prefix'             : 'a$'
            }

        self.settings_to_write: dict = self.DEFAULT_SETTINGS

        if os.path.isfile(self.CONFIG_LOCATION):
            logger.log('warn', 'Config File Already Exists', 'configSetup.init()')

            logger.log('question', 'Would you like to wipe the old config file and make a new one? (y/N): ', 'configSetup.init()')
            wipe_config_question: bool = yesOrNoQuestion(str(input()), False)
            if wipe_config_question:

                logger.log('question', 'Are you CERTAIN you want to delete the old config? (y/N): ', 'configSetup.init()')
                wipe_config_double_check: bool = yesOrNoQuestion(str(input()), False)
                if wipe_config_double_check:
                    logger.log('warn', 'Deleting Old Config...', 'configSetup.init()')
                    self.Delete_Old_Config()
                    logger.log('success', 'Old Config Deleted...', 'configSetup.init()')
                elif not wipe_config_double_check:
                    logger.log('info', 'Keeping Old Config...', 'configSetup.init()')
                    return

            elif not wipe_config_question:
                logger.log('info', 'Keeping Old Config...', 'configSetup.init()')
                return
        logger.log('question', 'Should the automaton sync on launch? (y/N): ', 'configSetup.init()')
        auto_sync_question: bool = yesOrNoQuestion(str(input()), False)
        if auto_sync_question:
            self.settings_to_write['auto_sync'] = True
            logger.log('warn', 'Auto-sync: Enabled...', 'configSetup.init()')
        elif not auto_sync_question:
            logger.log('info', 'Auto-sync: Disabled...', 'configSetup.init()')

        logger.log('question', 'Should the automaton attempt to reconnect if it loses connection? (Y/n): ', 'configSetup.init()')
        reconnect_question: bool = yesOrNoQuestion(str(input()), True)
        if reconnect_question:
            self.settings_to_write['reconnect'] = True
            logger.log('info', 'Reconnect: Enabled...', 'configSetup.init()')
        elif not reconnect_question:
            logger.log('warn', 'Reconnect: Disabled...', 'configSetup.init()')

        logger.log('question', 'Terminal Log Level? (critical/error/warn/success/INFO/debug): ', 'configSetup.init()')
        terminal_log_level_question: str = str(input())
        if terminal_log_level_question not in ('critical', 'error', 'warn', 'success', 'info', 'debug'):
            logger.log('warn', 'Defaulting to INFO terminal log level...', 'configSetup.init()')
            terminal_log_level_question = 'info'

        self.settings_to_write['terminal_log_level'] = terminal_log_level_question
        logger.log('info', f'Log Level: {terminal_log_level_question}...', 'configSetup.init()')

        logger.log('question', 'Please Input The Automaton\'s prefix: ): ', 'configSetup.init()')
        automaton_prefix_question = str(input())
        if automaton_prefix_question is None or automaton_prefix_question == '':
            automaton_prefix_question = self.settings_to_write['prefix']
        self.settings_to_write['prefix'] = automaton_prefix_question
        logger.log('info', f'Automaton Prefix: {self.settings_to_write['prefix']}', 'configSetup.init()')

        logger.log('warn', 'Please ensure the settings above are to your preference.', 'configSetup.init()')
        logger.log('question', 'Are you sure you want to write these settings to the config? (y/N): ', 'configSetup.init()')
        double_check_question: bool = yesOrNoQuestion(str(input()), False)
        if double_check_question:
            logger.log('warn', 'Writing Config...', 'configSetup.init()')
            self.Write_Config()
            logger.log('success', f'Config Written to {self.CONFIG_LOCATION}, Enjoy Babel_Automaton!', 'configSetup.init()')
        else:
            logger.log('info', 'Not Writing Config File...', 'configSetup.init()')
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
