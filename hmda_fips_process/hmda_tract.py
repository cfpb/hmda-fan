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
	mySQL = "ALTER TABLE " + schema + "." + myTB + " DROP COLUMN tract; "
#	theAltCur.execute(mySQL)
	conn.commit()
	mySQL = "ALTER TABLE " + schema + "." + myTB + " ADD COLUMN "
	mySQL = mySQL + " tract character varying(11);"
	theAltCur.execute(mySQL)
	conn.commit()
	mySQL = "CREATE INDEX " + schema + "_" + myTB + "_tract_btree ON "
	mySQL = mySQL + schema + "." + myTB + " USING btree (tract); " 
	theAltCur.execute(mySQL)
	conn.commit()

	
	theAltCur.close()
	del myTB, mySQL, theAltCur

def pop_tract(myTB, myST):
	theUpdCur = conn.cursor()
	mySQL = "UPDATE " + schema + "." + myTB + " SET tract = county_fips || "
	mySQL = mySQL + "left(census_tract_number,4) || right(census_tract_number,2) "
	mySQL = mySQL + "where state_abbr = '" + myST + "'; "
	theUpdCur.execute(mySQL)
	conn.commit()
	theUpdCur.close()
	del myTB, mySQL, theUpdCur

								
#create connection string to postgres
myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
conn = psycopg2.connect(myConn)

#drop and add column for state_fips
alter_table(outTB)

States = ["AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL"]
States = States + ["GA","HI","IA","ID","IL","IN","KS","KY","LA","MA"]
States = States + ["MD","ME","MI","MN","MO","MS","MT","NC","ND","NE"]
States = States + ["NH","NJ","NM","NV","NY","OH","OK","OR","PA","PR"]
States = States + ["RI","SC","SD","TN","TX","UT","VA","VT","WA","WI"]
States = States + ["WV","WY"]

#for each state populate the state_fips field
for theST in States:
	print theST
	pop_tract(outTB, theST) 

conn.commit()
now = time.localtime(time.time())
print "     end time: ", time.asctime(now)
