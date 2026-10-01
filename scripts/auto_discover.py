#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Awesome AI Skills — 自动发现脚本
=====================================

用 GitHub Search API 自动扫描热门 AI Skill 项目，
发现新的 → 拉 Star 数和描述 → 合并进 skills.json → 排序 → 保存。

GitHub Actions 每周自动运行，让你的项目自己"生长"！
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# ============== 配置区 ==============
# 搜索关键词（按优先级）
SEARCH_QUERIES = [
    "agent skill claude code stars:>100",
    "agent skills AI coding star stars:>200",
    "claude code skill stars:>100",
    "cursor skill AI agent stars:>100",
    "openclaw skill stars:>50",
    "mcp server AI tool stars:>200",
    "jailbreak red team LLM stars:>500",
    "prompt injection AI security stars:>200",
]

# 只收录这些主语言
PREFERRED_LANGS = {"python", "typescript", "javascript", "shell", "go", "rust"}

# 分类映射（基于 repo 描述 + 关键词）
CATEGORY_KEYWORDS = {
    "framework": ["agent framework", "agentic framework", "autonomous agent", "llm agent", "multi-agent"],
    "skills": ["skill", "skills", "agentic skills", "coding agent skill"],
    "memory": ["memory", "persistent", "vector memory", "long-term"],
    "web": ["web scraping", "crawl", "browser", "playwright", "firecrawl", "search api"],
    "code": ["coding", "code generation", "code review", "IDE", "developer tool"],
    "vertical": ["marketing", "ppt", "career", "research", "finance", "creative"],
    "learn": ["awesome", "learn", "tutorial", "course", "book"],
    "prompts": ["system prompt", "prompt engineering", "prompt injection", "jailbreak", "red team", "security"],
}

# 安装命令推断规则（简单启发式）
INSTALL_RULES = [
    ("pip install", lambda r: r.get("language", "").lower() == "python"),
    ("npm install -g", lambda r: r.get("language", "").lower() in ("typescript", "javascript")),
    ("npx skills add", lambda r: "skill" in r.get("description", "").lower() or "agentic skill" in r.get("description", "").lower()),
    ("git clone", lambda r: True),  # 兜底
]


# ============== GitHub API 工具 ==============
def gh_api(path, token=None):
    """调 GitHub API，自动处理限流"""
    url = f"https://api.github.com{path}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "awesome-ai-skills-discoverer",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"  ⚠️ 限流，等 30s..."); time.sleep(30); continue
            if e.code == 404:
                return None
            print(f"  ❌ HTTP {e.code}: {path}"); return None
        except Exception as e:
            print(f"  ❌ {e}"); time.sleep(5); return None
    return None


def search_repos(query, max_per_query=15):
    """搜 GitHub 仓库"""
    results = []
    for page in range(1, 4):  # 搜前 3 页
        q = urllib.parse.quote(query)
        data = gh_api(f"/search/repositories?q={q}&sort=stars&order=desc&per_page={max_per_query}&page={page}")
        if not data or "items" not in data:
            break
        items = data["items"]
        if not items:
            break
        results.extend(items)
        time.sleep(0.5)  # Search API 有限流
    return results


def repo_has_skill_file(full_name):
    """检查仓库根目录有没有 SKILL.md / skill.md / MCP 相关"""
    for filename in ["SKILL.md", "skill.md", "skill.json"]:
        data = gh_api(f"/repos/{full_name}/contents/{filename}")
        if data and "name" in data:
            return True
    # 也检查 .claude/skills/ 等常见路径
    for path in [".claude/skills", ".cursor/skills", ".openclaw/skills", "skills"]:
        data = gh_api(f"/repos/{full_name}/contents/{path}")
        if data and isinstance(data, list):
            for item in data:
                if item.get("name", "").lower().endswith(".md"):
                    return True
    return False


# ============== 分类 & 推断 ==============
def guess_category(repo):
    """根据仓库描述推断分类"""
    text = f"{repo.get('description', '')} {repo.get('name', '')}".lower()
    scores = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        scores[cat] = sum(1 for kw in kws if kw in text)
    if max(scores.values()) == 0:
        return "vertical"  # 默认归到垂直领域
    return max(scores, key=scores.get)


