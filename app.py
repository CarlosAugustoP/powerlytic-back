from flask import Flask, jsonify, request 
import utils as utils
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/hourly_consumption', methods=['GET'])
def get_hourly_consumption():
    """
    Obter consumo horário
    ---
    responses:
      200:
        description: Consumo horário médio por eletrodomésticos e luzes
      500:
        description: Erro interno do servidor
    """
    try:
        data = utils.spend_by_hour()
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/compare_months', methods=['GET'])
def compare_months():
    """
    Comparar consumo entre dois meses
    ---
    parameters:
      - name: month1
        in: query
        type: integer
        required: true
        description: Primeiro mês (1 a 12)
      - name: year1
        in: query
        type: integer
        required: true
        description: Ano do primeiro mês
      - name: month2
        in: query
        type: integer
        required: true
        description: Segundo mês (1 a 12)
      - name: year2
        in: query
        type: integer
        required: true
        description: Ano do segundo mês
    responses:
      200:
        description: Comparação de consumo entre os meses especificados
      500:
        description: Erro interno do servidor
    """
    try:
        month1 = int(request.args.get('month1'))
        year1 = int(request.args.get('year1'))
        month2 = int(request.args.get('month2'))
        year2 = int(request.args.get('year2'))

        data = utils.compare_months(month1, year1, month2, year2)
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/calculate_appliance_contribution', methods=['GET'])
def calculate_appliance_contribution():
    """
    Calcular contribuição de eletrodomésticos no consumo total
    ---
    responses:
      200:
        description: Contribuição de cada eletrodoméstico no consumo total
      500:
        description: Erro interno do servidor
    """
    try:
        data = utils.calculate_appliance_contribution(utils.folder_path)
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

@app.route('/generate_tip', methods=['GET'])
def generate_tip():
    """
    Gerar dicas para reduzir consumo
    ---
    responses:
      200:
        description: Dicas baseadas no consumo atual
      500:
        description: Erro interno do servidor
    """
    try:
        data = utils.calculate_appliance_contribution(utils.folder_path)
        results = data['appliance_data']
        total_consumption = data['total_consumption']
        
        tips = utils.generate_user_tips(results, total_consumption)

        return jsonify({
            'status': 'success',
            'tips': tips
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_prediction', methods=['GET'])
def get_prediction():
    """
    Gerar previsão de consumo
    ---
    responses:
      200:
        description: Previsão de consumo para os próximos dias
      500:
        description: Erro interno do servidor
    """
    try:
        data = utils.generate_prediction()
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)