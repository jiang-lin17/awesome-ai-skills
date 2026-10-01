#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AI 自动生成大白话描述（用 Pollinations.ai 免费 LLM）
=====================================================

- 完全免费，无需 API Key
- 每次请求间隔 15 秒（Pollinations 匿名限流）
- 找没有 useCase 的 Skill → 生成大白话 + 什么时候用 → 写回 skills.json
- GitHub Actions 每周跑完 auto_discover 后自动调用
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime

POLLINATIONS_URL = "https://text.pollinations.ai/openai"
MODEL = "deepseek"  # DeepSeek V3.1，中文好

# ========== 关键参数 ==========
BATCH_SIZE = 20        # 每次最多处理几个（防止 Actions 跑太久超时）
REQUEST_INTERVAL = 5   # 每次请求间隔秒数（Pollinations 匿名限流 ~1/15s，5s 够了）

# ========== Prompt 模板 ==========
SYSTEM_PROMPT = """\
你是一个给小白讲清楚 AI 工具的技术科普作者。
- 用大白话，不要用"Agentic""Pipeline""Orchestration"这种术语
- shortDesc：20字以内，直接说这是什么
- useCase：一句话，说清楚什么时候想用它
- 只输出 JSON，不要 markdown，不要解释
"""

USER_PROMPT = """\
帮我给这个 GitHub 项目写大白话介绍：

项目名：{name}
英文描述：{desc}
分类：{cat}
Star 数：{stars}

返回 JSON：
{{"shortDesc": "20字以内大白话", "useCase": "什么时候用"}}
"""


def call_pollinations(name, desc, cat, stars):
    """调 Pollinations.ai 免费 LLM，返回 (shortDesc, useCase) 或 None
    不重试，失败就失败，快速跳过"""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT.format(
                name=name, desc=desc[:200], cat=cat, stars=stars
            )},
        ],
        "temperature": 0.4,
        "stream": False,
    }

    # 单次尝试，失败直接跳过
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            POLLINATIONS_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "awesome-ai-skills-generator",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = result["choices"][0]["message"]["content"].strip()

        # 解析 JSON（AI 可能包 ```json ... ```）
        text = re.sub(r"^```(json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        parsed = json.loads(text)

        short = str(parsed.get("shortDesc", "")).strip()
        uc = str(parsed.get("useCase", "")).strip()
        if short and uc:
            return short, uc
        print(f"  ⚠️ 返回不完整: {text[:100]}")
        return None

    except urllib.error.HTTPError as e:
        print(f"  ⚠️ HTTP {e.code}，生成失败")
        return None
    except json.JSONDecodeError:
        print(f"  ⚠️ JSON 解析失败，生成失败")
        return None
    except Exception as e:
        print(f"  ⚠️ {e}，生成失败")
        return None


def main():
    print("=" * 60)
    print("🤖 AI 大白话生成器（Pollinations.ai 免费版）")
    print("=" * 60)

    here = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(here, "..", "docs", "data", "skills.json"))

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 找没有 useCase 的（就是自动发现新增的），取前 BATCH_SIZE 个
    need_gen_all = [s for s in data["skills"] if not s.get("useCase") or len(s.get("useCase", "")) < 5]
    need_gen = need_gen_all[:BATCH_SIZE]
    skipped = len(need_gen_all) - len(need_gen)
    print(f"\n📚 总 Skill: {len(data['skills'])}")
    print(f"🎯 本次生成: {len(need_gen)} 个（共 {len(need_gen_all)} 个待生成，分批次）")
    if skipped:
        print(f"⏭️  本次跳过: {skipped} 个（下次再处理）")

    if not need_gen:
        print("\n✅ 全部都有大白话了！无事可做。")
        return

    # 每 15 秒一个（Pollinations 匿名限流 ~1/15s）
    total = len(need_gen)
    success = 0
    failed = []

    for i, s in enumerate(need_gen, 1):
        print(f"\n[{i}/{total}] 🎨 {s['name']} ({s.get('stars',0):,}⭐) [{s.get('category','?')}]")
        print(f"  英文: {s.get('descEn', s.get('shortDesc',''))[:80]}")

        result = call_pollinations(
            name=s["name"],
            desc=s.get("descEn") or s.get("shortDesc") or "",
            cat=s.get("category", "vertical"),
            stars=s.get("stars", 0),
        )

        if result:
            short, uc = result
            s["shortDesc"] = short
            s["useCase"] = uc
            success += 1
            print(f"  ✅ 大白话: {short}")
            print(f"  💡 什么时候用: {uc}")
        else:
            failed.append(s["id"])
            print(f"  ❌ 生成失败，保留原文")

        # 限流间隔
        if i < total:
            time.sleep(REQUEST_INTERVAL)

    # 保存
    data["skills"].sort(key=lambda x: x.get("stars", 0), reverse=True)
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ 成功: {success}/{total}  失败: {len(failed)}")
    print(f"📝 已保存到 skills.json")
    if failed:
        print(f"⚠️  失败列表: {', '.join(failed[:10])}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
