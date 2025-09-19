import os
import json

empty_dictionary: dict = \
    {
        'Name': '',
        'Creator':
            {
                'id': '',
                'user': ''
            },
        'Access_Type': '',
        'Access_Users': {},
        'Words': {}
    }

class Dictionary_Manager:
    def __init__(self, dictionary_name: str, dictionary_owner_id: int):
        self.name: str = dictionary_name
        self.owner_id: int = dictionary_owner_id

        self.directory: str = f'Automaton/dictionaries/{self.owner_id}/'
        self.file: str = f'{self.directory}{self.name}.json'

        # TODO: proper exceptions
        try:
            if not os.path.isfile(self.file):
                raise FileNotFoundError

        except FileNotFoundError as error_message:
            print(error_message)

        except Exception as error_message:
            print(error_message)

        with open(self.file, "r") as json_file:
            self.data: dict = json.load(json_file)

    async def __dictionary_exist_check__(self):
        # TODO: proper exceptions
        try:
            if not os.path.isfile(self.file):
                raise FileNotFoundError

        except FileNotFoundError as error_message:
            print(error_message)

        except Exception as error_message:
            print(error_message)

    async def __update_dictionary_data__(self) -> None:
        await self.__dictionary_exist_check__()

        # TODO: proper exceptions
        with open(self.file, "w") as operate_file:
            json.dump(self.data, operate_file)

        return None

    async def __user_access_check__(self, user_id_to_check: int, access_type_to_check_for: str) -> bool:
        if access_type_to_check_for not in ('read', 'write', 'share'):
            raise ValueError

        if user_id_to_check == self.owner_id:
            print('user is owner')
            return True

        for entry in self.data['User_Access']:
            print(entry)
            if entry == user_id_to_check:
                print('user id found')
                if entry[access_type_to_check_for]:
                    print('valid access')
                    return True
        print('invalid access')
        return False

    async def __is_dictionary_private__(self) -> bool:
        # TODO: proper logging
        if self.data['Access_Type'] == 'group':
            return False
        else:
            return True

    async def all_access_users(self) -> list:
        access_users: list = []
        for access_id in self.data['Access_Users']:
            access_users.append(self.data['Access_Users'][access_id]['user'])
        return access_users

    # ------ #
    # I don't know if these will be needed, but I might as well write them now
    async def all_read_access_users(self) -> list:
        read_access_users: list = []
        for access_id in self.data['Access_Users']:

            if read_access_users.append(self.data['Access_Users'][access_id]['read']):
                continue

            read_access_users.append(self.data['Access_Users'][access_id]['user'])
        return read_access_users

    async def all_write_access_users(self) -> list:
        write_access_users: list = []
        for access_id in self.data['Access_Users']:

            if write_access_users.append(self.data['Access_Users'][access_id]['write']):
                continue

            write_access_users.append(self.data['Access_Users'][access_id]['user'])
        return write_access_users

    async def all_share_access_users(self) -> list:
        share_access_users: list = []
        for access_id in self.data['Access_Users']:

            if share_access_users.append(self.data['Access_Users'][access_id]['share']):
                continue

            share_access_users.append(self.data['Access_Users'][access_id]['user'])
        return share_access_users
    # ------ #

    async def change_dictionary_access_type(self, new_access_type: str) -> None:
        # TODO: proper logging & exceptions

        if new_access_type != 'personal' and new_access_type != 'group':
            raise ValueError(f'Invalid Access Type ({new_access_type}) passed to change_dictionary_access_type()')

        previous_access_type: str = self.data['Access_Type']

        if self.data['Access_Type'] == 'personal':
            self.data['Access_Type'] = 'group'
        elif self.data['Access_Type'] == 'group':
            self.data['Access_Type'] = 'personal'
        else:
            self.data['Access_Type'] = previous_access_type
            raise Exception('Invalid Access Type read during change_dictionary_access_type()')

        await self.__update_dictionary_data__()
        return None

    async def give_user_access_to_dictionary(self, interactor_id: int, new_access_user_id: int, new_access_user_name: str) -> None:
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

        self.data['Access_Users'][new_access_user_id] = {'user': new_access_user_name, 'read': True, 'write': False, 'share': False}

        await self.__update_dictionary_data__()

    async def remove_user_access_to_dictionary(self, interactor_id: int, remove_access_user_id: int) -> None:
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
            print(f'Key {remove_access_user_id} was not found in {self.data['Access_Users']}')
            return

        del(self.data['Access_Users'][str(remove_access_user_id)])
        await self.__update_dictionary_data__()

    async def add_word_to_dictionary(self, interactor_id: int, word_to_add: str, word_definition: str = 'No definition set.') -> None:
        """
        :param interactor_id: User running the command
        :param word_to_add: Word to be added to the dictionary
        :param word_definition: Word definition
        :return: None
        """
        if not await self.__user_access_check__(interactor_id, 'share'):
            return

        self.data['Words'] = {word_to_add: word_definition}
        await self.__update_dictionary_data__()


def make_dictionary(name: str, creator_id: int, creator_user: str, access_type: str) -> None:
    """

    :param name: Name of the Dictionary
    :param creator_id: ID of the user making the dictionary
    :param creator_user: Username of the user making the dictionary
    :param access_type: Personal or Group
    :return: None
    """

    dictionary_to_write: dict = empty_dictionary
    dictionary_to_write['Name'] = name
    dictionary_to_write['Creator']['id'] = creator_id
    dictionary_to_write['Creator']['user'] = creator_user
    dictionary_to_write['Access_Type'] = access_type

    dictionary_directory: str = f'Automaton/dictionaries/{creator_id}/'
    dictionary_file: str = f'{dictionary_directory}{name}.json'

    if not os.path.isdir(dictionary_directory):
        os.mkdir(dictionary_directory)

    if not os.path.isfile(dictionary_file):
        with open(dictionary_file, "w") as operate_file:
            json.dump(dictionary_to_write, operate_file)