def guess_install(repo):
    """猜测安装命令"""
    desc = repo.get("description", "").lower()
    lang = repo.get("language", "").lower()
    owner = repo.get("full_name", "")

    if lang == "python":
        return f"pip install {repo['name']}"
    if lang in ("typescript", "javascript") and "skill" in desc:
        return f"npx skills add {owner}"
    if lang in ("typescript", "javascript"):
        return f"npm install -g {repo['name']}"
    return f"git clone https://github.com/{owner}.git"


def guess_emoji(repo):
    """给每个 skill 一个 emoji（按分类）"""
    cat = guess_category(repo)
    emoji_map = {
        "framework": "🧠", "skills": "⚡", "memory": "💾",
        "web": "🌐", "code": "💻", "prompts": "🔍",
        "learn": "📚", "vertical": "🎯",
    }
    return emoji_map.get(cat, "✨")


# ============== 主流程 ==============
def main():
    print("=" * 60)
    print("🤖 Awesome AI Skills — 自动发现")
    print("=" * 60)

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("⚠️  未设置 GITHUB_TOKEN，API 限流会比较严（60次/小时）")
    else:
        print("✅ 已有 GITHUB_TOKEN（5000次/小时）")

    # 1. 读现有数据
    here = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(here, "..", "docs", "data", "skills.json")
    data_path = os.path.abspath(data_path)

    with open(data_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_ids = {s["id"] for s in existing["skills"]}
    existing_repos = {s["repo"] for s in existing["skills"]}
    print(f"\n📚 现有 {len(existing['skills'])} 个 Skill")

    # 2. 搜新仓库
    print(f"\n🔍 开始搜 GitHub（{len(SEARCH_QUERIES)} 个关键词）...")
    all_candidates = []
    for q in SEARCH_QUERIES:
        print(f"  🔎 {q}")
        repos = search_repos(q)
        for r in repos:
            full_name = r["full_name"]
            if full_name in existing_repos:
                continue  # 已有，跳过
            if r.get("stargazers_count", 0) < 50:
                continue  # 星太少
            if r.get("archived"):
                continue
            all_candidates.append(r)
        time.sleep(1)

    # 3. 去重 + 过滤
    seen = set()
    new_repos = []
    for r in sorted(all_candidates, key=lambda x: -x.get("stargazers_count", 0)):
        if r["id"] in seen:
            continue
        seen.add(r["id"])

        # 优先收有 SKILL.md 的
        has_skill = repo_has_skill_file(r["full_name"])
        if has_skill or r.get("stargazers_count", 0) >= 1000:
            new_repos.append(r)
            print(f"  ✅ 新候选: {r['full_name']} ({r['stargazers_count']:,}⭐) {'[有SKILL.md]' if has_skill else ''}")
        else:
            print(f"  ⏭️  跳过: {r['full_name']} ({r['stargazers_count']}⭐ 太小且无SKILL.md)")

    print(f"\n🎯 发现 {len(new_repos)} 个新 Skill 项目")

    # 4. 转成我们的数据格式
    for r in new_repos:
        cat = guess_category(r)
        stars = r.get("stargazers_count", 0)
        desc = r.get("description", "") or "(无描述)"

        # 生成 id（owner_name 形式，转小写+去特殊字符）
        safe_name = r["name"].lower().replace("-", "_").replace(".", "_")
        safe_owner = r["owner"]["login"].lower()
        sid = f"{safe_owner}_{safe_name}"
        if sid in existing_ids:
            continue

        entry = {
            "id": sid,
            "category": cat,
            "name": r["name"],
            "owner": r["owner"]["login"],
            "repo": r["full_name"],
            "stars": stars,
            "emoji": guess_emoji(r),
            "shortDesc": desc[:80],
            "descEn": desc[:100],
            "features": [],
            "install": guess_install(r),
            "usage": f"安装后参考 {r['html_url']} 的 README",
            "compatible": [],
            "repoUrl": r["html_url"],
            "discoveredAt": datetime.now().strftime("%Y-%m-%d"),
        }
        existing["skills"].append(entry)
        existing_ids.add(sid)

    # 5. 按 Star 排序
    existing["skills"].sort(key=lambda x: x["stars"], reverse=True)

    # 6. 保存
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完成！现在总共 {len(existing['skills'])} 个 Skill")
    print(f"📝 发现日志: {len(new_repos)} 个新增")

    # 7. 写发现日志（可选）
    log_dir = os.path.join(here, "..", "discovery-logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d_%H%M')}.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(new_repos, f, ensure_ascii=False, indent=2)
    print(f"📄 发现日志: {log_path}")


if __name__ == "__main__":
    main()
