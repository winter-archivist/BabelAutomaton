import datetime
import os

class Colors:
    RED       = '\033[31m'
    PURPLE    = '\033[35m'
    YELLOW    = '\033[33m'
    GREEN     = '\033[32m'
    BLUE      = '\033[34m'
    NORMAL    = '\033[0;0m'

class Logger:
    def __init__(self):

        self.LOGS_DIRECTORY: str = 'logs/'
        if os.path.isdir(self.LOGS_DIRECTORY):
            pass
        else:
            os.mkdir(self.LOGS_DIRECTORY)

        self.LOGFILE_LOCATION: str = f'{self.LOGS_DIRECTORY}/{datetime.datetime.now()}.log'
        with open(self.LOGFILE_LOCATION, "w") as opened_file:
            opened_file.write('LOGFILE, START')

    def log(self, log_level: str, source: str, log_message: str):

        match log_level:
            case 'critical' | 'crit' | 'crt' | 'c':
                log_level: str = 'critical'
                log_color: str = Colors.RED
                colorless_log_message: str = f'<{source}--> {log_message}'
                print(f'{log_color}{colorless_log_message}{Colors.NORMAL}')
                self.__log_to_logfile__(colorless_log_message, log_level)
                quit()

            case 'error' | 'err' | 'e':
                log_level: str = 'error'
                log_color: str = Colors.PURPLE

            case 'warn' | 'wrn' | 'w':
                log_level: str = 'warn'
                log_color: str = Colors.YELLOW

            case 'positive' | 'pos' | 'p':
                log_level: str = 'positive'
                log_color: str = Colors.GREEN

            case 'info' | 'inf' | 'i':
                log_level: str = 'info'
                log_color: str = Colors.BLUE

            case 'debug' | 'dbg' | 'd':
                log_level: str = 'debug'
                log_color: str = Colors.NORMAL

            case 'terminal' | 'term' | 'trm' | 't':
                log_level: str = 'terminal'
                log_color: str = Colors.NORMAL

            case _:
                self.log('warn', 'log', f'Invalid log_level passed to Logger.log, original log: ({log_level=} {source=} {log_message=})')
                return

        colorless_log_message: str = f'<{source}--> {log_message}'
        print(f'{log_color}{colorless_log_message}{Colors.NORMAL}')
        self.__log_to_logfile__(colorless_log_message, log_level)

    def __log_to_logfile__(self, colorless_log_message, log_level):
        with open(self.LOGFILE_LOCATION, "a") as opened_file:
            opened_file.write(f'\n{log_level} | {colorless_log_message}')
