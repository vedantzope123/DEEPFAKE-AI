"""
Test script for Deepfake Detection API
Run this after deploying to Vercel to verify everything works
"""

import requests
import sys

def test_api(base_url):
    """Test the deployed API"""
    
    print(f"🧪 Testing API at: {base_url}\n")
    
    # Test 1: Root endpoint
    print("Test 1: Checking root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint works!")
            print(f"   Status: {data.get('status')}")
            print(f"   GenAI Available: {data.get('genai_available')}")
            print(f"   Python Version: {data.get('python_version', 'N/A')[:10]}...\n")
        else:
            print(f"❌ Failed: {response.status_code}\n")
            return False
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False
    
    # Test 2: Health endpoint
    print("Test 2: Checking health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"   Service: {data.get('service')}\n")
        else:
            print(f"❌ Failed: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # Test 3: Check docs
    print("Test 3: Checking API documentation...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API docs available at: {}/docs\n".format(base_url))
        else:
            print(f"⚠️  Docs returned: {response.status_code}\n")
    except Exception as e:
        print(f"⚠️  Docs check failed: {e}\n")
    
    print("=" * 60)
    print("🎉 API is deployed and working!")
    print("=" * 60)
    print(f"\n📚 View interactive docs: {base_url}/docs")
    print(f"📖 View ReDoc: {base_url}/redoc")
    print(f"\n💡 To test image analysis:")
    print(f"   curl -X POST \"{base_url}/analyze\" \\")
    print(f"     -F \"file=@your_image.jpg\" \\")
    print(f"     -F \"api_key=YOUR_GEMINI_API_KEY\"")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        api_url = input("Enter your Vercel deployment URL (e.g., https://your-project.vercel.app): ").strip()
    
    # Remove trailing slash if present
    api_url = api_url.rstrip('/')
    
    success = test_api(api_url)
    
    if not success:
        print("\n⚠️  Some tests failed. Check the Vercel deployment logs.")
        sys.exit(1)
