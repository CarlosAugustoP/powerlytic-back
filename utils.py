import pandas as pd
import os 

folder_path = os.path.join(os.path.dirname(__file__), 'sensores')

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
