from flask import Flask,flash, request, make_response, render_template, redirect
import jwt

app = Flask(__name__)
app.config['my_session_COOKIE_PATH'] = '/'
app.secret_key="ajfjagflaljgfa"
SECRET_KEY="heysoumya"

users={}
passwords={}

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method=='POST':
        if "username" in request.form and "password" in request.form and "operator" in request.form:
            username=request.form["username"]
            password=request.form["password"]
            operator=request.form["operator"]
            if operator=="Login":
                if username in passwords and passwords[username]==password:
                    resp=make_response(redirect("/notes"))
                    token=jwt.encode({'username':username}, SECRET_KEY, "HS256")
                    resp.set_cookie('my_session', token,  path = '/')
                    return resp
                elif username in passwords and passwords[username]!=password:
                    flash("Incorrect details")
                    return redirect('/')
                else:
                    print(passwords)
                    flash("need to register first")
                    return redirect('/')
            else:
                if username not in passwords:
                    passwords[username]=password
                    flash("You are now registered! Login to continue")
                    return redirect('/')
                else:
                    flash("You are already registered!")
                    return redirect('/')
        else:
            flash("Enter username and password!")
            return redirect('/')
        
@app.route('/notes', methods=['GET','POST'])
def notes():
    my_session=request.cookies.get('my_session')
    if my_session:
        try:
            data=jwt.decode(jwt=my_session, key=SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            return f"Token is invalid {e}"   
        username=data["username"]
        if request.method=='GET':
            if username in users:
                return render_template("notes.html",notes=users[username])
            else:
                users[username]=[]
                return render_template("notes.html",notes=users[username])
        elif request.method=='POST':
            note=request.form["Note"]
            if username in users:
                users[username].append(note)
            else:
                users[username]=[note]
            return redirect("/notes")
    return redirect("/")

@app.route('/delete_note', methods=['POST'])
def delete_note():
    my_session = request.cookies.get('my_session')
    if my_session:
        try:
            data = jwt.decode(jwt=my_session, key=SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            return f"Token is invalid {e}"   
        username = data["username"]
        note_to_delete = request.form.get('note')
        if username in users and note_to_delete in users[username]:
            users[username].remove(note_to_delete)
    return redirect("/notes")


if __name__ == '__main__':
    app.run(debug=True)