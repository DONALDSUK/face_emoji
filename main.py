from flask import Flask, render_template, Response
from capture_overlay import generate_frames
import capture_overlay

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reset_overlay')
def reset_overlay():
    capture_overlay.overlay_status=0
    return ('', 204)

@app.route('/cat_overlay') #'/act_overlay' 주소로 POST 요청이 들어오면 아래의 함수를 실행
def cat_overlay():
    capture_overlay.overlay_status=1
    return ('', 204) #204 상태 코드는 성공했지만 내용이 없음을  의미

@app.route('/fox_overlay')
def fox_overlay():
    capture_overlay.overlay_status=2
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)

