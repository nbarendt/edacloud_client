#!/usr/bin/env python 
from cmd import Cmd

class EDACloudClient(Cmd):
    prompt = 'edacloud> '
    def do_echo(self, args):
        self.stdout.write(args)

    def do_quit(self, args):
        self.stdout.write("bye!")
        return True

    def do_EOF(self, args):
        return self.do_quit(args)



if __name__ == '__main__':
    cli = EDACloudClient()
    cli.cmdloop()
