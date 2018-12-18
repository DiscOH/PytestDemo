import paramiko
import paramiko_expect
from time import sleep


def connect(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, username=username, password=password)
    return client


def send_commands_and_exit(client, commands, timeout=10, display=True, last_n_messages=1):
    output = []

    with paramiko_expect.SSHClientInteraction(
            client,
            timeout=timeout,
            output_callback=lambda m: output.append(m),
            display=display
    ) as interact:
        for command in commands:
            interact.send(command)
            interact.expect('.*')
            # corrects an issue where only partial commands get sent / returned
            sleep(.1)
        results = list(output[-last_n_messages:])
        interact.send('exit')

        interact.expect()
        client.close()

        return results
