# -*- coding: utf-8 -*-

#	Adapt the data from the original list into a JSON

import sys
import codecs
import json

most_likely_ratio = 2

def adapt():
	firstnames = {}
	f = codecs.open('../original_data/firstname.csv','r',encoding='utf8')
	for line in f:
		line_elts = line.split(",")
		most_likely = "unisex"
		if float(line_elts[1]) >= most_likely_ratio * float(line_elts[2]):
			most_likely = "male"
		elif float(line_elts[2]) >= most_likely_ratio * float(line_elts[1]):
			most_likely = "female"
		firstnames[line_elts[0].title()] = {
			"male":int(line_elts[1]),
			"female":int(line_elts[2]),
			"most_likely": most_likely
		}
	f.close()
	with open('../fb-gender.json', 'w') as outfile:
		json.dump(firstnames, outfile, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    try:
        adapt()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)