from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import db
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import User, Income, Expense #importar desde models

app= Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Para seguridad, se puede modificar para tener tu propia "secret key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html")

#Pagina para registro de nuevo usuarios
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        new_user = User(name= name, email=email, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Pagina para hacer login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check your username and password.')
    return render_template('login.html')

# Dashboard
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == 'POST':
        if "add_income" in request.form:
        #Para añadir income
            amount = request.form["income_amount"]
            description = request.form["income_description"]
            new_income = Income(amount=amount, description=description, user_id=current_user.id)
            db.session.add(new_income)
            db.session.commit()
            flash("Income added successfully!", "success")
            return redirect(url_for('dashboard'))

        elif "add_expense" in request.form:
            print("hello")
            # para añadir Expense
            amount = request.form["expense_amount"]
            description = request.form["expense_description"]
            new_expense = Expense(amount=amount, description=description, user_id=current_user.id)
            db.session.add(new_expense)
            db.session.commit()
            flash("Expense added successfully!", "success")
            return redirect(url_for('dashboard'))

    # Obtener datos de ingresos y gastos para mostrar en el "Dashboard".
    incomes = db.session.query(Income).filter_by(user_id=current_user.id).all()
    expenses = db.session.query(Expense).filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", incomes=incomes, expenses=expenses)

# Route para eliminar una entrada de "income(ingresos)"
@app.route('/delete_income/<int:id>', methods=['POST'])
@login_required
def delete_income(id):
    db.session.query(Income).filter(Income.id == int(id)).delete()
    #if income.user_id != current_user.id:
        #flash('You do not have permission to delete this income.', 'error')
        #return redirect(url_for('dashboard'))
    db.session.commit()
    flash('Income deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# Route para eliminar una entrada de "Expense(Gastos)"
@app.route('/delete_expense/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    db.session.query(Expense).filter(Expense.id == int(id)).delete()
    #if expense.user_id != current_user.id:
        #flash('You do not have permission to delete this expense.', 'error')
        #return redirect(url_for('dashboard'))
    db.session.commit()
    flash('expense deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# Route para editar una entrada de "income(ingresos)"
@app.route('/edit_income/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_income(id):
    income=db.session.query(Income).filter(Income.id == int(id)).first()
    if income.user_id != current_user.id:
        flash('You do not have permission to edit this income.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        amount = request.form.get("income_amount")
        description = request.form.get("income_description")
        if not amount or not description:
            flash('Invalid form data. Please fill all fields.', 'error')
            return redirect(url_for('edit_income', id=id))
        income.amount = amount
        income.description = description
        db.session.commit()
        flash('Income updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_income.html', income=income)

# Route para editar una entrada de "Expenses(Gastos)"
@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense=db.session.query(Expense).filter(Expense.id == int(id)).first()
    if expense.user_id != current_user.id:
        flash('You do not have permission to edit this expense.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        amount = request.form.get("expense_amount")
        description = request.form.get("expense_description")
        if not amount or not description:
            flash('Invalid form data. Please fill all fields.', 'error')
            return redirect(url_for('edit_expense', id=id))
        expense.amount = amount
        expense.description = description
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_expense.html', expense=expense)

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine) # Para crear todas las tablas de la base de datos
    app.run(debug= True)