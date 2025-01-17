import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import numpy as np

class schoolsAgg(dml.Algorithm):
    contributor = 'carole07_echanglc_wongi'
    reads = ['carole07_echanglc_wongi.schools']
    writes = ['carole07_echanglc_wongi.schoolsAgg']
    
    
    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('carole07_echanglc_wongi', 'carole07_echanglc_wongi')

        repo.dropPermanent("schoolsAgg")
        repo.createPermanent("schoolsAgg")

        zipCount= []
        for entry in repo.carole07_echanglc_wongi.schools.find():
            for entry2 in entry["fields"]:
                if "zipcode" in entry2:
                    zipcode = entry2["zipcode"]
                    zipCount += [(zipcode, 1)]
    
        #Aggregate transformation for zipCount
                
        keys = {r[0] for r in zipCount}
        aggregate_val= [(key, sum([v for (k,v) in zipCount if k == key])) for key in keys]

        final= []
        for entry in aggregate_val:
            final.append({'schoolsZipcode:':entry[0], 'schoolsCount':entry[1]})

        repo['carole07_echanglc_wongi.schoolsAgg'].insert_many(final)
        
        for entry in repo.carole07_echanglc_wongi.schoolsAgg.find():
             print(entry)
             
        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}

    @staticmethod
    def execute(trial = True):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()
        
        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('carole07_echanglc_wongi', 'carole07_echanglc_wongi')
        
        repo.dropPermanent("schoolsAgg")
        repo.createPermanent("schoolsAgg")
        
        repo.dropPermanent("schoolsAgg")
        repo.createPermanent("schoolsAgg")
        
        schools = repo.carole07_echanglc_wongi.schools.find()
        zipcodes = [s['fields']['zipcode'] for s in schools]
        zipCount = [(zip , 1) for zip in zipcodes]
        
        #Aggregate transformation for zipCount
        
        keys = {r[0] for r in zipCount}
        aggregate_val= [(key, sum([v for (k,v) in zipCount if k == key])) for key in keys]
        
        final= []
        for entry in aggregate_val:
            final.append({'schoolsZipcode:':entry[0], 'schoolsCount':entry[1]})
                
        repo['carole07_echanglc_wongi.schoolsAgg'].insert_many(final)
                    
        for entry in repo.carole07_echanglc_wongi.schoolsAgg.find():
            print(entry)
                            
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
        repo.authenticate('carole07_echanglc_wongi', 'carole07_echanglc_wongi')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
        doc.add_namespace('bdp1', 'https://data.nlc.org/resource/')
        doc.add_namespace('bdp2', 'https://data.boston.gov/export/622/208/')

        this_script = doc.agent('alg:carole07_echanglc_wongi#schoolsAgg', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        resource_properties = doc.entity('dat:carole07_echanglc_wongi#schools', {'prov:label':' Schools Aggregate Zips', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        get_schoolsAgg = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(get_schoolsAgg, this_script)
        doc.usage(get_schoolsAgg, resource_properties, startTime,None,
                  {prov.model.PROV_TYPE:'ont:Computation'})


        schoolsAgg = doc.entity('dat:carole07_echanglc_wongi#schoolsAgg', {prov.model.PROV_LABEL:' Schools Aggregate Zips', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(schoolsAgg, this_script)
        doc.wasGeneratedBy(schoolsAgg, get_schoolsAgg, endTime)
        doc.wasDerivedFrom(schoolsAgg, resource_properties, get_schoolsAgg, get_schoolsAgg, get_schoolsAgg)



        repo.logout()
                  
        return doc

