#!/usr/bin/env python

import os
import redis
import subprocess
import time


mywreck = { "host": "mymas", "task": "halemary" }
mytarget = { "host": "storagebox", "target": "mymas"}
myredis = { "host": "localhost", "port": 6379, "db": 1 }



def initredis():
    r = redis.Redis()
    return r


def gettree(target):
  subprocess.call(["/usr/bin/ssh" , mywreck['host'], "sudo" , "/usr/bin/find", "/volume2/data/PAnik", "-type", "f", ">/tmp/tree"])
  subprocess.call(["/usr/bin/scp" , mywreck['host'] + ":/tmp/tree", "/tmp/tree" ])
  f = open("/tmp/tree")
  lines = f.readlines()
  count = { "total": 0, "new": 0 , "known": 0, "initial": 0, "digested": 0, "safe": 0}
  for line in lines:
    count['total'] = count['total'] + 1
    status = r.get(line)
    if ( status.decode() == "" ):
      count['new'] = count['new'] + 1
      count['initial'] = count['initial'] + 1
      r.set(line, "initial")
    else:
      count['known'] = count['known'] + 1

  print("total: %-12s new:%-12s known:%-12s" % ( count["total"], count["new"], count["known"]) )
  



r = initredis()

gettree(mytarget)
