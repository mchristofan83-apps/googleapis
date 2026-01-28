#!/usr/bin/env python3
"""
Test script for the Google APIs Generator API
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5000"

def test_api_endpoint():
    """Test the main API endpoint."""
    print("🔍 Testing API endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✅ API endpoint working")
            data = response.json()
            print(f"   API Name: {data['name']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print(f"❌ API endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        return False

def test_api_keys():
    """Test the API keys endpoint."""
    print("\n🔑 Testing API keys endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/api-keys")
        if response.status_code == 200:
            print("✅ API keys endpoint working")
            data = response.json()
            print(f"   Total API keys: {data['total_keys']}")
            for service, key in data['api_keys'].items():
                print(f"   - {service}: {key[:20]}...{key[-10:]}")
            return True
        else:
            print(f"❌ API keys endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing API keys: {e}")
        return False

def test_specific_api_key():
    """Test getting a specific API key."""
    print("\n🎯 Testing specific API key...")
    try:
        response = requests.get(f"{API_BASE_URL}/api-keys/google_cloud_vision")
        if response.status_code == 200:
            print("✅ Specific API key endpoint working")
            data = response.json()
            print(f"   Service: {data['service']}")
            print(f"   API Key: {data['api_key'][:20]}...{data['api_key'][-10:]}")
            return True
        else:
            print(f"❌ Specific API key endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing specific API key: {e}")
        return False

def test_list_apis():
    """Test listing available APIs."""
    print("\n📋 Testing available APIs endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/apis")
        if response.status_code == 200:
            print("✅ Available APIs endpoint working")
            data = response.json()
            print(f"   Total APIs: {data['total_apis']}")
            print(f"   Showing first {len(data['apis'])} APIs:")
            for api in data['apis'][:5]:
                print(f"   - {api}")
            return True
        else:
            print(f"❌ Available APIs endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing available APIs: {e}")
        return False

def test_generate_code():
    """Test code generation endpoint."""
    print("\n🔧 Testing code generation endpoint...")
    try:
        payload = {
            "api_path": "google/example/library/v1/library.proto",
            "language": "python"
        }
        response = requests.post(
            f"{API_BASE_URL}/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Code generation endpoint working")
            data = response.json()
            print(f"   Success: {data['success']}")
            print(f"   Message: {data['message']}")
            if 'api_key' in data:
                print(f"   API Key: {data['api_key'][:20]}...{data['api_key'][-10:]}")
            return True
        else:
            print(f"❌ Code generation endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing code generation: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Google APIs Generator API")
    print("=" * 50)
    
    # Wait a moment for the server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    tests = [
        test_api_endpoint,
        test_api_keys,
        test_specific_api_key,
        test_list_apis,
        test_generate_code
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs.")
    
    print("\n📖 API Documentation: http://localhost:5000/")
    print("🔑 API Keys: http://localhost:5000/api-keys")
    print("📋 Available APIs: http://localhost:5000/apis")

if __name__ == "__main__":
    main()
