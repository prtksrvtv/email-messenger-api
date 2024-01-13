import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from flask_mail import Mail, Message

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
    
api.add_resource(student_invoice_emailer, '/') 

if __name__ == '__main__': 
  
    #app.run(debug = True, host='127.1.1.3', port=8080) #local dev
    app.run(debug = True) #cloud run
