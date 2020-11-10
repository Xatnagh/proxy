from flask import Flask,jsonify,request,render_template_string
import json
import requests
import os
# import urllib.parse as urlparse
# from urllib.parse import parse_qs

from dbfunctions import updateDatabase,createfile,generateFilePath
app = Flask(__name__)

const_cashe_limit = 300

#explanation: I am using hashmap to store all the api calls and their popularity(so I get get rid of the least popular ones the moment the cashe limit is reached), I will store the result of the api calls in files 
db = json.load(open("database.json"))

@app.route('/get/<path:path>', defaults={'path': ''})
def Get(path):
  parsed_url=request.url.split('get/')[1]
  endpoint= parsed_url.split('?')[0].split('/')
  params = parsed_url.split('?')[1] if len( parsed_url.split('?'))>1 else ""
  print("endpoint", endpoint)
  print("params", params)
  filepath = generateFilePath(endpoint,params)
  realPath = filepath+".json"
  if(os.path.exists(realPath)):
    db[filepath]+=1 #increase popularity
    print("FILE DOES EXIST")
    updateDatabase(db)
    return jsonify(json.load(open(realPath)))
  response = requests.get("http://api.tvmaze.com/"+parsed_url)
  if(response):
    print("FILE DOESn't EXIST")
    createfile(endpoint,params,response.text)
    db[filepath]=1
    updateDatabase(db)
    return jsonify(response.text)
  return "hi,testing"
@app.route('/pop')
def popularity():
  return jsonify(db)
@app.route('/')
def home():

  return render_template_string("""This is a TVMaze proxy, to use it, take a regular TVMAZE api get call, example: http://api.tvmaze.com/schedule?country=US&date=2014-12-01, shave off the 'http://api.tvmaze.com/' and use 'http://localhost:5000/get/' in its place 
  <br>
  <br>Example: TV Maze api call: http://api.tvmaze.com/schedule?country=US&date=2014-12-01
  <br>
  <br>My proxy: http://localhost:5000/get/schedule?country=US&date=2014-12-01
 <br>
  <br>P.S: if you do http://localhost:5000/popularity, you will get the unsorted version of the popularity of what is in cache so far!(if you want the sorted version extra credits must be given as incentive)
  """)

app.run(host="0.0.0.0",debug=True)