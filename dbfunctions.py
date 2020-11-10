import os,json
def updateDatabase(db):
  if(len(db)>300):
    remove_n_minimums(db,100)
  #shamelessly copied from stackoverflow
  if os.path.exists('database.json'):
    with open('database.json', 'r+') as f:
         f.seek(0)
         f.truncate()
         json.dump(db, f)
  #check if cache is full  
def remove_n_minimums(dictionary, amountToRemove):
    for _ in range(n):
        filePathWithLowPop = min(d.keys(), key=lambda k: d[k])
        os.remove(filePathWithLowPop)
        del d[filePathWithLowPop]
    
def createfile(endpoint,param,data):
  currentfolder = ""
  for folder in endpoint:
    currentfolder+=folder+"/"
    if(not os.path.exists(currentfolder)):
      os.mkdir(currentfolder)
  filepath = generateFilePath(endpoint,param)
  newfile = open("{}.json".format(filepath),'w')
  newfile.write(data)
  newfile.close()

def generateFilePath(endpoint,param):
  path = ""
  for i in endpoint:
    path+=i+"/"
  return path+param
