#
# Conda environment: ltw-print
# Python version: 3.11.11
#

from flask import Flask, request, jsonify
import json
import subprocess
import threading
import os
from datetime import datetime

app = Flask(__name__)

def process_and_print(data):
    try:
        print(f"[{datetime.now()}] Processing print job...")
        
        data['timestamp'] = datetime.now().isoformat()
        
        temp_file = os.path.join(os.path.dirname(__file__), 'temp.json')
        with open(temp_file, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=2)
        
        print(f"Data written to {temp_file}")
        print(f"Main image: {len(data.get('main', ''))} characters")
        print(f"Second image: {len(data.get('second', ''))} characters")
        print(f"Body text: {data.get('body', 'No body text')}")
        
        print("Starting print script...")
        result = subprocess.run(
            ['python', 'print.py', '--file', temp_file], 
            capture_output=True, 
            text=True,
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode == 0:
            print("✓ Print job completed successfully")
            if result.stdout:
                print(f"Print script output: {result.stdout}")
        else:
            print(f"✗ Print job failed with return code {result.returncode}")
            if result.stderr:
                print(f"Print script errors: {result.stderr}")
        
        # os.remove(temp_file)
        
    except Exception as e:
        print(f"Error in process_and_print: {e}")
        import traceback
        traceback.print_exc()

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data received'}), 400
        
        print(f"\n[{datetime.now()}] ========== NEW PRINT JOB ==========")
        print(f"Received data from TouchDesigner")
        
        main = data.get('main', '')
        second = data.get('second', '')
        body = data.get('body', '')
        
        print(f"Main image: {'Present' if main else 'Missing'} ({len(main)} chars)")
        print(f"Second image: {'Present' if second else 'Missing'} ({len(second)} chars)")
        print(f"Body text: {body if body else 'No body text'}")
        
        response = jsonify({
            'success': True, 
            'message': 'Data received and queued for printing',
            'timestamp': datetime.now().isoformat()
        })
        
        print("Queuing print job for background processing...")
        thread = threading.Thread(target=process_and_print, args=(data,))
        thread.daemon = True
        thread.start()
        
        return response, 200
        
    except Exception as e:
        print(f"Error in receive_data: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False, 
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Print server is running'
    }), 200

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'active_threads': threading.active_count(),
        'message': 'TouchDesigner print server'
    }), 200

if __name__ == '__main__':
    print("="*50)
    print("TouchDesigner Print Server Starting...")
    print("="*50)
    print(f"Server will run on: http://localhost:3000")
    print(f"Health check: http://localhost:3000/health")
    print(f"Status check: http://localhost:3000/status")
    print(f"Print endpoint: http://localhost:3000/api/data")
    print("="*50)
    
    
    app.run(
        host='0.0.0.0',
        port=3000,
        debug=False, 
        threaded=True, 
        use_reloader=False 
    )