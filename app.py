#!/usr/bin/env python

import logging
from sqlalchemy.exc import IntegrityError
from models import Route, User

__author__ = 'lorenamesa'

from flask import Flask, request, jsonify
import records
from sqlalchemy import create_engine


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

db = records.Database("sqlite:////Users/lorenamesa/Desktop/pytennessee/pytennessee.db")
# engine = create_engine('sqlite:////Users/lorenamesa/Desktop/pytennessee/pytennessee.db')
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/users/", methods=['POST'])
def add_user():
    content = request.get_json(silent=True)
    user = User(**content.get('user'))
    try:
        db.query("INSERT INTO users " +
                 "(email, password) " +
                 "VALUES ('{0}', '{1}')".format(user.email,
                                               user.password))
    except IntegrityError as e:
        logger.info("User exists for {0}".format(user.email))
        return jsonify({"error": "Email {0} already has an user".format(user.email)})

    rows = db.query("SELECT seq FROM sqlite_sequence WHERE NAME = 'users'")
    user_id = rows.all()[0].get('seq', 0)

    created = db.query("SELECT * FROM users WHERE id = {0}".format(user_id))
    return jsonify(**created.all()[0])

@app.route("/<user_id>/routes/", methods=['POST'])
def add_route(user_id):
    route = Route(**request.form.get('route'))
    db.query("INSERT INTO routes " +
             "(time_start, time_stop, type, location, destination) " +
             "VALUES ({0}, {1}, '{2}', '{3}', '{4}')".format(route.time_start,
                                                             route.time_stop,
                                                             route.type,
                                                             route.location,
                                                             route.destination))

    rows = db.query("SELECT seq FROM sqlite_sequence WHERE NAME = 'routes' ")
    row = rows.all()[0]

    db.query("INSERT INTO routes_users " +
             "(user_id, route_id) " +
             "VALUES ({0}, {1})".format(user_id, row.get('id')))

    return jsonify(route.__dict__)

@app.route("/<user_id>/routes/", methods=['GET'])
def get_routes(user_id):
    rows = db.query("SELECT route_id FROM routes_users WHERE user_id = {0}".format(user_id))
    route_ids = rows.all()

    routes = db.query("SELECT * FROM routes WHERE id IN ({0})".format(",".join(id for id in route_ids)))

    routes = [Route(**route) for route in routes.all()]

    if routes:
        return jsonify({"routes": routes})

    return "Nothing here :-)"

if __name__ == "__main__":
    app.run()