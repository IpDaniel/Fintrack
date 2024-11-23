from dataclean import *
from modeling import *
import numpy as np
import matplotlib.pyplot as plt

def linear_regression(stock_df):
    independent_variables = [
        'Dividend_Rate',
        'PB_Ratio', 
        'PE_Ratio',
        'Dividend_Yield',
        'Beta',
        'Fifty_Two_Week_High',
        'Total_Revenue',
        'Profit_Margins',
        'Debt_to_Equity'
    ]

    # Convert dataframes to numpy arrays

    # The fundamental analysis variables
    x = stock_df[independent_variables].to_numpy()

    # The dependent variable
    y = stock_df['Returns'].to_numpy()

    # Add a column of ones to the independent variables to account for the intercept
    X = np.hstack([np.ones((x.shape[0], 1)), x])

    # We now need to minimize the sum of squared errors
    # This is done by taking the derivative of the sum of squared errors with respect to the beta vector and setting it to 0
    # When we solve for the Beta vector, this gives us the normal equation

    # Calculate the coefficients using the normal equation
    beta_vector = np.linalg.inv(X.T @ X) @ X.T @ y

    # X.T is the transpose of X
    # @ is the matrix multiplication operator
    # multplying a matrix by the transpose of another matrix is like "dividing" one matrix by the other
    # it is the inverse of the matrix multiplication

    # np.linalg.inv is the inverse of a matrix
    # The resulting vector represents the coefficients for each independent variable, with the first element being the intercept

    # Create dictionary mapping variables to their coefficients
    linear_equation = {'intercept': beta_vector[0]}
    linear_equation.update({var: beta_vector[i+1] for i, var in enumerate(independent_variables)})

    return linear_equation

def predict_returns(stock_df, linear_equation):
    independent_variables = list(linear_equation.keys())[1:]
    x = stock_df[independent_variables].to_numpy()

    # Add a column of ones to the independent variables to account for the intercept
    X = np.hstack([np.ones((x.shape[0], 1)), x])

    # Calculate the predicted returns
    predicted_returns = X @ np.array(list(linear_equation.values()))

    return predicted_returns

