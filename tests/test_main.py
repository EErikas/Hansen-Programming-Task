import unittest
from unittest.mock import patch, MagicMock
import logging
from io import StringIO
from main import view_message, validate_chars, validate_ints, map_characters


class TestViewMessage(unittest.TestCase):

    def setUp(self):
        self.mock_logger = MagicMock(spec=logging.Logger)

        self.patcher_log_error = patch('logging.error', self.mock_logger.error)
        self.addCleanup(self.patcher_log_error.stop)
        self.patcher_log_error.start()

        self.patcher_log_debug = patch('logging.debug', self.mock_logger.debug)
        self.addCleanup(self.patcher_log_debug.stop)
        self.patcher_log_debug.start()

        self.stdout = StringIO()
        self.patcher_stdout = patch('sys.stdout', self.stdout)
        self.addCleanup(self.patcher_stdout.stop)
        self.patcher_stdout.start()

    def test_view_message_prints_to_stdout_and_logs_correctly(self):
        msg = 'Test message'
        view_message(msg, log_level='error')
        self.assertEqual(self.mock_logger.error.call_count, 1)
        self.mock_logger.error.assert_called_with(msg)
        self.assertEqual(self.mock_logger.debug.call_count, 0)
        self.assertEqual(self.stdout.getvalue().strip(), msg)

    def test_view_message_only_logs_when_log_only_is_true(self):
        msg = 'Test message'
        view_message(msg, log_level='error', log_only=True)
        self.assertEqual(self.mock_logger.error.call_count, 1)
        self.mock_logger.error.assert_called_with(msg)
        self.assertEqual(self.mock_logger.debug.call_count, 0)
        self.assertEqual(self.stdout.getvalue().strip(), '')

    def test_view_message_defaults_to_error_log_level(self):
        msg = 'Test message'
        view_message(msg)
        self.assertEqual(self.mock_logger.error.call_count, 1)
        self.mock_logger.error.assert_called_with(msg)
        self.assertEqual(self.mock_logger.debug.call_count, 0)

    def test_view_message_logs_at_debug_level_when_specified(self):
        msg = 'Test message'
        view_message(msg, log_level='debug')
        self.assertEqual(self.mock_logger.debug.call_count, 1)
        self.mock_logger.debug.assert_called_with(msg)
        self.assertEqual(self.mock_logger.error.call_count, 0)

    def test_view_message_returns_none(self):
        msg = 'Test message'
        result = view_message(msg, log_level='error', log_only=False)
        self.assertIsNone(result)


class TestValidateChars(unittest.TestCase):
    def setUp(self):
        # Set up mock logger
        self.mock_logger = MagicMock(spec=logging.Logger)
        # Mock logger for error level
        self.patcher_log_error = patch('logging.error', self.mock_logger.error)
        self.addCleanup(self.patcher_log_error.stop)
        self.patcher_log_error.start()
        # Setup mock stdout
        self.stdout = StringIO()
        self.patcher_stdout = patch('sys.stdout', self.stdout)
        self.addCleanup(self.patcher_stdout.stop)
        self.patcher_stdout.start()

    def test_valid_pattern(self):
        self.assertTrue(validate_chars('STTTS'))

    def test_invalid_pattern(self):
        invalid_str = 'ABCD'
        self.assertFalse(validate_chars(invalid_str))
        error_msg = f'{invalid_str[0]} is not one of the allowed letters'
        self.mock_logger.error.assert_called_with(error_msg)
        self.assertEqual(self.mock_logger.error.call_count, 1)
        self.assertEqual(self.stdout.getvalue().strip(), error_msg)

    def test_empty_pattern(self):
        self.assertFalse(validate_chars(''))


