#!/usr/bin/env python3
"""
Quick test to check for syntax errors
"""

def test_basic_imports():
    """Test if the app can import without errors"""
    try:
        print("Testing basic Python imports...")
        import sqlite3
        print("✅ sqlite3 imported")
        
        import os
        print("✅ os imported") 
        
        import hashlib
        print("✅ hashlib imported")
        
        from datetime import datetime
        print("✅ datetime imported")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_flask_imports():
    """Test Flask-specific imports"""
    try:
        print("\nTesting Flask imports...")
        from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
        print("✅ Flask imports successful")
        
        return True
    except Exception as e:
        print(f"❌ Flask import error: {e}")
        return False

def test_app_creation():
    """Test if we can create the Flask app"""
    try:
        print("\nTesting app creation...")
        from flask import Flask
        test_app = Flask(__name__)
        test_app.secret_key = 'test-key'
        print("✅ Flask app created successfully")
        
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def test_database_import():
    """Test database module import"""
    try:
        print("\nTesting database module...")
        from database import FinanceDB
        print("✅ Database module imported")
        
        # Test database creation
        db = FinanceDB()
        print("✅ Database instance created")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Quick Error Check for Personal Finance Tracker")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_flask_imports, 
        test_app_creation,
        test_database_import
    ]
    
    all_passed = True
    
    for test in tests:
        try:
            result = test()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Your app should work now!")
        print("Run: python app.py")
        print("Visit: http://127.0.0.1:5000")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("Check the error messages above")
        print("Make sure all files are in the correct location")

if __name__ == "__main__":
    main()