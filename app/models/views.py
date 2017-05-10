from app import app
from flask import render_template,redirect, request, flash,g,session,url_for,json
from app.models.models import db_connect

###db_connect contains all query methods##
#db = db_connect()
#########################################3

###### LOGIN ########

# Run HomePage
@app.route('/')
def index():
    db = db_connect() # connect to the database
    #print(session.get("user"))
    return render_template('index.html', top_five=db.select_top5_rated())


# Run LogInPage
@app.route('/showLogIn/')
def showLogIn():
    return render_template("Log-In.html")


# Login Logic
@app.route('/login', methods=["GET",'POST'])
def login():
    db = db_connect()
    # Get details from the user
    user_id = request.form['username']
    password = request.form['password']

    # Get details from the db
    user_check = db.select_user_info(user_id)
    empl_check = db.select_employee_info(user_id)


    # Check user details against db
    if user_check and user_check[0][3] == password:
        session["user"] = user_id
        session["logged_in"] = True
        return view_user_page()

    if empl_check and empl_check[0][0] == 'M' and empl_check[1] == password:
        session["user"] = user_id
        session["logged_in"] = True
        return view_management_page()

    if empl_check and empl_check[0][0] == 'C' and empl_check[1] == password:
        session["user"] = user_id
        session["logged_in"] = True
        return view_chef_page()

    if empl_check and empl_check[0][0] == 'D' and empl_check[1] == password:
        session["user"] = user_id
        session["logged_in"] = True
        return view_delivery_page()

    else:
        flash("Login Failed :(")
        return showLogIn()



# Controlling Logging Out
@app.route('/logout/')
def logout():

    # remove the un from the session if it is there
    session.pop('user', None)
    session["logged_in"] = False
    return index()


# LOGIN AS DELIVERY PERSONS
@app.route('/loginDelivery')
def view_delivery_page():
    return render_template("loginDELIVERY.html")


# LOGIN AS USER
@app.route('/loginUser/')
def view_user_page():
    db = db_connect()
    return render_template("loginUSER.html", top_five=db.select_top5_rated())


# LOGIN AS CHEF -- make SURE TO INCLUDE SOME SECURITY
@app.route('/loginChef')
def view_chef_page():
    return render_template("loginCHEF.html")


# LOGIN AS MANAGER
@app.route('/loginManager')
def view_management_page():
    db = db_connect()

    unregistered_users = db.select_all_unregistered_users()
    registered = db.select_all_registered_users()
    hired_employees = db.select_all_hired_employees()
    unhired_employees = db.select_all_pending_employees()
    list_of_complaints = db.select_all_pending_complaints()

    return render_template("loginMANAGER.html", registered_users=registered, unregistered=unregistered_users,
                           hired_employees=hired_employees, unhired_employees=unhired_employees, complaints=list_of_complaints )

# Run SignUpPage
@app.route('/showSignUp/')
def showSignUp():
    db = db_connect()

    return render_template('signup.html')


# Run Register
@app.route('/signup/', methods=["GET",'POST'])
def sign_up():
    db = db_connect()
    # read the values from the UI
    _firstName = request.form['first_name']
    _lastName = request.form['last_name']
    _userName = request.form['user_name']
    _password = request.form['password']
    _address = request.form['address']
    _city = request.form['city']
    _state = request.form['state']
    _postal = request.form['postal']
    _apt = request.form['apt']
    _phone = request.form['phone']

    # Check if username exists
    user_check = db.select_user_info(_userName)

    # If the username exists
    if user_check and user_check[0][0] == _userName:
        flash("Sorry, Username Exists", 'error')
        return render_template("signup.html")
    # If the key fields are not entered
    elif not _firstName or not _lastName or not _userName or not _password or not _address or not _city or not _state:
        flash("Please Enter All Info with Asterisks")
        return render_template("signup.html")
    # Insert User
    else:
        db.insert_users(_userName, _firstName, _lastName, _password, _address, _city, _state, _postal, _apt, _phone, acc_funds=0)
        return render_template("loginUSER.html")

###### DISPLAY COMPLIMENT/COMPLAINT FORM ##############

@app.route('/show_complaint_form/')
def show_complaint_form():
    db = db_connect()
    hired_employees = db.select_all_hired_employees()
    return render_template("/complaints.html", employees=hired_employees)

