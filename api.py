from flask import Flask, request, jsonify
from researchGate import findResearchGate
from googleAcademic import findGoogle
from database import queryDatabase, insertData, insertTest, replaceTest
from bson import json_util
import redis
from rq import Queue

app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)


# Consulta la base de datos, de no tener datos se hace el scrape
@app.route('/<string:name>')
def query_by_name(name):

    queryResult = queryDatabase(name)
    if(queryResult != None):
        return queryResult
    else:
        scrapeResults = {
            'research_gate' : findResearchGate(name),
            'google' : findGoogle(name)
        }

        insertedData = insertData(name, scrapeResults)
        
        return insertedData

# Consulta únicamente la base de datos
@app.route('/db/<string:name>')
def query(name):
    results = queryDatabase(name)
    if(results != None):
        print (results)
        return results
    else:
        return { 'error' : 'Sin resultados' }

# Realiza únicamente el scrape guardando o sobreescribiendo los datos de la base de datos
@app.route('/scrape/<string:name>')
def scrape(name):

    scrapeResults = {
        'research_gate' : findResearchGate(name),
        'google' : findGoogle(name)
    }

    insertedData = insertData(name, scrapeResults)
    
    return insertedData

# Testing
@app.route('/test/insert/<string:name>')
def testinsertendpoint(name):

    try:
        return insertTest(name)
        # return "Success"
    except:
        return "Fail"



# Testing
@app.route('/test/replace/<string:name>/<string:newname>')
def testreplaceendpoint(name,newname):

    try:
        return replaceTest(name, newname)
        # return "Success"
    except:
        return "Fail"

def scrapeQ(name):
    scrapeResults = {
        'research_gate' : findResearchGate(name),
        'google' : findGoogle(name)
    }

    insertedData = insertData(name, scrapeResults)

# Testing
@app.route('/test/scrape/<string:name>')
def testscrape(name):

    job = q.enqueue(scrapeQ, name)

    return {"success" : "please check back in a minute"}


if __name__ == "__main__":
    app.run(debug=True)