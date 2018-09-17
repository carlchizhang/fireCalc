# What is fireCalc?

FireCalc is a simple Monte Carlo retirement finances portfolio simulator. You put in the parameters, and you get the charts.

## About the code

The app is built in Python and Javascript. Most of this app is built with Django, with Chart.js supplying front-end charts.
Data is drawn from historical S&P500 values as well as data from [Professor Robert Shiller](http://www.econ.yale.edu/~shiller/data.htm).
The code generates a histogram from historical values and uses the histogram to generate possible future portfolio values.

Note. Historical performance is not a sufficient indicator of future performance.