@app.route('/submit_complaint', methods=["GET",'POST'])
def submit_complaint():
    db = db_connect()

    employee = request.form["employee"]
    employee = employee.strip().split(" ")
    emp_fname = str(employee[0])
    emp_lname = employee[1]
    emp_id = db.select_employee_id_from_name(emp_fname, emp_lname)[0]

    user = "Lenny"
    complaint = request.form["complaint"]
    try:
        db.insert_complaints(user,emp_id,complaint)
    except:
        flash("Submittion failed")
        return render_template("complaints.html")
    return redirect("/")

@app.route('/show_compliment_form')
def show_compliment_form():
    return render_template("compliments.html")


@app.route('/submit_compliment', methods=["GET",'POST'])
def submit_compliment():
    db = db_connect()
    chef = request.form["chef"]
    user = session['user']
    compliment = request.form["compliment"]
    try:
        db.insert_compliments(user, chef, compliment)
    except:
        print("failed")
        flash("Submittion failed")
        return render_template("compliments.html")
    return redirect("/")


######### MENU SECTION ###########

# Run MenuPage
@app.route('/menu', methods=["GET",'POST'])
def showMenu():
    db = db_connect()
    formlist = []
    return render_template('Menu.html',databaseitems = db.select_menu_items(),numbers=db.select_menu_rating(), menu_items=db.select_menu())

@app.route('/add_to_cart', methods=["GET",'POST'])
def add_to_cart():
    db = db_connect()
    count = request.form.getlist("quantity")
    print(count)
    # try:
    #     # db.insert_compliments(user, chef, compliment)
    # except:
    #     print("failed")
    #     flash("Submittion failed")
    #     return render_template("compliments.html")
    return showMenu()
# EMPLOYEE MANAGEMENT TOOLS
@app.route('/accept_user/<user>', methods=['GET'])
def accept_user(user):
    db = db_connect()
    db.register(user)
    return view_management_page()


@app.route('/hire_employee/<empl_name>', methods=['GET'])
def hire(empl_name):
    db = db_connect()
    db.hire_employee(empl_name)
    return view_management_page()

@app.route('/fire/<empl_name>', methods=['GET'])
def fire(empl_name):
    db = db_connect()
    db.fire_employee(empl_name)
    return view_management_page()

@app.route('/upgrade_user/<user>', methods=['GET'])
def upgrade(empl_name):
    db = db_connect()
    db.upgrade_user(empl_name)
    return view_management_page()


@app.route('/promote/<empl_name>', methods=['GET'])
def promote(empl_name):
    db = db_connect()
    db.promote_employee(empl_name)
    return view_management_page()

@app.route('/demote/<empl_name>', methods=['GET'])
def demote(empl_name):
    db = db_connect()
    db.add_demotions(empl_name)
    db.demote_employee(empl_name)
    print(db.check_demotions(empl_name)[0])
    if db.check_demotions(empl_name)[0] > 1:
        db.fire_employee(empl_name)
    return view_management_page()

@app.route('/add_warning/<user>', methods=['GET'])
def add_warning(user_id):
    db = db_connect()
    db.update_warnings(user_id)
    return view_management_page()

@app.route('/accept_complaint/<complaint_id>/<emp_id>', methods=['GET'])
def accept_complaint(complaint_id, emp_id):
    db = db_connect()
    db.confirm_complaint(complaint_id)
    #I dk what this is for. -Eddy
    employee = emp_id
    if db.check_complaints(employee)[0][0] >= 3:
        db.demote_employee(employee)

        if db.check_demotions(employee)[0] >= 2:
            db.fire_employee(employee)

    return view_management_page()

@app.route('/decline_complaint/<complaint_id>/<user_id>', methods=['GET'])
def decline_complaint(complaint_id,user_id):
    db = db_connect()
    db.delete_complaint(complaint_id)

    db.update_warnings(user_id)
    return view_management_page()

@app.route('/add_compliment/<user>', methods=['GET'])
def accept_compliment(compliment_id):
    db = db_connect()
    db.confirm_compliment(compliment_id)
    #IDK what this is for. -Eddy
    # we need to check if the employee has 3 or more compliments. so we
    # use select_compliment to find out who the compliment is referring to
    employee = db.select_compliment(compliment_id).empl_id
    if db.check_compliments(employee) >= 3:
        db.promote_employee(employee)
        db.delete_complaint(employee)

    return view_management_page()



# Handles Any Page That Doesn't Exist
@app.errorhandler(404)
def PageNotFound(error):
    return render_template('errors/404.html'), 404


