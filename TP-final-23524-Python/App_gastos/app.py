from flask import Flask, jsonify, render_template, request, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False)

    def __init__(self, category, amount, description, date):
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date

with app.app_context():
    db.create_all()

class ExpenseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'category', 'amount', 'description', 'date')

expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = float(request.form['amount'])
    description = request.form.get('description', '')
    date = request.form['date']

    new_expense = Expense(category=category, amount=amount, description=description, date=date)
    db.session.add(new_expense)
    db.session.commit()

    return jsonify({'message': 'Gasto agregado con éxito'})

@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    expense_list = [
        {'id': expense.id, 'category': expense.category, 'amount': expense.amount, 'description': expense.description, 'date': expense.date}
        for expense in expenses
    ]
    total_expense = sum(expense.amount for expense in expenses)

    return jsonify({'expenses': expense_list, 'totalExpense': total_expense})

@app.route('/delete_expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()

    return jsonify({'message': 'Gasto eliminado con éxito'})

if __name__ == '__main__':
    app.run(debug=True)
