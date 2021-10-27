from flask import Flask , render_template  , request , flash ,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager ,login_user ,UserMixin ,logout_user
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    fname = db.Column(db.String(120),  nullable=False)
    lname = db.Column(db.String(120),  nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),  nullable=False)
    city = db.Column(db.String(120),  nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Blog(db.Model):
    blog_id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(80),  nullable=False)
    author = db.Column(db.String(50),  nullable=False)
    content = db.Column(db.Text(),  nullable=False)
    pub_date = db.Column(db.DateTime(),  nullable=False , default = datetime.utcnow)

    def __repr__(self):
        return '<Blog %r>' % self.title


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/main")
def main():
    return render_template('main.html')

@app.route("/")
def index():
    data = Blog.query.all()
    return render_template('index.html',data = data)

@app.route("/register" , methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        password = request.form.get('password')
        city = request.form.get('city')
        email = request.form.get('email')
        user = User(fname=fname,lname = lname , username = username , password = password ,city = city,email = email)
        db.session.add(user)
        db.session.commit()
        flash ('user has been registered succesfully','sucess')
        return redirect ('/login')

    return render_template('register.html')

@app.route("/login", methods = ['GET','POST'] )
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect('/')
        else:
            flash('invalid credentials','danger')
            return redirect('/login')

    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@app.route("/blogpost" , methods = ['GET','POST'])
def blogpost():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        blog = Blog(title=title,author=author,content=content)
        db.session.add(blog)
        db.session.commit()
        flash ("your post has been submitted","success")
        return redirect('/')
    return render_template('blog.html')

@app.route("/blog_detail/<int:id>" , methods = ['GET','POST'])
def blogdetail(id):
    blog = Blog.query.get(id)
    return render_template('blog_detail.html',blog=blog)

@app.route("/delete/<int:id>" , methods = ['GET','POST'])
def blogdelete(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash('post has been deleted','success')
    return redirect('/')

@app.route("/update/<int:id>" , methods = ['GET','POST'])
def blogupdate(id):
    blog = Blog.query.get(id)
    if request.method == 'POST':
        blog.title = request.form.get('title')
        blog.author = request.form.get('author')
        blog.content = request.form.get('content')
        db.session.commit()
        flash('post has been updated','success')
        return redirect('/')

    return render_template('blogupdate.html',blog=blog)

if __name__ == "__main__":
    app.run(debug=True,port = 5000)