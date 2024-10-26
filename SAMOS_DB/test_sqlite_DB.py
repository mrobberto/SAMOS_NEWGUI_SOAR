from sqlite_db import SAMOS_DB
db = SAMOS_DB()
db.show_DB()
db.update_DB('Telescope', 'SOAR')
db.show_DB()
db.update_DB('Instrument', 'SAMI')
db.show_DB()
db.fetch_DB("Observer")
db.fetch_DB("Filter")
quit()
 