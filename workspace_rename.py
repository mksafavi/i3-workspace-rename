from enum import Enum
from typing import Iterable, Generator

from i3ipc import Connection, Con


class WindowProperty(Enum):
    wm_name = 0
    wm_instance = 1
    wm_class = 2


def rename_workspace(connection: Connection, rename_command: list[str]):
    connection.command(
        payload=' '.join(rename_command)
    )


def get_rename_command(workspace, separator, max_length, window_property):
    windows_properties = _get_workspace_windows_properties(workspace=workspace)
    windows_names = _get_windows_names(windows_properties=windows_properties, window_property=window_property, max_length=max_length)
    new_name = _create_workspace_name(windows_names=windows_names, separator=separator)
    return _create_rename_command(number=workspace.num, name=workspace.name, new_name=new_name)


def _get_workspace_windows_properties(workspace: Iterable[Con]) -> Generator:
    # TODO: add test
    return (
        (str(node.window_title), str(node.window_instance), str(node.window_class))
        for node in workspace if node.window
    )


def _get_windows_names(windows_properties: Iterable[tuple], window_property: WindowProperty, max_length: int) -> list:
    return [
        _truncate_string(window[window_property.value], max_length=max_length)
        for window in windows_properties
    ]


def _create_workspace_name(windows_names: list, separator: str = ' ') -> str:
    return separator.join(windows_names)


def _create_rename_command(number: int, name: str, new_name: str) -> list:
    return ['rename', 'workspace', f'"{_escape_double_quote(name)}"', 'to',
            f'"{number}: {_escape_double_quote(new_name)}"']


def _escape_double_quote(s):
    return s.replace('"', r'\"')


def _truncate_string(data: str, max_length: int = None) -> str:
    if max_length and len(data) > max_length:
        return f"{data[0:max_length - 3]}..."
    else:
        return data
