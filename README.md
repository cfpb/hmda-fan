hmda-fan
========

post processing Home Mortgage Disclosure Act data from the cfpb.gov/hmda site

This repo presents post-processing scripts on data files delivered from the [cfpb](http://www.cfpb.gov) [public data platform](http://www.consumerfinance.gov/hmda/) which delivers slices of Home Mortgage Disclosure Data.  The intent of the public data platform is to provide filtered data for mostly researchers.

This repo does two things with the files delivered from the public data platform.  First it ensures formatting for use in the postGis database/libraries.  Second it uses tilemill to present the data in perhaps some unique cartographically ways.

all of the product and code presented here is based on public data.

Processing for inclusion in PostGIS
-----------------------------------
The data delivered out of the public data platform has several limitations for which i hope to offer simple solutions.  The limitations are, a) the lack of a ddl for dealing with the data in postgres and b) the lack of an 11 character string tract code so that the data can definitively linked to census geography.

i developed a ddl for the data in postgress.  this ddl can easily be used in other databases (sqlserver, oracle, mysql etc).  simple relative alterations can be made for use in these containers.  while the delivery of files form the public data platform makes small files highly useful in say ms excel, most researchers (and indeed geospatial folks) and anyone wanting to use larger datasets want a database.  the fist script i developed then is a function of processing the csv file for pulling it into postgress.  below are the steps and appropriate scrips to ensure public data platform files can be used in postgres.

- [hmda_data_create.sql](https://github.com/cfpb/hmda-fan/blob/master/data_process/hmda_data_create.sql) - this is the ddl file for the hmda data delivered out of the public data platform.  at this stage this ddl is only developed for the 'labels' file type.  I have not developed a ddl for the 'labels and codes'.

- [hmda_sed.sh](https://github.com/cfpb/hmda-fan/blob/master/data_process/hmda_sed.sh) - this is a simple shell script to double quotes (e.g. "").  double quotes are Null values in these files, but PostGres will throw an error for numeric types for double quotes.  removal of the double quotes results in a Null value that PG is expecting.

- [hmda_data_load.sql](https://github.com/cfpb/hmda-fan/blob/master/data_process/hmda_load_data_all.sql) - this is the simple copy from script.  make sure it is pointing at the resulting file from the hmda_sed.sh.

- [investigate.sql](https://github.com/cfpb/hmda-fan/blob/master/data_process/investigate.sql) - this is just a simple set of sql statements that allows the end use to know the unique characteristics of the newly loaded table.

the next set of routines ensures that there is an 11 character field for tract.  this approach guarantees that one can match a single tract number in the hmda data delivered from the public data platform to census delivered geography.  currently the data delivered from the public data platform cannot be linked to census delivered geography because tract numbers are only in one field, the 7 character field w/ the decimal point.  census does not deliver tract geography this way, because these numbers are not unique.  only the 11 character combination of state, county and 6 digit (non-decimal) place are unique as delivered from census.

- [hmda_state.py](https://github.com/cfpb/hmda-fan/blob/master/hmda_fips_process/hmda_state.py) - this script creates a field called state_fips and populates it with a two digit state number (e.g. California is 06).

- [hmda_county.py](https://github.com/cfpb/hmda-fan/blob/master/hmda_fips_process/hmda_county.py) - this scripts creates field called county_fips (a 5 character field) and populates it with the 5 digit number combination of state fips code and 3 digit county character code.  this script is dependent on county json files containing the data for linking county names (only county names are contained in the public data platform) to the county fips codes.  this script relies on the hmda_state_script being run first, but an enhancement would be to put the state update into this script and removing one step.

- [hmda_tract.py](https://github.com/cfpb/hmda-fan/blob/master/hmda_fips_process/hmda_tract.py) - this script concatenates the newly formed county_fips (5 characters) and tract_fips (6 characters - removing the decimal place) into a newly formed 11 character field.  this new 11 character field now allows for anyone to definitively link the hmda data from the public data platform to census published geography.

Map Generation and Presentation 
-------------------------------
this [set](https://github.com/cfpb/hmda-fan/tree/master/base_map) of directories and files are the setup/investigation, carto.css files and design files used in tilmill.  tilemill will generate the cartography used in mapbox.  at this stage the only developed cartography is a map which displays the financial institutions with the most mortgage activity as collected by hmda in every census tract.  the top 10 financial institutions based on total number of mortgage activity per tract are displayed in unique colors, while the remainder are combined in gray tones.  for every tract a mouse over delivers the top 3 mortgage activity financial institutions in that tract.

at this stage no filters for mortgage activity have been applied.  future iterations would include a matrix of filters such as, agency (giving top mortgage activity by supervising agency), loan type (giving top mortgage activity by loan type) and combinations of agency and loan type.  


future enhancements
-------
...in progress ...
 
