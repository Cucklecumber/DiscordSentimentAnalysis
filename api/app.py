########  imports  ##########
from flask import Flask, jsonify, request, render_template
from discord_conversation_rater import run


token = ''
channel_id = ''

total_predictions, user_prediction_scores, overall_judgement = run(token, channel_id)
app = Flask(__name__)

@app.route('/')
def home_page():
    example_embed = f'The final judgement: {overall_judgement} ------ Model prediction output (bad score, nuetral score, good score): {total_predictions} ------ Individual user output: {user_prediction_scores}'
    return render_template('index.html', embed=example_embed)

@app.route('/test', methods=['GET', 'POST'])
def testfn():
    # GET request
    if request.method == 'GET':
        message = {'greeting':total_predictions}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200

data = total_predictions 
app.run(debug=True)
