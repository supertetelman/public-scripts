#/usr/bin/env python
'''This is a basic script created for Upwork.

The script will maintain a pool of THREAD_COUNT threads, each thread will make BATCH_SIZE calls to a website.

The calls made to the website will be a query, each query will be for a number START to END.

Note: because of how fast these threads are kicked off some HTTP/HTTPS errors might occur.
   If that is the case try reducing the BATCH_SIZE or THREAD_COUNT a bit to limit your traffic.

'''

import threading
import requests
import os
import time
import random


THREAD_COUNT = 200
BATCH_SIZE = 10
START = 0
END = 1839379
SITE = "https://www.google.com/?q="


class Worker(threading.Thread):
    '''Main worker, does a requests to site followed by a echo from start to end times'''
    count = 0
    def __init__(self, start, end, site):
        self._start = start
	self._end = end
	self._site = site
	threading.Thread.__init__(self)

    def run(self):
        for i in xrange(self._start, self._end):
            r = requests.get(self._site + str(i))
            os.system('echo 1')
	    Worker.count += 1


def cap_val(val, inc, end):
    '''Increment the start val, and return start + the increment or end depending on what is greater'''
    return min(val + inc + 1, end)


def inc_start(start, batch):
    '''Increment the starting value for the next thread that will be started'''
    return start + batch + 1


def main(start, end, site, thread_count, batch):
    '''Maintain 200 worker threads at all time'''
    threads = []
    end += 1 # enforce inclusivness for the very last value
    for i in xrange(0,thread_count): # XXX: Create initial threads
        thread = Worker(start, cap_val(start, batch, end), site)
	start = inc_start(start, batch)
	thread.start()
	threads.append(thread)
    while start <= end: 
        for thread in threads: # XXX: If a single thread completes kick off a replacement
	    if not thread.is_alive():
	        threads.remove(thread)
                thread = Worker(start, cap_val(start, batch, end), site)
		thread.start()
		threads.append(thread)
	        start = inc_start(start, batch)
    for thread in threads: # XXX: Wait for all threads to finish
        thread.join()
    print "ran a total of %d times" %(Worker.count)
    assert Worker.count == end # XXX: Verify we ran the correct # of threads


def test():
    '''Quick function to test the code'''
    assert cap_val(0,10,100) == 11
    assert cap_val(0,100,10) == 10
    assert cap_val(0,10,10) == 10

    assert inc_start(0,10) == 11

    t = Worker(0,2,'test')
    p = Worker(2,4,'test')
    t.start()
    p.start()
    t.join()
    p.join()
    assert p.count == 4
    print "script passed testing"


if __name__ == '__main__':
    #test()
    main(START, END, SITE, THREAD_COUNT, BATCH_SIZE)
