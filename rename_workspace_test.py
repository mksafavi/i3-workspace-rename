import random
import string
from enum import Enum
from typing import Iterable, Generator

from i3ipc import Connection, Con, WindowEvent


def truncate_window_name(name: str, max_length: int = None) -> str:
    if max_length:
        return f"{name[0:max_length]}..."
    else:
        return name


def random_string_generator(length=10) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))


def test_truncate_window_name():
    name = random_string_generator()
    actual_name = truncate_window_name(name=name)
    assert actual_name == name


def test_truncate_window_name_truncates_names_bigger_than_max_length():
    long_name = f"abcde{random_string_generator(length=100)}"
    max_length = 5
    actual_name = truncate_window_name(name=long_name, max_length=max_length)
    assert actual_name == f"abcde..."
    assert len(actual_name) == max_length + 3


def create_workspace_name(windows_names: list, separator: str = ' ') -> str:
    return separator.join(windows_names)


def test_create_workspace_name():
    windows_names = [random_string_generator(random.getrandbits(5)), random_string_generator(random.getrandbits(5))]
    separator = f"-{random_string_generator(2)}-"
    workspace_name = create_workspace_name(windows_names=windows_names, separator=separator)
    assert workspace_name == f"{windows_names[0]}{separator}{windows_names[1]}"


def create_rename_command(number: int, name: str, new_name: str) -> list:
    return ['rename', 'workspace', f'"{escape_double_quote(name)}"', f'"{number}: {escape_double_quote(new_name)}"']


def escape_double_quote(s):
    return s.replace('"', r'\"')


def test_create_rename_workspace_command():
    number = random.getrandbits(5)
    name = random_string_generator()
    new_name = random_string_generator()
    actual_command = create_rename_command(number=number, name=name, new_name=new_name)
    assert actual_command == ['rename', 'workspace', f'"{name}"', f'"{number}: {new_name}"']


def test_create_rename_workspace_command_must_escape_double_quotes_in_names():
    number = random.getrandbits(5)
    name = 'abc"def'
    new_name = 'tu"vwx"yz'
    actual_command = create_rename_command(number=number, name=name, new_name=new_name)
    assert actual_command == ['rename', 'workspace', f'"abc\\"def"', f'"{number}: tu\\"vwx\\"yz"']


def rename_workspace(connection: Connection, rename_command: list[str]):
    connection.command(
        payload=' '.join(rename_command)
    )


def get_workspace_windows_properties(workspace: Iterable[Con]) -> Generator:
    return (
        (window.window_title, window.window_instance, window.window_class)
        for window in workspace
    )


class WindowProperty(Enum):
    wm_name = 0
    wm_instance = 1
    wm_class = 2


def get_windows_names(windows_properties: Iterable[tuple], window_property: WindowProperty) -> list:
    return [
        window[window_property.value]
        for window in windows_properties
    ]


def test_get_windows_names():
    window_properties = [
        ('n1', 'i1', 'c1'),
        ('n2', 'i2', 'c2'),
    ]
    assert get_windows_names(
        windows_properties=window_properties,
        window_property=WindowProperty.wm_name
    ) == ['n1', 'n2']
    assert get_windows_names(
        windows_properties=window_properties,
        window_property=WindowProperty.wm_instance
    ) == ['i1', 'i2']

    assert get_windows_names(
        windows_properties=window_properties,
        window_property=WindowProperty.wm_class
    ) == ['c1', 'c2']


def rename_workspace_callback(connection: Connection, event: WindowEvent):
    workspace = connection.get_tree().find_by_window(event.container.window).workspace()
    rename_workspace(
        connection=connection,
        rename_command=get_rename_command(workspace, separator, window_property)
    )

def rename_all_workspaces_callback(connection: Connection, event: WindowEvent):
    for workspace in connection.get_tree().workspaces():
        rename_workspace(
            connection=connection,
            rename_command=get_rename_command(workspace, separator, window_property)
        )

def get_rename_command(workspace, separator, window_property):
    windows_properties = get_workspace_windows_properties(workspace=workspace)
    windows_names = get_windows_names(windows_properties=windows_properties, window_property=window_property)
    new_name = create_workspace_name(windows_names=windows_names, separator=separator)
    return create_rename_command(number=workspace.num, name=workspace.name, new_name=new_name)

# def get_workspace_windows()
