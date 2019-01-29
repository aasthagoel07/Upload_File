from flask import Flask, render_template, request, send_from_directory , redirect
from werkzeug import secure_filename
import os
from werkzeug import SharedDataMiddleware

app = Flask(__name__)
UPLOAD_FOLDER='files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload')
def upload_file():
   return render_template('form.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
	if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
	file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
	if file.filename == '':
		print('No selected file')
		return redirect(request.url)
	if request.method == 'POST':
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return 'Uploaded'

if __name__ == '__main__':
   app.run(debug = True)