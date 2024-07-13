from flask import Flask, render_template, Response
from capture_overlay import generate_frames, overlay_active

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', overlay_active=0)

@app.route('/act_overlay') #'/act_overlay' 주소로 POST 요청이 들어오면 아래의 함수를 실행
def act_overlay():
    overlay_active = 1  #overlay active를 true로
    return ('', 204) #204 상태 코드는 성공했지만 내용이 없음을  의미

@app.route('/deact_overlay')
def deact_overlay():
    overlay_active = 0 #overlay active를 false로
    return ('', 204)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

