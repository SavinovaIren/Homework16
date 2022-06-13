import datetime
from main import db
from models import User, Offer, Order
from data import users, offers, orders


db.drop_all()
db.create_all()

for i in users:
    db.session.add(User(
        id=i["id"],
        first_name=i["first_name"],
        last_name=i["last_name"],
        age=i["age"],
        email=i["email"],
        role=i["role"],
        phone=i["phone"]
    ))

for i in orders:
    month_start, day_start, year_start = [int(o) for o in i['start_date'].split("/")]
    month_end, day_end, year_end = i['end_date'].split("/")
    db.session.add(Order(
        id=i["id"],
        name=i["name"],
        description=i["description"],
        start_date=datetime.date(year=year_start, month=month_start, day=day_start),
        end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
        address=i["address"],
        price=i["price"],
        customer_id=i["customer_id"],
        executor_id=i["executor_id"]))

for i in offers:
    db.session.add(Offer(
        id=i["id"],
        order_id=i["order_id"],
        executor_id=i["executor_id"]
    ))

db.commit()