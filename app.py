from flask import Flask, jsonify, request 
import utils as utils

app = Flask(__name__)

@app.route('/hourly_consumption', methods=['GET'])
def get_hourly_consumption():
    try:
        data = utils.spend_by_hour()
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/compare_months', methods=['GET'])
def compare_months():
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
    try:
        data = utils.calculate_appliance_contribution(utils.folder_path)
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

@app.route('/generate_tip', methods=['GET'])
def generate_tip():
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

if __name__ == '__main__':
    app.run(debug=True)