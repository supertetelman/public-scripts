# Summary
This is a simple web crawler. It was originally created for a client but the code can easily be modified to suit a number of uses.

The idea is you have want to make many requests as quickly as possible for incrementing values.

The way this script is implemented is that it maintains a pool of 200 thread at all times, as soon as a thread completes it will get the next work item.

This code could easily be modified to crawl a site and grab, for example, all the product IDs from 0-10000 and save the output to a local file for future parsing.
