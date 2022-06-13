import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'GET':
        """получения всех пользователей"""
        data = User.query.all()
        result = []
        for user in data:
            result.append(user.user_dict())
        return jsonify(result)
    elif request.method == 'POST':
        try:
            """создание пользователя"""
            data_ = json.loads(request.data)
            new_user = User(id=data_["id"],
                            first_name=data_["first_name"],
                            last_name=data_["last_name"],
                            age=data_["age"],
                            email=data_["email"],
                            role=data_["role"],
                            phone=data_["phone"])
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            return 'Пользователь создан в базе данных', 200
        except Exception as e:
            return e


@app.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def get_users_by_id(uid):
    if request.method == 'GET':
        """получение одного пользователя по идентификатору"""
        data = db.session.query(User).get(uid)
        if data is None:
            return 'Пользователь не найден', 404
        else:
            return jsonify(data.user_dict())
    elif request.method == 'PUT':
        """обновление одного пользователя по идентификатору"""
        data_load = json.loads(request.data)
        data = db.session.query(User).get(uid)
        if data is None:
            return 'Пользователь не найден', 404
        else:
            data.id = data_load["id"]
            data.first_name = data_load["first_name"]
            data.last_name = data_load["last_name"]
            data.age = data_load["age"]
            data.email = data_load["email"]
            data.role = data_load["role"]
            data.phone = data_load["phone"]
            db.session.add(data)
            db.session.commit()
            db.session.close()
            return f"Объект с id {uid} успешно изменён!", 200
    elif request.method == 'DELETE':
        """удаление одного пользователя по идентификатору"""
        data = db.session.query(User).get(uid)
        if data is None:
            return 'Пользователь не найден', 404
        else:
            db.session.delete(data)
            db.session.commit()
            return f"Объект с id {uid} удалён!", 200


@app.route('/orders', methods=['GET', 'POST'])
def get_all_orders():
    if request.method == 'GET':
        """получения всех заказов"""
        order = Order.query.all()
        if order is None:
            return 'Заказ не найден', 404
        else:
            result = []
            for order_ in order:
                result.append(order_.order_dict())
            return jsonify(result)

    elif request.method == 'POST':
        try:
            """создание нового заказа"""
            order_ = json.loads(request.data)
            month_start, day_start, year_start = [int(o) for o in order_['start_date'].split("/")]
            month_end, day_end, year_end = order_['end_date'].split("/")
            new_order = Order(
                id=order_["id"],
                name=order_["name"],
                description=order_["description"],
                start_date=datetime.date(year=year_start, month=month_start, day=day_start),
                end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
                address=order_["address"],
                price=order_["price"],
                customer_id=order_["customer_id"],
                executor_id=order_["executor_id"])
            db.session.add(new_order)
            db.session.commit()
            db.session.close()
            return 'Новый заказ создан в базе данных', 200
        except Exception as e:
            return e


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def get_orders_by_id(order_id):
    if request.method == 'GET':
        """получение одного заказа по идентификатору"""
        order_ = Order.query.get(order_id)
        if order_ is None:
            return 'Заказ не найден', 404
        else:
            return jsonify(order_.order_dict())
    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Заказ не найден!", 404
        month_start, day_start, year_start = [int(o) for o in order_data['start_date'].split("/")]
        month_end, day_end, year_end = order_data['end_date'].split("/")
        order.name = order_data["name"]
        order.description = order_data["description"]
        order.start_date = datetime.date(year=year_start, month=month_start, day=day_start)
        order.end_date = datetime.date(year=int(year_end), month=int(month_end), day=int(day_end))
        order.address = order_data["address"]
        order.price = order_data["price"]
        order.customer_id = order_data["customer_id"]
        order.executor_id = order_data["executor_id"]
        db.session.add(order)
        db.session.commit()
        db.session.close()

        return f"Заказ с id {order_id} успешно изменён!", 2

    elif request.method == 'DELETE':
        """удаление одного заказа по идентификатору"""
        data = db.session.query(Order).get(order_id)
        if data is None:
            return 'Заказ не найден', 404
        else:
            db.session.delete(data)
            db.session.commit()
            return f"Объект с id {order_id} удалён!", 20


@app.route('/offers', methods=['GET', 'POST'])
def get_all_offers():
    if request.method == 'GET':
        """получения всех предложений"""
        data = Offer.query.all()
        result = []
        for offer in data:
            result.append(offer.offer_dict())
        return jsonify(result)
    elif request.method == 'POST':
        try:
            offer = json.loads(request.data)
            new_offer = Offer(id=offer["id"],
                              order_id=offer["order_id"],
                              executor_id=offer["executor_id"])
            db.session.add(new_offer)
            db.session.commit()
            db.session.close()
            return 'Пользователь создан в базе данных', 200
        except Exception as e:
            return e


@app.route('/offers/<int:offer_id>',methods=['GET', 'PUT', 'DELETE'])
def get_offer_by_id(offer_id):
    if request.method == 'GET':
       """получение одного предложения по идентификатору"""
       data = Offer.query.get(offer_id)
       if data is None:
           return 'Пользователь не найден', 404
       else:
           return jsonify(data.offer_dict())
    elif request.method == 'PUT':
        """обновление одного предложения по идентификатору"""
        data_load = json.loads(request.data)
        data = db.session.query(Offer).get(offer_id)
        if data is None:
            return 'Пользователь не найден', 404
        else:
            data.id = data_load["id"]
            data.order_id = data_load["order_id"]
            data.executor_id = data_load["executor_id"]
            db.session.add(data)
            db.session.commit()
            db.session.close()

            return f"Объект с id {offer_id} успешно изменён!", 200
    elif request.method == 'DELETE':
        """удаление одного предложения по идентификатору"""
        data = db.session.query(Offer).get(offer_id)
        if data is None:
            return 'Пользователь не найден', 404
        else:
            db.session.delete(data)
            db.session.commit()
            return f"Объект с id {offer_id} удалён!", 200



if __name__ == '__main__':
    app.run(debug=True)
