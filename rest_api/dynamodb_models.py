from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, NumberAttribute, JSONAttribute
from datetime import datetime


class FileModel(Model):
    """
    Dynamodb File model
    """
    class Meta:
        table_name = 'file_table'
        host = 'http://dynamodbservice:8000'

    file_name = UnicodeAttribute(range_key=True, attr_name='file_name')
    file_owner = UnicodeAttribute(hash_key=True, attr_name='file_owner')
    meta_data = JSONAttribute(attr_name='meta_data')
    upload_date = UTCDateTimeAttribute(null=True,
                                       default=datetime.utcnow(),
                                       attr_name='upload_date')


class UserModel(Model):
    """
    Dynamodb User Model
    """
    class Meta:
        table_name = 'user_table'
        host = 'http://dynamodbservice:8000'

    email = UnicodeAttribute(hash_key=True, attr_name='user_email')
    username = UnicodeAttribute(range_key=True, attr_name='user_name', null=True)


