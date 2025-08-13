#!/usr/bin/env python3
"""
Test script to verify Personal Finance Tracker setup
"""

import os
import sys
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    try:
        import flask
        print("✅ Flask imported successfully")
        
        import sqlite3
        print("✅ SQLite3 imported successfully")
        
        from database import FinanceDB
        print("✅ Database module imported successfully")
        
        from app import app
        print("✅ App module imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Test database creation and basic operations"""
    print("\n🗄️ Testing database...")
    try:
        from database import FinanceDB
        
        # Initialize database
        db = FinanceDB()
        print("✅ Database initialized successfully")
        
        # Test user creation
        user_id = db.create_user("testuser123", "test@example.com", "password123")
        if user_id:
            print("✅ Test user created successfully")
        else:
            print("⚠️ User already exists (this is normal)")
        
        # Test user verification
        user = db.verify_user("testuser123", "password123")
        if user:
            print("✅ User verification works")
        else:
            print("❌ User verification failed")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    required_files = [
        'app.py',
        'database.py',
        'requirements.txt',
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/register.html',
        'templates/dashboard.html',
        'templates/transactions.html',
        'templates/reports.html'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_exist = False
    
    return all_exist

def test_app_routes():
    """Test if Flask app can start and routes work"""
    print("\n🌐 Testing Flask app...")
    try:
        from app import app
        
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page (/) works")
            else:
                print(f"❌ Home page failed: {response.status_code}")
            
            # Test login page
            response = client.get('/login')
            if response.status_code == 200:
                print("✅ Login page (/login) works")
            else:
                print(f"❌ Login page failed: {response.status_code}")
            
            # Test register page
            response = client.get('/register')
            if response.status_code == 200:
                print("✅ Register page (/register) works")
            else:
                print(f"❌ Register page failed: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Personal Finance Tracker - Test Suite")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Test time: {datetime.now()}")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Imports", test_imports),
        ("Database Operations", test_database),
        ("Flask Routes", test_app_routes)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print("=" * 50)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Your app is ready to deploy!")
        print("\n🚀 Next steps:")
        print("1. Run: python app.py")
        print("2. Visit: http://127.0.0.1:5000")
        print("3. Create account and test features")
        print("4. Deploy to Render when ready")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
        print("\n🔧 Common fixes:")
        print("- Make sure all files are in the right location")
        print("- Check for typos in file names")
        print("- Verify Python dependencies are installed")
        print("- Look for syntax errors in your code")

if __name__ == "__main__":
    main()