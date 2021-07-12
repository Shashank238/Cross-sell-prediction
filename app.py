from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__,template_folder='templates')
model = pickle.load(open("b_model.pkl", "rb"))
scaling=pickle.load(open("min_max.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("predict.html")



@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        
        gender=request.form["gender"]
        gen = 0
        if(gender == "female"):
            gen=1
        else:
            gen=0
        
        age1=request.form['age']
        age=int(age1)
        
        r_c=request.form['region']
        reg_code=int(r_c)
        
        prev=request.form['p_ins']
        prev_ins=0
        if(prev == "Yes"):
            prev_ins=1
        else:
            prev_ins=0
        
        vehicleage=request.form['v_age']
        vehicleage=float(vehicleage)
        veh_age=0
        if(vehicleage < 1):
            veh_age = 0
        elif (vehicleage > 2):
            veh_age = 2
        else:
            veh_age = 1
        
        vehicledam= request.form['v_dam']
        veh_dam = 0
        if(vehicledam=="Yes"):
            veh_dam = 1
        else:
            veh_dam = 0
        
        annprem = request.form['annual']
        anu_pre = float(annprem)
        
        pol=request.form['policy']
        poli=float(pol)
        
        vintage=request.form['vintage']
        vin=int(vintage)
        
        lst=[[gen,age,reg_code,prev_ins,veh_age,veh_dam,anu_pre,poli,vin]]
        df=pd.DataFrame(lst,columns=['gender','age','reg_code','prev','veh_age','veh_damage','annual','policy','vintage'])
        
        test=scaling.transform(df)
        
        pred=model.predict(test)
        
        result=""
        if(pred==1):
            result="Yes"
        else:
            result="No"
            
        return render_template("predict.html",prediction=result)
    
if __name__ == '__main__':
    app.run(debug=True,port=3000)
        
        
        
        
        
        
        
        
        
        
        
        
        