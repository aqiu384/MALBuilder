import cmd
import getpass
from aasession import AaSession, AaEntry


class AnimeAdviceInterface(cmd.Cmd):
    intro = "Welcome to AAI: The Anime Advice Interface:\nType 'help' for further information."
    prompt = "(AAI): "

    def __init__(self):
        super(AnimeAdviceInterface, self).__init__()
        self.session = None

    def cmdloop(self):
        self.session = AaSession()
        return cmd.Cmd.cmdloop(self)

    def do_search(self, line):
        '''Search AA by following criteria'''
        sparams = {}
        rparams = []

        print('Enter in [metric]:[value] pairs for search criteria.\nEnter "DONE" when finished.')
        while True:
            s = input('Search criteria: ').split(':')
            if s[0] == "DONE":
                break
            if s[0] not in self.session.QUERY_INPUTS:
                print('Error: invalid search criteria.')
                continue
            if len(s) < 2:
                print('Error: no search value given.')
                continue
            sparams[self.session.QUERY_INPUTS[s[0]]] = s[1]

        print('Enter in [metric] for return criteria.\nEnter "DONE" when finished.')
        while True:
            s = input('Return criteria: ')
            if s == "DONE":
                break
            if s not in self.session.QUERY_OUTPUTS:
                print('Error: invalid return criteria.')
                continue
            rparams.append(self.session.QUERY_OUTPUTS[s])

        results = self.session.searchanime(sparams, rparams)

        print('Search results:\nID\tTitle')
        for r in results:
            print('{:d}\t{:s}'.format(r.malid, r.title))

    def do_exit(self, line):
        '''Exits AAI'''
        return True

if __name__ == '__main__':
    AnimeAdviceInterface().cmdloop()