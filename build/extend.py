# -*- coding: utf-8 -*-

#	Extend the facebook generated name list with data from http://www.lexique.org/

import sys
import codecs
import json
import re

most_likely_ratio = 2

def extend():
	original_list = {}
	extension_list = {}
	extended_list = {}
	# load the facebook generated name list
	with open('../fb-gender.json') as data_file:
		original_list = json.load(data_file)

	# load the list from lexique.org
	extension_list = adaptDataFromLexiqueOrg('../original_data/Prenoms.txt')

	# merge the two lists
	extended_list = mergeTheOriginalAndTheExtendedLists(original_list, extension_list)

	with open('../fb-gender-extended.json', 'w') as outfile:
		json.dump(extended_list, outfile, sort_keys=True, indent=4, separators=(',', ': '))

def adaptDataFromLexiqueOrg(path):
	f = codecs.open(path,'r',encoding='cp1252')
	listAsJSON = {}
	for line in f:
		elements = line.split("\t")
		name = re.sub(r" \([0-9]\)", "", elements[0].title())
		male = 0
		female = 0
		if "m" in elements[1]:
			male = 1
		if "f" in elements[1]:
			female = 1

		if name not in listAsJSON:
			listAsJSON[name] = {
				"male":male,
				"female":female
			}
		else:
			listAsJSON[name]["male"] += male
			listAsJSON[name]["female"] += female

		# determine the gender of the name
		most_likely = "unisex"
		if float(listAsJSON[name]["male"]) >= most_likely_ratio * float(listAsJSON[name]["female"]):
			most_likely = "male"
		elif float(listAsJSON[name]["female"]) >= most_likely_ratio * float(listAsJSON[name]["male"]):
			most_likely = "female"
		listAsJSON[name]["most_likely"] = most_likely
	return listAsJSON

def mergeTheOriginalAndTheExtendedLists(original_list, extension_list):
	extended_list = {}
	# add the elements of the original list in the new one
	for elt in original_list:
		extended_list[elt] = original_list[elt]

	# log files
	debug_file_added = codecs.open('./log/ext_added.txt','w',encoding='utf8')
	debug_file_merged = codecs.open('./log/ext_merged.txt','w',encoding='utf8')

	# stats
	added = 0
	ignored = 0
	different = 0

	for elt in extension_list:
		if elt not in extended_list:
			debug_file_added.write(elt + " " + str(extension_list[elt]) + "\n")
			extended_list[elt] = extension_list[elt]
			added += 1
		else:
			ignored += 1
			debug_file_merged.write(elt + " " + str(extension_list[elt]) + "\n")
			debug_file_merged.write(elt + " " + str(extended_list[elt]) + "\n")
			if extension_list[elt]["most_likely"] != extended_list[elt]["most_likely"]:
				debug_file_merged.write("> Different\n")
				different += 1
			else:
				debug_file_merged.write("> Same\n")
			debug_file_merged.write("\n")
	print str(added) + " name(s) added, " + str(ignored) + " name(s) ignored (already present) and " + str(different) + " differences."
	print "See the log directory."
	return extended_list


if __name__ == '__main__':
    try:
        extend()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)