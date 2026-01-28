#!/usr/bin/env python3
"""
Google APIs Generator API
A web API to generate Google API client code and manage API keys.
"""

import os
import sys
import json
import subprocess
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import logging
from datetime import datetime

# Add the output directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'output'))

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
PROTOC_PATH = os.path.join(os.path.dirname(__file__), 'bin', 'protoc.exe')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
GOOGLE_APIS_ROOT = os.path.dirname(__file__)

# Mock API keys storage (in production, use a secure database)
API_KEYS = {
    "google_cloud_vision": "AIzaSyB2X8Cr7XgYzZ9K8J7Q6L5M4N1P3O2R9S8T",
    "google_cloud_speech": "AIzaSyD3Y9Ds8H0A1K9L8M7N6O5P4Q3R2S1T9U8V",
    "google_cloud_translate": "AIzaSyE4Z0Et9I1B2L9M8N7O6P5Q4R3S2T1U9V0W",
    "google_maps_places": "AIzaSyF5A1Fu0J2C3M9L8N7O6P5Q4R3S2T1U9V0X",
    "google_ai_platform": "AIzaSyG6B2Gv0K3D4M9L8N7O6P5Q4R3S2T1U9V0Y"
}

class GoogleAPIGenerator:
    def __init__(self):
        self.protoc_path = PROTOC_PATH
        self.output_dir = OUTPUT_DIR
        self.google_apis_root = GOOGLE_APIS_ROOT
        
    def generate_api_code(self, api_path, language="python"):
        """Generate client code for a specific Google API."""
        try:
            # Ensure output directory exists
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Build protoc command
            cmd = [
                self.protoc_path,
                f"--{language}_out={self.output_dir}",
                "--proto_path=.",
                api_path
            ]
            
            logger.info(f"Generating code for {api_path}")
            result = subprocess.run(
                cmd,
                cwd=self.google_apis_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Successfully generated code for {api_path}",
                    "output_path": os.path.join(self.output_dir, api_path.replace('.proto', '_pb2.py'))
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "message": f"Failed to generate code for {api_path}"
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Generation timed out after 60 seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_available_apis(self):
        """List all available Google API proto files."""
        apis = []
        try:
            for root, dirs, files in os.walk(self.google_apis_root):
                if 'google' in root:
                    for file in files:
                        if file.endswith('.proto'):
                            rel_path = os.path.relpath(os.path.join(root, file), self.google_apis_root)
                            apis.append(rel_path)
            return sorted(apis)
        except Exception as e:
            logger.error(f"Error listing APIs: {e}")
            return []

generator = GoogleAPIGenerator()

@app.route('/')
def home():
    """API documentation endpoint."""
    return jsonify({
        "name": "Google APIs Generator API",
        "version": "1.0.0",
        "description": "Generate Google API client code and manage API keys",
        "endpoints": {
            "GET /": "API documentation",
            "GET /api-keys": "List all available API keys",
            "GET /api-keys/<service>": "Get API key for specific service",
            "GET /apis": "List all available Google APIs",
            "POST /generate": "Generate client code for an API",
            "GET /download/<path:filename>": "Download generated code"
        },
        "examples": {
            "generate_code": {
                "method": "POST",
                "url": "/generate",
                "body": {
                    "api_path": "google/example/library/v1/library.proto",
                    "language": "python"
                }
            },
            "get_api_key": {
                "method": "GET", 
                "url": "/api-keys/google_cloud_vision"
            }
        }
    })

@app.route('/api-keys')
def list_api_keys():
    """List all available API keys with service names."""
    return jsonify({
        "api_keys": API_KEYS,
        "total_keys": len(API_KEYS),
        "generated_at": datetime.now().isoformat()
    })

@app.route('/api-keys/<service>')
def get_api_key(service):
    """Get API key for a specific Google service."""
    if service in API_KEYS:
        return jsonify({
            "service": service,
            "api_key": API_KEYS[service],
            "generated_at": datetime.now().isoformat(),
            "note": "This is a demo API key for testing purposes"
        })
    else:
        return jsonify({
            "error": "Service not found",
            "available_services": list(API_KEYS.keys())
        }), 404

@app.route('/apis')
def list_apis():
    """List all available Google API proto files."""
    apis = generator.list_available_apis()
    return jsonify({
        "total_apis": len(apis),
        "apis": apis[:50],  # Limit to first 50 for performance
        "has_more": len(apis) > 50
    })

@app.route('/generate', methods=['POST'])
def generate_api():
    """Generate client code for a specific Google API."""
    data = request.get_json()
    
    if not data or 'api_path' not in data:
        return jsonify({
            "error": "Missing api_path in request body"
        }), 400
    
    api_path = data['api_path']
    language = data.get('language', 'python')
    
    # Validate language
    supported_languages = ['python', 'java', 'cpp', 'csharp']
    if language not in supported_languages:
        return jsonify({
            "error": f"Unsupported language: {language}",
            "supported_languages": supported_languages
        }), 400
    
    result = generator.generate_api_code(api_path, language)
    
    if result['success']:
        return jsonify({
            **result,
            "api_key": API_KEYS.get(extract_service_name(api_path), "No API key available"),
            "generated_at": datetime.now().isoformat()
        })
    else:
        return jsonify(result), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download generated code files."""
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_service_name(api_path):
    """Extract service name from API path for API key lookup."""
    if 'vision' in api_path.lower():
        return 'google_cloud_vision'
    elif 'speech' in api_path.lower():
        return 'google_cloud_speech'
    elif 'translate' in api_path.lower():
        return 'google_cloud_translate'
    elif 'maps' in api_path.lower() or 'places' in api_path.lower():
        return 'google_maps_places'
    elif 'aiplatform' in api_path.lower() or 'ai' in api_path.lower():
        return 'google_ai_platform'
    return None

if __name__ == '__main__':
    print("🚀 Starting Google APIs Generator API...")
    print(f"📍 Protoc path: {PROTOC_PATH}")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"🔑 Available API keys: {len(API_KEYS)}")
    print("\n📖 API Documentation: http://localhost:5000/")
    print("🔑 API Keys: http://localhost:5000/api-keys")
    print("📋 Available APIs: http://localhost:5000/apis")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
