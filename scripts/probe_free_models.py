import urllib.request
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))
base_url = env.get('GATEWAY_BASE_URL', '').rstrip('/')
api_key = env.get('GATEWAY_API_KEY', '')

nv_models = [
    'nv-z-ai-glm-5-3',
    'nv-moonshotai-kimi-k3',
    'nv-nvidia-nemotron-3-ultra-550b-a55b',
    'nv-nvidia-nemotron-3-super-120b-a12b',
    'nv-deepseek-ai-deepseek-v4-1-flash',
    'nv-z-ai-glm-5-3-flash',
    'nv-google-gemma-4-31b-it',
    'or-free'
]

print("Probing Free Models via Gateway...", flush=True)

for m in nv_models:
    payload = {
        'model': m,
        'messages': [{'role': 'user', 'content': 'Respond with OK.'}],
        'max_tokens': 50
    }
    req = urllib.request.Request(
        f'{base_url}/chat/completions',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            content = data['choices'][0]['message']['content'].strip()
            print(f"[PASS] {m:<38} -> '{content[:40]}'", flush=True)
    except Exception as e:
        print(f"[FAIL] {m:<38} -> Error: {e}", flush=True)
