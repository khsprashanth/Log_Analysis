#!/usr/bin/env python3
import re
import sys
import subprocess
import operator
import csv
import os
error={}
per_user={}

with open("syslog.log","r") as file:
  for i in file:
    flag=1
    s=re.search(r"ticky: ERROR ([\w ']*) ",i)
    if(s is not None):
     flag=0
     if s.group(1) in error:
       error[s.group(1)] = error.get(s.group(1)) +1
     else:
       error[s.group(1)]=1
    s=re.search(r"\(([\w.]*)\)$",i)
    if flag==0:
     if(s.group(1) in per_user):
       per_user[s.group(1)][1] += 1
     else:
       per_user[s.group(1)]=[0,1]
    else:
     if(s.group(1) in per_user):
       per_user[s.group(1)][0]+=1
     else:
       per_user[s.group(1)]=[1,0]
er=sorted(error.items(),key=operator.itemgetter(1),reverse=True)
usr=sorted(per_user.items(),key=operator.itemgetter(0))

with open("error_message.csv","w") as f:
  fieldnames=["Error","Count"]
  write=csv.writer(f)
  write.writerow(fieldnames)
  for x,y in er:
   write.writerow([x,y])
  f.close()
with open("user_statistics.csv","w") as f:
  fieldname=["Username","INFO","ERROR"]
  write=csv.writer(f)
  write.writerow(fieldname)
  for x,y in usr:
   write.writerow([x,y[0],y[1]])
  f.close()
