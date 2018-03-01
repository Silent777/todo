"""
Project validators
==================

Module that provides validation functions for all kinds of project's data.
"""

STR_MIN_LENGTH = 0
STR_MAX_LENGTH = None


def string_validator(value, min_length=STR_MIN_LENGTH, max_length=STR_MAX_LENGTH):
    """
    Function that provides string validation.

    :param value: the string literal itself.
    :type value: string

    :param min_length: the minimal length of the received string value.
    :type min_length: integer

    :param max_length: the maximum length of the received string value.
    :type max_length: integer

    :return: `True` if value if valid and `False` if it is not.
    """

    if not isinstance(value, str):
        return False

    if len(value) < min_length:
        return False

    if max_length:
        if len(value) > max_length:
            return False

    return True


def required_keys_validator(data, keys_required, strict=True):
    """
    Provide required keys validation.

    :param data: data from request.
    :type data: dictionary

    :param keys_required: set or list or tuple of requied keys for method.
    :type keys_required: set or list or tuple

    :param strict: shows the status of strict method of comparing keys
                   in input data with required keys in method.
    :type strict: Bool

    :return: `True` if data is valid and `False` if it is not valid.
    """
    keys = set(data.keys())
    keys_required = set(keys_required)
    if strict:
        return not keys.symmetric_difference(keys_required)

    return not keys_required.difference(keys)




def task_data_validate_create(data):
    """
    Function that provides complete task model data validation

    :param data: the data that is received by task view.
    :type data: dict

    :return: `True' if all data is valid or `False` if some fields are invalid.
    :rtype `bool`
    """
    status = data.get('status')
    status_range = range(0, 3)
    required_keys = ['title', 'description', 'status']

    if not required_keys_validator(data, required_keys, False):
        return False
    if not string_validator(data.get('title'), max_length=255):
        return False
    if not string_validator(data.get('description'), max_length=1024):
        return False
    if not(isinstance(status, int) and status in status_range):
        return False
    return True

def task_data_validate_update(data):
    """
    Function that provides complete task model data validation

    :param data: the data that is received by task view.
    :type data: dict

    :return: `True' if all data is valid or `False` if some fields are invalid.
    :rtype `bool`
    """

    errors = []
    task_model_fields = ['title', 'description', 'status']

    filtered_data = {key: data.get(key) for key in task_model_fields}
    validation_rules = {'title': lambda val: string_validator(val, max_length=255),
                        'description': lambda val: string_validator(val, max_length=1024),
                        'status': lambda val: isinstance(val, int) and val in range(0, 3)}

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                errors.append(key + ' field error')

    is_data_valid = len(errors) == 0
    return is_data_valid
