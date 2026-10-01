#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Awesome AI Skills — 自动发现（限流优化版）
==============================================

核心优化：
  1. 只读 Search API（30次/分钟），删掉每个 repo 多调 3-4 次的 repo_has_skill_file
  2. 读 Retry-After / X-RateLimit-Reset 头精确等待，不瞎 sleep
  3. 精准关键词 + 高 stars 门槛，减少无效调用
  4. per_page=30 一次拿满，比分 3 页更高效
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# ============== 精准关键词（6 个，覆盖全品类）==============
# 用 stars: 前置过滤，直接排除垃圾
SEARCH_QUERIES = [
    # 核心 Skill / Agent
    "stars:>500 skill agent language:python",
    "stars:>500 agentic skill claude cursor",
    "stars:>1000 AI agent framework language:python",
    # 安全 / 红队
    "stars:>500 LLM jailbreak red team",
    # MCP / 工具链
    "stars:>500 MCP server AI tool",
    # 学习 / Awesome
    "stars:>500 awesome AI agent",
]

# ============== 分类推断（只用 repo desc + name，0 额外 API）==============
CATEGORY_RULES = [
    ("prompts", ["jailbreak", "red team", "prompt injection", "security", "pentest", "attack"]),
    ("framework", ["agent framework", "agentic framework", "autonomous agent", "multi-agent", "llm agent", "agent loop"]),
    ("skills", ["agent skill", "agentic skill", "coding agent skill", "skill pack", "skills bundle"]),
    ("memory", ["persistent memory", "long-term memory", "vector memory", "llm memory"]),
    ("web", ["web scraping", "crawl", "firecrawl", "playwright", "browser automation"]),
    ("code", ["code generation", "code review", "IDE plugin", "developer tool", "coding assistant"]),
    ("vertical", ["marketing", "ppt", "career", "finance", "research agent"]),
    ("learn", ["awesome", "tutorial", "course", "learn ai", "agent course"]),
]

CATEGORY_EMOJI = {
    "framework": "🧠", "skills": "⚡", "memory": "💾",
    "web": "🌐", "code": "💻", "prompts": "🔍",
    "learn": "📚", "vertical": "🎯",
}


# ============== 限流感知的 API 调用 ==============
def gh_search(query, token=None):
    """
    调 GitHub Search API（30次/分钟 限流）
    - 读 X-RateLimit-Remaining 头，剩 <3 就 sleep 到 Reset
    - 403 限流时读 Retry-After 头精确等待
    - 每页 30 条，只拿第 1 页（够用了）
    """
    q = urllib.parse.quote(query)
    url = f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=30&page=1"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "awesome-ai-skills-v2",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for attempt in range(5):  # 最多重试 5 次
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                remaining = int(resp.headers.get("X-RateLimit-Remaining", "999"))
                reset_ts = int(resp.headers.get("X-RateLimit-Reset", "0"))
                if remaining < 3:
                    wait = max(1, reset_ts - int(time.time()) + 1)
                    print(f"  🕐 Search API 剩 {remaining} 次，等 {wait}s 到限流恢复...")
                    time.sleep(wait)
                return json.loads(resp.read().decode("utf-8"))

        except urllib.error.HTTPError as e:
            if e.code == 403:
                retry_after = int(e.headers.get("Retry-After", "30"))
                print(f"  ⚠️ 403 限流！Retry-After={retry_after}s，等完再试（第 {attempt+1} 次重试）")
                time.sleep(retry_after + 1)
                continue
            if e.code == 422:
                print(f"  ⏭️  422 搜不到: {query}"); return None
            print(f"  ❌ HTTP {e.code}: {query}"); return None
        except Exception as ex:
            print(f"  ❌ {ex}"); time.sleep(3); continue
    return None


# ============== 快速推断（0 额外 API）==============
def guess_category(repo):
    text = f"{repo.get('description','')} {repo.get('name','')}".lower()
    for cat, kws in CATEGORY_RULES:
        if any(kw in text for kw in kws):
            return cat
    return "vertical"

