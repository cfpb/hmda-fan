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


now = time.localtime(time.time())
print "     start time: ", time.asctime(now)

#global variables - database connections
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
schema = "hmda"
outTB = "all_label_2012"

def alter_table(myTB):
	theAltCur = conn.cursor()
	mySQL = "ALTER TABLE " + schema + "." + myTB + " DROP COLUMN state_fips; "
#	theAltCur.execute(mySQL)
	conn.commit()
	mySQL = "ALTER TABLE " + schema + "." + myTB + " ADD COLUMN "
	mySQL = mySQL + " state_fips character varying(2);"
	theAltCur.execute(mySQL)
	conn.commit()
	mySQL = "CREATE INDEX " + schema + "_" + myTB + "_state_fips_btree ON "
	mySQL = mySQL + schema + "." + myTB + " USING btree (state_fips); " 
	theAltCur.execute(mySQL)
	conn.commit()
	theAltCur.close()
	del myTB, mySQL, theAltCur

def pop_state_fips(myTB, myST):
	theUpdCur = conn.cursor()
	theFips = returnFIPS(myST)
	mySQL = "UPDATE " + schema + "." + myTB + " SET state_fips = '" + theFips + "'"
	mySQL = mySQL + " where state_abbr = '" + myST + "'; " 
	theUpdCur.execute(mySQL)
	conn.commit()
	theUpdCur.close()
	del myTB, mySQL, theUpdCur

def returnFIPS(myST):
	myFips = '00'
	if myST == 'AK':
		myFips = '02'
	if myST == 'AL':
		myFips = '01'
	if myST == 'AR':
		myFips = '05'
	if myST == 'AZ':
		myFips = '04'
	if myST == 'CA':
		myFips = '06'
	if myST == 'CO':
		myFips = '08'
	if myST == 'CT':
		myFips = '09'
	if myST == 'DC':
		myFips = '11'
	if myST == 'DE':
		myFips = '10'
	if myST == 'FL':
		myFips = '12'

	if myST == 'GA':
		myFips = '13'
	if myST == 'HI':
		myFips = '15'
	if myST == 'IA':
		myFips = '19'
	if myST == 'ID':
		myFips = '16'
	if myST == 'IL':
		myFips = '17'
	if myST == 'IN':
		myFips = '18'
	if myST == 'KS':
		myFips = '20'
	if myST == 'KY':
		myFips = '21'
	if myST == 'LA':
		myFips = '22'
	if myST == 'MA':
		myFips = '25'

	if myST == 'MD':
		myFips = '24'
	if myST == 'ME':
		myFips = '23'
	if myST == 'MI':
		myFips = '26'
	if myST == 'MN':
		myFips = '27'
	if myST == 'MO':
		myFips = '29'
	if myST == 'MS':
		myFips = '28'
	if myST == 'MT':
		myFips = '30'
	if myST == 'NC':
		myFips = '37'
	if myST == 'ND':
		myFips = '38'
	if myST == 'NE':
		myFips = '31'

	if myST == 'NH':
		myFips = '33'
	if myST == 'NJ':
		myFips = '34'
	if myST == 'NM':
		myFips = '35'
	if myST == 'NV':
		myFips = '32'
	if myST == 'NY':
		myFips = '36'
	if myST == 'OH':
		myFips = '39'
	if myST == 'OK':
		myFips = '40'
	if myST == 'OR':
		myFips = '41'
	if myST == 'PA':
		myFips = '42'
	if myST == 'PR':
		myFips = '72'
		
	if myST == 'RI':
		myFips = '44'
	if myST == 'SC':
		myFips = '45'
	if myST == 'SD':
		myFips = '46'
	if myST == 'TN':
		myFips = '47'
	if myST == 'TX':
		myFips = '48'
	if myST == 'UT':
		myFips = '49'
	if myST == 'VA':
		myFips = '51'
	if myST == 'VT':
		myFips = '50'
	if myST == 'WA':
		myFips = '53'
	if myST == 'WI':
		myFips = '55'

	if myST == 'WV':
		myFips = '54'
	if myST == 'WY':
		myFips = '56'
	return(myFips)
		
						
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
	pop_state_fips(outTB, theST)

conn.commit()
now = time.localtime(time.time())
print "     end time: ", time.asctime(now)
