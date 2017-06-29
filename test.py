import urllib2
import time
import datetime
import subprocess

def show_popup():
	subprocess.call("osascript -e'display dialog \"Probably Result is out ...\" with title \"Test output\"'", shell=True)

def check():
	old_html = "hello"
	while True:
		url = "http://utkaluniversity.nic.in/"
		response = urllib2.urlopen(url)
		html = response.read()
		if(old_html != html):
			print "html has changed at " + str(datetime.datetime.now())
			show_popup()
		else:
			print "html has not changed " + str(datetime.datetime.now())
		old_html = html
		time.sleep(60)

check()