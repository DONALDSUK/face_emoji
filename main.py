# main.py
from flask import Flask, render_template, Response
from capture_overlay import generate_frames
from first import main_frames

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(main_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_cat')
def video_cat():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
