#!  /bin/bash
cd /home/mvirtel/logins

. ../login_check/bin/activate


python ./Datengewinnung.py 'data/log/*cookie*'
python ./Report.py >data/report/report.txt
