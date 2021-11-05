from flask import Flask, request, jsonify;
from flask_sqlalchemy import SQLAlchemy ;
from flask_marshmallow import Marshmallow ; 
from flask_cors import CORS ;
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    host = db.Column(db.String )
    post = db.Column(db.String )
    postType = db.Column(db.String)
    description = db.Column(db.String)

    def __init__(self, host, post, postType, description, key ):
        self.host = host
        self.post = post
        self.postType = postType
        self.description = description
        self.key=key
        
class ItemSchema(ma.Schema):
    class Meta:
        fields = ("id", "key", "host", "post", "postType", "description",)

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@app.route("/item/add", methods=["POST"])
def add_item():
    host = request.json.get("host")
    post = request.json.get("post")
    key = request.json.get("key")
    postType = request.json.get("postType")
    description = request.json.get("description")

    record = Item(host, post, postType, description,key)
    db.session.add(record)
    db.session.commit()

    return jsonify(item_schema.dump(record))

@app.route("/item/get", methods=["GET"])
def get_all_items():
    all_items = Item.query.all()
    return jsonify(items_schema.dump(all_items))


if __name__ == "__main__":
    app.run(debug=True)