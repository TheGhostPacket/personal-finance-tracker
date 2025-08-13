from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from database import FinanceDB
from datetime import datetime, date
import calendar
import json
import os

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Initialize database
db = FinanceDB()

# Helper function to check if user is logged in
def is_logged_in():
    return 'user_id' in session

# Helper function to get current user info
def get_current_user():
    if is_logged_in():
        return {
            'id': session['user_id'],
            'username': session['username']
        }
    return None

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise show landing page"""
    if is_logged_in():
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Basic validation
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        
        # Try to create user
        user_id = db.create_user(username, email, password)
        
        if user_id:
            # Auto-login after successful registration
            session['user_id'] = user_id
            session['username'] = username
            return jsonify({'success': True, 'message': 'Account created successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Username or email already exists'}), 400
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = db.verify_user(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Log out user"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Main dashboard - shows overview of finances"""
    if not is_logged_in():
        return redirect(url_for('login'))
    
    user = get_current_user()
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # Get monthly summary
    monthly_summary = db.get_monthly_summary(user['id'], current_year, current_month)
    
    # Get recent transactions (last 10)
    recent_transactions = db.get_transactions(user['id'], limit=10)
    
    # Get spending by category for current month
    start_date = f"{current_year}-{current_month:02d}-01"
    end_date = f"{current_year}-{current_month:02d}-{calendar.monthrange(current_year, current_month)[1]:02d}"
    spending_by_category = db.get_spending_by_category(user['id'], start_date, end_date)
    
    return render_template('dashboard.html', 
                         user=user,
                         monthly_summary=monthly_summary,
                         recent_transactions=recent_transactions,
                         spending_by_category=spending_by_category,
                         current_month=calendar.month_name[current_month],
                         current_year=current_year)

@app.route('/transactions')
def transactions():
    """View all transactions"""
    if not is_logged_in():
        return redirect(url_for('login'))
    
    user = get_current_user()
    all_transactions = db.get_transactions(user['id'])
    categories = db.get_categories(user['id'])
    
    return render_template('transactions.html', 
                         user=user,
                         transactions=all_transactions,
                         categories=categories)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """Add a new transaction"""
    if not is_logged_in():
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    data = request.get_json()
    user = get_current_user()
    
    try:
        # Validate required fields
        required_fields = ['category_id', 'amount', 'description', 'transaction_type', 'date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        # Add transaction to database
        db.add_transaction(
            user_id=user['id'],
            category_id=int(data['category_id']),
            amount=float(data['amount']),
            description=data['description'],
            transaction_type=data['transaction_type'],
            date=data['date']
        )
        
        return jsonify({'success': True, 'message': 'Transaction added successfully!'})
        
    except Exception as e:
        print(f"Error adding transaction: {e}")
        return jsonify({'success': False, 'message': 'Error adding transaction'}), 500

@app.route('/api/categories')
def get_categories():
    """API endpoint to get user's categories"""
    if not is_logged_in():
        return jsonify({'error': 'Not logged in'}), 401
    
    user = get_current_user()
    categories = db.get_categories(user['id'])
    return jsonify(categories)

@app.route('/api/spending_by_category')
def api_spending_by_category():
    """API endpoint for spending by category data"""
    if not is_logged_in():
        return jsonify({'error': 'Not logged in'}), 401
    
    user = get_current_user()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    spending_data = db.get_spending_by_category(user['id'], start_date, end_date)
    return jsonify(spending_data)

@app.route('/api/monthly_summary/<int:year>/<int:month>')
def api_monthly_summary(year, month):
    """API endpoint for monthly summary"""
    if not is_logged_in():
        return jsonify({'error': 'Not logged in'}), 401
    
    user = get_current_user()
    summary = db.get_monthly_summary(user['id'], year, month)
    return jsonify(summary)

@app.route('/reports')
def reports():
    """Reports and analytics page"""
    if not is_logged_in():
        return redirect(url_for('login'))
    
    user = get_current_user()
    current_date = datetime.now()
    
    # Get last 6 months of data for trends
    monthly_data = []
    for i in range(6):
        month = current_date.month - i
        year = current_date.year
        
        if month <= 0:
            month += 12
            year -= 1
        
        summary = db.get_monthly_summary(user['id'], year, month)
        monthly_data.append({
            'month': calendar.month_name[month],
            'year': year,
            'summary': summary
        })
    
    monthly_data.reverse()  # Oldest to newest
    
    return render_template('reports.html', 
                         user=user,
                         monthly_data=monthly_data)

@app.route('/export_csv')
def export_csv():
    """Export transactions as CSV"""
    if not is_logged_in():
        return redirect(url_for('login'))
    
    from flask import make_response
    import csv
    import io
    
    user = get_current_user()
    transactions = db.get_transactions(user['id'])
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Date', 'Category', 'Description', 'Type', 'Amount'])
    
    # Write transactions
    for transaction in transactions:
        writer.writerow([
            transaction['date'],
            transaction['category_name'],
            transaction['description'],
            transaction['transaction_type'].title(),
            f"${transaction['amount']:.2f}"
        ])
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=transactions_{user["username"]}.csv'
    
    return response

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create database tables if they don't exist
    db.init_database()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)