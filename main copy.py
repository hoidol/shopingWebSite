from flask import Flask, render_template, request,redirect,url_for
import sys

app = Flask(__name__)

students_data = {
1 :{"name":"홍길동","score":{"국어":88,"영어":95}},
2 :{"name":"김철수","score":{"국어":62,"영어":12}},
3 :{"name":"이영희","score":{"국어":72,"영어":62}}
}

def list_function():
    str=""
    i = 3
    while i :
        str +=f"<li><a href='/'>{i}</a></li>"
        i = i-1       
    return str

app.jinja_env.globals.update(l_function=list_function)


@app.route("/")
def home():
    return render_template("children.html", 
    s_data = students_data) 

@app.route("/student/<int:key>/")
def student(key):
    print(key)
    print(students_data[key])
    print(students_data[key]['name'])
    print(students_data[key]['score'])
    return render_template("student.html", 
    name = students_data[key]['name'], 
    scores = students_data[key]['score'])  
    
@app.route("/addCustomerInfo/<id>", methods=["POST"]) # methods = ["GET"]   "GET", "POST"
def addCustomerInfo(id):

    print(id)
    print(request.method)

    #get 방식에서 받을 때
    nameGet = request.values.get('name')
    emailGet = request.values.get('email')
    phoneGet = request.values.get('phone')
    messageGet =request.values.get('message')

    print(nameGet, emailGet, phoneGet, messageGet)

    #Post 방식에서 받을때
   #방법 1
    name1 = request.values.get('name')

    #방법2
    name2 = request.form['name']

    #방법3
    name3 = request.form.get('name') # 키가 존재하지 않을 수도 있다면 사용

    #방법4
    name4 = request.form.getlist('name') #  키가 여러번 전송되고 값의 리스트를 원하면 사용
    
    print(name1 , name2 , name3 , name4)

    if request.method == 'GET' :
        #Get 으로 전달
        return "GET"
    else : 
        #Post로 전달
        return "POST"


    pass

topics = [
    {'id':1,'title':'html','body':'html is...'},
    {'id':2,'title':'css','body':'css is...'},
    {'id':3,'title':'javascript','body':'javascript is...'}
]

portfolioList =[
    {'id':0,'imgPath':'assets/img/portfolio/1.jpg','title':'0','content':'test0','body':'bodytest0'},
    {'id':1,'imgPath':'assets/img/portfolio/2.jpg','title':'1','content':'test1','body':'bodytest1'},
    {'id':2,'imgPath':'assets/img/portfolio/3.jpg','title':'2','content':'test2','body':'bodytest2'},
    {'id':3,'imgPath':'assets/img/portfolio/4.jpg','title':'3','content':'test3','body':'bodytest3'},
    {'id':4,'imgPath':'assets/img/portfolio/5.jpg','title':'4','content':'test4','body':'bodytest4'},
    {'id':5,'imgPath':'assets/img/portfolio/6.jpg','title':'5','content':'test5','body':'bodytest5'},

]

globalInt =10
globalStr = '안녕하세요'

def logGlobal():
    global globalInt,globalStr

    print(f'globalInt {globalInt}')
    print(f'globalStr {globalStr}')
    return  

def intFunction(intValue):
    print(f'intFunction {intValue}')
    return intValue

def getContents():
     liTags = ''
    #  for topic in topics:
    #     liTags += f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
     
     for topic in topics:
        liTags += f'<li><a href= {url_for("read",id = topic["id"])}>{topic["title"]}</a></li>'
        
     return liTags


def template(contents, body, id=None):
    contextUI=''
    if id !=None:
        contextUI=f'''
            <li><a href="/update/{id}/">update</a></li>
        <li><form method='POST' action = '/delete/{id}'> <input type='submit' value ='delete'></form></li>
        '''
    else:
        contextUI= f'''
        <li><a href="/create/">create</a></li>
        '''


    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href ="/">WEB</a></h1>
            <ol>
            {contents}
            </ol>
            {body}
            <ul>
                {contextUI}
            </ul>
        </body>

    </html>
    '''


def GetTopic(id):

    if type(id) != int :
        print(f'{id} {type(id)}')
        id =int(id)
        print(f'{id} {type(id)}')

    for list in topics:
        if list['id'] == id:
            return list

    return None
    
@app.route("/create/", methods=['GET','POST']) 
def create():     
    if request.method == 'GET':
        content ='''
            <form action="/create/" method = 'POST'>
                <p><input type="text" name="title" placeholder = 'title'></p>
                <p><textarea  name="body"></textarea></p>
                <p><input type="submit" value = "create"></p>
            </form>
        '''
        return template(getContents(),content) 
    elif request.method == 'POST':        
        title = request.form['title']
        body = request.form['body']

        print(len(topics)+1)

        addInfo = {'id':len(topics)+1,'title':title,'body':body }
        topics.append(addInfo)
        return redirect(f"/read/{addInfo['id']}")

@app.route('/update/<id>/', methods=['GET','POST'])
def update(id):
    tTopic = GetTopic(id)
    idInt = int(id)
    if request.method == 'GET':
        content =f'''
            <form action="/update/{id}" method = 'POST'>
                <p><input type="text" name="title" placeholder = 'title' value = '{tTopic['title']}'></p>
                <p><textarea  name="body" placeholder='body' >{tTopic['body']}</textarea></p>
                <p><input type="submit" value = "update"></p>
            </form>
        '''
        return template(getContents(),content) 
    elif request.method == 'POST':        
        title = request.form['title']
        body = request.form['body']
        print(" update request.method == POST" )

        

        tTopic['title'] = title
        tTopic['body'] = body

        return redirect(url_for("read", id =str(idInt)))
@app.route('/delete/<id>',methods=['POST'])
def delete(id):
    id = int(id)
    targetTopic = GetTopic(id)
    topics.remove(targetTopic)
    
    return redirect('/')
@app.route("/read/<id>/" ) 
def read(id): # 변수는 받을 수 있는 파라미터 선언 필요
    
    print(id)
    print(type(id))  

    idInt = int(id) 
    targetData ={}
    for list in topics:
        if list['id'] == idInt :
            targetData = list
            break    
    # print(targetData)
    return template(getContents(),
    f'''<h2>{targetData["title"]}</h2>
            {targetData["body"]}''',list['id']) 


# @app.route('/')
# def index():   
#     return template(getContents(),
#     '''<h2>welcome</h2>
#             Hello,web''') 
            
            


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug =True)
