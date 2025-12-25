#!/usr/bin/env python3
"""
Get public IP address and access information
"""
import socket
import subprocess
import sys

def get_public_ip():
    """Get the machine's public IP address"""
    try:
        # Try using ipconfig on Windows
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if 'IPv4 Address' in line:
                ip = line.split(':')[1].strip()
                return ip
    except:
        pass
    
    try:
        # Fallback: get IP from socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unable to determine"

print("\n" + "="*70)
print("🚀 Flask LIMS Server - Public Access Information")
print("="*70)

ip = get_public_ip()
print(f"\n📱 Your Computer's Local IP:  http://{ip}:5000")
print(f"💻 Localhost Only:            http://localhost:5000")
print(f"\n⚠️  IMPORTANT:")
print(f"   - Both should be used over LAN/local network only")
print(f"   - For PUBLIC internet access, use an ngrok free account:")
print(f"     1. Sign up: https://dashboard.ngrok.com/signup")
print(f"     2. Copy your authtoken from dashboard")
print(f"     3. Install it: ngrok config add-authtoken YOUR_TOKEN")
print(f"     4. Run: ngrok http 5000")
print("\n" + "="*70 + "\n")
