
import sys, csv
import pyodbc

args_num = len(sys.argv)
print("==============================")
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

print("==============================\n")







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
	
print("==============================")
print("Voyager IDs extracted from DB")
print("==============================")
print(wct_ids)


""" Read csv file of Alma-Voyager IDs into list """
with open(input_file, 'r') as f:
	reader = csv.reader(f)
	voyager_alma_list = list(reader)


""" Cross reference with csv file to build dictionary of IDs to update """
print("\n")
print("==============================")
print("Searching csv file matches...")
print("==============================")

for row in voyager_alma_list:
	if row[1] in wct_ids:
		new_wct_ids[row[1]] = row[0]
		print("Found Voyager ID in csv: ", row[1])


		
""" Once dictionary is built, then prompt user asking if they want to continue with updating db """
voyager_alma_list = None
print("\n")
choice = input("Dictonary has been built, do you want to continue updating WCT database? (y/n)").lower()
if choice != "y":
	sys.exit()



cursor.execute("select usr_oid, usr_firstname, usr_email from db_wct.wctuser where usr_firstname =?", "Ben")
row = cursor.fetchone()
if row:
    print(row)
	
	
print("\n")
print("==============================")
print("Updating WCT database")
print("==============================")

for voyager_id, alma_id in new_wct_ids.items():
	print("Updating {} with {}".format(voyager_id, alma_id))
	print("UPDATE abstract_target SET at_reference = {} WHERE at_reference = {}".format(alma_id, voyager_id))
	cursor.execute("UPDATE db_wct.abstract_target SET at_reference = ? WHERE at_reference = ?", str(alma_id), str(voyager_id))
	cnxn.commit()
	
	
	
print("\n")
choice = input("Update complete. Roll back updates? (y/n)").lower()
if choice != "y":
	sys.exit()
	
for voyager_id, alma_id in new_wct_ids.items():
	cursor.execute("UPDATE db_wct.abstract_target SET at_reference = ? WHERE at_reference = ?", str(voyager_id), str(alma_id))
	cnxn.commit()

print("Rollback complete")

	
cnxn.close()











