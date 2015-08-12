from paramiko.client import SSHClient
import paramiko
import time


class FlatSSH(SSHClient):
    def __init__(self, hostname, port, username, password):
        super(FlatSSH, self).__init__()
        self.username = username
        self.password = password
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password
        )

    def run(self, command, timeout=15):
        channel = self.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb')
        stdin.write(command)
        time.sleep(timeout)

        stdin.close()
        stdout.close()


    def sudo(self, command, timeout=15):
        command = "sudo -S -p '' %s" % command
        channel = self.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb')
        stdin.write(command)
        stdin.write(self.password + '\n')
        time.sleep(timeout)

        stdin.close()
        stdout.close()
