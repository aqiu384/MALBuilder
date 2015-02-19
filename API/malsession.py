class MalSession:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        # Authenticate username with password through MAL
        if username != password:
            raise Exception('Invalid MAL credentials')