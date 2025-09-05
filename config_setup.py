import getpass
import json
import os

class Colors:
    RED       = '\033[91m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    BLUE      = '\033[94m'
    CLEAR     = '\033[39;49m'

def YesOrNoQuestionCheck(answer: str, default: bool) -> bool:
    answer.lower()

    if answer == 'y' or answer == 'yes':
        return True
    elif answer == 'n' or answer == 'no':
        return False
    elif answer == '':
        return default
    print(f'{Colors.RED}<Babel--> Invalid answer passed to final check in YesOrNoQuestionCheck()')
    raise ValueError

class ConfigSetup:
    def __init__(self):
        self.CONFIG_DIRECTORY: str = 'Automaton/'
        self.CONFIG_FILENAME: str = 'config'
        self.CONFIG_LOCATION: str = f'{self.CONFIG_DIRECTORY}{self.CONFIG_FILENAME}.json'
        self.DEFAULT_SETTINGS: dict = \
            {
                'example_setting_0': 'a',
                'example_setting_1': 'b',
                'example_setting_2': 'c',
                'example_setting_3': 'c',

                'auto_sync': False,
                'reconnect': False,
                'client_secret': ''
            }

        self.EXITING_MESSAGE: str = f'{Colors.RED}<Babel--> Exiting{Colors.CLEAR}'

        self.settings_to_write: dict = self.DEFAULT_SETTINGS

        if os.path.isfile(self.CONFIG_LOCATION):
            print(f'{Colors.YELLOW}<Babel--> Config File Already Exists')
            wipe_config_question: bool = YesOrNoQuestionCheck(str(input(f'{Colors.BLUE}<Babel--> Would you like to wipe the old config file and make a new one? (y/N): ')), False)
            if wipe_config_question:
                print(f'{Colors.GREEN}<Babel--> Deleting Old Config...')
                self.Delete_Old_Config()
                pass
            elif not wipe_config_question:
                print(f'{Colors.RED}<Babel--> Keeping Old Config...')
                print(self.EXITING_MESSAGE)
                return


        auto_sync_question: bool = YesOrNoQuestionCheck(str(input(f'{Colors.BLUE}<Babel--> Should the bot sync on launch? (y/N): ')), False)
        if auto_sync_question:
            self.settings_to_write['auto_sync'] = True
            print(f'{Colors.GREEN}<Babel--> Auto-sync: Enabled')
        elif not auto_sync_question:
            print(f'{Colors.RED}<Babel--> Auto-sync: Disabled')


        reconnect_question: bool = YesOrNoQuestionCheck(str(input(f'{Colors.BLUE}<Babel--> Should the bot attempt to reconnect if it loses connection? (Y/n): ')), True)
        if reconnect_question:
            self.settings_to_write['reconnect'] = True
            print(f'{Colors.GREEN}<Babel--> Reconnect: Enabled')
        elif not reconnect_question:
            print(f'{Colors.RED}<Babel--> Reconnect: Disabled')

        client_token_input_as_file_question: bool = YesOrNoQuestionCheck(str(input(f'{Colors.BLUE}<Babel--> Get Client Secret from ./client_token.secret? Alternative is inputting the token directly into your terminal (not recommended) (Y/n): ')), True)
        if client_token_input_as_file_question:
            if not os.path.isfile('client_token.secret'):
                print(f'{Colors.RED}<Babel--> client_token.secret not found')
                print(Colors.CLEAR)
                raise FileNotFoundError

            with open('client_token.secret') as opened_file:
                self.settings_to_write['client_secret'] = opened_file.read()
            print(f'{Colors.GREEN}<Babel--> Client Secret Set Via client_token.secret')
        elif not client_token_input_as_file_question:
            self.settings_to_write['client_secret'] = str(getpass.getpass(f'{Colors.RED}<Babel--> Please Input Your Client Secret: '))
            print(f'{Colors.RED}<Babel--> Client Secret Set Via Terminal')

        print(f'{Colors.BLUE}<Babel--> Please ensure the settings above are to your preference.')
        double_check_question: bool = YesOrNoQuestionCheck(str(input(f'{Colors.BLUE}<Babel--> Are you sure you want to write these settings to the config? (y/N): ')), False)
        if double_check_question:
            print(f'{Colors.GREEN}<Babel--> Writing Config...')
            self.Write_Config()
            print(f'{Colors.GREEN}<Babel--> Config Written to {self.CONFIG_LOCATION}, Enjoy Babel_Automaton!')
            print(self.EXITING_MESSAGE)
        else:
            print(f'{Colors.RED}<Babel--> Not Writing Config File')
            print(self.EXITING_MESSAGE)
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