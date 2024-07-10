from flask import Flask, render_template, Response, request
import threading
from capture_overlay import generate_frames, overlay_active

app = Flask(__name__)

@app.route('/toggle_overlay', methods=['POST']) #'/toggle_overlay' 주소로 POST 요청이 들어오면 아래의 함수를 실행
def toggle_overlay():
    if overlay_active.is_set():  #overlay_active 라는 것이 있다면 
        overlay_active.clear()  #비활성화 상태로 만듬
    else:   
        overlay_active.set() # 아니라면 활성화 상태로 만듬
    return ('', 204)  #204 상태 코드는 성공했지만 내용이 없음을  의미

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
