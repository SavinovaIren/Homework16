from main import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    age = db.Column(db.Integer)
    email = db.Column(db.Text)
    role = db.Column(db.Text)
    phone = db.Column(db.Integer)

    def user_dict(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "age": self.age,
                "email": self.email,
                "role": self.role,
                "phone": self.phone}


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.Text)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def order_dict(self):
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "address": self.address,
                "price": self.price,
                "customer_id": self.customer_id,
                "executor_id": self.executor_id}


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def offer_dict(self):
        return {"id": self.id,
                "order_id": self.order_id,
                "executor_id": self.executor_id}