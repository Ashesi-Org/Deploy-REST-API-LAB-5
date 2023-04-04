
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore


# cred = credentials.Certificate("./venv/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

# db=firestore.client()
# import json
# from flask import Flask, request, jsonify

# #Add documents

# data = {'name':'Jane Does', 'age':34, 'employed': False}
# studentVoter_Firestorage = db.collection('studentVoter')
# studentVoter_Firestorage.add(data)




# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def query_records():
#     name = request.args.get('name')
#     print(name)
#     with open('./tmp/data.txt', 'r') as f:
#         data = f.read()
#         records = json.loads(data)
#         for record in records:
#             if record['name'] == name:
#                 return jsonify(record)
#         return jsonify({'error': 'data not found'}), 404

# @app.route('/', methods=['PUT'])
# def create_record():
#     record = json.loads(request.data)
#     with open('./tmp/data.txt', 'r') as f:
#         data = f.read()
#     if not data:
#         records = [record]
#     else:
#         records = json.loads(data)
#         records.append(record)
#     with open('./tmp/data.txt', 'w') as f:
#         f.write(json.dumps(records, indent=2))
#     return jsonify(record)

# @app.route('/', methods=['POST'])
# def update_record():
#     record = json.loads(request.data)
#     new_records = []
#     with open('./tmp/data.txt', 'r') as f:
#         data = f.read()
#         records = json.loads(data)
#     for r in records:
#         if r['name'] == record['name']:
#             r['email'] = record['email']
#         new_records.append(r)
#     with open('./tmp/data.txt', 'w') as f:
#         f.write(json.dumps(new_records, indent=2))
#     return jsonify(record)
    
# @app.route('/', methods=['DELETE'])
# def delte_record():
#     record = json.loads(request.data)
#     new_records = []
#     with open('./tmp/data.txt', 'r') as f:
#         data = f.read()
#         records = json.loads(data)
#         for r in records:
#             if r['name'] == record['name']:
#                 continue
#             new_records.append(r)
#     with open('./tmp/data.txt', 'w') as f:
#         f.write(json.dumps(new_records, indent=2))
#     return jsonify(record)

# app.run(debug=True)



""" import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("./venv/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

from flask import Flask, request, jsonify
import json

app = Flask(__name__)



# Registering a student as a voter
@app.route('/registerStudentVoter', methods=['PUT'])
def register_voter():
    voter_data = request.get_json()
    studentVoter_Firestorage = db.collection('studentVoter')
    studentVoter_Firestorage.add(voter_data)
    # validate voter data here
    with open('studentVoters.txt', 'a') as f:
        json.dump(voter_data, f)
        f.write('\n')
    return jsonify({'message': 'Voter registered successfully. '})

# De-registering a student as a voter
@app.route('/deregisterVoter/<voterID>', methods=['DELETE'])
def deregister_voter(voterID):
    # delete voter data with voterID
    return jsonify({'message': 'Voter de-registered successfully'})

# Updating a registered voter's information
@app.route('/update/<voterID>', methods=['POST'])
def update_voter(voterID):
    updated_data = request.get_json()
    # validate updated data here
    # update voter data with student_id
    return jsonify({'message': 'Voter updated successfully'})

# Retrieving a registered voter
@app.route('/getVoterInfo/<voterID>', methods=['GET'])
def get_voter(voterID):
    
# def query_records():
    voterID = request.args.get('voterID')
    print(voterID)
    with open('studentVoter_Firestorage', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for record in records:
            if record['voterID'] == voterID:
                return jsonify(record)
        return jsonify({'error': 'data not found'}), 404
    # get voter data with voterID
    return jsonify({'message': 'Voter retrieved successfully', 'data': voter_data})

# Creating an election
@app.route('/createElection', methods=['PUT'])
def create_election():
    election_data = request.get_json()
    studentElections_Firestorage = db.collection('studentElections')
    studentElections_Firestorage.add(election_data)
    # validate election data here
    with open('elections.txt', 'a') as f:
        json.dump(election_data, f)
        f.write('\n')
    return jsonify({'message': 'Election created successfully',
                    })

# Retrieving an election (with its details)
@app.route('/getElectionDetails/<id>', methods=['GET'])
def get_election(id):
    # get election data with election_id
    return jsonify({'message': 'Election retrieved successfully'})

# Deleting an election
@app.route('/election/<id>', methods=['DELETE'])
def delete_election(id):
    # delete election data with election_id
    return jsonify({'message': 'Election deleted successfully'})

# Voting in an election
@app.route('/vote/<id>', methods=['POST'])
def vote(id):
    vote_data = request.get_json()
    electionVotes_Firestorage = db.collection('electionVotes')
    electionVotes_Firestorage.add(vote_data)
    # validate vote data here
    # add vote to election data with election_id
    return jsonify({'message': 'Vote cast successfully'})


    
app.run(debug=True)"""


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from flask import Flask, request, jsonify

# initialize Firebase app
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Cloud Function entry point
def main(request):
    request_json = request.get_json()
    if request_json and 'action' in request_json:
        action = request_json['action']
        if action == 'register_voter':
            return register_voter(request_json)
        elif action == 'deregister_voter':
            return deregister_voter(request_json)
        elif action == 'update_voter':
            return update_voter(request_json)
        elif action == 'get_voter':
            return get_voter(request_json)
        elif action == 'create_election':
            return create_election(request_json)
        elif action == 'get_election':
            return get_election(request_json)
        elif action == 'delete_election':
            return delete_election(request_json)
        elif action == 'vote':
            return vote(request_json)
        else:
            return 'Invalid action'
    else:
        return 'Invalid request'

# Registering a student as a voter
def register_voter(request_json):
    voter_data = request_json['voter_data']
    studentVoter_Firestorage = db.collection('studentVoter')
    studentVoter_Firestorage.add(voter_data)
    # validate voter data here
    with open('studentVoters.txt', 'a') as f:
        json.dump(voter_data, f)
        f.write('\n')
    return {'message': 'Voter registered successfully'}

# De-registering a student as a voter
def deregister_voter(request_json):
    voterID = request_json['voterID']
    # delete voter data with voterID
    return {'message': 'Voter de-registered successfully'}

# Updating a registered voter's information
def update_voter(request_json):
    voterID = request_json['voterID']
    updated_data = request_json['updated_data']
    # validate updated data here
    # update voter data with student_id
    return {'message': 'Voter updated successfully'}

# Retrieving a registered voter
def get_voter(request_json):
    voterID = request_json['voterID']
    voter_ref = db.collection('studentVoter').where('voterID', '==', voterID).get()
    if len(voter_ref) > 0:
        return jsonify(voter_ref[0].to_dict())
    else:
        return {'error': 'Voter not found'}

# Creating an election
def create_election(request_json):
    election_data = request_json['election_data']
    studentElections_Firestorage = db.collection('studentElections')
    studentElections_Firestorage.add(election_data)
    # validate election data here
    with open('elections.txt', 'a') as f:
        json.dump(election_data, f)
        f.write('\n')
    return {'message': 'Election created successfully'}

# Retrieving an election (with its details)
def get_election(request_json):
    election_id = request_json['election_id']
    election_ref = db.collection('studentElections').document(election_id).get()
    if election_ref.exists:
        return jsonify(election_ref.to_dict())
    else:
        return {'error': 'Election not found'}

# Deleting an election
def delete_election(request_json):
    election_id = request_json['election_id']
    return jsonify({'message' 'Election deleted successfully'})