class TestValidateInts(unittest.TestCase):
    def setUp(self):
        # Set up mock logger
        self.mock_logger = MagicMock(spec=logging.Logger)
        # Mock logger for error level
        self.patcher_log_error = patch('logging.error', self.mock_logger.error)
        self.addCleanup(self.patcher_log_error.stop)
        self.patcher_log_error.start()
        # Setup mock stdout
        self.stdout = StringIO()
        self.patcher_stdout = patch('sys.stdout', self.stdout)
        self.addCleanup(self.patcher_stdout.stop)
        self.patcher_stdout.start()

        self.error_msg = '{} is not valid number (should be integer greater than 0)'

    def test_valid_ints(self):
        self.assertEqual(validate_ints(['1', '5', '8']), [1, 5, 8])

    def test_invalid_ints_zero(self):
        invalid_ints = ['1', '0', '8']
        self.assertEqual(validate_ints(invalid_ints), [])
        error_msg = self.error_msg.format(invalid_ints[1])
        self.mock_logger.error.assert_called_with(error_msg)
        self.assertEqual(self.mock_logger.error.call_count, 1)
        self.assertEqual(self.stdout.getvalue().strip(), error_msg)

    def test_invalid_ints_negative(self):
        invalid_ints = ['-1', '0', '8']
        self.assertEqual(validate_ints(invalid_ints), [])
        error_msg = self.error_msg.format(invalid_ints[0])
        self.mock_logger.error.assert_called_with(error_msg)
        self.assertEqual(self.mock_logger.error.call_count, 1)
        self.assertEqual(self.stdout.getvalue().strip(), error_msg)

    def test_invalid_ints_string(self):
        invalid_ints = ['1', 'abc', '8']
        self.assertEqual(validate_ints(invalid_ints), [])
        error_msg = self.error_msg.format(invalid_ints[1])
        self.mock_logger.error.assert_called_with(error_msg)
        self.assertEqual(self.mock_logger.error.call_count, 1)
        self.assertEqual(self.stdout.getvalue().strip(), error_msg)

    def test_invalid_ints_float(self):
        invalid_ints = ['1', '9', '8.3']
        self.assertEqual(validate_ints(invalid_ints), [])
        error_msg = self.error_msg.format(invalid_ints[2])
        self.mock_logger.error.assert_called_with(error_msg)
        self.assertEqual(self.mock_logger.error.call_count, 1)
        self.assertEqual(self.stdout.getvalue().strip(), error_msg)

    def test_empty_input(self):
        self.assertEqual(validate_ints([]), [])


class TestMapCharacters(unittest.TestCase):
    def setUp(self):
        # Set up mock logger
        self.mock_logger = MagicMock(spec=logging.Logger)
        # Mock logger for error level
        self.patcher_log_error = patch('logging.error', self.mock_logger.error)
        self.addCleanup(self.patcher_log_error.stop)
        self.patcher_log_error.start()

        self.error_msg = 'Inproper output length ({}) provided'

    def test_single_char_pattern(self):
        self.assertEqual(map_characters('S', 3), 'Soft, Soft and Soft.')

    def test_multiple_char_pattern(self):
        self.assertEqual(map_characters('STTTS', 5),
                         'Soft, Tough, Tough, Tough and Soft.')

    def test_pattern_length_greater_than_output_length(self):
        self.assertEqual(map_characters('ST', 1), 'Soft.')

    def test_pattern_length_divisible_by_output_length(self):
        self.assertEqual(map_characters('SSTT', 4),
                         'Soft, Soft, Tough and Tough.')

    def test_pattern_length_not_divisible_by_output_length(self):
        self.assertEqual(map_characters('STTTS', 7),
                         'Soft, Tough, Tough, Tough, Soft, Soft and Tough.')

    def test_pattern_length_is_zero(self):
        self.assertEqual(map_characters('', 7), '')
        self.mock_logger.error.assert_called_with(
            'An empty string has been passed to the function')
        self.assertEqual(self.mock_logger.error.call_count, 1)

    def test_output_length_is_zero(self):
        number = 0
        self.assertEqual(map_characters('SST', number), '')
        self.mock_logger.error.assert_called_with(
            self.error_msg.format(number))
        self.assertEqual(self.mock_logger.error.call_count, 1)

    def test_output_length_is_negative(self):
        number = -10
        self.assertEqual(map_characters('SST', number), '')
        self.mock_logger.error.assert_called_with(
            self.error_msg.format(number))
        self.assertEqual(self.mock_logger.error.call_count, 1)


if __name__ == '__main__':
    unittest.main()
