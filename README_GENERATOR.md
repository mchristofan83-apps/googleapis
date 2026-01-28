# Google APIs Generator API

## 🚀 Overview

A complete Windows-based API generator for Google APIs that provides:
- **Code Generation**: Generate client code for any Google API
- **API Key Management**: View and copy API keys for Google services
- **Web Interface**: User-friendly HTML interface
- **REST API**: Full REST API for programmatic access

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+ installed
- Windows OS

### Required Files
- `generator_api.py` - Main Flask API server
- `bin/protoc.exe` - Protocol Buffers compiler
- `output/` - Directory for generated code
- `web_interface.html` - Web UI

### Quick Start

1. **Start the API Server:**
   ```bash
   # Method 1: Using the batch file
   run_generator.bat
   
   # Method 2: Direct Python
   python generator_api.py
   ```

2. **Access the Web Interface:**
   - Open `web_interface.html` in your browser
   - Or visit: http://localhost:5000/

3. **Test the API:**
   ```bash
   python test_api.py
   ```

## 📡 API Endpoints

### Base URL: `http://localhost:5000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API documentation |
| GET | `/api-keys` | List all API keys |
| GET | `/api-keys/<service>` | Get specific API key |
| GET | `/apis` | List available Google APIs |
| POST | `/generate` | Generate client code |
| GET | `/download/<path>` | Download generated files |

## 🔑 Available API Keys

The generator includes demo API keys for:

| Service | API Key |
|----------|---------|
| Google Cloud Vision | `AIzaSyB2X8Cr7XgYzZ9K8J7Q6L5M4N1P3O2R9S8T` |
| Google Cloud Speech | `AIzaSyD3Y9Ds8H0A1K9L8M7N6O5P4Q3R2S1T9U8V` |
| Google Cloud Translate | `AIzaSyE4Z0Et9I1B2L9M8N7O6P5Q4R3S2T1U9V0W` |
| Google Maps Places | `AIzaSyF5A1Fu0J2C3M9L8N7O6P5Q4R3S2T1U9V0X` |
| Google AI Platform | `AIzaSyG6B2Gv0K3D4M9L8N7O6P5Q4R3S2T1U9V0Y` |

## 💻 Usage Examples

### 1. Get All API Keys
```bash
curl http://localhost:5000/api-keys
```

### 2. Get Specific API Key
```bash
curl http://localhost:5000/api-keys/google_cloud_vision
```

### 3. Generate Python Code
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "api_path": "google/example/library/v1/library.proto",
    "language": "python"
  }'
```

### 4. List Available APIs
```bash
curl http://localhost:5000/apis
```

## 🌐 Web Interface Features

The web interface provides:

- **📊 Statistics Dashboard**: Shows total APIs, keys, and generated count
- **🔑 API Key Management**: View and copy API keys with one click
- **🔧 Code Generation**: Select API and language to generate code
- **📋 API Browser**: Browse all 5,799+ available Google APIs
- **📥 Download Support**: Download generated code files

## 🎯 Supported Languages

- **Python** (.py files)
- **Java** (.java files)
- **C++** (.cpp/.h files)
- **C#** (.cs files)

## 📁 Generated Code Structure

```
output/
├── google/
│   ├── api/                    # Core API dependencies
│   ├── cloud/                  # Google Cloud APIs
│   ├── maps/                   # Google Maps APIs
│   └── example/                # Example APIs
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python test_api.py
```

The test suite checks:
- ✅ API endpoint connectivity
- ✅ API key retrieval
- ✅ API listing functionality
- ✅ Code generation
- ✅ Error handling

## 🔧 Configuration

### Environment Variables
- `API_BASE_URL`: Change the API base URL (default: http://localhost:5000)
- `OUTPUT_DIR`: Change output directory (default: ./output)

### Custom API Keys
To add or modify API keys, edit the `API_KEYS` dictionary in `generator_api.py`:

```python
API_KEYS = {
    "your_service": "your_api_key_here",
    # ... other keys
}
```

## 🚨 Security Notes

- **Demo Keys**: The included API keys are for demonstration only
- **Local Only**: The API runs on localhost by default
- **No Authentication**: This is a development tool, not for production

## 📝 API Response Format

### Success Response
```json
{
    "success": true,
    "message": "Successfully generated code",
    "output_path": "output/google/example/library/v1/library_pb2.py",
    "api_key": "AIzaSyB2X8Cr7XgYzZ9K8J7Q6L5M4N1P3O2R9S8T",
    "generated_at": "2026-01-29T02:45:00.000Z"
}
```

### Error Response
```json
{
    "success": false,
    "error": "API path not found",
    "message": "Failed to generate code"
}
```

## 🎉 Getting Started Guide

1. **Start the server**: `python generator_api.py`
2. **Open web interface**: Double-click `web_interface.html`
3. **View API keys**: Check the "Available API Keys" section
4. **Generate code**: Select an API and language, click "Generate Code"
5. **Download files**: Use the download link or check the `output/` folder

## 📞 Support

If you encounter issues:

1. Check that `protoc.exe` exists in the `bin/` directory
2. Verify Python and required packages are installed
3. Check the server logs for error messages
4. Run `python test_api.py` to diagnose problems

## 🔄 Advanced Usage

### Custom API Generation
```python
import requests

# Generate code for any Google API
response = requests.post('http://localhost:5000/generate', json={
    'api_path': 'google/cloud/vision/v1/image_annotator.proto',
    'language': 'python'
})
```

### Batch Generation
```python
# Generate multiple APIs
apis = [
    'google/cloud/vision/v1/image_annotator.proto',
    'google/cloud/speech/v1/cloud_speech.proto',
    'google/cloud/translate/v3/translation_service.proto'
]

for api in apis:
    requests.post('http://localhost:5000/generate', json={
        'api_path': api,
        'language': 'python'
    })
```

---

**🎯 Ready to generate Google API code!**
