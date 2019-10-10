import requests
from flask import jsonify, Flask, render_template, request

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('assignment1.html')

@app.route('/postingOrder', methods=['POST'])
def postingOrder():
    # html에서 넘어 오는 값
    # name_give: name, count_give: count, address_give: address, phone_give: phone, item_give: item
    request_field = ['name_give', 'count_give', 'address_give', 'phone_give', 'item_give']
    for field in request_field:
        if(field not in request.form):
            print('do not exist {} field value'.format(field))

    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']
    item_receive = request.form['item_give']

    order = {
        'name': name_receive,
        'count': count_receive,
        'address': address_receive,
        'phone': phone_receive,
        'item': item_receive
    }

    db.orders.insert_one(order)

    return jsonify({'result': 'success'})




@app.route('/listingOrder', methods=['GET'])
def listingOrder():
    item_recieve = request.args.get('item')

    # item_list = list(db.orders.find({'item':item_recieve}, {'_id':0}))

    if item_recieve is not None:
        find_condition = {'item': item_recieve}
    else:
        find_condition = {}

    item_list = list(db.orders.find(find_condition, {'_id': 0}))
    print(item_list)

    return jsonify({'result': 'success', 'orders': item_list})          # html 스크립스 상에서 response의 객체에서 orders로 접근을 한다고 원래 표기 되어있어서 api에서 고치던가
                                                                        # 아니면 html 스크립트 상에서 고쳐야함.


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)