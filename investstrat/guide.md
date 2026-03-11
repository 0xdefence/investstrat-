As a developer, lots of your time will be spent navigating big data and APIs. 
In light of this, we would like you to code a system that pulls live Bitcoin (BTC) price data      (this can be at any time interval <= 15 minutes).

You should also take time to compute a SIMPLE 30-day moving average. From this, you can create a very basic long/short signal (If price is above moving avg —> Long indication OR If price is below moving avg —> Short Indication). 
With this in mind, you should print a log of the following: 

TIMESTAMP | LONG OR SHORT | PRICE VALUE | MOVING AVG VALUE

You should gather data over the course of 4 hours (in respect to the quality of results you get —> NO RESULTS = unacceptable, run testing again at a different date). 

Note: This can be done in any programming language of your choosing.

Languages to be used: 
Python
PostGreSQL 

APIs: 
CoinGecko 
