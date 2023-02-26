from i3ipc import Connection, Event
from i3ipc.events import IpcBaseEvent

from workspace_rename import rename_workspace, get_rename_command, WindowProperty

def main():
    # TODO: add cli args
    separator = ' || '
    max_length = 40
    window_property = WindowProperty['wm_name']


    def rename_workspace_callback(connection: Connection, event: IpcBaseEvent):
        workspace = connection.get_tree().find_by_window(event.container.window).workspace()
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

if __name__ == '__main__':
    main()
