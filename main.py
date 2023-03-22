import logging
from typing import List
from argparse import ArgumentParser


# Mapping of pattern characters to human readable text
CHAR_MAP = {
    'S': 'Soft',
    'T': 'Tough'
}


def view_message(msg: str, log_level: str = 'error', log_only: bool = False) -> None:
    """
    Prints message to standard output and to the log

    Args:
        msg (str): Message to display.
        log_level (str): Type of log level ('debug' or 'error'). Default value is 'error
        log_only (bool): Print message only to the log. Default value is False

    Returns:
        Nothing
    """
    if log_level == 'error':
        logging.error(msg)
    else:
        logging.debug(msg)

    if not log_only:
        print(msg)


def validate_chars(pattern_string: str) -> bool:
    """
    Checks if the given string only consists of valid characters.

    Args:
        pattern_string (str): The pattern string to validate.

    Returns:
        bool: True if pattern is valid, False otherwise.
    """
    if len(pattern_string) > 0:
        for char in pattern_string:
            if char not in CHAR_MAP.keys():
                view_message(f'{char} is not one of the allowed letters')
                return False
        return True
    return False


def validate_ints(numbers: List[str]) -> List[int]:
    """
    Converts a list of strings to a list of integers greater than 0.

    Args:
        numbers (List[str]): The input arguments to validate.

    Returns:
        List[int]: A list of integers if all input arguments are valid, 
        an empty list otherwise.
    """
    integers = []
    for number in numbers:
        try:
            n = int(number)
            if n < 1:
                raise ValueError()
            integers.append(n)
        except ValueError:
            view_message(f'{number} is not valid number (should be integer greater than 0)')
            return []
    return integers


def map_characters(pattern_string: str, output_len: int) -> str:
    """
    Map pattern characters to human readable text and repeat the pattern for given number of times.

    Args:
        pattern_string (str): The pattern string to map.
        output_len (int): The length of the output.

    Returns:
        str: A string of mapped characters with the required output length.
    """

    if len(pattern_string) == 0:
        view_message('An empty string has been passed to the function', log_only=True)
        return pattern_string

    # Get qoutient of length, or the number of times the string will be repeated in full
    full_copies = output_len // len(pattern_string)
    # Number of elements that need to be taken from the provided string
    remainder = output_len % len(pattern_string)

    pattern_string = pattern_string * full_copies + pattern_string[:remainder]

    if len(pattern_string) == 1:
        return f'{CHAR_MAP[pattern_string]}.'
    # Join the translated words with commas and add the las word with the word 'and'
    return '{0} and {1}.'.format(', '.join(CHAR_MAP[foo] for foo in pattern_string[:-1]),
                                 CHAR_MAP[pattern_string[-1]])


if __name__ == '__main__':
    # Logging setup with customized format, date and file
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                        datefmt='%d.%m.%Y-%H:%M:%S',
                        filename='main.log',
                        encoding='utf-8',
                        level=logging.DEBUG)

    # Command line argument parser setup
    parser = ArgumentParser()
    parser.add_argument('pattern',
                        help=f'A string consisting of the following chars: {",".join(CHAR_MAP.keys())}')
    parser.add_argument('numbers',
                        nargs='+',
                        help=f'Integers separated by spaces. Should be higher than 0')
    args = parser.parse_args()

    view_message('User input: {pattern} {numbers}'.format(**vars(args)),
                 log_level='debug', log_only=True)

    numbers = validate_ints(args.numbers)
    if validate_chars(args.pattern) and numbers:
        for number in numbers:
            view_message(map_characters(args.pattern, number), log_level='debug')
