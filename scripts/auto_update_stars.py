#!/usr/bin/env python3
"""
auto_update_stars.py — 自动从 GitHub API 拉取项目最新 Star 数，更新 README.md

用法:
    python scripts/auto_update_stars.py              # 直接运行
    python scripts/auto_update_stars.py --token XXX  # 带 token (避免限流)

GitHub Actions 会每天自动跑一次，也支持手动触发。
"""

import os
import re
import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

# README 中所有需要更新 Star 数的项目
# 格式: (github_repo, 当前显示的 star 列中的锚点标识)
PROJECTS = [
    # ---- 1. Agent Skills 技能库 ----
    ("obra/superpowers", "superpowers"),
    ("JuliusBrussee/caveman", "caveman"),
    ("addyosmani/agent-skills", "addyosmani/agent-skills"),
    ("K-Dense-AI/scientific-agent-skills", "scientific-agent-skills"),
    ("anthropics/skills", "anthropics/skills"),
    ("vercel-labs/skills", "Vercel find-skills"),

    # ---- 2. Agent 框架 ----
    ("NousResearch/hermes-agent", "hermes-agent"),
    ("Significant-Gravitas/AutoGPT", "AutoGPT"),
    ("langgenius/dify", "dify"),
    ("langflow-ai/langflow", "langflow"),
    ("msitarzewski/agency-agents", "agency-agents"),
    ("langchain-ai/langchain", "langchain"),

    # ---- 3. 持久化记忆 ----
    ("thedotmack/claude-mem", "claude-mem"),
    ("MemPalace/mempalace", "MemPalace"),

    # ---- 4. 网络访问 ----
    ("firecrawl/firecrawl", "firecrawl"),
    ("browser-use/browser-use", "browser-use"),
    ("Panniantong/Agent-Reach", "Agent-Reach"),
    ("unclecode/crawl4ai", "crawl4ai"),

    # ---- 5. 代码开发 ----
    ("DietrichGebert/ponytail", "ponytail"),
    ("google-gemini/gemini-cli", "gemini-cli"),
    ("earendil-works/pi", "pi"),
    ("rtk-ai/rtk", "rtk"),

    # ---- 6. System Prompts ----
    ("x1xhlol/system-prompts-and-models-of-ai-tools", "system-prompts-and-models-of-ai-tools"),

    # ---- 7. Awesome Lists ----
    ("Shubhamsaboo/awesome-llm-apps", "awesome-llm-apps"),
    ("datawhalechina/Hello-Agents", "Hello-Agents"),

    # ---- 8. 垂直领域 ----
    ("n8n-io/n8n", "n8n"),
    ("infiniflow/ragflow", "ragflow"),
    ("career-ops-hq/career-ops", "career-ops"),
    ("karpathy/autoresearch", "autoresearch"),
]


def fmt_stars(n: int) -> str:
    """把 star 数格式化成 README 里用的字符串"""
    if n >= 1_000:
        return f"{n / 1_000:.0f}K" if n % 1_000 == 0 else f"{n / 1_000:.1f}K".rstrip("0").rstrip(".")
    return str(n)


def fetch_stars(repo: str, token: str | None) -> int | None:
    """从 GitHub API 拉取 star 数"""
    url = f"https://api.github.com/repos/{repo}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "awesome-ai-skills-updater",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                return data.get("stargazers_count")
        except urllib.error.HTTPError as e:
            if e.code == 403 and "rate limit" in str(e).lower():
                print(f"  ⚠️ 限流了，等 10s 再试 ({repo})")
                time.sleep(10)
                continue
            if e.code == 404:
                print(f"  ⚠️ 仓库不存在或重命名: {repo}")
                return None
            print(f"  ❌ HTTP {e.code} for {repo}")
            return None
        except Exception as e:
            print(f"  ❌ 请求失败 {repo}: {e}")
            time.sleep(5)
    return None


def update_readme(readme_path: str, updates: dict[str, int]) -> int:
    """更新 README 里的 star 数，返回修改行数"""
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    changed = 0
    for repo, stars in updates.items():
        if stars is None:
            continue
        new_val = fmt_stars(stars)
        # 在 README 表格里匹配: | 序号 | [项目名](链接) | 旧Stars |
        # 旧 Stars 列的值格式可能是 291K、13K、— 等
        pattern = rf"(https://github\.com/{re.escape(repo)}\) \|)\s*[\w\-Kk万\.+]*\s*\|"
        new_pattern = rf"\1 {new_val} |"
        new_content, count = re.subn(pattern, new_pattern, content)
        if count > 0:
            content = new_content
            changed += count
            print(f"  ✅ {repo}: → {stars} stars ({new_val})")
        else:
            print(f"  ⚠️ 未在 README 里找到匹配: {repo}")

    # 更新日期标记
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    content = re.sub(
        r"\(数据更新于[^)]+\)",
        f"(数据更新于 {today})",
        content,
    )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    return changed


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if len(sys.argv) > 1:
        # 支持 --token XXX 命令行参数
        for i, arg in enumerate(sys.argv):
            if arg == "--token" and i + 1 < len(sys.argv):
                token = sys.argv[i + 1]

    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    readme_path = os.path.abspath(readme_path)

    print(f"🚀 开始更新 Star 数 (token: {'有' if token else '无'})")
    print(f"📄 README 路径: {readme_path}")
    print(f"📦 共 {len(PROJECTS)} 个项目待更新\n")

    updates = {}
    for i, (repo, label) in enumerate(PROJECTS, 1):
        print(f"[{i}/{len(PROJECTS)}] {repo} ...", end=" ")
        stars = fetch_stars(repo, token)
        if stars is not None:
            updates[repo] = stars
        time.sleep(0.3)  # 避免限流

    print(f"\n💾 写入 README ...")
    changed = update_readme(readme_path, updates)
    print(f"\n🎉 完成！修改了 {changed} 处 Star 数。")


if __name__ == "__main__":
    main()
