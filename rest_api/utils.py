from .dynamodb_models import FileModel, UserModel, PaymentModel

def create_tables():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1)
    FileModel.create_table(read_capacity_units=1, write_capacity_units=1)
    PaymentModel.create_table(read_capacity_units=1, write_capacity_units=1)
    return True