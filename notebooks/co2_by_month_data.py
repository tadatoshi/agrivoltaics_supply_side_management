import numpy as np
import pandas as pd

def co2_by_month_data():

    co2_by_month = pd.read_csv("../data/monthly_mauna_loa_co2_20220721.csv", 
                               comment='#')
    co2_by_month['year_string'] = co2_by_month['year'].astype(str)
    co2_by_month['month_string'] = co2_by_month['month'].astype(str)
    co2_by_month['date_month'] = pd.to_datetime(co2_by_month['year_string'] 
                                        + '/' + co2_by_month['month_string'])
    co2_by_month.set_index('date_month', drop=True, inplace=True)
    co2_by_month.drop(columns=['year', 'month', 'year_string', 
                               'month_string'], inplace=True)
    co2_by_month['CO2'] = co2_by_month['average'].astype(np.float32)
    co2_by_month.drop(columns=['decimal date', 'average', 'deseasonalized', 
                               'ndays', 'sdev', 'unc'], inplace=True)

    num_forecast_steps = 12 * 10 # Forecast the final ten years
    co2_by_month_training_data = co2_by_month[:-num_forecast_steps]
    co2_by_month_testing_data = co2_by_month[-num_forecast_steps:]
    
    num_forecast_steps = 12 * 10 # Forecast the final ten years
    trend_all = np.linspace(0., 1., len(co2_by_month))[..., None]
    trend_all = trend_all.astype(np.float32)
    seasonality_all = pd.get_dummies(
       co2_by_month.index.month).values.astype(np.float32)
    trend = trend_all[:-num_forecast_steps, :]
    seasonality = seasonality_all[:-num_forecast_steps, :]
    
    return (co2_by_month, co2_by_month_training_data, 
            co2_by_month_testing_data, trend_all, seasonality_all, 
            trend, seasonality)