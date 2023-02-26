from enum import Enum
from typing import Iterable, Generator

from i3ipc import Connection, Con


class WindowProperty(Enum):
    wm_name = 0
    wm_instance = 1
    wm_class = 2

    @classmethod
    def names(cls):
        return [n.name for n in cls]


def rename_workspace(connection: Connection, workspace: Con, separator: str, max_length: int,
                     window_property: WindowProperty):
    name = workspace.name
    new_name = _add_workspace_number_to_name(
        number=workspace.num,
        name=_create_workspace_name(
            windows_names=_get_windows_names(
                windows_properties=_get_workspace_windows_properties(workspace=workspace),
                window_property=window_property,
                max_length=max_length
            ),
            separator=separator
        )
    )
    if name != new_name:
        connection.command(
            payload=' '.join(
                _create_rename_command(
                    name=name,
                    new_name=new_name
                )
            )
        )


def _get_workspace_windows_properties(workspace: Iterable[Con]) -> Generator:
    # TODO: add test
    # TODO: fix crash on workspace=None
    return (
        (str(node.window_title), str(node.window_instance), str(node.window_class))
        for node in workspace if node.window
    )


def _get_windows_names(windows_properties: Iterable[tuple], window_property: WindowProperty, max_length: int) -> list[
    str]:
    return [
        _truncate_string(window[window_property.value], max_length=max_length)
        for window in windows_properties
    ]


def _add_workspace_number_to_name(number: int, name: str) -> str:
    return f'{number}: {name}'


def _create_workspace_name(windows_names: list, separator: str = ' ') -> str:
    return separator.join(windows_names)


def _create_rename_command(name: str, new_name: str) -> list[str]:
    return ['rename', 'workspace', f'"{_escape_double_quote(name)}"', 'to', f'"{_escape_double_quote(new_name)}"']


def _escape_double_quote(s):
    return s.replace('"', r'\"')


def _truncate_string(data: str, max_length: int = None) -> str:
    if max_length and len(data) > max_length:
        return f"{data[0:max_length - 3]}..."
    else:
        return data
