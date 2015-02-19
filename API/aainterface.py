#!/usr/bin/env
import cmd
import getpass
from aasession import AaSession, AaEntry


class AnimeAdviceInterface(cmd.Cmd, object):
    # http://pymotw.com/2/cmd/
    intro = "Welcome to AAI: The Anime Advice Interface:\nType 'help' for further information."
    prompt = "(AAI): "

    def __init__(self):
        super(AnimeAdviceInterface, self).__init__()
        self.session = None

    def do_EOF(self, line):
        return True

    def cmdloop(self):
        self.session = AaSession()
        return cmd.Cmd.cmdloop(self)

    def do_search(self, line):
        """Search AA by following criteria"""
        sparams = {}
        rparams = []

        print('Enter in [metric]:[value] pairs for search criteria.\nEnter "DONE" when finished.')
        while True:
            s = raw_input('Search criteria: ').upper().split(':')
            if s[0] == "DONE":
                break
            if s[0] not in self.session.QUERY_INPUTS.keys():
                print('Error: invalid search criteria.')
                continue
            if len(s) < 2:
                print('Error: no search value given.')
                continue
            sparams[self.session.QUERY_INPUTS[s[0]]] = s[1]

        print('Enter in [metric] for return criteria.\nEnter "DONE" when finished.')
        while True:
            s = raw_input('Return criteria: ').upper()
            if s == "DONE":
                break
            if s not in self.session.QUERY_OUTPUTS.keys():
                print('Error: invalid return criteria.')
                continue
            rparams.append(self.session.QUERY_OUTPUTS[s])

        results = self.session.searchanime(sparams, rparams)

        print('Search results:\nID\tTitle')
        for r in results:
            print('{:d}\t{:s}'.format(r.malid, r.title))

    def complete_search(self, text, line, begidx, endidx):
        """tabbing for results"""
        if not text:
            completions = self.session.QUERY_INPUTS.keys()
        else:
            completions = [f
                           for f in self.session.QUERY_INPUTS.keys()
                           if f.startswith(text.upper())
            ]
        return completions

    def do_results(self, line):
        """tabbing for results"""
        line = ""

    def complete_results(self, text, line, begidx, endidx):
        if not text:
            completions = self.session.QUERY_OUTPUTS.keys()
        else:
            completions = [f
                           for f in self.session.QUERY_OUTPUTS.keys()
                           if f.startswith(text.upper())
            ]
        return completions

    def do_exit(self, line):
        """Exits AAI"""
        return True

if __name__ == '__main__':
    AnimeAdviceInterface().cmdloop()