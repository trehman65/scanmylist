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
            try:
                if item['product'] != '':
                    wrt.writerow([item['input'], item['product'], item['quantity']])
                else:
                    wrt.writerow([item['input']])
            except:
                pass
