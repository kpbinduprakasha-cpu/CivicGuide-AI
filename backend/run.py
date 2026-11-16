import os
import sys

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1']
    print(f"==================================================")
    print(f" CivicGuide AI - Backend Server Starting")
    print(f" Location Focus: Vijayanagara District, Karnataka")
    print(f" Port: {port} | Debug: {debug}")
    print(f"==================================================")
    app.run(host='0.0.0.0', port=port, debug=debug)
