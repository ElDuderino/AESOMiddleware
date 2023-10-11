# AESOMiddleware
Middleware for the AESO API

AESO (Alberta Electric System Operator) provides realtime and historical pricing for the Alberta energy market. 

In order to build forecasting and realtime buy/sell models with this data, it's useful to bring the historical pricing data
into the Aretas Platform and then continuously update the pricing data. 

We can then use the ASN platform API to run energy price predictions, forecasting and run custom analytics, alerts, etc. 

Even more importantly, we can feed the realtime data into our forecasting microservices and perform just-in-time forecasts for peak and minimum energy price hours. 

Then, we can execute arb strategies and monitor performance in realtime as well.

More documentation to come.
