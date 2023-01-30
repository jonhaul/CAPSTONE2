from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
# import os

app = Flask(__name__)
CORS(app)

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ocrtltiumojrsv:907f40e2749ef444270accfb2dc5390c204a74e64f543e022e9719a67d29a8cc@ec2-34-231-63-30.compute-1.amazonaws.com:5432/d406s5j0hs462c'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Pix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False)
    content = db.Column(db.String, unique=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

class PixSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content')

pix_schema = PixSchema()
pics_schema = PixSchema(many=True)


@app.route('/pix/add', methods=["POST"])
def add_pic():
    if request.content_type != 'application/json':
        return jsonify("Data needs to be sent as JSON")   
    
    post_data = request.get_json()
    title = post_data.get('title')
    content = post_data.get('content')

    new_pix = Pix(title, content)

    db.session.add(new_pix)
    db.session.commit()

    return jsonify(pix_schema.dump(new_pix))
    
@app.route('/pix/get')
def get_pics():
    all_pics = db.session.query(Pix).all()
    return jsonify(pics_schema.dump(all_pics))

@app.route('/pix/get/<id>')
def get_one_pic(id):
    one_pic = db.session.query(Pix).filter(Pix.id == id).first()
    return jsonify(pix_schema.dump(one_pic))

@app.route('/pix/edit/<id>', methods=["PUT"])
def edit_pic(id):
    if request.content_type != 'application/json':
        return jsonify('Error: send data as JSON')
    
    put_data = request.get_json()
    title = put_data.get('title')
    content = put_data.get('content')

    edit_pic = db.session.query(Pix).filter(Pix.id == id).first()

    if title != None:
        edit_pic.title = title
    if content != None:
        edit_pic.content = content
    
    db.session.commit()

    return jsonify(pix_schema.dump(edit_pic))

@app.route('/pix/delete/<id>', methods=["DELETE"])
def delete_pic(id):
    delete_pic = db.session.query(Pix).filter(Pix.id == id).first()
    db.session.delete(delete_pic)
    db.session.commit()

    return jsonify('picture is GONE')

if __name__ == '__main__':
    app.run(debug=True)
