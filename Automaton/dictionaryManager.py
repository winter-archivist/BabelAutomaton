import os
import json
import uuid
import random

from logger import Logger

empty_dictionary: dict = \
    {
        'uuid': '',
        'Name': '',
        'Owner':
            {
                'id': '',
                'user': ''
            },
        'Access_Type': '',
        'Access_Users':
            {
                '0':
                    {
                        'read': False,
                        'write': False,
                        'share': False,
                    }
            },
        'Words':
            {
                'Word': 'Definition'
            }
    }

    # invitation system


def make_dictionary(name: str, owner_id: int, owner_user: str, access_type: str) -> str:
    """
    :param name: Name of the Dictionary
    :param owner_id: ID of the user making the dictionary
    :param owner_user: Username of the user making the dictionary
    :param access_type: Personal or Group
    :return: None
    """

    base_dictionary_directory: str = 'Automaton/dictionaries/'
    if not os.path.isdir(base_dictionary_directory):
        os.mkdir(base_dictionary_directory)

    dictionary_uuid: str = str(uuid.uuid4())

    dictionary_to_write: dict = empty_dictionary
    dictionary_to_write['uuid'] = dictionary_uuid
    dictionary_to_write['Name'] = name
    dictionary_to_write['Owner']['id'] = owner_id
    dictionary_to_write['Owner']['user'] = owner_user
    dictionary_to_write['Access_Type'] = access_type

    dictionary_file: str = f'Automaton/dictionaries/{dictionary_uuid}.json'

    with open(dictionary_file, "w") as operate_file:
        json.dump(dictionary_to_write, operate_file)

    return dictionary_uuid


def set_target_uuid(user_id: int, dictionary_uuid: str) -> None:
    user_directory: str = f'Automaton/dictionaries/{user_id}'
    if not os.path.isdir(user_directory):
        os.mkdir(user_directory)

    target_dictionary_file: str = f'Automaton/dictionaries/{user_id}/target_dictionary.json'
    with open(target_dictionary_file, "w") as open_file:
        open_file.write(dictionary_uuid)

    return None


def get_target_uuid(user_id: int, logger: Logger) -> str:
    target_dictionary_file: str = f'Automaton/dictionaries/{user_id}/target_dictionary.json'
    if os.path.isfile(target_dictionary_file):
        with open(target_dictionary_file, "r") as open_file:
            data: str = open_file.read()
            logger.log('debug', f'Target UUID Found: {data}', 'main.configSetup.get_target_uuid()')
    else:
        logger.log('warn', '"target_dictionary_file" not found, please ensure the user has set a target dictionary already.',f'main.configSetup.get_target_uuid()')
        raise FileNotFoundError

    return data