def guess_install(repo):
    lang = (repo.get("language") or "").lower()
    name = repo.get("name", "")
    owner = repo.get("full_name", "")
    desc = repo.get("description", "").lower()
    if lang == "python":
        return f"pip install {name}"
    if lang in ("typescript", "javascript") and "skill" in desc:
        return f"npx skills add {owner}"
    if lang in ("typescript", "javascript"):
        return f"npm install -g {name}"
    return f"git clone https://github.com/{owner}.git"

def guess_emoji(cat):
    return CATEGORY_EMOJI.get(cat, "✨")


# ============== 主流程 ==============
def main():
    print("=" * 60)
    print("🤖 Awesome AI Skills — 自动发现 v2（限流优化版）")
    print("=" * 60)

    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        print("✅ 已有 GITHUB_TOKEN")
    else:
        print("⚠️  未设置 GITHUB_TOKEN，限流 30次/分钟（Search API）")

    # 1. 读现有
    here = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(here, "..", "docs", "data", "skills.json"))

    with open(data_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_ids = {s["id"] for s in existing["skills"]}
    existing_repos = {s["repo"] for s in existing["skills"]}
    print(f"\n📚 现有 {len(existing['skills'])} 个 Skill")

    # 2. 搜（仅 Search API，6 关键词 × 1 页 = 6 次调用）
    print(f"\n🔍 开始搜 GitHub（{len(SEARCH_QUERIES)} 个精准关键词）...")
    all_candidates = []

    for i, q in enumerate(SEARCH_QUERIES, 1):
        print(f"  [{i}/{len(SEARCH_QUERIES)}] 🔎 {q}")
        data = gh_search(q, token=token)
        if data and "items" in data:
            for r in data["items"]:
                if r["full_name"] in existing_repos:
                    continue
                if r.get("archived"):
                    continue
                if r.get("stargazers_count", 0) < 50:
                    continue
                all_candidates.append(r)
        # Search API 30次/分钟，每次间隔 2.1s 刚好不触发限流
        if i < len(SEARCH_QUERIES):
            time.sleep(2.1)

    # 3. 去重 + 排序
    seen_ids = set()
    new_repos = []
    for r in sorted(all_candidates, key=lambda x: -x.get("stargazers_count", 0)):
        if r["id"] in seen_ids:
            continue
        seen_ids.add(r["id"])
        new_repos.append(r)

    print(f"\n🎯 去重后 {len(new_repos)} 个候选新 Skill")

    # 4. 入库（0 额外 API！）
    added = 0
    for r in new_repos:
        cat = guess_category(r)
        stars = r.get("stargazers_count", 0)
        desc = r.get("description", "") or "(无描述)"
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
            "emoji": guess_emoji(cat),
            "shortDesc": desc[:80],
            "descEn": desc[:120],
            "features": [],
            "install": guess_install(r),
            "usage": f"安装后参考 {r['html_url']} 的 README",
            "compatible": [],
            "repoUrl": r["html_url"],
            "discoveredAt": datetime.now().strftime("%Y-%m-%d"),
        }
        existing["skills"].append(entry)
        existing_ids.add(sid)
        added += 1
        print(f"  ✅ [{cat[:8]}] {r['full_name']} ({stars:,}⭐) — {desc[:50]}")

    # 5. 排序 + 保存
    existing["skills"].sort(key=lambda x: x["stars"], reverse=True)

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ 新增 {added} 个 Skill！总计 {len(existing['skills'])} 个")
    print(f"{'='*60}")

    # 6. 发现日志
    if new_repos:
        log_dir = os.path.abspath(os.path.join(here, "..", "discovery-logs"))
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d_%H%M')}.json")
        summary = [{"repo": r["full_name"], "stars": r["stargazers_count"],
                    "desc": r.get("description","")[:100],
                    "html_url": r["html_url"]} for r in new_repos]
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"📄 发现日志: {log_path}")


if __name__ == "__main__":
    main()
