import os 
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


folder_path = os.path.join(os.path.dirname(__file__), 'sensores')

def analyze_correlations():
    """
    Gera e visualiza a matriz de correlação para as variáveis relevantes.
    """

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'powerlytic_train.csv'))

    variables = [
        'Appliances', 'lights', 'T1', 'RH_1', 'T2', 'RH_2', 'T3', 'RH_3',
        'T_out', 'RH_out', 'Windspeed', 'Visibility', 'Tdewpoint'
    ]

    df_filtered = df[variables]

    correlation_matrix = df_filtered.corr()

    return correlation_matrix

def spend_by_hour():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'powerlytic.csv'))
    df['date'] = pd.to_datetime(df['date'])
    df['hour'] = df['date'].dt.hour
    hourly_consumption = df.groupby('hour')[['Appliances', 'lights']].mean().reset_index()
    return hourly_consumption.to_dict(orient='records')
    
def compare_months(month1, year1, month2, year2):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'powerlytic.csv'))
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    monthly_consumption = df.groupby(['year', 'month'])[['Appliances', 'lights']].sum().reset_index()
    monthly_consumption['total_consumption'] = monthly_consumption['Appliances'] + monthly_consumption['lights']

    month1_data = monthly_consumption[(monthly_consumption['month'] == month1) & (monthly_consumption['year'] == year1)]
    month2_data = monthly_consumption[(monthly_consumption['month'] == month2) & (monthly_consumption['year'] == year2)]

    if month1_data.empty or month2_data.empty:
        raise ValueError('Um dos meses especificados não possui dados.')

    month1_consumption = int(month1_data['total_consumption'].values[0])
    month2_consumption = int(month2_data['total_consumption'].values[0])

    percentage_change = ((month2_consumption - month1_consumption) / month1_consumption) * 100

    return {
        'month1': {'year': year1, 'month': month1, 'total_consumption': month1_consumption},
        'month2': {'year': year2, 'month': month2, 'total_consumption': month2_consumption},
        'percentage_change': percentage_change
    }

def calculate_appliance_contribution(folder_path):
    results = {}
    total_consumption = 0

    files = os.listdir(folder_path)
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        mean_power = df['power'].mean()
        
        results[file] = {'mean_power': mean_power}
        total_consumption += mean_power

    for appliance, data in results.items():
        percentage = (data['mean_power'] / total_consumption) * 100
        results[appliance]['percentage'] = percentage

    return {
        'appliance_data': results,
        'total_consumption': total_consumption
    }

def generate_user_tips(results, total_consumption):

    tips = []
   
    max_consumption = max(results.items(), key=lambda x: x[1]['mean_power'])
    tips.append(
        f"O eletrodoméstico que mais consome energia é '{max_consumption[0]}' com {max_consumption[1]['mean_power']:.2f} kWh "
        f"({max_consumption[1]['percentage']:.2f}% do consumo total). Considere usá-lo com moderação."
    )

    for appliance, data in results.items():
        if data['percentage'] > 20:  
            tips.append(
                f"O '{appliance}' é responsável por {data['percentage']:.2f}% do consumo total. Considere avaliar o uso ou substituí-lo por uma versão mais eficiente."
            )

    
    for appliance, data in results.items():
        if data['percentage'] < 5:  
            tips.append(
                f"O '{appliance}' consome apenas {data['percentage']:.2f}% do total. É eficiente e não representa um grande impacto no consumo."
            )

    tips.append(
        f"O consumo total de energia é {total_consumption:.2f} kWh. Avalie o uso de aparelhos em horários de pico para reduzir custos."
    )

    return tips

def generate_prediction():
    powerlytic_train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'powerlytic_train.csv'))

    powerlytic_train['date'] = pd.to_datetime(powerlytic_train['date'])
    powerlytic_train.set_index('date', inplace=True)
    powerlytic_train = powerlytic_train.asfreq('D').sort_index()
    powerlytic_train.interpolate(method='linear', inplace=True)

    train_data = powerlytic_train['Appliances'].values
    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(train_data.reshape(-1, 1))

    sarima_order = (2, 1, 2)
    seasonal_order = (1, 1, 1, 12)
    model = SARIMAX(train_scaled, order=sarima_order, seasonal_order=seasonal_order, enforce_stationarity=False)
    model_fit = model.fit(disp=False)

    forecast_steps = 30
    forecast_scaled = model_fit.forecast(steps=forecast_steps)
    forecast = scaler.inverse_transform(forecast_scaled.reshape(-1, 1)).flatten()

    last_date = powerlytic_train.index[-1]
    forecast_dates = pd.date_range(start=last_date, periods=forecast_steps + 1, freq='D')[1:]

    prediction_data = [
        {"date": str(date), "forecast": round(value, 2)}
        for date, value in zip(forecast_dates, forecast)
    ]

    return prediction_data

