#!/usr/bin/env python
"""
Quiz Master App Startup Script
Run this script to start the Flask development server
"""

import os
import sys
from app import app, db

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Quiz Master App Starting...")
    print("=" * 60)
    
    # Print admin credentials
    print("\n📋 DEFAULT ADMIN CREDENTIALS:")
    print("   Email: admin@gmail.com")
    print("   Password: admin123")
    
    print("\n🌐 Access the app at: http://localhost:5000")
    print("\n⚙️  Running on debug mode...")
    print("=" * 60 + "\n")
    
    # Run the Flask app
    app.run(debug=True, host='localhost', port=5000)
