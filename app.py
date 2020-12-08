from flask import Flask,abort,render_template,request,redirect,url_for,send_from_directory,Response
import os
import main
import detect2
import pandas as pd
import webbrowser
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER    #Uploading Files through website
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route('/')
def index():
    if os.path.exists("static/images/test4.jpg"):
        os.remove("static/images/test4.jpg")
    return redirect(url_for('upload_file'))


@app.route('/casestudy1/',methods = ['GET','POST'])
def hello1(name = None):
    return render_template('dwnld.html',name=name)

@app.route('/casestudy2/',methods = ['GET','POST'])
def hello2(name = None):
    full_filename='/static/images/test4.jpg'
    return webbrowser.open_new_tab('dwnld2.html',name=name,user_image = full_filename)

@app.route('/trinityIMG2EXCEL/',methods = ['GET','POST'])
def upload_file():
    if request.method =='POST':
        optn=request.form.get('options')
        print(optn)
        file = request.files['file']
        if file:
            filename = file.filename
            location=UPLOAD_FOLDER+'/'+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            if(optn=='op1'):
                main.convertndocr(location)
                main.deletedir()
                return redirect(url_for('hello1'))
            elif(optn=='op2'):
                img_loc=main.alltoexcel(location)
                print(img_loc)
                detect2.detectshapescs2(img_loc)
                main.deletedir()
                return redirect(url_for('hello2'))
    return render_template('index.html')


@app.route("/getfile1/",methods=['GET'])                #Case Study 1 Path
def getPlotDOC():
    with open("file.doc") as fp:
        docc = fp.read()
    return Response(
        docc,
        mimetype="text/plain",
        headers={"Content-disposition":
                 "attachment; filename=file.doc"})

@app.route("/getfile2/",methods=['GET'])                 #Case Study 2 Path
def getPlotXL():
    excelDownload = open("test.xls",'rb').read()
    return Response(
        excelDownload,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-disposition":
                 "attachment; filename=test.xls"})

if __name__ == '__main__':
    app.run(debug = False,host='0.0.0.0', port=5000)        #Flask Server run