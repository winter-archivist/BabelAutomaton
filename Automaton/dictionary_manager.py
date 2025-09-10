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


def get_dictionary_data(dictionary_name: str, dictionary_owner_id: int) -> dict:
    dictionary_directory: str = f'Automaton/dictionaries/{dictionary_owner_id}/'
    dictionary_file: str = f'{dictionary_directory}{dictionary_name}.json'

    if not os.path.isfile(dictionary_file):
        raise FileNotFoundError

    with open(dictionary_file, "r") as json_file:
        dictionary_data: dict = json.load(json_file)

    return dictionary_data


def update_dictionary_data(dictionary_name: str, dictionary_owner_id: int, new_dictionary_data: dict) -> None:
    dictionary_directory: str = f'Automaton/dictionaries/{dictionary_owner_id}/'
    dictionary_file: str = f'{dictionary_directory}{dictionary_name}.json'

    if not os.path.isfile(dictionary_file):
        raise FileNotFoundError

    with open(dictionary_file, "w") as operate_file:
        json.dump(new_dictionary_data, operate_file)

    return None


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


def is_dictionary_private(dictionary_data: dict) -> bool:
    if dictionary_data['Access_Type'] == 'group':
        return False
    else:
        return True
    raise Exception('Invalid Access Type read during is_dictionary_private()')


def change_dictionary_access_type(dictionary_name: str, dictionary_owner_id: int, new_access_type: str) -> None:

    if new_access_type != 'personal' and new_access_type != 'group':
        raise ValueError(f'Invalid Access Type ({new_access_type}) passed to change_dictionary_access_type()')

    dictionary_data: dict = get_dictionary_data(dictionary_name, dictionary_owner_id)

    if dictionary_data['Access_Type'] == 'personal':
        dictionary_data['Access_Type'] = 'group'
    elif dictionary_data['Access_Type'] == 'group':
        dictionary_data['Access_Type'] = 'personal'
    else:
        raise Exception('Invalid Access Type read during change_dictionary_access_type()')

    update_dictionary_data(dictionary_name, dictionary_owner_id, dictionary_data)
    return None


def give_user_access_to_dictionary(dictionary_name: str, dictionary_owner_id: int, new_access_user_id: int) -> None:
    """

    :param dictionary_name: Name of the dictionary
    :param dictionary_owner_id: Owner of the dictionary
    :param new_access_user_id: The user id of the user being added to the dictionary
    :return: None
    """

    dictionary_directory: str = f'Automaton/dictionaries/{dictionary_owner_id}/'
    dictionary_file: str = f'{dictionary_directory}{dictionary_name}.json'

    if not os.path.isfile(dictionary_file):
        return

    with open(dictionary_file, "r") as json_file:
        dictionary_data: dict = json.load(json_file)

    if is_dictionary_private(dictionary_data):
        return

    try:
        if dictionary_data['Access_Users'][new_access_user_id]:
            return
    except KeyError:
        pass
    else:
        return

    dictionary_data['Access_Users'][new_access_user_id] = {'read': True, 'write': False, 'share': False}

    update_dictionary_data(dictionary_name, dictionary_owner_id, dictionary_data)


def remove_user_access_to_dictionary(dictionary_name: str, dictionary_owner_id: int, remove_access_user_id: int) -> None:
    """

    :param dictionary_name: Name of the dictionary
    :param dictionary_owner_id: Owner of the dictionary
    :param remove_access_user_id: The user id of the user being removed access to the dictionary
    :return: None
    """

    dictionary_directory: str = f'Automaton/dictionaries/{dictionary_owner_id}/'
    dictionary_file: str = f'{dictionary_directory}{dictionary_name}.json'

    if not os.path.isfile(dictionary_file):
        return

    with open(dictionary_file, "r") as json_file:
        dictionary_data: dict = json.load(json_file)

    if is_dictionary_private(dictionary_data):
        return

    try:
        if dictionary_data['Access_Users'][str(remove_access_user_id)]:
            print(1)
            pass
    except KeyError:
        print(f'Key {remove_access_user_id} was not found in {dictionary_data['Access_Users']}')
        return
    print(3)

    del(dictionary_data['Access_Users'][str(remove_access_user_id)])

    update_dictionary_data(dictionary_name, dictionary_owner_id, dictionary_data)
