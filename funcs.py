import numpy as np 

def currency_convert(col):
    col = col.replace('N/A', np.nan)
    col = col.replace('[\$,)]', '', regex=True)
    col = col.replace('\(', '-', regex=True)
    col = col.replace('',np.nan)
    col = col.astype(float)
    return col