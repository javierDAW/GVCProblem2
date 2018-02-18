#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import urllib2
from subprocess import check_output

#We have to define our functions here.

def fetchURL(action,v1):
	try:
		url= str(action.split("\"")[1])
		url = url.replace("$1",str(v1))
		response = urllib2.urlopen(url)
		html = response.read()
		return "This is what I found:"+html
	except:
		return "No access to URL "+url
def grep(action,v1,v2):
	try:
		grep = 'grep "%s" /var/log/logstore/%s | head -10'%(v1 ,v2) 
		out = check_output(grep, shell=True)
		return "\nResults: \n"+out
	except:
		return "No permissions to this file or file does not exist"


def external(action,v1):
	try:
		exe= './external.sh %s %s'%(str(action.split("\"")[1]) ,v1) 
		print exe
		out = check_output(exe, shell=True)
		return "\nResults: \n"+out
	except:
		return "No permissions to this file or file does not exist"




