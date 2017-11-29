import os
import csv
import json

total = 0
correct = 0
count=0

fp=0
fn=0
tp=0
tn=0

files = [f for f in os.listdir('TestData') if f.endswith('_nltk.json')]


for test_file in files:
	count=count+1

	print('File: '+test_file)
	gt_file = test_file + '.csv'
	with open('TestData/'+test_file) as fx:
		temp_data = json.load(fx)
		temp_data = temp_data['ie_result']['lines']
		test_data = []
		for row in temp_data:
			test_data.append([row['input'], row['product'], row['quantity']])
	with open('TestData/'+gt_file) as fx:
		gt_data = []
		for row in csv.reader(fx):
			if len(row) == 0:
				row = ['','','']
			if len(row) == 1:
				row = [row[0], '', '']
			if len(row) == 2:
				row = [row[0], row[1], '']
			gt_data.append(row)
	if len(test_data) != len(gt_data):
		print('Cant compare file: '+test_file)
		continue
	tot = 0
	cor = 0
	for i in range(len(test_data)):
		test = test_data[i]
		gt = gt_data[i]
		total += 1
		tot += 1
		
		if len(test[1]) !=0 and len(gt[1])==0:
			fp += 1

		if len(test[1]) ==0 and len(gt[1]) !=0:
			fn += 1
		
		if len(test[1]) ==0 and len(gt[1])==0:
			tn += 1

		if len(test[1]) !=0 and len(gt[1]) !=0:
			tp += 1
		if test[2] == gt[2] and test[1] == gt[1]:
			correct += 1
			cor += 1
	print('\tAccuracy: ', 100*cor/tot)

print "\n ANALYTICS"
print "Total Files: ",count
print'Final Accuray: ', 100*correct/total
print "True Negative: ",100*tn/total
print "True positive ",100*tp/total
print "False Negative: ",100*fn/total
print "False positive ",100*fp/total

	
