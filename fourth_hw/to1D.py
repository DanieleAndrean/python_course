import pandas as pd
def to_1D(series):
 return pd.DataFrame(series.tolist())    