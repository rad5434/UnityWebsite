from flask import Flask,render_template, request, jsonify
import json,ast
from flask_pymongo import PyMongo
from random import *
from pymongo import MongoClient

app=Flask(__name__)
@app.route('/')
def hello():
    return "This is Unity database ec2 instance"

#waaa has the results data
app.config['MONGO_DBNAME'] = 'caaaa'
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = 27017

app.config['MONGO2_DBNAME'] = 'baaaa'
app.config['MONGO2_HOST'] = '127.0.0.1'
app.config['MONGO2_PORT'] = 27017

mongo = PyMongo(app, config_prefix='MONGO')
mongo2 = PyMongo(app, config_prefix='MONGO2')

count=0
#cdbb actual data is stored



@app.route('/data', methods=['GET'])
def get_all_datas():
    data = mongo.db.data
    output = []
    for s in data.find():
        #s.pop('_id')
        print s
        output.append(s['num'])
        #{'vector' : s['vector']}
    #output=output.encode("ascii", "replace")
    output = json.dumps(output)
    output = json.loads(output)
    #type(loaded_r)  # Output dict
    print "Getting " + str(output[0])
    #print "Type: "+ str(type(output))
    return jsonify(output[0])

@app.route('/sketches', methods=['GET'])
def get_all_sketches():
    data = mongo2.db.data
    output = []
    for s in data.find():
        #s.pop('_id')
        print s
        output.append(s['vector'])
        #{'vector' : s['vector']}
    #output=output.encode("ascii", "replace")
    output = json.dumps(output)
    output = json.loads(output)
    #type(loaded_r)  # Output dict
    print "Getting " + str(output)
    #print "Type: "+ str(type(output))
    return jsonify({"results":output})


@app.route('/sketches/<int:count>', methods=['GET'])
def get_all_sketche(count):
    print "got here"
    data = mongo2.db.data
    output = []
    for s in data.find():
        # s.pop('_id')
        print s
        output.append(s['vector'])

    #output={'results': output}
    output = json.dumps(output)
    output = json.loads(output)
    print "Getting " + str(output)
    #print "The first one:" + str(output[0])
    return jsonify(output[count])


'''@app.route('/data/<int:count>', methods=['GET'])
def get_all_data(count):
    data = mongo.db.data
    output = []
    for s in data.find():
        # s.pop('_id')
        output.append(s['vector'])

    #output={'results': output}
    output = json.dumps(output)
    output = json.loads(output)
    print "Getting " + str(output)
    #print "The first one:" + str(output[0])
    return jsonify(output[count])

@app.route('/data/<int:count>', methods=['GET'])
def get_one_data(count):
    data = mongo.db.data
    output=[]
    for s in data.find():
        # s.pop('_id')
        output.append(s['vector'])
    #print output
    print data.find_one({"vector":{"id":count}})
    s = data.find_one({'_id':count})
    if s:
        output = { 'check': s['check'],'id': s['id'],'x_data': s['x_data'],'y_data': s['y_data']}
    else:
        output = "No such name"
    return jsonify({'data': output})'''


'''@app.route('/data/<int:count>', methods=['DELETE'])
def do_delete(count):
    data = mongo.db.data
    output = []
    for s in data.find():
        output.append(s['vector'])
        print (s['vector']['check'])

    output.remove(output[count])
    return jsonify(output)'''

@app.route('/sketches/<int:count>', methods=['PUT'])    #"""PUT"""
def update_task(count):
    print "\n\n PUT \n\n"
    data = mongo2.db.data
    reqdata = json.loads(request.data)
    vector = reqdata
    print vector
    postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
    #postall_id = data.insert({'vector': vector})
    print postall_id.matched_count
    new_postall = data.find_one({'_id': vector['id']})
    output = {'vector': new_postall['vector']}
    print "Posting " + str(output)
    return jsonify(output)
    #data = mongo.db.data
    # output = []
    # for s in mongo2.db.data.find():
    #     if s['vector']['id']==count:
    #         s['vector']['check']=5000
    #         output.append(s['vector'])

    # #print output[count]
    # return jsonify(output)

@app.route('/data', methods=['POST'])
def add_data():
    data = mongo.db.data
    #data.remove({})
    reqdata = json.loads(request.data)
    vector = reqdata['data']
    #myaxis=vector['axis']
    #num =  vector['num']
    print vector
    #print vector['num']
    #if vector['id'] ==0:
    data.remove({})
    postall_id = data.insert({'num':vector})
    #print postall_id
    new_postall = data.find_one({'_id': postall_id })
    #print new_postall
    output = {'num': new_postall['num']}
    print "Posting " + str(output)
    return jsonify({'data': output})

