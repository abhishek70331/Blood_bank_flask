from flask import Flask, render_template,request,session,redirect,url_for
from flask_mail import Mail, Message
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blood'
 
mysql = MySQL(app)

# instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'meditationmind70@gmail.com'
app.config['MAIL_PASSWORD'] = 'qrpqtdcuoqouuzna'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


app.secret_key = "hellome"


@app.route("/")
@app.route('/index')
def index():
   cursor = mysql.connection.cursor()
   cursor.execute("SELECT * FROM store")
   data = cursor.fetchall()
   cursor.close()
   return render_template("index.html", store=data)

@app.route("/login", methods=['GET','POST'])
def login():
   if request.method=="POST":
      email = request.form["email"]
      password = request.form["password"]
      print(email,password)
      cursor = mysql.connection.cursor()
      cursor.execute("SELECT * FROM login WHERE email = %s AND password = %s",(email,password))
      record = cursor.fetchone()
      if record:
         session['logedin'] = True
         session['email'] = record[0]
         return redirect(url_for("home"))
      else:
         return "Invalid hai bhai"
   return render_template("login.html")

@app.route("/logout")
def logout():
   session.pop('logedin',None)
   session.pop('email',None)        
   return redirect(url_for("index"))


@app.route("/signup", methods=['GET','POST'])
def signup():
   if request.method=="POST":
      name = request.form["name"]
      phone = request.form["phone"]
      email = request.form["email"]
      password = request.form["password"]
      cursor = mysql.connection.cursor()
      cursor.execute("INSERT INTO login VALUES (%s,%s,%s,%s)",(name,phone,email,password))
      cursor.connection.commit()
      cursor.close()
   return render_template("signup.html")

#After login
@app.route("/home",methods=['GET','POST'])
def home():

   cursor = mysql.connection.cursor()
   cursor.execute("SELECT * FROM store")
   data = cursor.fetchall()
   cursor.close()


   if request.method=="POST":
      id = request.form['id']
      name = request.form["name"]
      address = request.form["address"]
      blood = request.form["blood"]
      gender = request.form["gender"]
      age = request.form["age"]
      number = request.form["number"]
      cursor = mysql.connection.cursor()
      cursor.execute("INSERT INTO store VALUES (%s,%s,%s,%s,%s,%s,%s)",(id,name,address,blood,gender,age,number))
      cursor.connection.commit()
      cursor.close()
      return redirect(url_for("home"))
   return render_template("home.html", email = session['email'], store=data)

@app.route("/delete/<string:id>", methods=['GET','POST'])
def delete(id):

   cursor = mysql.connection.cursor()
   cursor.execute("DELETE FROM store WHERE id = %s", (id))
   mysql.connection.commit()

   return redirect(url_for("home"))  


#contact Us form
@app.route("/contact", methods=['GET','POST'])
def contact():
   if request.method=="POST":
      email = request.form['email']
      message = request.form['message']
      print(email,message)
      msg = Message(
                'Hello',
                sender =email,
                recipients = ['meditationmind70@gmail.com']
               )
      msg.body = message
      mail.send(msg)
      return 'Sent'
   return render_template("contact.html")

if __name__ == '__main__':
   app.run(debug=True)