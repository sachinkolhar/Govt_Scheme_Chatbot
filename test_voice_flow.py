#!/usr/bin/env python3
"""
Voice Assistant Flow Diagnostic Test

Tests the complete voice flow:
1. Backend /api/voice-assistant/chat endpoint
2. Response generation with Groq
3. Error handling and fallbacks
"""

import sys
import base64
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✓ Backend is running (status: {response.status_code})")
        return True
    except Exception as e:
        print(f"✗ Backend not responding: {e}")
        return False

def test_voice_chat_endpoint():
    """Test the /api/voice-assistant/chat endpoint"""
    print("\n" + "="*80)
    print("Testing /api/voice-assistant/chat Endpoint")
    print("="*80)
    
    test_queries = [
        {
            "query": "Tell me about PM-KISAN scheme",
            "language": "en",
            "description": "English scheme query"
        },
        {
            "query": "सरकारी योजनाओं के बारे में बताएं",
            "language": "hi", 
            "description": "Hindi scheme query"
        },
        {
            "query": "What are scholarships?",
            "language": "en",
            "description": "Scholarship query"
        }
    ]
    
    for test in test_queries:
        print(f"\n--- Test: {test['description']} ---")
        print(f"Query: {test['query']}")
        print(f"Language: {test['language']}")
        
        try:
            payload = {
                "query": test["query"],
                "language": test["language"],
                "history": []
            }
            
            response = requests.post(
                f"{BASE_URL}/api/voice-assistant/chat",
                json=payload,
                timeout=60
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Response received")
                print(f"  - Query echo: {data.get('query', 'N/A')[:50]}...")
                print(f"  - Language: {data.get('language')}")
                print(f"  - Answer length: {len(data.get('answer', ''))} chars")
                print(f"  - Answer preview: {data.get('answer', 'N/A')[:100]}...")
                
                # Check if answer is empty or error
                if not data.get('answer'):
                    print(f"  ✗ WARNING: Empty answer!")
                elif "I am unable to answer" in data.get('answer', ''):
                    print(f"  ⚠ GROQ fallback response (no API key or error)")
                else:
                    print(f"  ✓ Valid answer received")
            else:
                print(f"✗ Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"✗ Exception: {type(e).__name__}: {e}")

def test_tts_endpoint():
    """Test the /api/audio/synthesize endpoint with voice response"""
    print("\n" + "="*80)
    print("Testing /api/audio/synthesize Endpoint (TTS)")
    print("="*80)
    
    test_texts = [
        {
            "text": "You are eligible for the PM-KISAN scheme",
            "language": "en",
            "description": "English voice response"
        },
        {
            "text": "आप पीएम-किसान योजना के लिए पात्र हैं",
            "language": "hi",
            "description": "Hindi voice response"
        }
    ]
    
    for test in test_texts:
        print(f"\n--- Test: {test['description']} ---")
        print(f"Text: {test['text'][:50]}...")
        print(f"Language: {test['language']}")
        
        try:
            payload = {
                "text": test["text"],
                "language": test["language"]
            }
            
            response = requests.post(
                f"{BASE_URL}/api/audio/synthesize",
                json=payload,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    audio_data = data.get('data')
                    if audio_data:
                        audio_bytes = base64.b64decode(audio_data)
                        print(f"✓ Audio generated ({len(audio_bytes)} bytes)")
                    else:
                        print(f"✗ No audio data in response")
                        print(f"  Error: {data.get('error')}")
                else:
                    print(f"✗ Synthesis failed: {data.get('error')}")
            else:
                print(f"✗ Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"✗ Exception: {type(e).__name__}: {e}")

def test_complete_flow():
    """Test the complete voice flow"""
    print("\n" + "="*80)
    print("Testing Complete Voice Flow")
    print("="*80)
    
    print("\nStep 1: Get voice response from /api/voice-assistant/chat")
    try:
        chat_response = requests.post(
            f"{BASE_URL}/api/voice-assistant/chat",
            json={
                "query": "What is PMAYG scheme?",
                "language": "en",
                "history": []
            },
            timeout=60
        )
        
        if chat_response.status_code != 200:
            print(f"✗ Chat failed: {chat_response.status_code}")
            return
        
        chat_data = chat_response.json()
        answer = chat_data.get('answer', '')
        language = chat_data.get('language', 'en')
        
        print(f"✓ Chat response received ({len(answer)} chars)")
        
        print("\nStep 2: Synthesize response to audio")
        tts_response = requests.post(
            f"{BASE_URL}/api/audio/synthesize",
            json={
                "text": answer,
                "language": language
            },
            timeout=30
        )
        
        if tts_response.status_code != 200:
            print(f"✗ TTS failed: {tts_response.status_code}")
            return
        
        tts_data = tts_response.json()
        if tts_data.get('success'):
            audio_data = tts_data.get('data')
            if audio_data:
                audio_bytes = base64.b64decode(audio_data)
                print(f"✓ Audio generated ({len(audio_bytes)} bytes)")
                print(f"\n✓ COMPLETE FLOW SUCCESSFUL")
                
                # Save audio for testing
                with open("test_voice_response.mp3", "wb") as f:
                    f.write(audio_bytes)
                print(f"  Audio saved to: test_voice_response.mp3")
            else:
                print(f"✗ No audio data in TTS response")
        else:
            print(f"✗ TTS failed: {tts_data.get('error')}")
            
    except Exception as e:
        print(f"✗ Exception: {type(e).__name__}: {e}")

def check_groq_api_key():
    """Check if GROQ_API_KEY is set"""
    print("\n" + "="*80)
    print("Environment Check")
    print("="*80)
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv("backend/.env")
        groq_key = os.getenv("GROQ_API_KEY", "")
        
        if groq_key:
            print(f"✓ GROQ_API_KEY is set (length: {len(groq_key)} chars)")
        else:
            print(f"✗ GROQ_API_KEY is NOT set")
            print(f"  Voice responses will use fallback mode")
    except Exception as e:
        print(f"⚠ Could not check env: {e}")

def main():
    print("="*80)
    print("Voice Assistant Flow Diagnostic")
    print("="*80)
    
    check_groq_api_key()
    
    if not test_health():
        print("\n⚠ Backend is not running. Start it with:")
        print("  python -m uvicorn backend.main:app --reload")
        return
    
    test_voice_chat_endpoint()
    test_tts_endpoint()
    test_complete_flow()
    
    print("\n" + "="*80)
    print("Diagnostic Complete")
    print("="*80)
    print("\nKey findings:")
    print("1. Check if GROQ_API_KEY is set in backend/.env")
    print("2. Voice assistant responses are generated (even if fallback)")
    print("3. TTS endpoint can synthesize the responses")
    print("4. Frontend should be able to play the audio")

if __name__ == "__main__":
    main()
