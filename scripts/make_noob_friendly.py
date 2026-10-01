#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 61 个 Skill 全部改成大白话 + 加 useCase 场景"""
import json

# 大白话描述映射表（按 id 匹配）
VERBOSE = {
    "superpowers": ("让 AI 先写计划等你确认再动手，不瞎写代码", "AI 写代码写一半方向错了？强制它先给大纲再干活"),
    "caveman": ("让 AI 用最少的字说清楚事，省 65% API 钱", "嫌 AI 太啰嗦、想快速看重点、API 又贵的时候用"),
    "agent-skills": ("Google Addy Osmani 出品，AI 写代码的 20 个专业套路", "想让 AI 写出更专业、更规范的代码时用"),
    "system-prompts": ("扒了 Cursor/Claude Code/Copilot/Kiro 的内部提示词", "想知道各款 AI 工具背后怎么调教 AI 的，来围观"),
    "mattpocock-skills": ("Vercel 大神做的想法审查器，像面试官一样怼你的创意", "想做新项目、写论文开题、怕想法太天真，让它帮你泼冷水"),
    "last30days-skill": ("自动上 Reddit/B站/YouTube/HackerNews 搜最近 30 天热点", "写论文找热点、想知道 AI 圈最近有啥新瓜、选题材没灵感"),
    "antigravity-skills": ("500+ 个 AI Skill 大合集，开发/安全/DevOps 全都有", "想挖更多好用的 Skill、逛技能超市找合适的工具"),
    "academic-skills": ("13 个 AI 组成研究团队 + 12 个 AI 写论文 + 同行评审", "写论文、做科研、需要 AI 帮你查文献和起草"),
    "humanizer": ("AI 写的东西一看就像机器？帮你改成真人语气，去 AI 味", "AI 写了作文、论文、朋友圈文案，要洗稿变自然"),
    "marketingskills": ("AI 营销全家桶，写文案、想标题、做 SEO、搞增长", "写小红书标题、朋友圈文案、电商详情页，相当于有个营销经理"),
    "scientific-agent-skills": ("AI 科学家技能包，数据分析、科研流程自动化", "理工科做实验、跑数据、想让 AI 帮你干科研活"),

    "openclaw-fw": ("现象级开源 AI 助手，本地跑 + 接 WhatsApp/Telegram 全天候干活", "想有个 7x24 小时帮你查邮件、管日程、刷网页的私人助理"),
    "hermes-agent": ("AI 助手会学习，每次干活都积累经验，越用越聪明", "想让 AI 记住你之前让它做过啥、下次自动优化"),
    "agency-agents": ("一个 AI 公司，前端、文案、运营、代码全是不同角色", "一个人干不过来？让 5 个 AI 角色分工帮你干"),
    "dify": ("搭 AI 应用的乐高，拖拖拽拽做聊天机器人和 Agent 流程", "不会写代码也想搭个 AI 聊天机器人，用 Dify 拖就行"),
    "langflow": ("LangChain 的可视化版本，画流程图拼 AI Agent", "喜欢可视化编程、想拖拽搭建 AI Agent 工作流"),
    "pi-fw": ("轻量 AI Agent 工具箱，统一 API + 漂亮终端界面", "想要一个好用的终端 AI 助手、不想折腾太多依赖"),
    "AutoGPT": ("大名鼎鼎的自主 AI，给个目标它自己拆步骤去实现", "你说帮我做个网站，它自己查资料、写代码、搭起来"),
    "orca": ("让多个 AI Agent 同时写代码，比谁写得好就用谁", "一个 AI 可能搞错，让 3 个 AI 并行干，选最好的结果"),
    "paseo": ("手机 + 电脑统一管 AI Agent，iOS/Android/桌面/Web 全覆盖", "想在手机上用语音指挥 AI、跨设备接着干"),
    "GenericAgent": ("AI 自己长技能，从种子代码长出完整的系统 Agent", "想看 AI 怎么自我进化、研究级玩法"),
    "autogen": ("微软出品，多个 AI 对话协作框架", "想让多个 AI 像开会一样讨论、互相配合完成复杂任务"),

    "claude-mem": ("让 AI 跨会话记住你，上次聊的事下次接着来", "AI 每次都失忆重新聊？装上它帮 AI 记住你的历史对话"),
    "MemPalace": ("AI 长期记忆宫殿，存到向量数据库，永远不丢", "想让 AI 长期记住你的偏好、项目背景、做过的事"),
    "mem0": ("给任何 LLM 加持久化记忆的通用层", "自己在搭 AI 应用、想给你的 LLM 加记忆功能"),

    "firecrawl": ("给 AI 一个万能上网钥匙，搜全网、爬网页、抓数据", "AI 只能回答训练过的东西？装上它就能实时搜全网"),
    "browser-use": ("让 AI 真的像人一样操作浏览器，点按钮、填表单、截图", "让 AI 帮你自动填表单、刷网页、截图留证"),
    "Agent-Reach": ("让 AI 能看 Twitter/YouTube/小红书/B站，零 API 费", "想让 AI 帮你刷社交媒体、汇总热点、看视频"),
    "crawl4ai": ("专为 AI Agent 设计的爬虫，抓完直接给 AI 用", "给 AI 喂网页数据、做 RAG、建知识库"),
    "playwright-skill": ("让 AI 自动打开浏览器，测试你的网站看 UI 对不对", "写完网站想自动测一下、让 AI 帮你截图看效果"),

    "ponytail": ("让 AI 像最懒老油条程序员，能不写就不写", "嫌 AI 写代码写太多、想用最少的代码解决问题"),
    "gemini-cli": ("Google 出品的终端 AI 助手，在命令行里用 Gemini", "喜欢在终端里干活、想用 Gemini 模型写代码"),
    "pi": ("轻量 AI Agent 工具箱，统一 LLM API + Agent Loop + TUI", "想有个好用的终端 AI、不想折腾太多依赖"),
    "rtk": ("让 AI 自动写测试、跑测试、看结果", "写完代码懒得写测试、让 AI 帮你测"),
    "plannotator": ("AI 写的计划和代码，用浏览器可视化批注，反馈自动回传", "AI 写完代码你想先审一下、加批注、然后让它改"),
    "oh-my-pi": ("Pi Agent 增强版，自动重命名、自动调试、LSP 集成", "想要更聪明的 AI 编辑器、重命名自动更所有引用"),
    "cua": ("给 AI Agent 一个专用电脑，自动化操作应用、上网、办公", "想让 AI 在隔离环境里帮你跑用电脑的任务"),
    "anthropics-frontend": ("Anthropic 官方出品，让 AI 写专业级前端 UI 组件", "想让 AI 写 React/Tailwind 页面、要生产级质量"),

    "garak": ("NVIDIA 出的 AI 杀毒软件，自动跑 100 种攻击看你的 AI 安不安全", "自己做了 AI 产品想测漏洞、想学 AI 安全研究"),
    "promptfoo": ("被 OpenAI 收购的 AI 测试工具，Prompt 对不对、红队能不能攻破", "上线 AI 产品前先测一遍、集成到 CI/CD 自动化测试"),
    "PurpleLlama": ("Meta 出品，AI 安全评估框架 + 运行时防护墙", "想给 AI 产品加一层安全防护、防 Prompt Injection"),
    "PyRIT": ("微软出品，AI 红队工具箱，多轮越狱 + 多模态攻击", "想研究 AI 越狱攻击、学安全攻防技术"),
    "Giskard": ("AI 质量保证自动红队，自动生成攻击探针找漏洞", "想自动化测试 AI 安全、一键扫描"),
    "snyk-agent-scan": ("Snyk 出品，扫 AI Agent/MCP/Skill 有没有恶意代码", "装了新 Skill 想先扫一下安不安全"),
    "cisco-skill-scanner": ("Cisco AI Defense，扫 Agent Skill 的风险模式和隐藏威胁", "批量审查 Skill 库、担心装了恶意 Skill"),
    "llm-guard": ("给 AI 加安全护栏，输入输出双向过滤", "自己做的 AI 产品想防 Prompt Injection"),
    "seclab-taskflow": ("GitHub 安全实验室出品，AI 安全自动化发现漏洞", "想让 AI 自动帮你审代码、找漏洞"),
    "slowmist-agent-sec": ("慢雾科技出品，AI Agent 安全审查框架", "自己搭了 Agent 想请安全专家审一下"),

    "n8n": ("280+ 自动化模板，Gmail/Slack/Notion/Telegram 一键搭工作流", "想自动发邮件、自动同步数据、不想写代码搭自动化"),
    "ragflow": ("开源 RAG 引擎，把你的文档喂给 AI，让它基于你的知识回答", "想搭一个只懂你公司知识的 AI 助手"),
    "career-ops": ("AI 职业教练，简历改写、面试模拟、职业规划", "写简历、准备面试、想换方向"),
    "autoresearch": ("AI 自动做科研，给个方向自动跑实验看结果", "想让 AI 帮你跑科研实验、看 AI 论文自动汇总"),
    "huginn": ("让 AI 创建/监控/执行数据代理，经典自动化平台", "想让 AI 定时自动干活、监控数据、执行任务"),
    "dashi-ppt": ("把文字丢给 AI，直接出可编辑 PPT，网页版 + 一键导出 PPTX", "老师让做汇报、要交 PPT、懒得一页页写"),
    "book-to-skill": ("把技术书/文档自动转成 AI Skill，章节拆分 + SKILL.md 生成", "想让 AI 基于某本书/文档回答问题"),

    "awesome-llm-apps": ("100+ AI Agent 和 RAG 应用合集，Python + 开源", "想找现成的 AI 项目抄、学习别人怎么搭的"),
    "Hello-Agents": ("Agent 教程合集，从入门到高级", "想学 AI Agent、找系统的教程"),
    "ai-agent-book": ("李博杰著开源书，《深入理解 AI Agent》设计原理与工程实践", "想系统学 AI Agent 原理、有配套代码可以跑"),
}

