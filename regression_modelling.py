import pandas
import numpy as np


class CustomLinearRegression:
    """
    Class implement model fitting for a given dataset or predict outcome based on a model.
    """

    def __init__(self, dataframe, fit_intercept=True, transpose=True):
        """

        @param dataframe: a pandas.Dataframe. y-values (dependent variable) is last row. X-matrix (independent values)
         are first rows.
        @param fit_intercept: specify if intercept is part of modelling or not. default is True.
        @param transpose: If dataframe has variable data in rows, keep default. If y in separate column, set as False.
        """
        self.fit_intercept = fit_intercept

        if transpose:
            dataframe = dataframe.transpose()
        if fit_intercept:
            dataframe.insert(0, "ones", 1)
        self.X = np.array(dataframe.iloc[:, :-1])
        self.Y = np.array(dataframe.iloc[:, -1])

        self.beta = None
        self.intercept = None
        self.coefficient = None
        self.y_hat = None
        self.r2_score = None
        self.rmse_score = None

    def fit(self):
        xt_at_x_inverse = np.linalg.inv(self.X.transpose() @ self.X)
        xt_by_y = self.X.transpose() @ self.Y

        self.beta = xt_at_x_inverse @ xt_by_y
        self.intercept, *self.coefficient = self.beta

    def predict(self):
        if self.beta is None:
            self.fit()
        self.y_hat = self.X @ self.beta

    def r2(self):
        if self.y_hat is None:
            self.predict()

        nominator = sum([(i - j) ** 2 for i, j in zip(self.Y, self.y_hat)])
        denominator = sum([(i - self.Y.mean()) ** 2 for i in self.Y])

        self.r2_score: float = 1 - (nominator / denominator)

    def rmse(self):
        if self.y_hat is None:
            self.predict()
        self.rmse_score = (sum([(i - j) ** 2 for i, j in zip(self.Y, self.y_hat)]) / len(self.Y)) ** 0.5
