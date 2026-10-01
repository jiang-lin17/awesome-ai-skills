#!/usr/bin/env python3
"""把 AI 红队安全类项目合并进 skills.json"""
import json, urllib.request, time

# 11 个新项目
NEW = [
    ("NVIDIA/garak", "NVIDIA/garak", "Garak", "vertical", "🛡️",
     "NVIDIA 出品 LLM 漏洞扫描器——越狱、提示注入、幻觉、数据泄露全测",
     "NVIDIA's LLM vulnerability scanner — jailbreaks, prompt injection, hallucination, data leakage",
     ["~100 攻击向量", "自动越狱测试", "Prompt Injection 检测", "AVID 社区漏洞共享"],
     "pip install garak",
     "pip 安装后 garak --list-probes 看所有攻击向量",
     ["Python", "跨平台"]),

    ("facebookresearch/PurpleLlama", "PurpleLlama", "PurpleLlama (Meta)", "vertical", "🟪",
     "Meta 出品 LLM 安全评估框架——越狱测试 + 运行时防护",
     "Meta's LLM security eval framework — jailbreak testing + runtime guardrails",
     ["内容审核器", "Prompt Injection 防火墙", "恶意代码扫描", "安全基准测试集"],
     "pip install llama-stack",
     "pip 安装后调用安全评估模块",
     ["Python", "Meta 出品"]),

    ("microsoft/PyRIT", "PyRIT", "PyRIT (Microsoft)", "vertical", "🔴",
     "微软 AI 红队工具——多轮对抗 + 多模态攻击编排",
     "Microsoft's AI red team tool — multi-turn adversarial testing, multi-modal",
     ["多轮越狱", "多模态攻击", "攻击剧本编排", "零信任身份"],
     "pip install pyrit",
     "pip 安装后运行预构建的攻击剧本",
     ["Python", "微软出品"]),

    ("promptfoo/promptfoo", "promptfoo", "promptfoo", "vertical", "🧪",
     "被 OpenAI 收购！Prompt 测试 + AI 红队旗舰工具",
     "Acquired by OpenAI! Prompt testing + AI red team flagship tool",
     ["MIT 开源", "CI/CD 集成", "15 万+ 开发者", "OpenAI 内部在用"],
     "npm install -g promptfoo",
     "npm 全局安装后 promptfoo eval 运行红队测试",
     ["Node.js", "OpenAI 背书"]),

    ("giskard-ai/giskard-oss", "giskard", "Giskard", "vertical", "🎯",
     "AI 质量保证 + 自动化红队——Prompt Injection 探针自动生成",
     "AI QA + automated red team — auto-generate prompt injection probes",
     ["自动对抗测试", "Agent 审计", "RAG 质量验证", "Python"],
     "pip install giskard",
     "pip 安装后 giskard scan 一键扫描",
     ["Python", "跨平台"]),

    ("snyk/agent-scan", "snyk-agent-scan", "Snyk Agent Scan", "vertical", "🔒",
     "AI Agent / MCP Server / Skill 安全扫描——15+ 风险类型",
     "Security scanner for AI agents, MCP servers, and agent skills",
     ["15+ 风险类型", "自动发现本地 Agent 配置", "Prompt Injection 检测", "Snyk 出品"],
     "npx snyk-agent-scan scan",
     "npx 一键扫描本地 Agent 配置",
     ["Claude Code", "Cursor", "Windsurf", "Node.js"]),

    ("cisco-ai-defense/skill-scanner", "cisco-skill-scanner", "Cisco Skill Scanner", "vertical", "🛡️",
     "Cisco AI Defense——Agent Skill 风险模式检测",
     "Cisco AI Defense — detect risk patterns in agent skills",
     ["签名检测", "LLM 语义分析", "行为数据流", "可配置规则包"],
     "pip install cisco-ai-defense",
     "pip 安装后调用扫描 API",
     ["Python", "Cisco"]),

    ("protectai/llm-guard", "llm-guard", "LLM Guard", "vertical", "🧱",
     "LLM 交互安全工具包——输入输出双向防护",
     "Security toolkit for LLM interactions — input + output scanning",
     ["输入净化", "有害语言检测", "数据泄露防护", "Prompt Injection 抵抗"],
     "pip install llm-guard",
     "pip 安装后 import 使用",
     ["Python", "跨平台"]),

    ("GitHubSecurityLab/seclab-taskflow-agent", "seclab-taskflow", "SecLab Taskflow Agent", "vertical", "🕵️",
     "GitHub 安全实验室 AI 安全自动化框架——24 Android 漏洞发现",
     "GitHub Security Lab AI security automation framework",
     ["安全研究员 workflow", "Taskflow YAML", "MCP 工具", "漏洞自动发现"],
     "gh codespace create -r GitHubSecurityLab/seclab-taskflow-agent",
     "在 Codespace 里运行 ./scripts/audit/run_mobile.sh",
     ["GitHub Codespaces", "Copilot"]),

    ("slowmist/slowmist-agent-security", "slowmist-agent-sec", "慢雾 Agent 安全", "vertical", "🌫️",
     "慢雾科技 AI Agent 安全审查框架——代码+URL+链上地址",
     "SlowMist AI Agent security review framework — code, URL, on-chain",
     ["GitHub Repo 审计", "URL/文档分析", "链上地址审查", "对抗环境"],
     "git clone https://github.com/slowmist/slowmist-agent-security",
     "克隆后运行审查脚本",
     ["Python", "慢雾科技"]),

    ("adversa-ai/adversa-red-team-agent", "adversa-redteam", "Adversa AI Red Team Agent", "vertical", "💀",
     "专门攻破 AI Agent 的自动化红队——GitHub ProdBot CTF 全通关",
     "AI agent red team agent — cleared all GitHub ProdBot CTF levels",
     ["自动越狱", "多轮对抗", "Agent 权限提升", "MCP Tool 污染"],
     "pip install adversa-redteam",
     "pip 安装后 point at target",
     ["Python", "研究级"]),
]

