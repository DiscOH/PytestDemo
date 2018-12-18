import pytest

from demo_libraries import global_variables, ssh_library

def test_ftg():
    ssh_client = ssh_library.connect(global_variables.hostname, global_variables.username, global_variables.password)
    commands = [
        'config vdom',
        'edit root',
        'config user local',
        'edit ?',
        'end'
    ]
    users = ssh_library.send_commands_and_exit(ssh_client, commands)
    print(users)
    assert users
