# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_Moving_Average.ipynb (unless otherwise specified).

__all__ = ['simple', 'weighted', 'SMA', 'WMA']

# Cell
import numpy as np
from numba import jit
import pandas as pd

from time_series_model_basics import simulate_data

# Cell
@jit(nopython=True)
def simple(
    ts,
    n=1,
):

    l = len(ts)
    if n > l:
        raise Exception('n should be less than the length of the time-series')

    f = np.zeros((l,))
    f[:n] = np.full(n, np.nan)

    for i in range(l - n + 1):
        f[n + i] = np.mean(ts[i:n + i])
    return f

# Cell
@jit(nopython=True)
def weighted(
    ts,
    ws,
):

    l = len(ts)
    n = len(ws)
    w = np.sum(ws)

    if n > l:
        raise Exception('The length of ws should be less than the length of ts')

    f = np.zeros((l,))
    f[:n] = np.full(n, np.nan)

    for i in range(l - n + 1):
        f[n + i] = (1 / w) * np.dot(ws, ts[i:n + i])
    return f

# Cell
def SMA(*args, df=None, ts_col='time_series', **kwargs):
    """
    Forescasts  with Simple Moving Average

    -----
    Parameters
    -----
    df : DataFrame, default None. If df is None a dataframe
         with simulated data is generated.
    ts_col : str, default 'time_series'. The column name with the
         time series. Ignored if df is None.
    *args : int.  Each value represent a Moving
           Average Forecast and its corresponding
           window size
    **kwargs : passed to __pandas_time_series
    -------
    Returns
    -------
    tuple: First element is the Pandas Dataframe and the second
           is ploty's fig object
    """

    if len(args) == 0:
        raise Exception("list in *args should include at least one value")

    if df is None:
        df = simulate_data.pandas_time_series(**kwargs)

    ts = df[ts_col].to_numpy()
    for n in args:
        df[f'ma_{n}'] = simple(ts=ts, n=n)

    fig = df.plot(
        backend='plotly',
        title=f'Simple Moving Average',
    )

    fig.update_layout(template="plotly_dark",)

    return df, fig

# Cell
def WMA(*args, df=None, ts_col='time_series', **kwargs):
    """
    Forescasts with Weighted Moving Average

    -----
    Parameters
    -----
    df : DataFrame, default None. If df is None a dataframe
         with simulated data is generated.
    ts_col : str, default 'time_series'. The column name with the
         time series. Ignored if df is None.
    *args : int.  Each value represent a Moving
           Average Forecast and its corresponding
           window size
    **kwargs : passed to __pandas_time_series
    -------
    Returns
    -------
    tuple: First element is the Pandas Dataframe and the second
           is ploty's fig object
    """

    if len(args) == 0:
        raise Exception("list in *args should include at least one value")

    if df is None:
        df = simulate_data.pandas_time_series(**kwargs)

    ts = df[ts_col].to_numpy()
    for ws in args:
        nws = np.array(ws, dtype=float)
        df[f'weights_{ws}'] = weighted(ts=ts, ws=nws)

    fig = df.plot(
        backend='plotly',
        title=f'Weighted Moving Average',
    )

    fig.update_layout(template="plotly_dark",)

    return df, fig