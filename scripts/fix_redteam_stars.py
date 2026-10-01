#!/usr/bin/env python3
"""修复红队项目的 Star 数——重新从 GitHub API 拉"""
import json, urllib.request, time

TARGETS = [
    ("NVIDIA/garak", "Garak"),
    ("facebookresearch/PurpleLlama", "PurpleLlama (Meta)"),
    ("microsoft/PyRIT", "PyRIT (Microsoft)"),
    ("promptfoo/promptfoo", "promptfoo"),
    ("giskard-ai/giskard-oss", "Giskard"),
    ("snyk/agent-scan", "Snyk Agent Scan"),
    ("cisco-ai-defense/skill-scanner", "Cisco Skill Scanner"),
    ("protectai/llm-guard", "LLM Guard"),
    ("GitHubSecurityLab/seclab-taskflow-agent", "SecLab Taskflow Agent"),
    ("slowmist/slowmist-agent-security", "慢雾 Agent 安全"),
]

def get_stars(repo):
    url = f"https://api.github.com/repos/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "awesome-ai-skills"}
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read().decode("utf-8")
                return json.loads(body).get("stargazers_count", 0)
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print("  限流，等 15s..."); time.sleep(15); continue
            print(f"  {repo}: HTTP {e.code}"); return None
        except Exception as e:
            print(f"  {repo}: {e}"); time.sleep(2); return None
    return None

# 拉
stars_map = {}
for repo, name in TARGETS:
    s = get_stars(repo)
    print(f"  {name:28s} => {s}")
    stars_map[name] = s
    time.sleep(0.6)

# 更新 JSON
with open("docs/data/skills.json", "r", encoding="utf-8") as f:
    data = json.load(f)

updated = 0
for s in data["skills"]:
    if s["name"] in stars_map and stars_map[s["name"]] is not None and stars_map[s["name"]] > 0:
        if s["stars"] == 0:
            s["stars"] = stars_map[s["name"]]
            updated += 1
            print(f"✅ {s['name']}: {stars_map[s['name']]} ⭐")

data["skills"].sort(key=lambda x: x["stars"], reverse=True)

with open("docs/data/skills.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n🎉 更新 {updated} 个，总计 {len(data['skills'])} 个 Skill")
