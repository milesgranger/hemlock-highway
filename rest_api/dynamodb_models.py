import os

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from datetime import datetime


class FileModel(Model):
    """
    Dynamodb File model
    """
    class Meta:
        table_name = 'ol_file_table'
        host = os.environ.get('DYNAMODB_ENDPOINT')

    file_name = UnicodeAttribute(range_key=True, attr_name='file_name')
    file_owner = UnicodeAttribute(hash_key=True, attr_name='file_owner')
    meta_data = JSONAttribute(attr_name='meta_data')
    upload_date = UTCDateTimeAttribute(null=True,
                                       default=datetime.utcnow(),
                                       attr_name='upload_date')


class UserUsernameIndex(GlobalSecondaryIndex):
    """
    Global Secondary Index to allow querying by username instead of email
    Used to check if there exists someone with this username
    """
    class Meta:
        projection = AllProjection()
        read_capacity_units = 1
        write_capacity_units = 1
    username = UnicodeAttribute(hash_key=True, attr_name='username')


class UserModel(Model):
    """
    Dynamodb User Model
    """
    class Meta:
        table_name = 'ol_user_table'
        host = os.environ.get('DYNAMODB_ENDPOINT')

    email = UnicodeAttribute(hash_key=True, attr_name='email')
    username = UnicodeAttribute(range_key=True, attr_name='username', default='N/A')
    username_index = UserUsernameIndex()
    name = UnicodeAttribute(attr_name='name')
    balance = NumberAttribute(default=0, attr_name='balance')
    bytes_stored = NumberAttribute(default=0, attr_name='bytes_stored')
    profile_img = UnicodeAttribute(attr_name='profile_img')


class PaymentModel(Model):
    """
    Dynamodb Payment Model
    Saves all payments
    """
    class Meta:
        table_name = 'ol_payment_table'
        host = os.environ.get('DYNAMODB_ENDPOINT')

    username = UnicodeAttribute(hash_key=True, attr_name='username')
    payment_id = UnicodeAttribute(range_key=True, attr_name='payment_id')
    payment_details = JSONAttribute(default={}, attr_name='payment_details')