class DictionaryManager:
    def __init__(self, interactor_id, logger: Logger):
        """
        :param interactor_id: User running the command
        :param logger: The user id of the user being added to the dictionary
        :return: None
        """

        self.logger = logger
        target_dictionary_uuid: str = get_target_uuid(interactor_id, self.logger)
        self.file: str = f'Automaton/dictionaries/{target_dictionary_uuid}.json'

        try:
            if not os.path.isfile(self.file):
                raise FileNotFoundError

        except FileNotFoundError as error_message:
            self.logger.log('error', str(error_message), f'dictionaryManager.DictionaryManager.__init__()')

        except Exception as error_message:
            self.logger.log('error', str(error_message), 'dictionaryManager.DictionaryManager.__init__()')

        with open(self.file, "r") as json_file:
            self.data: dict = json.load(json_file)

    async def __dictionary_exist_check__(self):
        try:
            if not os.path.isfile(self.file):
                raise FileNotFoundError

        except FileNotFoundError as error_message:
            self.logger.log('error', str(error_message), 'dictionaryManager.DictionaryManager.__dictionary_exist_check__()')

        except Exception as error_message:
            self.logger.log('error', str(error_message), 'dictionaryManager.DictionaryManager.__dictionary_exist_check__()')

    async def __update__(self) -> None:
        await self.__dictionary_exist_check__()

        with open(self.file, "w") as operate_file:
            json.dump(self.data, operate_file)

        return None

    async def __user_access_check__(self, user_id_to_check: int, access_type_to_check_for: str) -> bool:
        if access_type_to_check_for not in ('read', 'write', 'share'):
            raise ValueError

        if user_id_to_check == self.data['Owner']['id']:
            self.logger.log('success', f'User({user_id_to_check}) is Owner({self.data['Owner']['id']:}', 'dictionaryManager.DictionaryManager.__user_access_check__()')
            return True

        if str(user_id_to_check) in self.data['Access_Users'] and self.data['Access_Users'][str(user_id_to_check)][access_type_to_check_for]:
            self.logger.log('debug', f'User ID({user_id_to_check}) Has The Incorrect Access Type({access_type_to_check_for})', 'dictionaryManager.DictionaryManager.__user_access_check__()')
            return True
        self.logger.log('debug', f'User ID({user_id_to_check}) Has The Incorrect Access Type({access_type_to_check_for}) or was not found in Access_Users', f'dictionaryManager.DictionaryManager.__user_access_check__()')
        return False

    async def __is_dictionary_private__(self) -> bool:
        if self.data['Access_Type'] == 'group':
            self.logger.log('debug', f'Dictionary {self.data['uuid']} Access Type Checked, found to be Group', 'dictionaryManager.DictionaryManager.__is_dictionary_private__()')
            return False
        else:
            self.logger.log('debug',  f'Dictionary {self.data['uuid']} Access Type Checked, found to be Personal', 'dictionaryManager.DictionaryManager.__is_dictionary_private__()')
            return True

    async def all_access_users(self) -> list:
        access_users: list = []
        for access_id in self.data['Access_Users']:
            access_users.append(self.data['Access_Users'][access_id]['user'])
        return access_users

    async def set_access_type(self, access_type: str) -> None:

        if access_type != 'personal' and access_type != 'group':
            self.logger.log('warn', f'Invalid Access Type ({access_type}) Given', 'dictionaryManager.DictionaryManager.set_access_type()')
            raise ValueError
        else:
            self.logger.log('debug', f'Changing {self.data['uuid']}\'s access type to {access_type}', 'dictionaryManager.DictionaryManager.set_access_type()')

        self.data['Access_Type'] = access_type
        await self.__update__()
        return None

    async def add_user(self, interactor_id: int, new_access_user_id: int, new_access_user_name: str) -> None:
        """
        :param interactor_id: User running the command
        :param new_access_user_id: The user id of the user being added to the dictionary
        :param new_access_user_name: The username of the user being added to the dictionary
        :return: None
        """

        if await self.__is_dictionary_private__():
            raise NotImplementedError('Dictionary Private')

        if not await self.__user_access_check__(interactor_id, 'share'):
            raise NotImplementedError('User doesnt have share perms')

        # TODO: check if the user is already in Access_Users

        if str(new_access_user_id) in self.data['Access_Users'].keys():
            self.logger.log('warn', f'User {new_access_user_id} already found in {self.data['uuid']}\'s Access_Users', 'dictionaryManager.DictionaryManager.add_user()')
            raise Exception

        self.data['Access_Users'][new_access_user_id] = {'user': new_access_user_name, 'read': True, 'write': False, 'share': False}

        await self.__update__()

    async def remove_user(self, interactor_id: int, remove_access_user_id: int) -> None:
        """
        :param interactor_id: User running the command
        :param remove_access_user_id: The user id of the user being removed access to the dictionary
        :return: None
        """

        if await self.__is_dictionary_private__():
            return

        if not await self.__user_access_check__(interactor_id, 'share'):
            return

        try:
            if self.data['Access_Users'][str(remove_access_user_id)]:
                pass
        except KeyError:
            self.logger.log('debug', f'Key {remove_access_user_id} was not found in {self.data['Access_Users']}', 'dictionaryManager.DictionaryManager.remove_user()')
            return

        del(self.data['Access_Users'][str(remove_access_user_id)])
        await self.__update__()

    async def add_word(self, interactor_id: int, word_to_add: str, word_definition: str = 'No definition set.') -> None:
        """
        :param interactor_id: User running the command
        :param word_to_add: Word to be added to the dictionary
        :param word_definition: Word definition
        :return: None
        """
        if not await self.__user_access_check__(interactor_id, 'share'):
            return

        self.data['Words'][word_to_add] = word_definition
        await self.__update__()

    async def remove_word(self, interactor_id: int, word_to_remove: str) -> None:
        """
        :param interactor_id: User running the command
        :param word_to_remove: Word to be removed from the dictionary
        :return: None
        """
        if not await self.__user_access_check__(interactor_id, 'write'):
            return

        del self.data['Words'][word_to_remove]
        await self.__update__()

    async def random(self, interactor_id: int) -> str:
        """
        :param interactor_id: User running the command
        :return: The random word
        """
        if not await self.__user_access_check__(interactor_id, 'read'):
            self.logger.log('debug', 'Invalid Access to Dictionary.', 'dictionaryManager.DictionaryManager.random()')
            raise Exception

        return random.choice(list(self.data['Words'].keys()))
