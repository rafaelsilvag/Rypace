__author__ = 'rafaelguimaraes'
from database.DatabaseSQL import Ips, Blacklists, Session

session = Session()
ips = session.query(Ips, Blacklists).filter(Ips.blacklist_id == Blacklists.id, Ips.ip == "209.35.186.59").all()

for i in ips:
    print "%s %s ==> %s " % (i[0].blacklist_id,i[0].ip, i[1].id)