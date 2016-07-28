
import sys, csv
import pyodbc

args_num = len(sys.argv)
print("Number of arguments provided: ", args_num)
print('Argument List: ', str(sys.argv))

""" Parse command line arguments """
if args_num < 2:
	print("No CSV file argument provided")
	sys.exit()
elif args_num == 2:
	print("Correct number of arguments provided")
	input_file = sys.argv[1]
	print("CSV file: ", input_file)
else:
	print("Too many arguments provided")
	sys.exit()

"""Take a filename as an argument"""




"""Read the csv file into a list"""
"""
with open(input_file, 'r') as f:
	reader = csv.reader(f)
	voyager_list = list(reader)
	
print(voyager_list)
"""


wct_ids = list()
new_wct_ids = dict()


""" Open odbc connection to WCT database """
cnxn = pyodbc.connect('DSN=wct-dev;PWD=usr_wct')

# Opening a cursor
cursor = cnxn.cursor()



""" Get list of CMS IDs in wct db """
cursor.execute("SELECT DISTINCT(at_reference) AS ref FROM db_wct.abstract_target")
for row in cursor:
	wct_ids.append(row[0])
	
print(wct_ids)



""" Read csv file of Alma-Voyager IDs into list """
with open(input_file, 'r') as f:
	reader = csv.reader(f)
	voyager_alma_list = list(reader)


""" Cross reference with csv file to build dictionary of IDs to update """
for row in voyager_alma_list:
	if row[1] in wct_ids:
		print("Found Voyager ID in csv: ", row[1])
		new_wct_ids[row[1]] = row[0]

print(new_wct_ids)

		
""" Once dictionary is built, then prompt user asking if they want to continue with updating db """
voyager_alma_list = None

choice = input("Dictonary has been built, do you want to continue updating WCT database? (y/n)").lower()
if choice != "y":
	sys.exit()



cursor.execute("select usr_oid, usr_firstname, usr_email from db_wct.wctuser where usr_firstname =?", "Ben")
row = cursor.fetchone()
if row:
    print(row)
	
	
"""cursor.execute("UPDATE abstract_target SET at_reference =? WHERE at_reference =?")"""


cnxn.close()