Read file 202604_LTO.xlsx
and load data into the sk_lto_history
use following mapping 
table_field - xls_documet_field:
date_from -WPP Start Date
date_to  - WPP End Date 
cspcid - SLGA Item No.
wholesale -  Wholesale Base Price 
LTO -   WPP Savings 
Table could contain records, do not delete them , but follow the instruction:
- if tuple (cspcid,date_from,date_to) exists then update other fields 
if values not matching, but if new value is empty then do not update.
- If pair tuple (cspcid,date_from,date_to) doesn't exist then insert data.

use following db credentials
host: localhost
database: bottlebridge
schema: public
username: olena
password: Barnet359?
