import os
import json

from logger import Logger

def readFile(logger: Logger, file_path: str, file_type: str, hide_data: bool = True):
    if not os.path.isfile(file_path):
        logger.log('warn', f'File Not Found.... [{file_path}]', 'utils.readFile()')
        raise FileNotFoundError

    supported_file_types: tuple = ('json', 'text')
    if file_type not in supported_file_types:
        logger.log('warn', f'File Not Found.... [{file_type}]', 'utils.readFile()')
        raise Exception

    logger.log('debug', f'Reading {file_type} File... {file_path}', 'utils.readFile()')
    match file_type:
        case 'json':
            with open(file_path, 'r') as json_file:
                file_data = json.load(json_file)
        case 'text':
            with open(file_path, 'r') as text_file:
                file_data = text_file.read()

    if not hide_data:
        logger.log('debug', f'{file_type} Data... {file_data}', 'utils.readFile()')
    else:
        logger.log('debug', f'{file_type} Data Hidden...', 'utils.readFile()')
    return file_data
