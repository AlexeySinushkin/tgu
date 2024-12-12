import pandas as pd
from scipy.signal import square


def r2_calc(y_true, y_pred):
  err = y_true - y_pred
  err = err*err

  mse = err.sum()/len(err)
  print(f'MSE {mse}')

  avg_true = y_true.sum()/len(y_true)
  err_mean = y_true - avg_true
  err_mean = err_mean * err_mean
  mse_mean = err_mean.sum()/len(err_mean)
  print(f'MSE mean {mse_mean}')

  r2 = 1 - mse/mse_mean
  print(f'r2 {r2}')


def rmse_calc(y_true, y_pred):
  err = y_true - y_pred
  err = err * err

  mse = err.sum() / len(err)
  rmse = mse ** 0.5
  print(f'MSE {mse}')
  print(f'RMSE {rmse}')

y_true = pd.Series([22.4, 20.6, 23.9, 22.0, 11.9])
y_pred = pd.Series([20.5, 20.2, 20.3, 19.0, 11.0])
r2_calc(y_true, y_pred)

y_true = pd.Series([1.23, 2.35, 2.75])
y_pred = pd.Series([1.01, 12.3, 2.74])
rmse_calc(y_true, y_pred)