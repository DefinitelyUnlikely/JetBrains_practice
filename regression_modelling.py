import pandas
import numpy as np


class CustomLinearRegression:
    """
    Class implement model fitting for a given dataset or predict outcome based on a model.
    """

    def __init__(self, dataframe, fit_intercept=True):
        """

        @param dataframe: a pandas.Dataframe. y-values (dependent variable) is last row. X-matrix (independent values)
         are first rows.
        @param fit_intercept: specify if intercept is part of modelling or not. default is True.
        """
        self.fit_intercept = fit_intercept

        dataframe = dataframe.transpose()
        if fit_intercept:
            dataframe.insert(0, "ones", 1)
        self.X = np.array(dataframe.iloc[:, :-1])
        self.Y = np.array(dataframe.iloc[:, -1])

        self.beta = None
        self.intercept = None
        self.coefficient = None
        self.y_hat = None

    def fit(self):
        xt_at_x_inverse = np.linalg.inv(self.X.transpose() @ self.X)
        xt_by_y = self.X.transpose() @ self.Y

        self.beta = xt_at_x_inverse @ xt_by_y
        self.intercept, *self.coefficient = self.beta

    def predict(self):
        if not self.beta:
            self.fit()
        self.y_hat = self.X @ self.beta

    def r2_score(self):
        pass

    def rmse(self):
        pass
