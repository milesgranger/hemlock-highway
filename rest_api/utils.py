from .models import FileModel, UserModel, PaymentModel
from .models import POSTGRES_DB


def create_tables():

    FileModel.create_table(read_capacity_units=1, write_capacity_units=1)

    POSTGRES_DB.connect()
    POSTGRES_DB.create_tables([UserModel, PaymentModel], safe=True)
    POSTGRES_DB.close()

    return True
