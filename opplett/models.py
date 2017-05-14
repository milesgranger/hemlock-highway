from rest_api.dynamodb_models import UserModel

class User:
    """
    Representation of an OAuth user
    Data is the json acquired from successful authentication via an OAuth service. Google, etc.
    """
    def __init__(self, data, source):
        if source == 'google':
            self.name = data.get('name')
            self.profile_img = data.get('picture')
            self.email = data.get('email')


