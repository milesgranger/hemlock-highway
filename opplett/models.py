# -*- encoding: UTF-8 -*-

import os

import peewee as pw
from redis import StrictRedis


POSTGRES_DB = pw.PostgresqlDatabase(database=os.environ.get('POSTGRES_DB'),
                                    host=os.environ.get('POSTGRES_ENDPOINT'),
                                    user=os.environ.get('POSTGRES_USER'),
                                    password=os.environ.get('POSTGRES_PASSWORD')
                                    )


def get_redis_con() -> StrictRedis:
    """
    Get a Redis DB connection
    :returns StrictRedis: StrictRedis connection
    """
    REDIS_DB = StrictRedis(host=os.environ.get('REDIS_ENDPOINT'),
                           port=6379)
    return REDIS_DB


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
    id = pw.CharField(null=True, primary_key=True)
    amount = pw.FloatField(null=True)
    amount_refunded = pw.FloatField(null=True)
    balance_transaction = pw.CharField(null=True)
    captured = pw.BooleanField(null=True)
    created = pw.TimestampField(null=True)
    currency = pw.CharField(null=True)
    customer = pw.CharField(null=True)
    description = pw.CharField(null=True)
    destination = pw.CharField(null=True)
    dispute = pw.CharField(null=True)
    failure_code = pw.CharField(null=True)
    failure_message = pw.CharField(null=True)
    invoice = pw.CharField(null=True)
    livemode = pw.BooleanField(null=True)
    object = pw.CharField(null=True)
    on_behalf_of = pw.CharField(null=True)
    order = pw.CharField(null=True)
    outcome = pw.CharField(null=True)
    paid = pw.CharField(null=True)
    receipt_email = pw.CharField(null=True)
    receipt_number = pw.CharField(null=True)
    refunded = pw.BooleanField(null=True)
    refunds = pw.FloatField(null=True)
    review = pw.CharField(null=True)
    source = pw.CharField(null=True)
    source_transfer = pw.CharField(null=True)
    status = pw.CharField(null=True)






