# Demand-Price-prediction
Demand/Price prediction in a Monopolistic market using Naive Bayes Classification and KNN Algorithm

OVERVIEW
In a monopolistic market, brand loyalty is the key to market positioning. Since the scope, still
lying in an imperfect competition, a numerous firms have the right to “free entry and exit”, thus
affecting the position (either negative or positive) resulting in a price rise/fall.

ABSTRACT
Monopolistically competitive firms are inefficient, it is usually the case that the costs of
regulating prices for products sold in monopolistic competition exceed the benefits of such
regulation, which might lead to a decline in the firm’s capability to sustain itself (Total Revenue
is less than the Total Cost of Production), thus reaching the shutdown point.
We propose to design a model which given the factors of a specific product will give a
probabilistic review to its survival depending on numerous factors (Brand Loyalty, Market
Domination, Distribution Map etc. )
The first step would be to identify a suitable product which fulfills the specific requirements to
which we would be targeting on. The second step would be to gather data on related products
and their market history (Quantity expectation and not price expectation) .
The next step would be to identifying the long run and short run variables to factor into the
fuzzy based bayesian classification, which would then be vital for prediction. Once identified, a
mathematical model can be prepared for quantization/ standardization. That standardised
value can then be used to train a model which can in time and with use, accurately predict a
pattern.
Once the pattern (curve) is identified we can use simple differentiation to identify how accurate
our value is.

REQUIREMENTS
Python3, Pip3, Libraries(tkinter, Numpy, Pandas)

HOW TO RUN:
1. Download the file Two_Classifiers.py
2. Download the data set
3. Open the .py file with IDLE and run it.
4. If you have all the necessasry dependancies, it will open a new window.
5. In this window, simply browse and select the dataset.
6. 'Add Label' button will add a new field in which you can choose any column of the data set as your predictor.
7. Click on 'done' and in the second drop down, choose one of the unique values of the column selected in first dropdown.
8. You can add as many predictors you want by clicking on add label.
9. After you are done, click on 'check' button to see the results.
