import json
import csv
import os

files = [f for f in os.listdir('TestData') if f.endswith('_nltk.json')]

for filename in files:
    
    print(filename)
    jsonfilename=filename.replace('.json','')

    with open('TestData/'+filename, 'r') as f:
        data = json.load(f)
    with open('TestData/'+jsonfilename+'.csv', 'w') as f:
    	wrt = csv.writer(f)
    	wrt.writerow(["Input","Product","Quantity","Tags","Comment"])
        
        for item in data['ie_result']['lines']:

            if item['Product'] != '':
                
                tags=""
                
                if len(item['Tags']) != 0:
                    for tag in item['Tags']:
                        tags = tags+tag+','
                    tags=tags.rstrip(',')
    
                wrt.writerow([item['input'].encode('utf-8'), item['Product'].encode('utf-8'), item['Quantity'].encode('utf-8'),tags,item['Comment'].encode('utf-8')])
            else:
                wrt.writerow([item['input'].encode('utf-8')])