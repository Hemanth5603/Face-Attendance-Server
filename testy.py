
import sqlite3
from flask import *
from flask_mail import *
from VideoPreoprocess import VideoPreprocessor
from Face_recog_methods_2 import FaceRecognition
app = Flask(__name__)
app.secret_key = "i_am_ironman"
@app.route("/")
def head():
    return render_template("newForm.html")
@app.route('/video-upload')
def index():
    return render_template('index.html')

ALLOWED_EXTENSIONS = ['mp4']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/uploadStudentForm",methods = ["POST","GET"])
def uploadStudentForm():
    if request.method == "POST":
         name =  request.form["Name"]
         roll_no = request.form["Roll"]
         image_path = request.form["Image"]
         if fetchFromDataBase(roll_no):
             return jsonify("Already Present in the DataBase")
         new_student_encoding = FaceRecognition.load_new_student(image_path)
         if saveIntoDataBase(roll_no,name,new_student_encoding):
              return url_for('upload')
         return jsonify("Error in Details")
def saveIntoDataBase(roll,name,student_encoding):
    with sqlite3.connect('Attendance.db') as conn: 
        cursor = conn.cursor()
        encoded_string = "/".join([str(i) for i in student_encoding])
        try:
          cursor.execute('''INSERT INTO USERS (ROLL_NO ,NAME,FACE_ENCODINGS ) VALUES (?,?,?)''',(roll,name,encoded_string))
          conn.commit()
        except:
           return False 
    return True   
@app.route("/upload",methods = ['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify("NO video File found")
    video = request.files['video']
    if video.filename == "":
        return "NO video file selected"
    if video and allowed_file(video.filename):
        video.save('static/videos/' + video.filename)
        if VideoPreprocessor.empty_folder():
                VideoPreprocessor.extract_frames_per_second()
                images_paths = FaceRecognition.load_image_paths()
                final_face = FaceRecognition.find_faces(images_paths)
                attendees_list = FaceRecognition.compare_faces(final_face)
                return jsonify(attendees_list)
        return jsonify("Error in emptying the folder")
    return jsonify("inavalid file type")
def fetchFromDataBase(roll_no):
    with sqlite3.connect('Attendance.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM USERS ''')
        only_roll_list = [ i[0] for i in cursor]
        if roll_no in only_roll_list:
            return True 
        return False
def create_Table_inSqlite():
    with sqlite3.connect('Attendance.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE USERS (ROLL_NO VARCHAR(255) , NAME VARCHAR(255) , FACE_ENCODINGS TEXT(16000))''')
        print("SuccessFully Created The Table")
if __name__ == '__main__':
    app.run(debug=True)
    