# -*- coding: utf-8 -*-

import requests
import json
import numpy as np
import pandas as pd

def nppes (criteria):
    #number Exactly 10 digits
    number=criteria[0]
    #enumeration_type NPI-1 or NPI-2 (Other criteria required)
    enumeration_type=criteria[1]	
    #taxonomy_description Exact Description or Exact Specialty or wildcard * after 2 characters
    taxonomy_descprition=criteria[2]
    #first_name Exact name, or wildcard * after 2 character Use for type 1
    first_name=criteria[3]
    #last_name Exact name, or wildcard * after 2 characters	Use for type 1
    last_name=criteria[4]
    #organization_name Exact name, or wildcard * after 2 characters	Use for type 2
    organization_name=criteria[5]
    #address_purpose LOCATION or MAILING (Other criteria required)
    address_purpose=criteria[6]
    #city Exact Name
    city=criteria[7]
    #state 2 Characters (Other criteria required)
    state=criteria[8]
    #postal_code At least 2 characters, wildcard is implied
    postal_code=criteria[9]
    #country_code Exactly 2 characters (if "US", other criteria required)
    country_code=criteria[10]
    #limit Limit results, default = 10, max = 200
    limit=criteria[11]
    #skip Skip first N results, max = 1000
    skip=criteria[12]
    
    #Pull data from NPI registry
    URL=str('https://npiregistry.cms.hhs.gov/api/?number=%s&enumeration_type=%s&taxonomy_description=%s&first_name=%s&last_name=%s&organization_name=%s&address_purpose=%s&city=%s&state=%s&postal_code=%s&country_code=%s&limit=%s&skip=%s') %(number,enumeration_type,taxonomy_descprition,first_name,last_name,organization_name,address_purpose,city,state,postal_code,country_code,limit,skip)
    response = requests.get(URL)
    data = response.json()
    
    #Initialize final output data frames
    addresses=pd.DataFrame()
    identifiers=pd.DataFrame()
    other_names=pd.DataFrame()
    basic=pd.DataFrame()
    taxonomies=pd.DataFrame()
    
    #Loop through each result and pull data into data frames
    for i in range(data['result_count']):
        NPI=(data['results'][i]['number'])
        
        new_addresses=pd.DataFrame.from_dict(data['results'][i]['addresses'])
        new_identifiers=pd.DataFrame.from_dict(data['results'][i]['identifiers'])
        new_other_names=pd.DataFrame.from_dict(data['results'][i]['other_names'])
        new_basic=pd.DataFrame.from_dict([(data['results'][i]['basic'])])
        new_taxonomies=pd.DataFrame.from_dict(data['results'][i]['taxonomies'])
        
        new_addresses['NPI']=NPI
        new_identifiers['NPI']=NPI
        new_other_names['NPI']=NPI
        new_basic['NPI']=NPI
        new_taxonomies['NPI']=NPI
        
        addresses=addresses.append(new_addresses)
        identifiers=identifiers.append(new_identifiers)
        other_names=other_names.append(new_other_names)
        basic=basic.append(new_basic)
        taxonomies=taxonomies.append(new_taxonomies)
    
    result= pd.merge(pd.merge(pd.merge(addresses,taxonomies,on='NPI',how='inner') ,identifiers,on='NPI',how='inner'),basic,on='NPI',how='inner') 
    return result
    #created_epoch
    #last_updated_epoch
    #enumeration_type

NPI_file=open('/Users/user/Documents/API_NPI_Lookup.txt','r')
NPIs=NPI_file.readlines()
final=pd.DataFrame()
for i in NPIs:
    i=i.rstrip()
    criteria_inputs=[i,'','','','','','','','','','','','']
    result=nppes(criteria_inputs)
    final=final.append(result)
final.to_csv('/Users/user/Documents/NPIs_output.csv',index=False)