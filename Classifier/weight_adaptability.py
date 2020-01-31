import datetime
import math
import random

import Classifier.accuracy
import Classifier.storage
from Classifier.verifier_distance import Verifier_Distance

test_table_to_verification = {}
test_table_to_verification['scores']  = 'verification'
test_table_to_verification['test_scores']  = 'verification'
test_table_to_verification['test_scores2'] = 'verification2'
test_table_to_verification['test_scores3'] = 'verification3'
test_tables = ['test_scores', 'test_scores2', 'test_scores3']

verDistance = Verifier_Distance()

def CheckAccuracy(new_weights):
	# - update classifier with new weights
	verDistance.weights = new_weights
	# verDistance.weights = [16.7194209217615, 2.60829499230467,2.2260372998623,2.90305925398725,5.09533279100191,2.99409304662811,3.1147007335932,5.27110197918494,7.929635390837,3.5367525886694,6.76277542448109,1.62292767902453,0.707530369202495,0.492143303569623,0.644893274893918]

	# first, re-calculate Cosine distance values with new weights (on training set)
	for url in Classifier.storage.Select('SELECT domainName FROM scores'):
		print('CA_1:VERIFYING URL: ' + url[0])
		verDistance.Cosine_Distance('scores', test_table_to_verification['scores'], url[0])

	# second, check Cosine distance accuracy on 100 thresholds and select best T
	# (on scores database)
	threshold_results = Classifier.accuracy.CalculateThresholds(100, 'cosine', 'scores')
	# - find best result
	best_t		 = 0.0
	max_accuracy = 0.0
	for i in range(0, len(threshold_results)):
		# - get classification accuracy and error rates
		true_positives  = threshold_results[i]['tp']
		true_negatives  = threshold_results[i]['tn']
		false_positives = threshold_results[i]['fp']
		false_negatives = threshold_results[i]['fn']
		nr_total = len(true_positives)  + len(true_negatives)  + len(false_positives) + len(false_negatives)
		CAR      = (len(true_positives) + len(true_negatives)) / nr_total
		TI_er    = len(false_positives) / nr_total
		TII_er   = len(false_negatives) / nr_total
		print(CAR)
		if CAR > max_accuracy:
			max_accuracy = CAR
			# - calculate threshold value t in range [0,1] from range [0,100]
			t = i / (len(threshold_results) - 1)
			# - set as current beste threshold value t
			best_t = t
	print('best threshold: ' + str(best_t))
	# final, use selected threshold value T to calculate new accuracy rates / error function and return
	# - determine accuracy on test dataset, so re-calculate Cosine values.
	# for table in test_tables:
		# print()
		# print('CA_3:TEST TABLE: ' + table)
		# print()
		# for url in storage.Select('SELECT domainName FROM ' + table):
			# print('CA_3:VERIFYING URL: ' + url[0])
			# verDistance.Cosine_Distance(table, test_table_to_verification[table], url[0])
	# this is commented, as we now test on the scores table alone

	# - then use best threshold found to calculate accuracy of current metric
	thresholds 		 = [0.0, 0.0, 0.0, best_t, 0.0, 0.0, 0.0] # we only care about Cosine threshold
	accuracy_results = Classifier.accuracy.CalculateAccuracy(thresholds)
	# - now get accuracy rate of cosine distance with new weights and threshold best_t
	true_positives  = accuracy_results['cosine']['tp']
	true_negatives  = accuracy_results['cosine']['tn']
	false_positives = accuracy_results['cosine']['fp']
	false_negatives = accuracy_results['cosine']['fn']
	nr_total = true_positives  + true_negatives  + false_positives + false_negatives
	CAR      = (true_positives + true_negatives) / nr_total
	TI_er    = false_positives / nr_total
	TII_er   = false_negatives / nr_total
	# - finally return newly calculated accuracy
	return [CAR, TI_er, TII_er]


# gaussian function: a * e^((-(x - b)^2) / (2 * c^2))
# a = peak y-value. 
# b = center of curve
# c = std. deviation
def Gaussian(x = 0.5):
	a = 1.0 # Y-value of Gaussian curve peak
	b = 0.5  # center of Gaussian curve 
	c = 0.5  # Std. deviation
	value = a * math.exp(-((x - b)**2) / (2 * c**2))
	return value

iterations = 1
while True:
	iterations += 1
	# 1, get current best set of weights and corresponding accuracy rate
	row 		= Classifier.storage.Select('SELECT * FROM weight_adaptability ORDER BY car DESC LIMIT 1')
	car 		= row[0][1] # best CAR stored in database
	new_weights = list(row[0][4:])
	# 2. update weights based on Guassian distribution curve
	for w in range(0, len(new_weights)):
		random_value = Gaussian(random.uniform(0.0, 1.001))
		new_weights[w] *= random_value 
	# 3. create random outliers as to evolute the algorithm and throw it in different directions
	# - do this once every 5 iterations
	if iterations % 5 == 0:
		# select which weight index to alter
		w     = random.randrange(0, len(new_weights))
		# increase weight by score between 1.0 - 2.5
		boost = random.uniform(1.0, 2.5)
		print('outlier ' + str(w) + ' boosted by ' + str(boost))
		new_weights[w] *= boost
	# 4. use updated weights to calculate new CAR
	error_rates = CheckAccuracy(new_weights) # [CAR, TI_er, TII_er]
	print('new CAR: ' +str(error_rates[0]))
	if error_rates[0] > car:
		print('new set of weights found: ' + str(new_weights))
	# 5. store and repeat
	Classifier.storage.Insert('weight_adaptability',
		[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		error_rates[0],
		error_rates[1],
		error_rates[2], 
		new_weights[0], 
		new_weights[1],
		new_weights[2],
		new_weights[3],
		new_weights[4],
		new_weights[5],
		new_weights[6],
		new_weights[7],
		new_weights[8],
		new_weights[9],
		new_weights[10],
		new_weights[11],
		new_weights[12],
		new_weights[13],
		new_weights[14]]
	)