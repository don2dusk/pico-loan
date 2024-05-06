from peewee import * # type: ignore

db: SqliteDatabase = SqliteDatabase('model.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(unique=True, primary_key=True)
    amount_loaned = FloatField(null=False)
    balance = FloatField(null=False)
    rate = FloatField(null=False)
    initial_month = IntegerField(default=1)


class Payment(BaseModel):
    user = ForeignKeyField(User, backref='user', field='name')
    amount_paid = FloatField(null=False)
    month_paid = IntegerField(null=False)
    balance = FloatField(null=False)

def init() -> None:
    db.connect()
    db.create_tables([User, Payment])
    print("Connected!")