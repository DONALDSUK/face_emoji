from flask import Flask, render_template, Response
from animal_overlay_filter import generate_frames
import animal_overlay_filter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reset_overlay')
def reset_overlay():
    animal_overlay_filter.overlay_status=0
    return ('', 204)

@app.route('/cat_overlay')
def cat_overlay():
    animal_overlay_filter.overlay_status=1
    return ('', 204)

@app.route('/fox_overlay')
def fox_overlay():
    animal_overlay_filter.overlay_status=2
    return ('', 204)


if __name__ == '__main__':
    app.run(debug=True)