def compare_weeks(week1, year1, week2, year2):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'powerlytic.csv'))
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['week'] = df['date'].dt.isocalendar().week

    weekly_consumption = df.groupby(['year', 'week'])[['Appliances', 'lights']].sum().reset_index()
    weekly_consumption['total_consumption'] = weekly_consumption['Appliances'] + weekly_consumption['lights']

    week1_data = weekly_consumption[(weekly_consumption['week'] == week1) & (weekly_consumption['year'] == year1)]
    week2_data = weekly_consumption[(weekly_consumption['week'] == week2) & (weekly_consumption['year'] == year2)]

    if week1_data.empty or week2_data.empty:
        raise ValueError('Uma das semanas especificadas não possui dados.')

    week1_consumption = int(week1_data['total_consumption'].values[0])
    week2_consumption = int(week2_data['total_consumption'].values[0])

    percentage_change = ((week2_consumption - week1_consumption) / week1_consumption) * 100

    return {
        'week1': {'year': year1, 'week': week1, 'total_consumption': week1_consumption},
        'week2': {'year': year2, 'week': week2, 'total_consumption': week2_consumption},
        'percentage_change': percentage_change
    }

def generate_multivariate_prediction():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'powerlytic_train.csv'))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df = df.asfreq('D').sort_index()
    df.fillna(method='ffill', inplace=True)
    
    exog_variables = ['T_out', 'RH_out', 'Windspeed', 'Visibility']
    df_exog = df[exog_variables]
    df_endog = df['Appliances']
    
    scaler = MinMaxScaler()
    df_endog_scaled = scaler.fit_transform(df_endog.values.reshape(-1, 1))
    
    model = SARIMAX(df_endog_scaled, exog=df_exog, order=(2, 1, 2), seasonal_order=(1, 1, 1, 12))
    model_fit = model.fit(disp=False)
    
    forecast_steps = 30
    
    last_exog = df_exog.iloc[-1]
    exog_forecast = pd.DataFrame([last_exog.values] * forecast_steps, columns=exog_variables)
    exog_forecast.index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
    
    forecast_scaled = model_fit.forecast(steps=forecast_steps, exog=exog_forecast)
    
    forecast = scaler.inverse_transform(forecast_scaled.values.reshape(-1, 1)).flatten()
    
    forecast_dates = exog_forecast.index
    
    prediction_data = [
        {"date": str(date.date()), "forecast": round(value, 2)}
        for date, value in zip(forecast_dates, forecast)
    ]
    
    return prediction_data

def evaluate_models():
    # Load the data
    df = pd.read_csv('powerlytic_train.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df = df.asfreq('D').sort_index()
    df.fillna(method='ffill', inplace=True)

    # Split the data into training and testing sets
    split_point = int(len(df) * 0.8)
    train = df.iloc[:split_point]
    test = df.iloc[split_point:]
    
    # Exogenous variables (predictors)
    exog_variables = ['T_out', 'RH_out', 'Windspeed', 'Visibility']
    X_train = train[exog_variables]
    X_test = test[exog_variables]
    
    # Endogenous variable (target)
    y_train = train['Appliances']
    y_test = test['Appliances']

    # Scale the endogenous variable
    scaler = MinMaxScaler()
    y_train_scaled = scaler.fit_transform(y_train.to_numpy().reshape(-1, 1))
    y_test_scaled = scaler.transform(y_test.to_numpy().reshape(-1, 1))

    # Model with exogenous variables
    sarimax_exog = SARIMAX(y_train_scaled, exog=X_train, order=(2, 1, 2), seasonal_order=(1, 1, 1, 12))
    model_exog_fit = sarimax_exog.fit(disp=False)

    # Forecast with exogenous variables
    forecast_exog_scaled = model_exog_fit.forecast(steps=len(X_test), exog=X_test)
    
    # Ensure forecast_exog_scaled is a NumPy array
    if isinstance(forecast_exog_scaled, pd.Series):
        forecast_exog_scaled = forecast_exog_scaled.values
    
    forecast_exog = scaler.inverse_transform(forecast_exog_scaled.reshape(-1, 1)).flatten()

    # Model without exogenous variables
    sarimax_no_exog = SARIMAX(y_train_scaled, order=(2, 1, 2), seasonal_order=(1, 1, 1, 12))
    model_no_exog_fit = sarimax_no_exog.fit(disp=False)

    # Forecast without exogenous variables
    forecast_no_exog_scaled = model_no_exog_fit.forecast(steps=len(y_test))
    
    # Ensure forecast_no_exog_scaled is a NumPy array
    if isinstance(forecast_no_exog_scaled, pd.Series):
        forecast_no_exog_scaled = forecast_no_exog_scaled.values
    
    forecast_no_exog = scaler.inverse_transform(forecast_no_exog_scaled.reshape(-1, 1)).flatten()

    # Evaluation metrics
    metrics = {
        "With Exogenous Variables": {
            "MAE": mean_absolute_error(y_test, forecast_exog),
            "RMSE": np.sqrt(mean_squared_error(y_test, forecast_exog)),
            "R2": r2_score(y_test, forecast_exog)
        },
        "Without Exogenous Variables": {
            "MAE": mean_absolute_error(y_test, forecast_no_exog),
            "RMSE": np.sqrt(mean_squared_error(y_test, forecast_no_exog)),
            "R2": r2_score(y_test, forecast_no_exog)
        }
    }

    return metrics