def get_stars(repo):
    url = f"https://api.github.com/repos/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "awesome-ai-skills"}
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r).get("stargazers_count", 0)
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print("  限流等 15s...")
                time.sleep(15); continue
            print(f"  {repo}: HTTP {e.code}")
            return None
        except Exception as e:
            print(f"  {repo}: {e}"); time.sleep(5); return None
    return None

# 拉 star
print("🚀 开始拉 Star 数...")
enriched = []
for i, p in enumerate(NEW, 1):
    stars = get_stars(p[0])
    print(f"[{i}/{len(NEW)}] {p[0]:45s} => {stars}", flush=True)
    time.sleep(0.5)
    enriched.append((*p, stars))

# 合并
with open("docs/data/skills.json", "r", encoding="utf-8") as f:
    data = json.load(f)

existing_ids = {s["id"] for s in data["skills"]}
added = 0
for repo, pid, name, cat, emoji, zh, en, feats, install, usage, compat, stars in enriched:
    if pid in existing_ids:
        continue
    data["skills"].append({
        "id": pid, "category": cat, "name": name,
        "owner": repo.split("/")[0], "repo": repo,
        "stars": stars or 0, "emoji": emoji,
        "shortDesc": zh, "descEn": en,
        "features": feats, "install": install,
        "usage": usage, "compatible": compat,
        "repoUrl": f"https://github.com/{repo}"
    })
    added += 1

# 排序 + 去重
seen = set()
clean = []
for s in data["skills"]:
    if s["id"] not in seen:
        seen.add(s["id"])
        clean.append(s)
data["skills"] = sorted(clean, key=lambda x: x["stars"], reverse=True)

with open("docs/data/skills.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n🎉 新增 {added} 个，总计 {len(data['skills'])} 个 Skill")
print("\n新增 Top 5:")
for s in sorted([x for x in data["skills"] if x["id"] in {e[1] for e in enriched}], key=lambda x: -x["stars"])[:5]:
    print(f"  {s['stars']:>8,} ⭐  {s['name']}")

