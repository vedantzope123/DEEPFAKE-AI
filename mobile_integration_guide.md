# 📱 Mobile Integration Guide

This guide explains how to integrate the Deepfake Detector into mobile applications.

## 🌐 Option 1: Deploy Streamlit App (Easiest)

### Step 1: Deploy to Streamlit Cloud
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Deploy - you'll get a URL like `https://your-app.streamlit.app`

### Step 2: Access on Mobile
- The Streamlit app is **responsive** and works on mobile browsers
- Users can add it to their home screen (PWA-like)
- No native app development needed!

**Pros:**
- ✅ Free hosting
- ✅ Works on all devices
- ✅ No app store approval needed
- ✅ Automatic updates

**Cons:**
- ❌ Requires internet
- ❌ Not a "native" app experience

---

## 🔌 Option 2: REST API + Native Mobile App

### Backend: FastAPI (Already Created)

**File:** `api_backend.py`

**Run locally:**
```bash
pip install -r requirements_api.txt
uvicorn api_backend:app --reload
```

**Deploy API:**
- **Railway:** https://railway.app (free tier)
- **Render:** https://render.com (free tier)
- **Fly.io:** https://fly.io (free tier)
- **Heroku:** https://heroku.com

### Mobile Frontend Examples

#### **React Native (iOS/Android)**

```javascript
// DeepfakeDetector.js
import React, { useState } from 'react';
import { View, Button, Image, Text } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

const DeepfakeDetector = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const API_URL = 'https://your-api.railway.app/analyze';
  const API_KEY = 'your-gemini-api-key'; // Store securely!

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      quality: 1,
    });

    if (!result.canceled) {
      analyzeMedia(result.assets[0]);
    }
  };

  const analyzeMedia = async (media) => {
    setLoading(true);
    
    const formData = new FormData();
    formData.append('file', {
      uri: media.uri,
      type: media.type === 'image' ? 'image/jpeg' : 'video/mp4',
      name: 'upload.jpg',
    });
    formData.append('api_key', API_KEY);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Button title="Pick Image/Video" onPress={pickImage} />
      
      {loading && <Text>Analyzing...</Text>}
      
      {result && (
        <View style={{ marginTop: 20 }}>
          <Text style={{ fontSize: 24, fontWeight: 'bold' }}>
            Verdict: {result.verdict}
          </Text>
          <Text>Confidence: {result.confidence}</Text>
          <Text>{result.analysis}</Text>
        </View>
      )}
    </View>
  );
};

export default DeepfakeDetector;
```

#### **Flutter (iOS/Android)**

```dart
// deepfake_detector.dart
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:convert';

class DeepfakeDetector extends StatefulWidget {
  @override
  _DeepfakeDetectorState createState() => _DeepfakeDetectorState();
}

class _DeepfakeDetectorState extends State<DeepfakeDetector> {
  final String apiUrl = 'https://your-api.railway.app/analyze';
  final String apiKey = 'your-gemini-api-key'; // Store securely!
  
  bool isLoading = false;
  Map<String, dynamic>? result;

  Future<void> pickAndAnalyze() async {
    final ImagePicker picker = ImagePicker();
    final XFile? image = await picker.pickImage(source: ImageSource.gallery);

    if (image != null) {
      setState(() => isLoading = true);

      var request = http.MultipartRequest('POST', Uri.parse(apiUrl));
      request.fields['api_key'] = apiKey;
      request.files.add(await http.MultipartFile.fromPath('file', image.path));

      var response = await request.send();
      var responseData = await response.stream.bytesToString();
      
      setState(() {
        result = json.decode(responseData);
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Deepfake Detector')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: pickAndAnalyze,
              child: Text('Select Image/Video'),
            ),
            if (isLoading) CircularProgressIndicator(),
            if (result != null) ...[
              SizedBox(height: 20),
              Text(
                'Verdict: ${result!['verdict']}',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              Text('Confidence: ${result!['confidence']}'),
              SizedBox(height: 10),
              Text(result!['analysis']),
            ],
          ],
        ),
      ),
    );
  }
}
```

#### **Swift (iOS Native)**

```swift
// DeepfakeDetector.swift
import UIKit

class DeepfakeDetector: UIViewController {
    let apiUrl = "https://your-api.railway.app/analyze"
    let apiKey = "your-gemini-api-key" // Store in Keychain!
    
    func analyzeImage(_ image: UIImage) {
        guard let imageData = image.jpegData(compressionQuality: 0.8) else { return }
        
        let url = URL(string: apiUrl)!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"api_key\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(apiKey)\r\n".data(using: .utf8)!)
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data else { return }
            let result = try? JSONDecoder().decode(AnalysisResult.self, from: data)
            // Update UI with result
        }.resume()
    }
}

struct AnalysisResult: Codable {
    let verdict: String
    let confidence: String
    let analysis: String
    let is_fake: Bool
}
```

---

## 🌍 Option 3: GitHub Pages + Streamlit Cloud

**GitHub Pages** hosts static HTML/JS only, so you can't run Python there. Instead:

1. **Deploy Streamlit app** to Streamlit Cloud (free)
2. **Create a landing page** on GitHub Pages that links to your Streamlit app

**Example landing page:**

```html
<!-- index.html for GitHub Pages -->
<!DOCTYPE html>
<html>
<head>
    <title>Deepfake Detector</title>
</head>
<body style="text-align: center; padding: 50px;">
    <h1>🛡️ Deepfake AI Detector</h1>
    <p>Detect AI-generated deepfakes using advanced Gemini AI</p>
    <a href="https://your-app.streamlit.app" style="
        background: linear-gradient(45deg, #00c6ff, #0072ff);
        color: white;
        padding: 15px 30px;
        text-decoration: none;
        border-radius: 25px;
        font-size: 18px;
    ">Launch App</a>
</body>
</html>
```

---

## 📊 Comparison

| Method | Cost | Complexity | Mobile UX | Best For |
|--------|------|-----------|-----------|----------|
| **Streamlit Cloud** | Free | ⭐ Easy | Good | Quick deployment |
| **API + Native App** | Free-$5/mo | ⭐⭐⭐ Advanced | Excellent | Production apps |
| **WebView Wrapper** | Free | ⭐⭐ Medium | Good | Hybrid approach |

---

## 🚀 Recommended Approach

**For Most Users:**
1. Deploy Streamlit app to Streamlit Cloud (free)
2. Share the URL - works on all devices
3. Users can "Add to Home Screen" on mobile

**For Production Mobile App:**
1. Deploy FastAPI backend to Railway/Render
2. Build React Native/Flutter app
3. Submit to App Store/Play Store

---

## 🔐 Security Notes

- **Never hardcode API keys** in mobile apps
- Use environment variables or secure key storage
- Implement rate limiting on your API
- Add authentication if needed

---

## 📞 API Testing

Test the API with curl:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@test_image.jpg" \
  -F "api_key=YOUR_GEMINI_API_KEY"
```

**Response:**
```json
{
  "verdict": "REAL",
  "confidence": "95%",
  "analysis": "Detailed analysis text...",
  "is_fake": false
}
```
