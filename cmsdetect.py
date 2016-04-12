# encoding:utf-8
from  multiprocessing import Pool
import io
import requests
import json
import hashlib
import re
import time

start = time.time()

global rules
with open("whatsweb.json") as f:
    rules = json.load(f)
f.close()

def cmsscan(iplist):
    cmslist = list(rules.keys())
    for cms in cmslist:
        for rule in rules[cms]:
            job_url = "http://"+ str(iplist).strip()+rule["url"]
            try:
                r=requests.get(job_url, timeout=2, verify=False)
                r.encoding = r.apparent_encoding
                r.close()
                if ("md5" in rule and hashlib.md5(r.content).hexdigest() == rule["md5"]) or ("header" in rule and rule["header"] in str(r.headers)
                                                                                             ) or ("text" in rule and rule["text"] in r.text) or ("regexp" in rule and re.search(rule["regexp"], r.text)):
                    result = str(iplist).strip() + "|" + cms+"\r"
                    fileHandler = file('result.txt','a')
                    fileHandler.write(result)
                    fileHandler.close()
                    return
            except Exception:
                pass
if __name__ == "__main__":
    iplist = []
    with open('ip.txt') as f:
        iplist = f.readlines()
    f.close()
    p = Pool(10)
    p.map(cmsscan, iplist)
    end = time.time()
    print "use: %s" % (end - start)
