########  imports  ##########
from flask import Flask, jsonify, request, render_template
from discord_conversation_rater import total_predictions, user_prediction_scores


app = Flask(__name__)

@app.route('/')
def home_page():
    example_embed='This string is from python'
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

@app.route('/getdata/<index_no>', methods=['GET','POST'])
def data_get(index_no):
    
    if request.method == 'POST': # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200
    
    else: # GET request
        return str(data)

data = total_predictions 
app.run(debug=True)