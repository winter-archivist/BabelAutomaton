import datetime
import os
import json

def valueSpacer(string: str, *args) -> str:
    if isinstance(args[0], int):
        longest_length = args[0]
    elif isinstance(args[0], tuple):
        longest_length: int = 0
        for arg in args[0]:
            current_length: int = len(arg)
            if current_length > longest_length:
                longest_length = current_length
        longest_length += 2


    string_flipper: bool = False
    while len(string) < longest_length:
        if string_flipper:
            string = f'{string} '
            string_flipper = False
        else:
            string = f' {string}'
            string_flipper = True

    return string


class Colors:
    normal = '\033[0;0m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    gray = '\033[90m'
    bright_red = '\033[91m'
    bright_green = '\033[92m'
    bright_yellow = '\033[93m'
    bright_blue = '\033[94m'
    magenta = '\033[95m'
    bright_cyan = '\033[96m'
    bright_white = '\033[97m'


class Logger:
    def __init__(self):
        config_file_path: str = 'Automaton/config.json'
        if not os.path.isfile(config_file_path):
            print('!!!---BabelAutomaton : NO CONFIG FOUND, PLEASE GENERATE ONE WITH configSetup.py, DEFAULTING TO INFO ---!!!')
            self.terminal_log_level = 'info'
        else:
            with open(config_file_path, 'r') as json_file:
                self.terminal_log_level = json.load(json_file)['terminal_log_level']

        self.LOGS_DIRECTORY: str = 'Automaton/logs/'
        if os.path.isdir(self.LOGS_DIRECTORY):
            pass
        else:
            os.mkdir(self.LOGS_DIRECTORY)

        self.LOGFILE_LOCATION: str = f'{self.LOGS_DIRECTORY}/{datetime.datetime.now()}.log'
        with open(self.LOGFILE_LOCATION, "w") as opened_file:
            opened_file.write('LOGFILE, START')

        #self.__printTest__()

    def __printTest__(self):
        print(f'{Colors.normal}TEST_message-here-normal{Colors.normal}')
        print(f'{Colors.red}TEST_message-here-red{Colors.normal}')
        print(f'{Colors.green}TEST_message-here-green{Colors.normal}')
        print(f'{Colors.yellow}TEST_message-here-yellow{Colors.normal}')
        print(f'{Colors.blue}TEST_message-here-blue{Colors.normal}')
        print(f'{Colors.purple}TEST_message-here-purple{Colors.normal}')
        print(f'{Colors.cyan}TEST_message-here-cyan{Colors.normal}')
        print(f'{Colors.white}TEST_message-here-white{Colors.normal}')
        print(f'{Colors.gray}TEST_message-here-gray{Colors.normal}')
        print(f'{Colors.bright_red}TEST_message-here-red{Colors.normal}')
        print(f'{Colors.bright_green}TEST_message-here-green{Colors.normal}')
        print(f'{Colors.bright_yellow}TEST_message-here-yellow{Colors.normal}')
        print(f'{Colors.bright_blue}TEST_message-here-blue{Colors.normal}')
        print(f'{Colors.magenta}TEST_message-here-magenta{Colors.normal}')
        print(f'{Colors.bright_cyan}TEST_message-here-cyan{Colors.normal}')
        print(f'{Colors.bright_white}TEST_message-here-white{Colors.normal}')
        self.log('error', 'Error', 'logger.levelPrintTest()')
        self.log('warn', 'Warn', 'logger.levelPrintTest()')
        self.log('success', 'Success', 'logger.levelPrintTest()')
        self.log('info', 'Info', 'logger.levelPrintTest()')
        self.log('question', 'Success', 'logger.levelPrintTest()')
        self.log('debug', 'Debug', 'logger.levelPrintTest()')
        self.log('critical', 'Critical', 'logger.levelPrintTest()', False)

    def log(self, log_level: str, log_message: str, log_depth: str, exit_on_critical: bool = True) -> None:
        log_levels: tuple = ('critical', 'error', 'warn', 'question', 'success', 'info', 'debug')
        if log_level not in log_levels:
            self.log('warn', 'Invalid log_level Given', 'logger.Logger.log()')
            return None

        match log_level:
            case 'critical':
                log_color: str = Colors.bright_red
                if exit_on_critical:
                    quit()

            case 'error':
                log_color: str = Colors.red

            case 'warn':
                log_color: str = Colors.yellow

            case 'success':
                log_color: str = Colors.green

            case 'question':
                log_color: str = Colors.purple

            case 'info':
                log_color: str = Colors.blue

            case 'debug':
                log_color: str = Colors.gray

        spaced_log_level: str = valueSpacer(log_level, log_levels)
        spaced_log_depth: str = valueSpacer(log_depth, 40)
        complete_log_message: str = f'{log_color}<{spaced_log_level}-{spaced_log_depth}--> {log_message}{Colors.normal}'
        with open(self.LOGFILE_LOCATION, "a") as opened_file:
            opened_file.write(complete_log_message)

        match self.terminal_log_level:
            case 'critical':
                if log_level != 'critical':
                    pass
                else:
                    return None

            case 'error':
                if log_level in ('critical', 'error'):
                    pass
                else:
                    return None

            case 'warn':
                if log_level in ('critical', 'error', 'warn'):
                    pass
                else:
                    return None

            case 'success':
                if log_level in ('critical', 'error', 'warn', 'success'):
                    pass
                return None

            case 'question':
                if log_level in ('critical', 'error', 'warn', 'success', 'question'):
                    pass
                else:
                    return None

            case 'info':
                if log_level in ('critical', 'error', 'warn', 'success', 'question', 'info'):
                    pass
                else:
                    return None

            case 'debug':
                if log_level in ('critical', 'error', 'warn', 'success', 'question', 'info', 'debug'):
                    pass
                else:
                    return None

            case _:
                self.log('critical', 'No terminal_log_level match found, quitting...', 'logger.Logger.log()')
                quit()

        print(f'{complete_log_message}')
        return None
