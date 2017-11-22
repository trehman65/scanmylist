import os
import csv
import json

total = 0
correct = 0
count=0

for test_file in os.listdir('TestData'):
	count=count+1
	if test_file.endswith('.csv'):
		continue
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
		if test[2] == gt[2]:
			correct += 1
			cor += 1
	print('\tAccuracy: ', 100*cor/tot)
print('Final Accuray: ', 100*correct/total)
print "Total Files: ",count/2

print correct
print total

	
