from flask import Flask, render_template,request
import pickle
import numpy as np

app = Flask(__name__)

def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value
    
@app.route('/', methods=['POST','GET'])
def index():
    pred = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename= request.form['typename']
        operatingsystem= request.form['operatingsystem']
        cpuname= request.form['cpuname']
        gpuname= request.form['gpuname']
        touchscreen= request.form.getlist('touchscreen')
        ips= request.form.getlist('ips')
       
        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        Company_list = ['Acer','Apple','Asus','Dell','HP','Lenovo','MSI','other','Toshiba']
        TypeName_list =['2in1Convertible','Gaming','Netbook','Notebook','Ultrabook','Workstation']
        OpSys_list =['Linux','Mac','Other','Windows']
        cpu_list = ['AMD','IntelCorei3','IntelCorei5','IntelCorei7','Other']
        gpu_list = ['AMD','Intel','Nvidia']

        def traverse(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        
        traverse(Company_list, company)
        traverse(TypeName_list, typename)
        traverse(OpSys_list,operatingsystem)
        traverse(cpu_list, cpuname)
        traverse(gpu_list, gpuname)

        pred = prediction(feature_list)*219
        pred = np.round(pred[0])

    return render_template('index.html', pred=pred)


if __name__ == "__main__":
    app.run(debug=True)

