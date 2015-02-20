import cmd
import getpass
from dbsession import DbSession, DbAuthError, DbEntry
from sqlalchemy import create_engine


class DatabaseInterface(cmd.Cmd):
    intro = "Welcome to MALB Database Interface:\nType 'help' for further information."
    prompt = "(DBI): "

    def __init__(self):
        super(DatabaseInterface, self).__init__()
        self.session = None

    def cmdloop(self):
        print('MAL credentials required for login.')
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        try:
            self.session = DbSession(username, password)
        except DbAuthError:
            print('Error: invalid MAL credentials.')
            return
        return cmd.Cmd.cmdloop(self)

    def do_view(self, line):
        '''View current completed, watching, and not-seen lists'''
        print('Completed:')
        for entry in self.session.getlist('completed'):
            print('{:d}\t{:s}'.format(entry.malid, entry.title))

        print('Watching:')
        for entry in self.session.getlist('watching'):
            print('{:d}\t{:s}'.format(entry.malid, entry.title))

        print('Not seen:')
        for entry in self.session.getlist('notseen'):
            print('{:d}\t{:s}'.format(entry.malid, entry.title))

    def do_searchkey(self, line):
        '''Search anime by keyword'''
        if line == "":
            print('Usage: searchkey [keyword]')
            return
        print('Search for "{}" returned:'.format(line))

    def do_searchid(self, line):
        '''Search anime by ID'''
        try:
            id = int(line)
            print('Description for {}'.format(id))
        except ValueError:
            print('Usage: searchkey [mal_id]')

    def do_add(self, line):
        '''Add a new anime given the ID'''
        try:
            args = line.split()
            id = int(args[0])
            status = args[1]
            print('Adding "{:d}" with watch status "{:s}" to MAL.'.format(id, status))
        except (ValueError, IndexError):
            print('Usage: add [mal_id] [watch status]')

    def do_update(self, line):
        '''Update an existing anime given the ID'''
        try:
            args = line.split()
            id = int(args[0])
            metric = args[1]
            value = args[2]
            print('Updating "{:d}" with "{:s}: {:s}" in MAL.'.format(id, metric, value))
        except (ValueError, IndexError):
            print('Usage: update [mal_id] [metric] [value]')

    def do_delete(self, line):
        '''Delete an exiting anime given the ID'''
        try:
            id = int(line)
            print('Deleting {}'.format(id))
        except ValueError:
            print('Usage: delete [mal_id] from MAL.')

    def do_exit(self, line):
        '''Exits AAI'''
        return True

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
    DatabaseInterface().cmdloop()