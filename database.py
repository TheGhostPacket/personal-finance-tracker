import sqlite3
import hashlib
from datetime import datetime
import os

class FinanceDB:
    def __init__(self, db_path='instance/finance.db'):
        """Initialize the database connection"""
        self.db_path = db_path
        # Create the instance directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This lets us access columns by name
        return conn
    
    def init_database(self):
        """Create all tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table - stores user account information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Categories table - types of spending (Food, Transport, etc.)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                color TEXT DEFAULT '#3b82f6',
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Transactions table - all money movements
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                description TEXT,
                transaction_type TEXT CHECK (transaction_type IN ('income', 'expense')) NOT NULL,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Budgets table - spending limits for categories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                month_year TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (category_id) REFERENCES categories (id),
                UNIQUE(user_id, category_id, month_year)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database tables created successfully!")
    
    def hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password):
        """Create a new user account"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            
            user_id = cursor.lastrowid
            
            # Create default categories for new user
            default_categories = [
                ('Food & Dining', '#ef4444'),
                ('Transportation', '#3b82f6'),
                ('Shopping', '#8b5cf6'),
                ('Entertainment', '#10b981'),
                ('Bills & Utilities', '#f59e0b'),
                ('Healthcare', '#ec4899'),
                ('Education', '#06b6d4'),
                ('Travel', '#84cc16'),
                ('Income', '#22c55e'),
                ('Other', '#6b7280')
            ]
            
            for category_name, color in default_categories:
                cursor.execute('''
                    INSERT INTO categories (name, color, user_id)
                    VALUES (?, ?, ?)
                ''', (category_name, color, user_id))
            
            conn.commit()
            print(f"✅ User '{username}' created successfully with default categories!")
            return user_id
            
        except sqlite3.IntegrityError as e:
            print(f"❌ Error creating user: {e}")
            return None
        finally:
            conn.close()
    
    def verify_user(self, username, password):
        """Verify user login credentials"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute('''
            SELECT id, username, email FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return dict(user)  # Convert to dictionary
        return None
    
    def add_transaction(self, user_id, category_id, amount, description, transaction_type, date):
        """Add a new transaction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (user_id, category_id, amount, description, transaction_type, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, category_id, amount, description, transaction_type, date))
        
        conn.commit()
        conn.close()
        print("✅ Transaction added successfully!")
    
    def get_transactions(self, user_id, limit=None):
        """Get user's transactions with category names"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT t.*, c.name as category_name, c.color as category_color
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = ?
            ORDER BY t.date DESC
        '''
        
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query, (user_id,))
        transactions = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in transactions]
    
    def get_categories(self, user_id):
        """Get user's categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM categories WHERE user_id = ?
            ORDER BY name
        ''', (user_id,))
        
        categories = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in categories]
    
    def get_spending_by_category(self, user_id, start_date=None, end_date=None):
        """Get spending breakdown by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT c.name, c.color, SUM(t.amount) as total_amount
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = ? AND t.transaction_type = 'expense'
        '''
        params = [user_id]
        
        if start_date:
            query += ' AND t.date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND t.date <= ?'
            params.append(end_date)
        
        query += ' GROUP BY c.id, c.name, c.color ORDER BY total_amount DESC'
        
        cursor.execute(query, params)
        spending = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in spending]
    
    def get_monthly_summary(self, user_id, year, month):
        """Get monthly income vs expenses summary"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get total income and expenses for the month
        cursor.execute('''
            SELECT 
                transaction_type,
                SUM(amount) as total
            FROM transactions
            WHERE user_id = ? 
            AND strftime('%Y', date) = ? 
            AND strftime('%m', date) = ?
            GROUP BY transaction_type
        ''', (user_id, str(year), f"{month:02d}"))
        
        results = cursor.fetchall()
        conn.close()
        
        summary = {'income': 0, 'expenses': 0}
        for row in results:
            if row['transaction_type'] == 'income':
                summary['income'] = float(row['total'])
            else:
                summary['expenses'] = float(row['total'])
        
        summary['balance'] = summary['income'] - summary['expenses']
        return summary

# Test the database setup
if __name__ == '__main__':
    # Initialize database
    db = FinanceDB()
    
    # Test creating a user (optional - you can comment this out)
    # test_user_id = db.create_user('testuser', 'test@example.com', 'password123')
    
    print("🎉 Database setup complete! Ready to build the app!")