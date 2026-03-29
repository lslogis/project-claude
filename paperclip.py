"""Paperclip API Helper — Synth Corp CEO's hands"""
import requests
import json
import sys

BASE = "http://192.168.219.100:3100"
COMPANY_ID = "fb0a1b46-94da-4f9a-a472-5ad50dd42742"
session = requests.Session()

def login():
    r = session.post(f"{BASE}/api/auth/sign-in/email", json={
        "email": "lslogis8082@gmail.com",
        "password": "U8h8MgqiXzGPX4M"
    })
    if r.ok:
        print("Logged in.")
    else:
        print(f"Login failed: {r.text}")
        sys.exit(1)

def api(method, path, data=None):
    url = f"{BASE}/api/companies/{COMPANY_ID}/{path}"
    headers = {"Origin": BASE, "Referer": f"{BASE}/SYN/dashboard"}
    r = getattr(session, method)(url, json=data, headers=headers)
    return r.json() if r.ok else {"error": r.status_code, "detail": r.text}

def list_issues():
    issues = api("get", "issues")
    if isinstance(issues, list):
        for i in issues:
            print(f"{i['identifier']} | {i['status']} | {i['title']}")
    else:
        print(issues)

def create_issue(title, description="", assignee_id=None, priority="medium"):
    data = {"title": title, "description": description, "priority": priority}
    if assignee_id:
        data["assigneeAgentId"] = assignee_id
    result = api("post", "issues", data)
    if "identifier" in result:
        print(f"Created: {result['identifier']} - {result['title']}")
    else:
        print(result)

def list_agents():
    agents = api("get", "agents")
    if isinstance(agents, list):
        for a in agents:
            print(f"{a.get('name','')} | {a.get('id','')}")
    else:
        print(agents)

if __name__ == "__main__":
    login()
    if len(sys.argv) < 2:
        print("Usage: python paperclip.py [issues|agents|create 'title' 'desc']")
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "issues":
        list_issues()
    elif cmd == "agents":
        list_agents()
    elif cmd == "create" and len(sys.argv) >= 3:
        title = sys.argv[2]
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        create_issue(title, desc)
    else:
        print(f"Unknown command: {cmd}")
