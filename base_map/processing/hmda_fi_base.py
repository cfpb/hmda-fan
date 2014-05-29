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

def createTable(myAct, myAg):
	theCur = conn.cursor()
	mySQL = "DROP TABLE IF EXISTS " + schema + ".fi_base_" + myAct + "_" + myAg + "; "
	theCur.execute(mySQL)
	conn.commit()	
	mySQL = "CREATE TABLE " + schema + ".fi_base_" + myAct + "_" + myAg + " ( "
	mySQL = mySQL + "tract character varying(11), count integer, "
	mySQL = mySQL + "base_1_respondent character varying(20), "
	mySQL = mySQL + "base_1_count integer, base_1_pct numeric, "
	mySQL = mySQL + "base_2_respondent character varying(20), "
	mySQL = mySQL + "base_2_count integer, base_2_pct numeric, "
	mySQL = mySQL + "base_3_respondent character varying(20), "
	mySQL = mySQL + "base_3_count integer, base_3_pct numeric, "
	mySQL = mySQL + "base_4_respondent character varying(20), "
	mySQL = mySQL + "base_4_count integer, base_4_pct numeric, "
	mySQL = mySQL + "base_5_respondent character varying(20), "
	mySQL = mySQL + "base_5_count integer, base_5_pct numeric ) "
	mySQL = mySQL + "WITH (OIDS=TRUE); " 
	mySQL = mySQL + "ALTER TABLE " + schema +  ".fi_base_" + myAct + "_" + myAg + " " 
	mySQL = mySQL + "OWNER TO feomike;	"
	theCur.execute(mySQL)
	conn.commit()
	del myAct, myAg, mySQL, theCur

def createTractList(myAct, myAg):
	theCur = conn.cursor()
	mySQL = "SELECT tract, count(*) from " + schema + "." + outTB + " " 
	mySQL = mySQL + "WHERE tract is not null " 
	#need to return the right values from the driver loops for which rows to be
	#operating on.  i am envisioning these as functions
	#mySQL = mySQL + returnActionTaken + returnAgency
	mySQL = mySQL + "group by tract order by count desc; "
	theCur.execute(mySQL)
	for r in theCur:
		myTract = r[0]
		myCount = r[1]
		print myTract
		popBase(myAct, myAg, r[0],r[1])
		popTop5(myAct, myAg, r[0])

def popBase(myAct, myAg, myTract, myCount):
	#insert a row into the table
	insCur = conn.cursor()
	#insert into hmda.fi_base_all (tract, count) values ('50001010101', 100);
	mySQL = "INSERT INTO " + schema + ".fi_base_" + myAct + "_" + myAg + " " 
	mySQL = mySQL + "(tract, count) values ('"
	mySQL = mySQL + myTract + "'," + str(myCount) + "); "
	insCur.execute(mySQL)			
	conn.commit()
	del insCur, mySQL, myAct, myAg, myTract, myCount

def popTop5(myAct, myAg, myTract):
	theCur = conn.cursor()
	uCur = conn.cursor()
	mySQL = "SELECT respondent_id, count(*) from " + schema + "." + outTB + " " 
	mySQL = mySQL + "where tract = '" + myTract + "' " 
	#need to return the right values from the driver loops for which rows to be
	#operating on.  i am envisioning these as functions
	#mySQL = mySQL + returnActionTaken + returnAgency
	mySQL = mySQL + "group by respondent_id order by count desc LIMIT 5; " 
	theCur.execute(mySQL)
	cnt = 1
	for r in theCur:
		mySQL = "UPDATE " + schema + ".fi_base_" + myAct + "_" + myAg + " "
		mySQL = mySQL + "set base_" + str(cnt) + "_respondent = '" + r[0] + "', "
		mySQL = mySQL + "base_" + str(cnt) + "_count = " + str(r[1]) + ", "
		mySQL = mySQL + "base_" + str(cnt) + "_pct =(" + str(r[1]) + "/count::float)*100 "
		mySQL = mySQL + "where tract = '" + myTract + "'; commit; "
		uCur.execute(mySQL)
		cnt = cnt + 1		

							
#create connection string to postgres
myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
conn = psycopg2.connect(myConn)

actionTaken = ["all","Loan originated","Application denied by financial institution"]
actionTaken = actionTaken + ["Loan purchased by the institution","Application withdrawn by applicant"]
actionTaken = actionTaken + ["Application approved but not accepted","File closed for incompleteness"]

agency = ["all","CFPB","NCUA","HUD","FDIC","OCC","FRS"]

actionTaken = ["act_all"]
agency = ["agency_all"]

for theAct in actionTaken:
	for theAg in agency:
		#create output table
		createTable(theAct, theAg)
		createTractList(theAct, theAg)
		#createTractList(theAct, theAg)
		#for each tract, populate table

conn.commit()
now = time.localtime(time.time())
print "     end time: ", time.asctime(now)
