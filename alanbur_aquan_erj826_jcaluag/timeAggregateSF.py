"""
CS591
Project 2
11.2.17
timeAggregateSF.py
"""

import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import requests

class timeAggregateSF(dml.Algorithm):
    contributor = 'alanbur_aquan_erj826_jcaluag'
    reads = ['alanbur_aquan_erj826_jcaluag.SFaccidents']
    writes = ['alanbur_aquan_erj826_jcaluag.timeAggregateSF']

    @staticmethod
    def execute(trial = False):
        '''Retrieve crime incident report information from Boston.'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo

        repo.authenticate('alanbur_aquan_erj826_jcaluag', 'alanbur_aquan_erj826_jcaluag')          

        collection = repo.alanbur_aquan_erj826_jcaluag.SFaccidents

        repo.dropCollection("alanbur_aquan_erj826_jcaluag.timeAggregateSF")
        repo.createCollection("alanbur_aquan_erj826_jcaluag.timeAggregateSF")


        bins = [0 for i in range(24)]

        for entry in collection.find():
            hour = int(entry["time"][0:entry["time"].index(":")])
            bins[hour] += 1
        print(bins)


        repo['alanbur_aquan_erj826_jcaluag.timeAggregateSF'].insert({'data':bins}, check_keys=False)

        repo['alanbur_aquan_erj826_jcaluag.timeAggregateSF'].metadata({'complete':True})
        print(repo['alanbur_aquan_erj826_jcaluag.timeAggregateSF'].metadata())

        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}

    @staticmethod

    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('alanbur_aquan_erj826_jcaluag', 'alanbur_aquan_erj826_jcaluag')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        #resources:
        
        #define the agent
        this_script = doc.agent('alg:alanbur_aquan_erj826_jcaluag#timeAggregateSF', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        #define the input resource
        resource = doc.entity('dat:SFaccidents', {'prov:label':'SF Parsed Data', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        #define the activity of taking in the resource
        action = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(action, this_script)
        doc.usage(action, resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Computation'
                  }
                  )
        
        
        #define the writeout 
        output = doc.entity('dat:alanbur_aquan_erj826_jcaluag#timeAggregateSF', {prov.model.PROV_LABEL:'SF Time Aggregated Data', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(output, this_script)
        doc.wasGeneratedBy(output, action, endTime)
        doc.wasDerivedFrom(output, resource, action, action, action)

        repo.logout()
                  
        return doc

# timeAggregateSF.execute()

## eof
