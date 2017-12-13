from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request

application= Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.TNOSGBCSI

@application.route("/addIncident",methods=['POST'])
def addIncident():
    print ('addIncident')
    try:
        print (request.json)
        # just persist the json data, which could be a STIX josn
        #db.Incidents.insert_one(request.json)
    
        json_data = request.json['incident']
        title = json_data['title']
        description = json_data['description']
        confidence = json_data['confidence']
        initial_compromise = json_data['initial_compromise']
        incident_discovery = json_data['incident_discovery']
        incident_reported = json_data['incident_reported']
        
        print (json_data)
        # NOTE: insert_one will fail if any fields values are empty!
        db.Incidents.insert_one({
            'title':title
            ,'description':description
            ,'confidence':confidence
            ,'initial_compromise':initial_compromise
            ,'incident_discovery':incident_discovery
            ,'incident_reported':incident_reported
            })
        
        return jsonify(status='OK',message='inserted successfully')
    except Exception as e: # python 3.x
        print (str(e))
        return jsonify(status='ERROR',message=str(e))

@application.route('/updateIncident',methods=['POST'])
def updateIncident():
    try:
        incidentInfo = request.json['incident']
        incidentId = incidentInfo['id']
        title = incidentInfo['title']
        description = incidentInfo['description']
        confidence = incidentInfo['confidence']
        initial_compromise = incidentInfo['initial_compromise']
        incident_discovery = incidentInfo['incident_discovery']
        incident_reported = incidentInfo['incident_reported']
        
        #db.Machines.update_one({'_id':ObjectId(machineId)},{'$set':{'device':device,'ip':ip,'username':username,'password':password,'port':port}})
        db.Incidents.update_one({
            '_id':ObjectId(incidentId)}
            ,{'$set':{
                'title':title
                ,'description':description
                ,'confidence':confidence
                ,'initial_compromise':initial_compromise
                ,'incident_discovery':incident_discovery
                ,'incident_reported':incident_reported}})
        return jsonify(status='OK',message='updated successfully')
    except Exception as e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/deleteIncident",methods=['POST'])
def deleteIncident():
    try:
        incidentId = request.json['id']
        db.Incidents.remove({'_id':ObjectId(incidentId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception as e:
        return jsonify(status='ERROR',message=str(e))
              
@application.route('/getIncident',methods=['POST'])
def getIncident():
    try:
        incidentId = request.json['id']
        incident = db.Incidents.find_one({'_id':ObjectId(incidentId)})
        incidentDetail = {
                'title':incident['title'],
                'description':incident['description'],
                'confidence':incident['confidence'],
                'initial_compromise':incident['initial_compromise'],
                'incident_discovery':incident['incident_discovery'],
                'incident_reported':str(incident['incident_reported'])
                }
        return json.dumps(incidentDetail)
    except Exception as e:
        return str(e)
        
@application.route("/getIncidentList",methods=['POST'])
def getIncidentList():
    try:
        incidents = db.Incidents.find()
        
        incidentList = []
        for incident in incidents:
            print (incident) # python 3.x
            item = {
                    'title':incident['title']
                    ,'description':incident['description']
                    ,'confidence':incident['confidence']
                    ,'initial_compromise':str(incident['initial_compromise'])
                    ,'incident_discovery':str(incident['incident_discovery'])
                    ,'incident_reported':str(incident['incident_reported'])
                    ,'id': str(incident['_id']) # IMPORTANT: the KEY
                    }
            incidentList.append(item)

    except Exception as e:
        return str(e)
    return json.dumps(incidentList)

@application.route('/')
def showIncidentList():
    return render_template('list.html')
    
if __name__ == "__main__":
    application.run(host='0.0.0.0')
    


