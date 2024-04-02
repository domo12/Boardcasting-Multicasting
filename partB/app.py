from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from db import db, Fan

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/asg/fans', methods=['GET'])
def get_fans():
    fans = Fan.query.all()
    fan_list = [{'id': fan.id, 'code': fan.code, 'brand': fan.brand, 'type': fan.fan_type} for fan in fans]
    return jsonify({'fans': fan_list})

@app.route('/asg/fans/<int:id>', methods=['GET'])
def get_fan(id):
    fan = Fan.query.get(id)
    if fan is None:
        return jsonify({'error': 'Fan not found'}), 404
    return jsonify({'id': fan.id, 'code': fan.code, 'brand': fan.brand, 'type': fan.fan_type})

@app.route('/asg/fans', methods=['POST'])
def create_fan():
    data = request.json
    fan = Fan(code=data['code'], brand=data['brand'], fan_type=data['type'])
    db.session.add(fan)
    db.session.commit()
    return jsonify({'message': 'Fan created successfully'}), 201

@app.route('/asg/fans/<int:id>', methods=['PUT'])
def update_fan(id):
    fan = Fan.query.get(id)
    if fan is None:
        return jsonify({'error': 'Fan not found'}), 404
    
    data = request.json
    fan.code = data['code']
    fan.brand = data['brand']
    fan.fan_type = data['type']
    db.session.commit()
    return jsonify({'message': 'Fan updated successfully'})

@app.route('/asg/fans/<int:id>', methods=['DELETE'])
def delete_fan(id):
    fan = Fan.query.get(id)
    if fan is None:
        return jsonify({'error': 'Fan not found'}), 404
    db.session.delete(fan)
    db.session.commit()
    return jsonify({'message': 'Fan deleted successfully'})

@app.route('/asg')
def home_page():
    return 'Hello World'

################################################################
##Services
################################################################
#for testing purpose to clean the db
@app.route('/asg/clean-db', methods=['POST'])
def clean_database():
    try:
        # Delete all records from the Fan table
        Fan.query.delete()
        db.session.commit()
        return jsonify({'message': 'Database cleaned successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to clean the database', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
