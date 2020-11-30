from logging import log
import flask
from main import app, db, bcrypt,login_manager
from main.models import Coffee, User, Review, BEAN, EXTRACTION_METHOD, MESH
from main.utils import *
from flask_login import login_user, logout_user, login_required,current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/')
def helloworld():
    return 'Hello, World!'


@app.route('/', methods=['POST'])
def oumugaeshi():
    return flask.request.get_data(), 418


# user Create
@app.route('/auth/create_user/', methods=['POST'])
def create_user():
    form_data = flask.request.json
    username = form_data['username']
    password = form_data['password']
    # TODO:有効な文字列か確認。
    if not username:
        return flask.jsonify({"message": "ユーザー名は必須です"}), 400
    if not password:
        return flask.jsonify({"message": "パスワードは必須です"}), 400
    users = User.query.filter_by(name=username).all()
    if len(users) != 0:
        return flask.jsonify({"message": "ユーザー名が利用されています。"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name=username, encrypted_password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return flask.jsonify({"message": "ユーザー("+username+")を作成しました。"})
# user index TODO:
# user show
# user update


@app.route('/auth/login/', methods=['POST'])
def login():
    form_data = flask.request.json
    username = form_data['username']
    password = form_data['password']
    # TODO:有効な文字列か確認。
    if not username:
        return flask.jsonify({"message": "ユーザー名は必須です"}), 400
    if not password:
        return flask.jsonify({"message": "パスワードは必須です"}), 400
    user = User.query.filter_by(name=username).first()
    if user and bcrypt.check_password_hash(user.encrypted_password, password):
        # ログイン成功
        login_user(user)
        print("ログイン成功")
        return flask.jsonify({"message": "ユーザー("+username+")のログインに成功しました。"})
    else:
        print("ログイン失敗")
        return flask.jsonify({"message": "ユーザー("+username+")のログインに失敗しました。"})

# coffee create


@app.route("/coffee/create/", methods=['POST'])
@login_required
def create_coffee():
    form_data = flask.request.json
    powder_amount = form_data["powder_amount"]
    extraction_time = form_data['extraction_time']
    extraction_method_id = form_data['extraction_method_id']
    mesh_id = form_data['mesh_id']
    water_amount = form_data['water_amount']
    water_temperature = form_data['water_temperature']
    bean_id = form_data['bean_id']
    dripper_id = current_user.id
    drinker_id = form_data['drinker_id']
    new_coffee = Coffee(powder_amount=powder_amount, extraction_time=extraction_time, extraction_method_id=extraction_method_id,
                        mesh_id=mesh_id, water_amount=water_amount, water_temperature=water_temperature, bean_id=bean_id, dripper_id=dripper_id, drinker_id=drinker_id)
    db.session.add(new_coffee)
    db.session.commit()
    return flask.jsonify({"message": "コーヒーを作成しました。"})
