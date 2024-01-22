import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from flask_mail import Mail, Message
import pandas as pd

#loading env variables
load_dotenv()
# creating the flask app 
app = Flask(__name__) 
# creating an API object 
api = Api(app) 

app.config['MAIL_SERVER']=os.environ['MAIL_SERVER']
app.config['MAIL_PORT']=os.environ['MAIL_PORT']
app.config['MAIL_USERNAME']=os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD']= os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)

class check(Resource):
    def get(self):
        return jsonify({'result':'Service is live!'}) 

class student_invoice_emailer(Resource):

    def post(self):
        output=request.get_json()
        output=json.loads(output)
        print(output)
        msg = Message(
                "STUDENT INVOICE " + output['action'] +"# "+ output['output']['Invoice No.'],
                sender =os.environ['SENDER'],
                recipients = [os.environ['RECIPIENTS']]
               )  
        msg.body = " Please see the details below."
        msg.html = render_template("student_invoice_print_template.html", output=output['output'], image=output['img_url'])
        mail.send(msg)
        return jsonify({'message':'email sent'})
    
class school_principal_bill_emailer(Resource):

    def post(self):
        output=request.get_json()
        output=json.loads(output)
        header_data=output['header']
        product_data=json.loads(output['products'])
        product_data=pd.DataFrame(product_data, columns=product_data.keys())
        msg = Message(
                "BILL TO " +(header_data['school_name']).upper()+ " PRINCIPAL GENERATED# "+header_data['inv_no'],
                sender =os.environ['SENDER'],
                recipients = [os.environ['RECIPIENTS']]
               )
        msg.body = "Please see the details below."
        msg.html = render_template("pricipal_bill_print_template.html", header=header_data, products=product_data.to_html(classes='data', justify='center').replace('<th>','<th style = "background-color: rgb(173, 171, 171)">'), image=output['img_url'])
        mail.send(msg)
        return jsonify({'message':'email sent'})

class house_cover_emailer(Resource):

    def post(self):
        output=request.get_json()
        output=json.loads(output)
        header_data=output['header']
        house_data=json.loads(output['data'])
        house_data=pd.DataFrame(house_data, columns=house_data.keys())
        msg = Message(
               "HOUSE COVER PAGE GENERATED# ",
               sender =os.environ['SENDER'],
               recipients = [os.environ['RECIPIENTS']]
               )
        msg.body = "Please see the details below."
        msg.html = render_template("cover_page_print.html",house_name=output['house'], header=header_data, house_data=house_data.to_html(classes='data', justify='center').replace('<th>','<th style = "background-color: rgb(173, 171, 171)">'), image=output['img_url'])
        mail.send(msg)
        return jsonify({'message':'email sent'})

class delete_invoice_emailer(Resource):

    def post(self):
        output=request.get_json()
        output=json.loads(output)
        msg = Message(
                "STUDENT INVOICE# "+output+ " DELETED",
                sender =os.environ['SENDER'],
                recipients = [os.environ['RECIPIENTS']]
               )
        msg.body = " Student Invoice has been deleted from the database. Please note that this action is irreversible and if it was done by mistake then a new invoice needs to be generated"
        mail.send(msg)
        return jsonify({'message':'email sent'})

class update_tc_leave_status_emailer(Resource):

    def post(self):
        output=request.get_json()
        output=json.loads(output)
        msg = Message(
                "STUDENT INVOICE# "+output['inv_no']+ "SET AS TC/LEAVE "+str(output['tc_leave'])+ " IN THE DATABASE",
                sender =os.environ['SENDER'],
                recipients = [os.environ['RECIPIENTS']]
               )
        msg.body = " Student Invoice TC/Leave status has been changed"
        mail.send(msg)
        return jsonify({'message':'email sent'})

api.add_resource(check, '/check')
api.add_resource(student_invoice_emailer, '/student_invoice_emailer') 
api.add_resource(school_principal_bill_emailer, '/school_principal_bill_emailer') 
api.add_resource(house_cover_emailer, '/house_cover_emailer') 
api.add_resource(delete_invoice_emailer, '/delete_invoice_emailer')
api.add_resource(update_tc_leave_status_emailer, '/update_tc_leave_status_emailer')

if __name__ == '__main__': 
  
    #app.run(debug = True, host='127.1.1.3', port=8080) #local dev
    app.run(debug = True) #cloud run
