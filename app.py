from flask import Flask, render_template, url_for, jsonify, request, abort
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
from flask_cors import CORS
import pickle
import stripe
# import emails
# from flask_emails import Message

import logging
import boto3
from botocore.exceptions import ClientError
import requests
import os

def get_object(filename):
	with open(filename, 'rb') as input:
		return pickle.load(input)

load_dotenv('.env')
app = Flask(__name__)
CORS(app)

# app.config['EMAIL']=os.environ.get('EMAIL')
# app.config['PASSWORD']=os.environ.get('PASSWORD')
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
app.config['PUBLISHABLE_KEY']=os.environ.get('PUBLISHABLE_KEY')
app.config['AWS_ACCESS_KEY_ID'] = os.environ['AWS_ACCESS_KEY_ID']
app.config['AWS_SECRET_ACCESS_KEY'] = os.environ['AWS_SECRET_ACCESS_KEY']
app.config['prices']=get_object('products.pkl')
# app.config['EMAIL_HOST']= 'smtp.gmail.com' 
# app.config['EMAIL_PORT']= 25
# app.config['EMAIL_TIMEOUT']= 30
# app.config['EMAIL_HOST_USER']= 'naturalingua.noreply@gmail.com'
# app.config['EMAIL_HOST_PASSWORD']= 'gloubiboulga123.M'
# app.config['EMAIL_USE_SSL']= True
# app.config['EMAIL_USE_TLS']= False

app.config['client'] = boto3.client('s3',
		region_name='eu-west-3',
		aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
		aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],)

app.config.update(dict(
	DEBUG = True,
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 465,
	MAIL_USE_TLS = False,
	MAIL_USE_SSL = True,
	MAIL_USERNAME = 'naturalingua.noreply@gmail.com', # app.config['EMAIL'],
	MAIL_PASSWORD = 'gloubiboulga123.M' # app.config['PASSWORD']
))

mail = Mail(app)

stripe.api_key = app.config['SECRET_KEY']


# @app.route('/', methods=['GET'])
# def index():
# 	myString=render_template('index.html', email='salut')
# 	# app.logger.info(f'email : {email}')
# 	return myString


# https://stackoverflow.com/questions/26980713/solve-cross-origin-resource-sharing-with-flask
@app.route('/stripe_pay/<id>/<email>', methods=['GET'])
def stripe_pay(id, email):
	id=str(id)
	email=str(email)
	if(not id in app.config['prices']):
		abort(400)
	product = app.config['prices'][id]
	fileName=str(product['name'])
	language=str(product['language'])
	docType=str(product['category'])
	channel=str(product['channel'])
	myPrice=product['price']
	priceId='price_1KIxBfL309RW9KQTeeiAZIUp'
	if(myPrice == 3):
		priceId='price_1KIxC7L309RW9KQT4etnStC1'
	# elif myPrice == 7:
	# 	priceId='price_1KDuC3L309RW9KQTNFw1YVhG'
	# https://stripe.com/docs/api/checkout/sessions/create?lang=python
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price': priceId,
			'quantity': 1,
		}],
		metadata={
			"language": language,
			"docType": docType,
			"fileName": fileName,
			"id": id,
			"typePurchase":'document'
		},
		customer_email=email,
		mode='payment',
		success_url=f'https://naturalingua.netlify.app/success/{email}',
		cancel_url='https://naturalingua.netlify.app/cancel' 
	)
	#url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
	#url_for('index', _external=True),
	response=jsonify({
		'checkout_session_id': session['id'], 
	})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response



def create_presigned_url(bucket_name, object_name, expiration=86400):
	try:
		response = app.config['client'].generate_presigned_url('get_object', Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)
	except ClientError as e:
		logging.error(e)
		return None
	return response

# def createMessage(html, subject):
# 	# emails.Message(text=T("Build passed: {{ project_name }} ..."),
# 	m = Message(html=html,
# 										subject=subject,
# 										mail_from=("naturalingua.noreply", "naturalingua.noreply@gmail.com"))
# 	return m

# def sendEmail(message, clientEmail):
# 	# m.send(render={"project_name": "user/project1", "build_id": 121},
# 	# 'port': 465, 'ssl': True,
# 	response = message.send(to=clientEmail,
#                   smtp={"host": "smtp.gmail.com",
# 												"port": 587, 
# 												'ssl': False,
# 												'tls': True,
# 												'user': 'naturalingua.noreply@gmail.com',
# 												'password': 'gloubiboulga123.M'})
# 	return response

# https://myaccount.google.com/lesssecureapps
# https://accounts.google.com/DisplayUnlockCaptcha
# https://mail.google.com/mail/u/0/#settings/fwdandpop
# def send(mydocument, customerEmail, fileName):
# 	url = create_presigned_url('naturalingua', mydocument)
# 	myString=render_template('index.html', url=url, fileName=fileName)
# 	email=app.config['MAIL_USERNAME']
# 	msg = Message(subject="Your document",
# 		body='',
# 		sender=email,
# 		recipients=[customerEmail])
# 	msg.html=myString
# 	mail.send(msg)


# @app.route('/test', methods=['GET'])
# def test():
# 	msg = Message(subject="Your document",
# 		body='',
# 		recipients=["nicolas.klarsfeld@gmail.com"],
# 		sender="naturalingua.noreply@gmail.com")
# 	msg.html = "<html>testing</html>"
# 	mail.send(msg)
# 	return {}


@app.route('/turlututu', methods=['POST'])
def stripe_webhook():
	print('WEBHOOK CALLED')
	if request.content_length > 1024 * 1024:
		print('REQUEST TOO BIG')
		abort(400)
	payload = request.get_data()
	sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
	endpoint_secret = 'whsec_cH3dNK4afiMjAhEfPiF0IiB149eErlNe'
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, endpoint_secret
		)
	except ValueError as e:
		# Invalid payload
		print('INVALID PAYLOAD')
		return {}, 400
	except stripe.error.SignatureVerificationError as e:
		# Invalid signature
		print('INVALID SIGNATURE')
		return {}, 400
    # Handle the checkout.session.completed event
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		print(session)
		line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
		print(line_items['data'][0]['description'])
		typePurchase = session['metadata']['typePurchase']
		isDocumentPurchase = (typePurchase == 'document')
		if not isDocumentPurchase:
			return {}
		language=session['metadata']['language']
		docType=session['metadata']['docType']
		fileName=session['metadata']['fileName']
		id=session['metadata']['id']
		if(not id in app.config['prices']):
			return {}
		mydocument=f"toEnglish/{language}/{docType}/{fileName}"
		customerEmail=session['customer_email']
		url = create_presigned_url('naturalingua', mydocument)
		myString=render_template('index.html', url=url, fileName=fileName)
		# email=app.config['MAIL_USERNAME']
		msg = Message(subject="Your document",
			body='',
			sender='naturalingua.noreply@gmail.com',
			recipients=[customerEmail])
		msg.html=myString
		mail.send(msg)
		# send(mydocument, customerEmail, fileName)
	return {}


if __name__ == '__main__':
	app.run()





	# message = Message(html='allo',
	# 						subject='hehe',
	# 						mail_from=("naturalingua.noreply", "naturalingua.noreply@gmail.com"))
	# response = sendEmail(message, 'nicolas.klarsfeld@gmail.com')
	# response = message.send(to=("nicoco", 'nicolas.klarsfeld@gmail.com'))
	# return {'coucou': response.status_code}
