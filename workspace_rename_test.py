import random
import string

from workspace_rename import \
    WindowProperty, \
    _truncate_string, \
    _create_workspace_name, \
    _create_rename_command, \
    _get_windows_names


def random_string_generator(length=10) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))


def test_get_windows_names():
    window_titles = [random_string_generator() for _ in range(3)]
    window_instances = [random_string_generator() for _ in range(3)]
    window_classes = [random_string_generator() for _ in range(3)]
    windows_properties = [i for i in zip(window_titles, window_instances, window_classes)]
    assert _get_windows_names(
        windows_properties=windows_properties, window_property=WindowProperty.wm_name
    ) == window_titles
    assert _get_windows_names(
        windows_properties=windows_properties, window_property=WindowProperty.wm_instance
    ) == window_instances

    assert _get_windows_names(
        windows_properties=windows_properties, window_property=WindowProperty.wm_class
    ) == window_classes


def test_get_windows_names_must_truncate_names_if_bigger_than_max_length():
    max_length = 10
    windows_properties = [(random_string_generator(100), random_string_generator(100), random_string_generator(100))]
    assert len(
        _get_windows_names(
            windows_properties=windows_properties, window_property=WindowProperty.wm_name, max_length=10
        )[0]
    ) == max_length


def test_create_rename_workspace_command():
    number = random.getrandbits(5)
    name = random_string_generator()
    new_name = random_string_generator()
    actual_command = _create_rename_command(number=number, name=name, new_name=new_name)
    assert actual_command == ['rename', 'workspace', f'"{name}"', 'to', f'"{number}: {new_name}"']


def test_create_rename_workspace_command_must_escape_double_quotes_in_names():
    number = random.getrandbits(5)
    name = 'abc"def'
    new_name = 'tu"vwx"yz'
    actual_command = _create_rename_command(number=number, name=name, new_name=new_name)
    assert actual_command == ['rename', 'workspace', f'"abc\\"def"', 'to', f'"{number}: tu\\"vwx\\"yz"']


def test_create_workspace_name():
    windows_names = [random_string_generator(random.getrandbits(5)), random_string_generator(random.getrandbits(5))]
    separator = f"-{random_string_generator(2)}-"
    workspace_name = _create_workspace_name(windows_names=windows_names, separator=separator)
    assert workspace_name == f"{windows_names[0]}{separator}{windows_names[1]}"


def test_truncate_string_must_not_truncate_given_no_max_length():
    expected_data = random_string_generator()
    assert _truncate_string(expected_data) == expected_data


def test_truncate_string_truncates_and_add_three_dots_when_length_bigger_than_max_length():
    long_data = f"abcde{random_string_generator(length=100)}"
    max_length = 5
    actual_name = _truncate_string(long_data, max_length=max_length)
    assert actual_name == f"ab..."
    assert len(actual_name) == max_length

def test_truncate_string_must_not_truncate_when_length_smaller_than_max_length():
    expected_data = random_string_generator(10)
    assert _truncate_string(expected_data, max_length=20) == expected_data
