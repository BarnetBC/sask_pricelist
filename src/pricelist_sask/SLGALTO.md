read xlsx file name from command line 
and load data into the lto
use following mapping 
table_field - xls_documet_field:
date_from -WPP Start Date
date_to  - WPP End Date 
cspcid - SLGA Item No.
new_price -  Wholesale Base Price 
price_diff -   WPP Savings 
province - 'SK'

Table could contain records, do not delete them , but follow the instruction:
- if tuple (province,cspcid,date_from,date_to) exists then update other fields 
if values not matching, but if new value is empty then do not update.
- If pair tuple (province,cspcid,date_from,date_to) doesn't exist then insert data.

use following db credentials
host: localhost
database: bottlebridge
schema: public
username: olena
password: Barnet359?