@app.route('/sketches', methods=['POST'])
def add_sketches():
    data = mongo2.db.data
    reqdata = json.loads(request.data)
    print reqdata
    vector = reqdata['results']
    print "\n\n\nhere we go\n\n\n"
    print vector
    print "\n\n\nthere we go\n\n\n"    
    #vector = vector['vector']
    print type(vector)
    #vector = json.loads(vector)
    index=0
    datastored=[]
    print "Length of vect list" + str(len(vector))
    while index < len(vector):
        #vector={'data': vector[index]}
        print "my Vector \n\n\n" + str(vector[index]) + "\n\n\n"
        #vector = vector['data']
        #myaxis=vector['axis']
        print vector[index]['id']
        print 
        try:
            postall_id = data.insert({'_id':vector[index]['id'],'vector': vector[index]})
        except:
            postall_id = data.update_one({'_id': vector[index]['id']}, {'$set': {'vector': vector[index]}})
        print postall_id
        new_postall = data.find_one({'_id': vector[index]['id'] })
        print new_postall
        output = {'vector': new_postall['vector']}
        datastored.append(output)
        index+=1
    return jsonify(datastored)


@app.route('/sketches/<int:count>', methods=['POST'])
def change_data(count):
    print "Posting in post"
    data = mongo2.db.data
    reqdata = request.data
    print reqdata
    print type(reqdata)
    if reqdata:
        print "Python"
        reqdata = json.loads(request.data)
        vector = reqdata['data']
        postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
        print postall_id.matched_count
        new_postall = data.find_one({'_id': vector['id']})
        print new_postall
        output = {'vector': new_postall['vector']}
        print "Posting " + str(output)
        return jsonify({'data': output})
    else:
        # print myDict
        # reqdata = json.loads(request.form)
        print "Unity"
        reqdata = dict(request.form)
        #reqdata={"data":reqdata}
        print "req data"
        print reqdata
        vector = reqdata['data']
        print "vector"
        # vector=dict(vector[0])
        vector = json.loads(vector[0])
        print vector
        postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
        print postall_id.matched_count
        new_postall = data.find_one({'_id': vector['id']})
        print new_postall
        output = {'vector': new_postall['vector']}
        print "Posting " + str(output)
        return jsonify({'data': output})

'''@app.route('/data/<int:count>', methods=['POST'])
def change_data(count):
    print "Posting in post"
    #mongo.db.user.remove({})
    data = mongo.db.data
    #data.remove({})
    reqdata = request.data
    print type(reqdata)
    if reqdata:
        print "Python"
        reqdata = json.loads(request.data)
        vector = reqdata['data']
        postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
        print postall_id.matched_count
        new_postall = data.find_one({'_id': vector['id']})
        print new_postall
        output = {'vector': new_postall['vector']}
        print "Posting " + str(output)
        return jsonify({'data': output})
    else:
        # print myDict
        # reqdata = json.loads(request.form)
        print "Unity"
        reqdata = dict(request.form)
        print "req data"
        print reqdata
        vector = reqdata['data']
        print "vector"
        # vector=dict(vector[0])
        vector = json.loads(vector[0])
        print vector
        postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
        print postall_id.matched_count
        new_postall = data.find_one({'_id': vector['id']})
        print new_postall
        output = {'vector': new_postall['vector']}
        print "Posting " + str(output)
        return jsonify({'data': output})

@app.route('/data/<int:count>', methods=['POST'])
def change_data(count):
    data = mongo.db.data
    reqdata = json.loads(request.data)
    vector = reqdata['data']
    postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
    print postall_id.matched_count
    new_postall = data.find_one({'_id': vector['id']})
    print new_postall
    output = {'vector': new_postall['vector']}
    print "Posting " + str(output)
    return jsonify({'data': output})'''



'''@app.route('/data', methods=['POST'])
def add_data(name):
    data = mongo.db.data
    vector = request.json['results']
    name = randint(1,100)
    #print "Hello World" + str(vector)
    lists=[]
    #for s in vector:
        #print s
        #lists.append(s)
    #print "List: "+str(lists)
    #print "Vector: " + str(vector)
    postall_id = data.insert({'vector': vector,'name':name})
    new_postall = data.find_one({'_id': postall_id })
    output = {'vector': new_postall['vector'],'name':new_postall['name']}
    print "Posting " + str(output)
    return jsonify(output)'''

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=80)

