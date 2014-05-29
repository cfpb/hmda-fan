#mike byrne
#consumer finance protection bureau
#may 2014
#update the state field on a hmda public data row
#processing step towards geospatial analysis

import os
import string
import psycopg2
import time
import datetime
from datetime import date
import json


now = time.localtime(time.time())
print "     start time: ", time.asctime(now)

#global variables - database connections
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
schema = "hmda"
outTB = "all_label_2012"
fileLoc = "/Users/feomike/documents/analysis/2014/hmda_mayor/data/countynames/"

def alter_table(myTB):
	theAltCur = conn.cursor()
	mySQL = "ALTER TABLE " + schema + "." + myTB + " DROP COLUMN county_fips; "
#	theAltCur.execute(mySQL)
	conn.commit()
	mySQL = "ALTER TABLE " + schema + "." + myTB + " ADD COLUMN "
	mySQL = mySQL + " county_fips character varying(5);"
	theAltCur.execute(mySQL)
	conn.commit()
	mySQL = "CREATE INDEX " + schema + "_" + myTB + "_county_fips_btree ON "
	mySQL = mySQL + schema + "." + myTB + " USING btree (county_fips); " 
	theAltCur.execute(mySQL)
	conn.commit()
	theAltCur.close()	
	del myTB, mySQL, theAltCur

def pop_cty_fips(myTB, myST, myCty, myFips):
	theUpdCur = conn.cursor()
	mySQL = "UPDATE " + schema + "." + myTB + " SET county_fips = '" + myFips + "'"
	mySQL = mySQL + " where state_abbr = '" + myST + "' and county_name like '"
	mySQL = mySQL + myCty + "%' ; "  
	theUpdCur.execute(mySQL)
	conn.commit()
	theUpdCur.close()
	del myTB, mySQL, theUpdCur

								
#create connection string to postgres
myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
conn = psycopg2.connect(myConn)

#drop and add column for state_fips
#alter_table(outTB)

States = ["AL","AR","AZ","CA","CO","CT","DC","DE","FL"] #"AK",
States = States + ["GA","HI","IA","ID","IL","IN","KS","KY","LA","MA"]
States = States + ["MD","ME","MI","MN","MO","MS","MT","NC","ND","NE"]
States = States + ["NH","NJ","NM","NV","NY","OH","OK","OR","PA","PR"]
States = States + ["RI","SC","SD","TN","TX","UT","VA","VT","WA","WI"]
States = States + ["WV","WY"]

#for each state populate the state_fips field
for theST in States:
	print theST
	json_data = open(fileLoc +  theST + "_counties.json") 
	data = json.load(json_data)
	for i in data["counties"]:
#		print i["cty_name"], i["cty_fips"]
		pop_cty_fips(outTB, theST, i["cty_name"], i["cty_fips"])

conn.commit()
now = time.localtime(time.time())
print "     end time: ", time.asctime(now)
