#!/usr/bin/env python3
"""
Expose local Flask app to public internet using ngrok tunneling
"""
from pyngrok import ngrok
import time

# Connect ngrok (no auth token needed for basic usage)
public_url = ngrok.connect(5000, "http")
print(f"\n{'='*60}")
print(f"🌐 PUBLIC URL: {public_url}")
print(f"{'='*60}\n")
print(f"Your Flask app is now publicly accessible at: {public_url}")
print(f"Local URL: http://localhost:5000")
print(f"\nKeep this script running to maintain the tunnel.")
print(f"Press Ctrl+C to stop.\n")

# Keep the tunnel alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down ngrok tunnel...")
    ngrok.disconnect(public_url)
    ngrok.kill()
