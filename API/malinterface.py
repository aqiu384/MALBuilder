import cmd
import getpass
from malsession import MalSession


class MyAnimeListInterface(cmd.Cmd):
    intro = "Welcome to MALI: The MyAnimeList Interface:\nType 'help' for further information."
    prompt = "(MALI): "

    def __init__(self):
        super(AnimeAdviceInterface, self).__init__()
        self.session = None

    def cmdloop(self):
        print('MAL credentials required for login.')
        username = input('Username: ')
        password = getpass('Password: ')
        self.session = MalSession(username, password)
        return cmd.Cmd.cmdloop(self)

    def do_view(self, line):
        '''View current MAL'''
        print('Current MAL:')

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

if __name__ == '__main__':
    MyAnimeListInterface().cmdloop()