import requests
import re
import time
import sys
import os

def run_verification(pdf_path):
    base_url = "http://127.0.0.1:5002"
    
    # 1. Upload the resume
    print(f"📤 Uploading resume from: {pdf_path}...")
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return False
        
    with open(pdf_path, 'rb') as f:
        files = {'resume': (os.path.basename(pdf_path), f, 'application/pdf')}
        response = requests.post(f"{base_url}/upload", files=files)
    
    if response.status_code != 200:
        print(f"❌ Upload failed with status code {response.status_code}")
        return False
    
    # 2. Extract eval_id from response html
    html_content = response.text
    match = re.search(r'const evalId = "([^"]+)";', html_content)
    if not match:
        print("❌ Could not find evalId in response HTML")
        return False
    
    eval_id = match.group(1)
    print(f"✅ Found eval_id: {eval_id}")
    
    # 3. Poll progress
    print("⏳ Polling progress...")
    start_time = time.time()
    for _ in range(120):
        time.sleep(0.5)
        try:
            progress_resp = requests.get(f"{base_url}/progress/{eval_id}")
        except Exception as e:
            print(f"⚠️ Progress request failed: {e}")
            continue
            
        if progress_resp.status_code != 200:
            print(f"❌ Progress check failed with status code {progress_resp.status_code}")
            return False
            
        data = progress_resp.json()
        print(f"   Status: {data.get('status')}, Progress: {data.get('progress')}%, Message: {data.get('message')}")
        
        if data.get('status') == 'complete':
            end_time = time.time()
            print(f"✅ Evaluation complete in {end_time - start_time:.2f} seconds!")
            print(f"\n🔗 RESULTS PAGE URL: {base_url}/result/{eval_id}")
            return eval_id
        elif data.get('status') == 'error':
            print(f"❌ Evaluation error: {data.get('error')}")
            return False
    else:
        print("❌ Polling timed out")
        return False

if __name__ == "__main__":
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/denis/Downloads/DENIS KURUDIMOV v2.pdf"
    run_verification(pdf_path)
