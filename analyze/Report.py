# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>



import dumptruck
import datetime
store=dumptruck.DumpTruck("data/sessions.db")

def active_users(pit) :
    start=(pit.replace(day=1)).strftime("%Y-%m-%d 00:00:00")
    ende=(pit+datetime.timedelta(days=32)).replace(day=1)+datetime.timedelta(days=-1)
    ende=ende.strftime("%Y-%m-%d 00:00:00")
    data=store.execute("select count(*) as sessions,user from (select distinct user, session from allhits where stamp>? and stamp<?) group by user order by sessions desc limit 30;",[start,ende])
    lformat="{sessions:>7} | {user}"
    print lformat.format(sessions="Logins",user="User (%s bis %s)" % (start[:10],ende[:10]))
    for d in data :
        print lformat.format(**d)
        

# <codecell>

now=datetime.datetime.now().replace(day=1)
months=[]
while now>datetime.datetime(year=2013,month=8,day=1) :
	months.append(now)
	m=now.month
	if (m==1) :
		now=now.replace(year=now.year-1, month=12)
	else :
		now=now.replace(month=m-1)

print "Bericht vom %s\n\n" % datetime.datetime.now()

print "Aktive Logins pro Nutzer"
for i in months :
    active_users(i)
    print

# <codecell>

def hits_per_user(pit) :
    start=(pit.replace(day=1)).strftime("%Y-%m-%d 00:00:00")
    ende=(pit+datetime.timedelta(days=32)).replace(day=1)+datetime.timedelta(days=-1)
    ende=ende.strftime("%Y-%m-%d 00:00:00")
    data=store.execute("select count(*) as hits,user from allhits where stamp>? and stamp<? group by user order by hits desc limit 30;",[start,ende])
    lformat="{hits:>8} | {user}"
    print lformat.format(hits="Seiten",user="User (%s bis %s)" % (start[:10],ende[:10]))
    for d in data :
        print lformat.format(**d)
        

# <codecell>

print "Artikelaufrufe pro Nutzer"
for i in months :
    hits_per_user(i)
    print

# <codecell>


