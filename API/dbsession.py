

class DbAuthError(Exception):
    pass


class DbEntry():
    def __init__(self, malid, title):
        self.malid = int(malid)
        self.title = title
        # Add more later if necessary


class DbSession:
    WATCH_STATUS = ['completed', 'watching', 'not-seen']

    def __init__(self, username, password):
        self.username = username
        self.password = password

        # Authenticate username with password through MAL
        if username != password:
            raise Exception('Invalid MAL credentials')