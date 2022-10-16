import pandas as pd

def produce_data_from_first_difference(first_difference_data, original_data):
    
    produced_data = first_difference_data.cumsum().dropna() + original_data[0]
    # This Series is missing the first row. 
    # Get the first row from the original data 
    # and concatenate it to the produced data:
    first_row = original_data[original_data.index == original_data.index[0]]
    produced_data =  pd.concat([first_row, produced_data])
    
    return produced_data
    