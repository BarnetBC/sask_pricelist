1)add following fields to lto table:
date_from date
date_to date 
province varchar(50)
2)create migrations for above changes
3)update task SLGApricelist.md following:
- implement command line parameter for reading xslx file name
- implement changes to line "the field province should be popolated as 'SK'"
4) delete table sk_lto_history
5) read SLGALTO.md and run
6) populate field pricelist_general.lto according to the following:
- the field lto.price_diff should go to pricelist_general.lto by matching province,cspcid, and pricelist_general.price_date should be between lto.date_from and lto.date_to
7) implement the 6) as separate procedure

use following db credentials
host: localhost
database: bottlebridge
schema: public
username: olena
password: Barnet359?