# 分类描述也改一下
CAT_DESC = {
    "skills": "🧠 纯技能包：装上就让 AI 多一种本事",
    "framework": "🔧 搭 Agent 用的平台：从零开始做 AI 助手",
    "memory": "💾 记忆增强：让 AI 跨会话记住东西不失忆",
    "web": "🌐 联网能力：让 AI 能上网搜数据、操作网站",
    "code": "🎨 编程辅助：让写代码的 AI 更专业、更聪明",
    "prompts": "🔍 System Prompts：扒 AI 工具背后的内幕",
    "learn": "📚 学习资源：想系统学 AI Agent 可以看这些",
    "vertical": "⚙️ 垂直场景：特定任务用的（PPT/营销/安全等）",
}

# 读现有数据
with open("docs/data/skills.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 更新分类描述
for cat in data["categories"]:
    if cat["id"] in CAT_DESC:
        cat["desc"] = CAT_DESC[cat["id"]]

# 更新每个 skill
updated = 0
for s in data["skills"]:
    vid = s["id"]
    if vid in VERBOSE:
        s["shortDesc"] = VERBOSE[vid][0]
        s["useCase"] = VERBOSE[vid][1]
        updated += 1
    elif "useCase" not in s:
        prefix = s["shortDesc"][:15] if len(s["shortDesc"]) > 15 else s["shortDesc"]
        s["useCase"] = "想让 AI 在「" + prefix + "」方面变强的时候用"

data["skills"].sort(key=lambda x: x["stars"], reverse=True)

with open("docs/data/skills.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK:", updated, "/", len(data["skills"]), "个 Skill 已更新为大白话")
print()
for s in data["skills"][:5]:
    print(">>", s["name"])
    print("   说人话:", s["shortDesc"])
    print("   什么时候用:", s.get("useCase", ""))
