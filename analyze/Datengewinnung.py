# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import dumptruck
from scrapelib import TextParser
import glob
import gzip
import bz2
import re
import pprint
import urllib
import sqlite3
import sys

# <codecell>

store=dumptruck.DumpTruck("./data/sessions.db")
t_parser=TextParser(r"__utma=\d+\.(?P<id>\d+\.\d+)",r"PHPSESSID=(?P<pid>[^\";]+)", r"^[^;]+;(?P<stamp>[^;]+)",r"wordpress_logged_in_[0-9a-f]+=(?P<user>.+?)%7C" )


bots=["bingbot","Googlebot","SISTRIX Crawler","MJ12bot","AhrefsBot", "uMBot", "msnbot", "Ezbooms" ]


def parser(a) :
    for b in bots :
        if a.find(b)>0 :
            return None
    g=t_parser(a)
    flag=""
    if "id" not in g and "pid" in g :
        g["id"]=g["pid"]
    for k in ("id","user","stamp","pid") :
        if k not in g :
            g[k]="no %s" % k
            flag="%s %s" % (flag, g[k])
    g["user"]=urllib.unquote(g["user"])
    if flag :
        errs.write("%s\t%s\n" % (flag,a))
    return g

# <codecell>


def compressed_open(a) :
    if re.search("\.bz2$",a) :
        return bz2.BZ2File(a,"r")
    if re.search("\.gz$",a) :
        return gzip.open(a,"r")
    return open(a,"r")



def datafeed(a) :
    for fn in (glob.glob(a)) : #  ,"../data/versicherungsmonitor.de-cookie.log.1") :
        for line in compressed_open(fn).readlines() :
            yield line

def get_or_create(d,table,store) :
    ex=["select * from %s where %s" % (table," and ".join(["%s=?" % k for k in d.keys()])),d.values()]
    try :
    	ob=store.execute(*ex)
    except sqlite3.OperationalError :
        ob=[]
    if (len(ob)==0) :
        store.insert(d,table)
        ob=store.execute(*ex)
    return ob[0]   

# <codecell>

data=[]

try :
	store.execute("delete from hits")
except Exception, e: 
	pass 
errs=open("./data/errors.log","w")

for line in datafeed(sys.argv[1]) :
    record=parser(line)
    if record is not None :
        try :
            session=get_or_create({'session' : record["id"]},"sessions",store)
            user=get_or_create({'user' : record["user"]},"users",store)
            data.append({ 'userid' : user['userid'], 'sessionid' : session['sessionid'], 'stamp' : record["stamp"]})
        except KeyError,e :
            pprint.pprint({ "Key" : e, "Value" : record})

r=store.insert(data,"hits")

    

# <codecell>


