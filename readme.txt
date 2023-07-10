

https://www.youtube.com/watch?v=Z1RJmh_OqeA&list=PLri3-ylOnP9ZdJ2oymBUKJzcrl4Ylf-K6

https://flask.palletsprojects.com/en/2.0.x/quickstart/
gunicorn app:app
export FLASK_APP=app
flask run

https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog

https://github.com/knowledgefactory4u/python_flask_vueJs_mongoDB_CRUD


https://www.google.com/search?q=heroku+deploy+flask&oq=heroku+deploy+flask&aqs=chrome..69i57.6750j0j7&client=ms-android-samsung-ga-rev1&sourceid=chrome-mobile&ie=UTF-8


https://stackoverflow.com/questions/29386995/how-to-get-http-headers-in-flask

https://stackoverflow.com/questions/28323666/setting-environment-variables-in-heroku-for-flask-app

https://flask.palletsprojects.com/en/2.0.x/logging/

=================

https://stackabuse.com/deploying-a-flask-application-to-heroku/

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install flask
pip install gunicorn
gunicorn app:app --log-file=-   # python app.py
pip freeze > requirements.txt
git add commit push
deactivate # to exit venv

https://dashboard.heroku.com/apps/naturalingua/deploy/heroku-git
https://naturalingua.herokuapp.com/
https://naturalingua.netlify.app/

stripe listen --forward-to 127.0.0.1:5000/stripe_webhook
stripe listen --forward-to https://naturalingua.herokuapp.com/stripe_webhook


==============

heroku create
git push heroku main
heroku open
heroku logs --tail
(Procfile)
bundle install
heroku ps:scale web=1
bundle exec rake db:create db:migrate
heroku local web
heroku local
heroku addons
heroku config
heroku pg
heroku run rake db:migrate
heroku pg:psql






https://support.google.com/mail/answer/7126229


smtplib.SMTPAuthenticationError: (534, b'5.7.14 <https://accounts.google.com/signin/continue?sarp=1&scc=1&plt=AKgnsbt\n5.7.14 EkYY87hor3NRiM2GITt-NEQK7aviEWukg_aUW9PxiVsigwG1H-Cgn2D9hB_9_fzDHBSpK\n5.7.14 WQluiYvhLwoZSxwINoLE5MV0_dy8lbL9jCFPPcZxjN9SPVVzmdQTkGxO9lU-tGE6>\n5.7.14 Please log in via your web browser and then try again.\n5.7.14  Learn more at\n5.7.14  https://support.google.com/mail/answer/78754 n7-20020a5d5987000000b00207891050d4sm7953154wri.46 - gsmtp')



https://stackoverflow.com/questions/34926570/flask-securitys-flask-mail-registration-receives-smtplib-smtpauthenticationerro


https://security.google.com/settings/security/apppasswords


https://www.twilio.com/blog/2018/03/send-email-programmatically-with-gmail-python-and-flask.html