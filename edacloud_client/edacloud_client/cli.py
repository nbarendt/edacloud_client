#!/usr/bin/env python 
from cmd import Cmd
from urllib2 import urlopen

class EDACloudClient(Cmd):
    prompt = 'edacloud> '
    server_hostname = 'localhost'
    server_portnumber = 8080

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        Cmd.__init__(self, completekey, stdin, stdout)

    def do_echo(self, args):
        self.stdout.write(args)

    def do_quit(self, args):
        self.stdout.write("bye!")
        return True

    def do_EOF(self, args):
        return self.do_quit(args)

    def do_datetime(self, args):
        result = urlopen('http://{0}:{1}/datetime'.format(self.server_hostname, self.server_portnumber))
        self.stdout.write(result.read())


if __name__ == '__main__':
    cli = EDACloudClient()
    cli.cmdloop()
