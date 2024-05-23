from flask import Flask



app = Flask(__name__)

topics = [
    {'id':5,'title':'html','body':'html is ...'},
    {'id':2,'title':'css','body':'css is ...'},
    {'id':3,'title':'javascript','body':'javascript is ...'}, #나중에 DB로 바꿀 코드
]





@app.route('/')
def index():
    liTags =''
    for topic in topics:
        liTags = liTags + f'<li><a href ="/read/{topic["id"]}/">{topic["title"]}</a></li>'

    return f'''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title></title>
        </head>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {liTags}
            </ol>
            <h2> WELCOME </h2>
            Hello , web
        </body>
        </html>
    '''

@app.route('/create/')
def create():
    return 'Create'

@app.route('/read/<id>/') #변수 <id>
def read(id): #파라미터로 호출  같은 이름의 파라미터가 값을 받을수 있음
    print(id)
    return 'Read '+id


#어떤 요청을 어떤 함수가 응답 할것인가를 연결시켜주는 작업을 라우팅이라함
#이런 작업을 기술하는 어떤 것들을 라우터라 함

app.run(port = 5001) # 코드를 수정하면 자동으로 꺼졌다 켜짐 debug =True 에러도 난다.
