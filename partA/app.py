from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from db import db, Fan


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # write your db location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)




# Create the database tables and insert some data into the database
with app.app_context():
    db.create_all()

    # Insert sample data into the database
    sample_data = [
        {"code": "SBK07", "brand": "AirPro Fan", "fan_type": "CENTRIFUGAL FAN"},
        {"code": "SBK08", "brand": "Cincinnati Fan", "fan_type": "CENTRIFUGAL FAN"},
        {"code": "SBK09", "brand": "New York Fan", "fan_type": "CENTRIFUGAL FAN"},
        {"code": "SBK10", "brand": "Calcutta Fan", "fan_type": "CENTRIFUGAL FAN"},
        {"code": "SBK12", "brand": "AirPro Fan", "fan_type": "AXIAL FAN"},
        {"code": "SBK13", "brand": "Cincinnati Fan", "fan_type": "AXIAL FAN"},
        {"code": "SBK14", "brand": "New York Fan", "fan_type": "AXIAL FAN"},
        {"code": "SBK15", "brand": "Calcutta Fan", "fan_type": "AXIAL FAN"},
        {"code": "SBK16", "brand": "AirPro Fan", "fan_type": "JET FAN"},
        {"code": "SBK17", "brand": "Cincinnati Fan", "fan_type": "JET FAN"},
        {"code": "SBK18A", "brand": "New York Fan", "fan_type": "JET FAN"},
    ]

    for data in sample_data:
        fan = Fan(code=data['code'], brand=data['brand'], fan_type=data['fan_type'])
        db.session.add(fan)

    db.session.commit()



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

if __name__ == '__main__':
    app.run(debug=True)