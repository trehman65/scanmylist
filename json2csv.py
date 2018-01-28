import json
import csv
import os

for filename in os.listdir('nltk-out'):
    print(filename)
    with open('nltk-out/'+filename, 'r') as f:
        data = json.load(f)
    with open('csv-out/'+filename+'.csv', 'w') as f:
        wrt = csv.writer(f)
        for item in data['ie_result']['lines']:

            if item['product'] != '':
                
                tags=""
                
                if len(item['tags']) != 0:
                    for tag in item['tags']:
                        tags = tags+tag+','
                    tags=tags.rstrip(',')
    
                wrt.writerow([item['input'].encode('utf-8'), item['product'].encode('utf-8'), item['quantity'].encode('utf-8'),tags])
            else:
                wrt.writerow([item['input'].encode('utf-8')])
    