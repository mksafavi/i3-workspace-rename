import argparse

from i3ipc import Connection, Event
from i3ipc.events import IpcBaseEvent

from workspace_rename import rename_workspace, get_rename_command, WindowProperty


def main():
    max_length, separator, window_property = parse_cli_args()
    print('config:', max_length, separator, window_property)

    def rename_workspace_callback(connection: Connection, event: IpcBaseEvent):
        workspace = connection.get_tree().find_by_window(event.container.window).workspace()
        if workspace:
            rename_workspace(
                connection=connection,
                rename_command=get_rename_command(
                    workspace=workspace,
                    separator=separator,
                    max_length=max_length,
                    window_property=window_property
                )
            )

    def rename_all_workspaces_callback(connection: Connection, event: IpcBaseEvent):
        for workspace in connection.get_tree().workspaces():
            rename_workspace(
                connection=connection,
                rename_command=get_rename_command(
                    workspace=workspace,
                    separator=separator,
                    max_length=max_length,
                    window_property=window_property
                )
            )

    i3 = Connection()
    i3.on(Event.WINDOW_TITLE, rename_workspace_callback)
    i3.on(Event.WINDOW_NEW, rename_workspace_callback)
    i3.on(Event.WINDOW_MOVE, rename_workspace_callback)
    i3.on(Event.WINDOW_CLOSE, rename_all_workspaces_callback)
    i3.main()


def parse_cli_args():
    parser = argparse.ArgumentParser(description='i3 dynamic workspace rename tool')
    parser.add_argument(
        '--max_length',
        metavar='N',
        type=int,
        default=40,
        help='set maximum length of window name'
    )
    parser.add_argument(
        '--separator',
        metavar='"str"',
        type=str,
        default=' | ',
        help='set separator between window name (use quotation to set spaces)'
    )
    parser.add_argument(
        '--window_property',
        default=WindowProperty.wm_class.name,
        metavar=WindowProperty.names(),
        type=str,
        help='set window property to use as window alias'
    )
    args = parser.parse_args()
    max_length = args.max_length
    separator = args.separator
    window_property = WindowProperty[args.window_property]
    return max_length, separator, window_property


if __name__ == '__main__':
    main()
