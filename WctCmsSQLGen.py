
import sys, csv

args_num = len(sys.argv)
print("==============================")
print('Argument List: ', str(sys.argv))

""" Parse command line arguments """
if args_num < 3:
	print("No CSV file arguments provided - <voyager_ids_in_wct>.csv <voyager_alma_mappings>.csv")
	sys.exit()
elif args_num == 3:
	print("Correct number of arguments provided")
	input_file_one = sys.argv[1]
	print("Existing Voyager IDs in WCT: ", input_file_one)
	input_file_two = sys.argv[2]
	print("Voyager - ALMA ID mapping: ", input_file_two)
else:
	print("Too many arguments provided - <voyager_ids_in_wct>.csv <voyager_alma_mappings>.csv")
	sys.exit()

print("==============================")







wct_ids = list()
wct_voyager_list = list()
new_wct_ids = dict()


""" Read csv file of Existing WCT Voyager IDs into list """
with open(input_file_one, 'r') as f:
	reader = csv.reader(f)
	for line in reader:
		wct_voyager_list.append(line[0])
	
"""print(wct_voyager_list)"""


""" Read csv file of Alma-Voyager IDs into list """
with open(input_file_two, 'r') as f:
	reader = csv.reader(f)
	voyager_alma_list = list(reader)


""" Cross reference with csv file to build dictionary of IDs to update """
print("\n")
print("==============================")
print("Searching csv files for matches...")
print("==============================")

	
for row in voyager_alma_list:
	if row[1] in wct_voyager_list:
		new_wct_ids[row[1]] = row[0]
		"""print("Found match for Voyager ID: ", row[1])"""
	
	
voyager_alma_list = None
print("\n")
db_prefix = input("Dictonary has been built, please enter the database prefix to be used in update:")
	
	
output_file = open("wct_cms_update.sql", "w")
output_file.write("UPDATE db_wct.abstract_target SET at_reference = LTRIM(RTRIM(at_reference));\n")
for voyager_id, alma_id in new_wct_ids.items():
	line = "UPDATE {}.abstract_target SET at_reference = '{}' WHERE at_reference = '{}';\n".format(db_prefix, alma_id, voyager_id)
	output_file.write(line)
output_file.close()
	
	
print("\n")
print("==============================")
print("SQLs saved to <cwd>/wct_cms_update.sql")
print("==============================")









