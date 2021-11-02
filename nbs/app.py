from flask import Flask, render_template, request
import jsonify
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

#Load Flask
app = Flask(__name__)

#Load Model
model = pickle.load(open('rf_car_prediction.pkl', 'rb'))

#------------------------------ API CALLS ---------------------------------------
# home page
@app.route('/', methods=['GET'])
def Home():
    print('Home Call')
    return render_template('index.html')

# api call : Predict
standard_to = StandardScaler()
@app.route('/predict', methods=['POST'])
def predict():
    #Set Default values
    Fuel_Type_Diesel = 0
    Fuel_Type_Petrol = 0
    Seller_Type_Individual = 0
    Transmission_Manual = 0
    
    if request.method == 'POST':
        No_Of_Years = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        No_Of_Owners = int(request.form['Owner'])
        Transmision_Manual = 0
        
        #Fuel Type Check
        Fuel_Type = request.form['Fuel_Type_Petrol']
        if Fuel_Type == 'Petrol':
            Fuel_Type_Petrol = 1
        else:
            Fuel_Type_Diesel = 1
        
        #Seller Type Check
        Seller_Type = request.form['Seller_Type_Individual']    
        if Seller_Type == 'Individual':
            Seller_Type_Individual = 1
            
        #Transmission Check
        Transmission_Type = request.form['Transmission_Mannual']
        if Transmission_Type == 'Manual':
            Transmision_Manual = 1
            
        #Predict the Result
        selling_price_predicted = model.predict([[Present_Price, Kms_Driven, No_Of_Owners,  No_Of_Years, Fuel_Type_Diesel,
                      Fuel_Type_Petrol, Seller_Type_Individual, Transmision_Manual]])
        
        output = round(selling_price_predicted[0], 2)
        print('output : ', output)
        if output < 0:
            print('Render call 1')
            return render_template('index.html', prediction_text = 'Sorry you cannot sell this car')
        else:
            print('Render call 2')
            print(f'You can sell your car for {output} Lacs. :)')
            return render_template('index.html', prediction_text = 'You can sell your car for {}'.format(output))
    else:
        print('Render call 3')
        return render_template('index.html')
        
if __name__ == '__main__':
    app.run(debug=True)

            
        
        