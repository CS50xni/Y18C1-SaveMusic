from flask import Flask, Response, flash, render_template as render, redirect, url_for, request, Markup
from forms import RegistrationForm, LoginForm
from flask_s3 import FlaskS3
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './musica'
ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#app.config['FLASKS3_BUCKET_NAME'] = 'kavv'
#s3 = FlaskS3(app)

#s3 = FlaskS3()

#def start_app():
#	app = Flask(__name__)
#	s3.init_app(app)
#	return app

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = "AKIA5YLJSMZDIY7E6YOV"

@app.route('/', methods=['GET', 'POST'])
def index():
    return render('index.html')

def stream_library(library, **context):
	app.update_template_context(context)
	t = app.jinja_env.get_template(library)
	rv = t.stream(context)
	rv.enable_buffering(5)
	return rv

@app.route('/library')
def library():
	return render('library.html')

#def streamogg():
#	def generate():
#		with open("signals/song.ogg", "rb") as fogg:
#			data = fogg.read(1024)
#			while data:
#				yield data
#				data = fogg.read(1024)
#	return Response(generate(), mimetype="audio/ogg")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return '''
    <!doctype html>
    <title>Upload</title>
    <h1>Upload your Music Here</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash('Account created for {form.username.data}!', 'Success')
		return redirect(url_for('index'))
	return render('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('You have logged in!', 'success')
		return redirect(url_for('index'))
	return render('login.html', title='Login', form=form)