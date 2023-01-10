from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =SQLAlchemy(app)
app.app_context().push() 
 
class ContactBook(db.Model):
    __tablename__ = "contacts"
 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    gender = db.Column(db.String())
    hobbies = db.Column(db.String())
    country = db.Column(db.String(80))
 
    def __init__(self, first_name,last_name,email,phone,gender,hobbies,country):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.gender = gender
        self.hobbies = hobbies
        self.country = country
 
    def __repr__(self):
        return f"{self.first_name}:{self.last_name}"

db.create_all()        


@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':

        hobby = request.form.getlist('hobbies')
        hobbies=",".join(map(str, hobby))


        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        hobbies = hobbies
        country = request.form['country']
        contacts = ContactBook(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            gender=gender, 
            hobbies=hobbies,
            country = country
        )
        db.session.add(contacts)
        db.session.commit()
        return redirect('/')
 
 
@app.route('/')
def RetrieveList():
    contacts = ContactBook.query.all()
    return render_template('datalist.html',contacts = contacts)
 
 
@app.route('/<int:id>')
def RetrieveContact(id):
    contacts = ContactBook.query.filter_by(id=id).first()
    if contacts:
        return render_template('data.html', contacts = contacts)
    return f"Employee with id ={id} Doenst exist"
 
 
@app.route('/<int:id>/edit',methods = ['GET','POST'])
def update(id):
    contact = ContactBook.query.filter_by(id=id).first()

    
    if request.method == 'POST':
        if contact:
            db.session.delete(contact)
            db.session.commit()
   
        hobby = request.form.getlist('hobbies')
        hobbies =  ",".join(map(str, hobby)) 
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        hobbies = hobbies 
        country = request.form['country']

        contact = ContactBook(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            gender=gender, 
            hobbies=hobbies,
            country = country
        )
        db.session.add(contact)
        db.session.commit()
        return redirect('/')
        return f"Contact with id = {id} Does nit exist"
 
    return render_template('update.html', contact = contact)
 
 
@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    contacts = ContactBook.query.filter_by(id=id).first()
    if request.method == 'POST':
        if contacts:
            db.session.delete(contacts)
            db.session.commit()
            return redirect('/')
        (404)
     
    return render_template('delete.html')


@app.route('/search', methods=['POST'])
def search_contacts():
  query = request.form['query']
  search_results = ContactBook.query.filter(ContactBook.first_name.contains(query)).all()
  return render_template('search_results.html', contacts=search_results)

app.run(host='localhost', port=5000, debug=True)