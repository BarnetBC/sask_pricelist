Read file 20260601.xlsx
and load data into the pricelist_general
use following mapping 
table_field - xls_documet_field:
price_date - take from file name in the format yyyyMMDD
cspcid - item
pid -UPC
description - Item Description
size_id  - Size (mL)
deposit -  Refund Dep
wholesale -  Wholesale Base Price 
category - everything after the first word with dash in the column "Product Hierarchy"
"group" - the first word in the column "Product Hierarchy"
supplier-  Manufacturer Name 
sweetness -Sweetness
alcohol - Alcohol Content (%)
multiple -Units/Case

Table could contain records, do not delete them , but follow the instruction:
- if pair (cspcid,pid) exists then update fields 
(price_date,description,size_id,deposit,wholesale,category,"group",supplier,sweetness,alcohol,multiple) if values not matching, but if new value is empty then do not update.
- If pair (cspcid,pid) doesn't exist then insert data.
-the field province should be popolated as 'SASK'

use following db credentials
host: localhost
database: bottlebridge
schema: public
username: olena
password: Barnet359?
