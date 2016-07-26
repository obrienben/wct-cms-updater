
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

with open(input_file, 'r') as f:
	reader = csv.reader(f)
	voyager_list = list(reader)
	
""""print(voyager_list)"""



""" Open odbc connection to WCT database """
cnxn = pyodbc.connect('DSN=wct-dev;PWD=usr_wct')


# Opening a cursor
cursor = cnxn.cursor()

cursor.execute("select usr_oid, usr_firstname, usr_email from db_wct.wctuser")
row = cursor.fetchone()
if row:
    print(row)


cnxn.close()