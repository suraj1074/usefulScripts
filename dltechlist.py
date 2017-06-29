import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
import threading

class myThread (threading.Thread):
   idCounter = 0
   def __init__(self):
      threading.Thread.__init__(self)
      self.threadID = myThread.idCounter
      self.name = "Thread" + "-" +str(myThread.idCounter)
      self.counter = myThread.idCounter
      myThread.idCounter = myThread.idCounter + 1
   
   def run(self):
      print "Starting " + self.name +"\n"
      # Get lock to synchronize threads
      threadLock.acquire()
      baseurl = get_first_url()
      # Free lock to release next thread
      threadLock.release()
      if(baseurl):
      	process_url(baseurl)

      threadLock.acquire()
      for i in xrange(max_threads):
      	if(len(links) != 0):
      		if(threading.activeCount() <= 2*max_threads):
      			thread = myThread()
      			thread.start()
      threadLock.release()

def get_first_url():
	if(len(links) != 0): 
		baseurl = links[0]
		del links[0]
		return baseurl
	else:
		return None

def process_url(baseurl):
	print "Trying for " + baseurl +"\n"
	response = urllib2.urlopen(baseurl)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	for link in soup.find_all('a'):
		if link.text.endswith("../"):
			pass
		elif link.text.endswith("/"):
			threadLock.acquire()
			links.append(urljoin(baseurl, link.get('href')))
			threadLock.release()
			print "from "+ threading.current_thread().name + "\t"+ urljoin(baseurl, link.get('href')),link.text + "\n"
		else:
			threadLock.acquire()
			to_write = link.text + " >> "  + urljoin(baseurl, link.get('href')) +"\n"
			to_write = to_write.encode('utf-8')
			output_file.write(to_write)
			threadLock.release()

def generate_html():
	movie_list = open("movie_list.txt","r")
	lines = movie_list.readlines()
	html_page = open("movie_list.html","w")
	first_line = "<table><tr><th>Movie name</th><th>Movie link</th></tr>\n"
	html_page.write(first_line)
	for line in lines:
		text, url = line.split(">>")[0],line.split(">>")[1]
		to_write = "<tr><th>"+text+"</th><th> <a href=\""+url+"\">this</a> </th></tr>\n"
		html_page.write(to_write)
	last_line = "</table>"
	html_page.write(last_line)
	html_page.close()

if __name__ == '__main__':
	url = "http://dl.tehmovies.com/"

	links = [url]
	output_file = open("movie_list.txt","w")

	counter = 1
	max_threads = 10

	threadLock = threading.Lock()

	thread = myThread()
	thread.start()


