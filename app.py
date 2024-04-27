from flask import *
from video_preprocess import video_preprocessing
app = Flask(__name__)
'''
SHOULD IMPLEMENT FOR FRAMES STILL '''
@app.route('/')
def index():
    return render_template('index.html')

ALLOWED_EXTENSIONS = ['mp4']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload",methods = ['POST'])
def upload():
    if 'video' not in request.files:
        return "NO video File found"
    video = request.files['video']
    if video.filename == "":
        return "NO video file selected"
    if video and allowed_file(video.filename):
        video.save('static/videos/' + video.filename)
        if video_preprocessing.empty_folder():
            return redirect(url_for("extract"))
        else:
            return "<h1> Error in the Folder"
    return "inavalid file type"
if __name__ == "__main__":
    app.run(debug=True)
