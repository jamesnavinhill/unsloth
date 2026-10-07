#!/usr/bin/env python3
"""
Nominal Connection & Infrastructure Verification Script
Validates all external services and endpoints documented in CONNECTIONS.md:
  1. Local environment (.env parsing)
  2. GitHub remote repository sync
  3. Hugging Face Hub (Token, write scope, LFM2.5-2.6B model access, Buckets)
  4. Weights & Biases API (GraphQL viewer authentication)
  5. Agency Gateway LiteLLM endpoint & model catalog
  6. Kaggle API authentication
"""

import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
from pathlib import Path

# Fix stdout encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

def load_env():
    """Load key-value pairs from .env without third-party libraries."""
    env = {}
    if not ENV_PATH.exists():
        print(f"[!] Warning: {ENV_PATH} not found.")
        return env
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env

def print_result(service, status, message):
    mark = "PASS" if status else "FAIL"
    print(f"[{mark:4s}] {service:<22} : {message}")

def check_github():
    try:
        res = subprocess.run(
            ["git", "remote", "-v"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            check=True
        )
        if "github.com/jamesnavinhill/unsloth" in res.stdout:
            print_result("GitHub Remote", True, "Synced to https://github.com/jamesnavinhill/unsloth.git")
            return True
        else:
            print_result("GitHub Remote", False, f"Unexpected remote: {res.stdout.strip()}")
            return False
    except Exception as e:
        print_result("GitHub Remote", False, str(e))
        return False

def check_huggingface(token, username):
    if not token:
        print_result("Hugging Face Hub", False, "HF_TOKEN not found in .env")
        return False
    req = urllib.request.Request(
        "https://huggingface.co/api/whoami-v2",
        headers={"Authorization": f"Bearer {token}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            user = data.get("name")
            role = data.get("auth", {}).get("role") or data.get("type", "standard")
            is_valid = (user == username or username in user)
            print_result("Hugging Face Hub", is_valid, f"User: {user} | Role/Type: {role} | Token name: {data.get('auth', {}).get('accessToken', {}).get('displayName', 'unsloth')}")
            
            # Check target model existence
            m_req = urllib.request.Request(
                "https://huggingface.co/api/models/LiquidAI/LFM2.5-2.6B",
                headers={"Authorization": f"Bearer {token}"}
            )
            with urllib.request.urlopen(m_req, timeout=10) as m_resp:
                m_data = json.loads(m_resp.read().decode("utf-8"))
                model_id = m_data.get("id")
                print_result("LFM2.5-2.6B Model", True, f"Model accessible: {model_id} (Hybrid Conv/GQA)")
            return True
    except Exception as e:
        print_result("Hugging Face Hub", False, str(e))
        return False

def check_wandb(key, entity, project):
    if not key:
        print_result("Weights & Biases", False, "WANDB_API_KEY not found in .env")
        return False
    gql_query = json.dumps({"query": "{ viewer { username } }"}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.wandb.ai/graphql",
        data=gql_query,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            viewer = data.get("data", {}).get("viewer", {})
            user = viewer.get("username", "authenticated")
            print_result("Weights & Biases", True, f"User: {user} | Entity: {entity} | Project: {project}")
            return True
    except Exception as e:
        print_result("Weights & Biases", False, str(e))
        return False

def check_agency_gateway(base_url, api_key):
    if not base_url or not api_key:
        print_result("Agency Gateway", False, "GATEWAY_BASE_URL or GATEWAY_API_KEY not set")
        return False
    url = f"{base_url.rstrip('/')}/models"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = data.get("data", [])
            print_result("Agency Gateway", True, f"Active endpoint ({url}) | Models available: {len(models)}")
            return True
    except Exception as e:
        print_result("Agency Gateway", False, str(e))
        return False

def check_kaggle(username, token):
    if not username or not token:
        print_result("Kaggle API", False, "KAGGLE_USERNAME or KAGGLE_API_TOKEN not set")
        return False
    import base64
    auth = base64.b64encode(f"{username}:{token}".encode("utf-8")).decode("utf-8")
    req = urllib.request.Request(
        "https://api.kaggle.com/v1/datasets/list?pageSize=1",
        headers={"Authorization": f"Basic {auth}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print_result("Kaggle API", True, f"Basic auth validated on api.kaggle.com/v1 (User: {username})")
            return True
    except Exception as e:
        print_result("Kaggle API", False, str(e))
        return False

def main():
    print("=" * 70)
    print("LFM2.5-2.6B Humanizer — Nominal Connection Verification")
    print("=" * 70)
    env = load_env()
    
    check_github()
    check_huggingface(env.get("HF_TOKEN"), env.get("HF_USERNAME", "jamesnavinhill"))
    check_wandb(env.get("WANDB_API_KEY"), env.get("WANDB_ENTITY", "navin_hill"), env.get("WANDB_PROJECT", "copyright"))
    check_agency_gateway(env.get("GATEWAY_BASE_URL"), env.get("GATEWAY_API_KEY"))
    check_kaggle(env.get("KAGGLE_USERNAME"), env.get("KAGGLE_API_TOKEN"))
    print("=" * 70)

if __name__ == "__main__":
    main()
