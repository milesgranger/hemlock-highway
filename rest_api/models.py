import os

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute
from datetime import datetime

import peewee as pw


class FileModel(Model):
    """
    Dynamodb File model
    """
    class Meta:
        table_name = 'ol_file_table'
        host = os.environ.get('DYNAMODB_ENDPOINT')

    file_owner = UnicodeAttribute(hash_key=True, attr_name='file_owner')
    file_name = UnicodeAttribute(range_key=True, attr_name='file_name')
    meta_data = JSONAttribute(attr_name='meta_data')
    upload_date = UTCDateTimeAttribute(null=True,
                                       default=datetime.utcnow(),
                                       attr_name='upload_date')


POSTGRES_DB = pw.PostgresqlDatabase('opplett',
                                    host='postgres-service',
                                    user=os.environ.get('POSTGRES_USER'),
                                    password=os.environ.get('POSTGRES_PASSWORD')
                                    )


class BaseModel(pw.Model):
    class Meta:
        database = POSTGRES_DB


class UserModel(BaseModel):
    """
    PostgreSQL User Table
    """
    class Meta:
        db_table = 'ol_user'

    username = pw.CharField(max_length=255, primary_key=True, unique=True, null=False)
    email = pw.CharField(max_length=255, unique=True, null=False)
    name = pw.CharField(max_length=255, null=True)
    balance = pw.FloatField(null=False, default=0)
    bytes_stored = pw.FloatField(null=False, default=0)
    profile_img = pw.CharField(max_length=2000, null=True)


class PaymentModel(BaseModel):
    """
    PostgreSQL Payment Table
    Saves all payments
    """
    class Meta:
        db_table = 'ol_payment'

    username = pw.ForeignKeyField(UserModel, related_name='payments')
    payment_id = pw.IntegerField(primary_key=True)
    payment_details = pw.BlobField()


