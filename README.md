### Required dependencies
- pandas
- matplotlib
- seaborn
- numpy

## Mote Carlo Simulations
- a monte carlo simulation is used to determine a probability distribution of outcomes
based on repeated random sampling for multiple input variables. 
- For example, if we simplify it down to just a single input variable of yearly return, 
we can say that a stock has an average yearly return of 10% and a standard deviation of 20%.
- From there, we can simulate the yearly return of the stock multiple times by randomly sampling a value for yearly return from a normal distribution and applying it 10 years in a row.
- we can then create a probability distribution of the results and describe properties like "there is a 50% chance that the stock will have a 10 year return between 50% and 150%".
- If there are multple input variables, we can do the same thing, except we now sample from a multivariate normal distribution.
