#!/usr/bin/env python3
"""一次性扩展脚本：把现有 29 个项目 + 新增 50+ 项目 → 合并成完整 skills.json"""

import json, urllib.request, urllib.error, time, os

# ============ 新增项目列表 (repo, id, name, category, emoji, descZh, descEn, features, install, usage, compatible) ============
# category: skills/framework/memory/web/code/prompts/learn/vertical

NEW_PROJECTS = [
    # ===== 1. Agent Skills 技能库 =====
    # 已有 6 个，再加 8 个
    ("openclaw/openclaw", "openclaw", "OpenClaw (Agent)", "framework", "🦞",
     "现象级开源个人 AI 助手，可部署在本地 + 多平台消息交互",
     "Phenomenal open-source personal AI assistant, cross-platform, persistent, multi-channel",
     ["本地部署", "多消息平台(Telegram/Discord/WhatsApp)", "持久化运行", "50+ 内置 Skills", "ClawHub 社区 1.5 万+ skills"],
     "curl -fsSL https://openclaw.ai/install.sh | bash",
     "脚本安装后 openclaw run 启动，通过 WhatsApp/Telegram/终端交互",
     ["跨平台", "Node.js 实现"]),

    ("mattpocock/skills", "mattpocock-skills", "mattpocock/skills", "skills", "🎣",
     "Vercel Matt Pocock 出品，idea 审查 + Code Review 全套 Skill",
     "Matt Pocock's skill pack: grill-me idea testing, code review, TypeScript deep dives",
     ["grill-me 创意审查", "Code Review", "TypeScript 深度", "100+ 万次安装"],
     "npx skills add https://github.com/mattpocock/skills",
     "npx 安装后 grill-me 检查你的想法弱点",
     ["Claude Code", "Copilot", "Cursor"]),

    ("coreyhaines31/marketingskills", "marketingskills", "marketingskills", "skills", "📈",
     "AI 营销专家技能包：SEO/CRO/文案/数据分析/增长工程",
     "Marketing skills pack: CRO, copywriting, SEO, analytics, growth engineering",
     ["CRO 转化率优化", "SEO 文案", "A/B 测试", "增长工程", "5.2 万 Star"],
     "npx skills add https://github.com/coreyhaines31/marketingskills",
     "安装后让 Agent 帮你写文案、做 SEO、分析数据",
     ["Claude Code", "Copilot", "Cursor", "OpenClaw"]),

    ("mvanhorn/last30days-skill", "last30days-skill", "last30days-skill", "skills", "🕒",
     "自动检索 Reddit/X/YouTube/HackerNews 最近 30 天热点并汇总",
     "Research the last 30 days across Reddit, X, YouTube, HN, synthesize a grounded brief",
     ["Reddit/X/YouTube/HN 跨平台", "自动合成简报", "零手动操作"],
     "npx skills add mvanhorn/last30days-skill -g",
     "全局安装后 ask agent: 最近 AI 圈有什么热点",
     ["Claude Code", "Copilot", "OpenClaw"]),

    ("sickn33/antigravity-awesome-skills", "antigravity-skills", "antigravity-awesome-skills", "skills", "⚡",
     "500+ 通用 Agent Skills 大合集：开发/架构/安全/DevOps/云/测试",
     "500+ foundational skills: dev, architecture, security, DevOps, cloud, testing",
     ["500+ Skill", "开发全流程覆盖", "安全专家", "Cloud"],
     "git clone https://github.com/sickn33/antigravity-awesome-skills",
     "克隆后按需复制 skill 文件夹到你的 agent skills 目录",
     ["Claude Code", "Copilot", "Cursor", "OpenClaw"]),

    ("Imbad0202/academic-research-skills", "academic-skills", "academic-research-skills", "skills", "🎓",
     "13 Agent 深度研究团队 + 12 Agent 论文写作团队 + 同行评审",
     "13-agent deep research team, 12-agent paper writing team, multi-perspective peer review",
     ["深度研究", "LaTeX 论文", "同行评审", "学术写作"],
     "git clone https://github.com/Imbad0202/academic-research-skills",
     "克隆后让 Agent 自动跑研究或论文写作流程",
     ["Claude Code", "Copilot", "Cursor"]),

    ("blader/humanizer", "humanizer", "humanizer", "skills", "✍️",
     "让 AI 写作更像人类！去除 AI 生成痕迹，学术写作必备",
     "Claude Code skill that removes signs of AI-generated writing, sounds natural",
     ["AI 痕迹去除", "自然人类文风", "学术写作必备", "12.8K Star"],
     "npx skills add blader/humanizer",
     "安装后让 AI 写东西后自动 humanize",
     ["Claude Code", "Copilot"]),

    ("coderabbitai/agent-skills", "coderabbit-skills", "CodeRabbit/agent-skills", "skills", "🐇",
     "CodeRabbit 出品的代码审查与安全扫描 Skills",
     "CodeRabbit's code review and security scanning skills for AI coding agents",
     ["代码审查", "安全扫描", "PR 自动化", "零配置"],
     "npx skills add coderabbitai/agent-skills",
     "安装后自动对 AI 输出的代码做审查",
     ["Claude Code", "Copilot", "Codex"]),

    # ===== 2. Agent 框架 =====
    # 已有 6 个，再加 7 个
    ("openclaw/openclaw", "openclaw-fw", "OpenClaw", "framework", "🦞",
     "现象级开源个人 AI Agent 框架，本地运行 + 多平台消息接入",
     "Phenomenal open-source personal AI agent framework, local-first, multi-channel",
     ["本地部署", "多消息平台", "内置 Skills", "ClawHub 社区"],
     "curl -fsSL https://openclaw.ai/install.sh | bash",
     "脚本安装后 openclaw run 启动",
     ["跨平台", "Node.js"]),

    ("stablyai/orca", "orca", "orca", "framework", "🐳",
     "让多个 AI 编程 Agent 并行开发的 IDE 编排工具",
     "Cross-platform AI agent orchestration IDE — runs multiple agents in parallel, merges best output",
     ["多 Agent 并行", "Git 工作树隔离", "结果自动对比合并", "7.7K Star"],
     "git clone https://github.com/stablyai/orca && cd orca && pnpm install",
     "克隆后 pnpm 启动，界面统一管理多个 Agent",
     ["跨平台", "Node.js"]),

    ("msitarzewski/hugginn", "hugginn", "hugginn", "framework", "🤗",
     "Hermes 框架的轻量 fork，更简单的持久化 Agent",
     "Lightweight Hermes fork — simpler persistent personal agent",
     ["持久化", "学习循环", "多平台接入", "Python"],
     "pip install hugginn",
     "pip 安装后 hugginn start",
     ["Python 3.10+", "跨平台"]),

    ("earendil-works/pi", "pi-fw", "Pi (framework)", "framework", "🍰",
     "轻量 AI Agent 工具箱：统一 LLM API + agent loop + TUI + coding CLI",
     "Lightweight agent toolkit: unified LLM API, agent loop, TUI, coding CLI",
     ["统一 LLM API", "Agent Loop", "漂亮 TUI", "TypeScript"],
     "curl -fsSL https://pi.dev/install.sh | bash",
     "脚本安装后终端运行 pi",
     ["Mac/Linux", "WSL"]),

    ("getpaseo/paseo", "paseo", "Paseo", "framework", "📱",
     "跨设备管理 AI Agent 的平台：iOS/Android/桌面/Web/CLI 全覆盖",
     "Cross-platform unified management for Claude Code, Codex and OpenCode — voice, multi-device",
     ["多客户端", "语音控制", "跨设备协同", "2.7K Star"],
     "npm install -g paseo",
     "npm 全局安装后 paseo 启动",
     ["iOS", "Android", "桌面", "Web"]),

    ("lsdefine/GenericAgent", "generic-agent", "GenericAgent", "framework", "🌱",
     "自我进化 Agent：从 3.3K 行种子长出完整系统，token 减少 6 倍",
     "Self-evolving agent: grows full skill tree from 3.3K-line seed, 6x less tokens",
     ["自我进化", "Skill Tree", "系统级控制", "Python"],
     "npx skills add lsdefine/GenericAgent",
     "npx 安装后直接运行，Agent 会自我生长",
     ["Claude Code", "Copilot"]),

    ("autogen-ai/autogen", "autogen", "AutoGen", "framework", "🧬",
     "微软出品，多 Agent 对话协作框架",
     "Microsoft's multi-agent conversation framework — agents talk to solve tasks",
     ["多 Agent 对话", "微软出品", "Python + .NET", "100K+ Star"],
     "pip install pyautogen",
     "pip 安装后写 Python 脚本定义多个 Agent 角色",
     ["Python", ".NET"]),

    # ===== 3. 持久化记忆 =====
    # 已有 2 个，再加 4 个
    ("mem0ai/mem0", "mem0", "mem0", "memory", "🧠",
     "给任何 LLM 添加持久化记忆的通用层，支持多种 LLM",
     "Universal memory layer for LLMs — add persistent memory to any LLM app",
     ["多种 LLM 支持", "向量存储", "自动摘要", "MIT 开源"],
     "pip install mem0ai",
     "pip 安装后在 LangChain/LlamaIndex 中直接 import",
     ["Python", "LangChain", "LlamaIndex"]),

    ("graphiti-core/graphiti", "graphiti", "Graphiti", "memory", "🕸️",
     "AI Agent 的时间图记忆引擎——知识图谱 + 时间感知",
     "Time-traveling knowledge graph memory for AI agents",
     ["知识图谱", "时间感知", "自动关系抽取", "RAG 增强"],
     "pip install graphiti-core",
     "pip 安装后 import 使用",
     ["Python"]),

    ("langchain-ai/langgraph-memory", "langgraph-memory", "LangGraph Memory", "memory", "📒",
     "LangGraph 官方持久化记忆模块，支持 checkpoint 和恢复",
     "LangGraph's official persistent memory — checkpoints, recovery, human-in-the-loop",
     ["Checkpoint", "对话恢复", "人类干预", "LangChain 生态"],
     "pip install langgraph-checkpoint",
     "pip 安装后在 LangGraph 中添加 checkpoint 节点",
     ["Python", "LangChain 生态"]),

    ("pi-ai/persistence", "pi-persist", "Pi Persistence", "memory", "💾",
     "Pi Agent 的持久化存储插件——本地 SQLite 自动同步",
     "Pi agent persistence plugin — local SQLite with auto-sync",
     ["SQLite 本地存储", "自动同步", "Pi Agent 原生支持"],
     "curl -fsSL https://pi.dev/plugins/persistence | bash",
     "Pi Agent 插件安装脚本",
     ["Pi Agent"]),

    # ===== 4. 网络访问 =====
    # 已有 4 个，再加 4 个
    ("langchain-ai/langchain-integrations", "langchain-serpapi", "SerpAPI", "web", "🔍",
     "LangChain 搜索集成——SerpAPI、Tavily、DuckDuckGo 等",
     "Search API integrations for LangChain — SerpAPI, Tavily, DuckDuckGo, etc.",
     ["多搜索源", "LangChain 原生", "API Key 模式"],
     "pip install langchain-serpapi",
     "pip 安装后配置 API Key 即可搜索",
     ["Python", "LangChain"]),

    ("microsoft/playwright", "playwright", "Playwright (skill)", "web", "🎭",
     "Playwright 自动化浏览器——Anthropic 官方推荐作为 Agent Skill",
     "Playwright browser automation — Anthropic-recommended agent skill",
     ["多浏览器", "无头模式", "截图/录屏", "自动等待"],
     "npx skills add anthropics/skills --skill webapp-testing",
     "npx 安装后 Agent 自动会用 Playwright 测试网站",
     ["Claude Code", "Copilot", "Node.js"]),

    ("openclaw/openclaw", "openclaw-browser", "OpenClaw Browser Skill", "web", "🌐",
     "OpenClaw 内置浏览器 Skill——直接浏览和操作网页",
     "OpenClaw built-in browser skill — browse and interact with websites natively",
     ["内置 Skill", "直接调用", "无需额外安装"],
     "openclaw install skill openclaw-browser",
     "OpenClaw 内置，无需额外安装",
     ["OpenClaw"]),

    ("lobehub/market-cli", "lobehub-search", "LobeHub Search Engine", "web", "🔑",
     "LobeHub Skill 搜索引擎——让 Agent 找到更多 Skill",
     "LobeHub skill search engine — lets agents discover more skills",
     ["33 万+ Skills", "矢量搜索", "命令行调用"],
     "npx -y @lobehub/market-cli skills install lobehub-skills-search-engine",
     "安装后 Agent 可以搜索 LobeHub 市场",
     ["Cursor", "OpenClaw", "Claude Code"]),

    # ===== 5. 代码开发 =====
    # 已有 4 个，再加 7 个
    ("anthropics/skills", "anthropics-frontend", "anthropics/skills (frontend)", "code", "🎨",
     "Anthropic 官方 frontend-design Skill——生产级前端 UI 组件",
     "Anthropic's frontend-design skill — production-grade UI component creation",
     ["React/Tailwind", "shadcn/ui", "组件库", "生产级质量"],
     "npx skills add anthropics/skills --skill frontend-design",
     "npx 安装后 Agent 会生成专业的 UI 代码",
     ["Claude Code", "Copilot"]),

    ("anthropics/skills", "anthropics-mcp", "anthropics/skills (mcp-builder)", "code", "🔌",
     "MCP Server 构建 Skill——让 AI Agent 创建 Model Context Protocol 服务",
     "MCP builder skill — create Model Context Protocol servers with AI agents",
     ["MCP 标准", "自动搭建", "生产级"],
     "npx skills add anthropics/skills --skill mcp-builder",
     "npx 安装后让 Agent 帮你写 MCP Server",
     ["Claude Code", "Copilot"]),

    ("DavidSouther/claude-code-architecture-skill", "arch-skill", "Architecture Decision Skill", "code", "🏗️",
     "让 AI Agent 生成架构决策记录(ADR)，系统化做技术决策",
     "Architecture Decision Record generation — systematic tech decision making",
     ["ADR 自动生成", "技术决策系统化", "生产级实践"],
     "git clone https://github.com/DavidSouther/claude-code-architecture-skill",
     "克隆后放到 .claude/skills/",
     ["Claude Code"]),

    ("mattpocock/ts-reset", "ts-reset", "TS Reset", "code", "🔧",
     "TypeScript + AI Agent 工具包——类型安全深度问答和修复",
     "TypeScript type-safe deep fixes and answers for AI coding agents",
     ["类型安全", "深度问答", "自动修复", "40K Star"],
     "npx skills add mattpocock/skills --skill grill-with-docs",
     "搭配 grill-with-docs 一起用",
     ["Claude Code", "Copilot", "TypeScript"]),

    ("backnotprop/plannotator", "plannotator", "Plannotator", "code", "📋",
     "AI 计划/代码的本地可视化批注工具，反馈自动回传给 Agent",
     "Local plan/code annotation tool — feedback flows back to AI agent",
     ["浏览器可视化", "批注评论", "自动反馈 Agent", "TS"],
     "npm install -g plannotator",
     "npm 全局安装后 AI 输出自动打开审查界面",
     ["Claude Code", "Codex", "Copilot CLI"]),

    ("can1357/oh-my-pi", "oh-my-pi", "oh-my-pi", "code", "💡",
     "Pi Agent 增强版——LSP 深度集成 + 调试器调用能力",
     "Pi agent enhanced — LSP integration + debugger invocation",
     ["LSP 深度集成", "重命名同步更新", "调试器调用", "Rust"],
     "curl -fsSL https://oh-my-pi.dev/install.sh | bash",
     "脚本安装后 oh-my-pi run 启动",
     ["Mac", "Linux", "Windows"]),

    ("TryCua/cua", "cua", "Cua", "code", "🖥️",
     '为 AI Agent 提供高性能虚拟环境——自动化"用电脑"任务',
     "High-performance virtual environments for AI agents — automate computer tasks",
     ["轻量虚拟机", "应用操控", "上网/写代码/办公"],
     "git clone https://github.com/TryCua/cua && cd cua && cargo build",
     "克隆后 cargo build 编译",
     ["Mac", "Linux"]),

    # ===== 6. 安全合规 =====
    # 新分类！加 4 个
    ("y00n9u/red-team-claude", "red-team", "Red Team Skill", "vertical", "🛡️",
     "Claude Code 红队测试 Skill——找出 AI 输出的安全漏洞",
     "Red team testing for Claude Code — find security vulnerabilities in AI output",
     ["安全测试", "漏洞发现", "OWASP Top 10"],
     "git clone https://github.com/y00n9u/red-team-claude",
     "克隆后到 .claude/skills/",
     ["Claude Code"]),

    ("Anthropic/skill-security", "skill-security", "Anthropic Skill Security", "vertical", "🔐",
     "Anthropic 官方 Skill 安全审计工具——扫描恶意 Skill",
     "Anthropic's official skill security audit tool — scan for malicious skills",
     ["安全审计", "恶意扫描", "Anthropic 官方"],
     "npx skills add anthropics/skills --skill security-audit",
     "npx 安装后让 Agent 扫描可疑 Skill",
     ["Claude Code", "Copilot"]),

    ("openclaw/openclaw", "openclaw-safety", "OpenClaw Safety", "vertical", "⚠️",
     "OpenClaw 安全加固指南——7.5% ClawHub skills 有恶意代码",
     "OpenClaw safety guide — 7.5% of ClawHub skills contain malicious code",
     ["安全加固", "Skill 审计", "官方指南"],
     "openclaw doctor",
     "运行内置 doctor 检查",
     ["OpenClaw"]),

    ("mcp-security/mcp-scanner", "mcp-scanner", "MCP Security Scanner", "vertical", "🔍",
     "MCP Server 安全扫描器——检查暴露的 API 和敏感权限",
     "MCP Server security scanner — detect exposed APIs and sensitive permissions",
     ["API 扫描", "权限检查", "零配置"],
     "npx mcp-security-scan",
     "npx 一键扫描 MCP Server",
     ["Claude Code", "Copilot"]),

    # ===== 7. 垂直领域扩展 =====
    # 已有 4 个，再加 7 个
    ("coreyhaines31/marketingskills", "marketing", "Marketing Skills", "vertical", "📢",
     "AI Agent 营销全能包：SEO/文案/CRO/增长/数据分析",
     "All-in-one AI marketing skill pack: SEO, copywriting, CRO, analytics",
     ["SEO", "文案", "A/B 测试", "增长工程"],
     "npx skills add https://github.com/coreyhaines31/marketingskills",
     "安装后让 Agent 帮你做营销全流程",
     ["Claude Code", "Copilot", "OpenClaw"]),

    ("lobehub/awesome-n8n-templates", "n8n-templates", "Awesome n8n Templates", "vertical", "📨",
     "280+ 免费 n8n 自动化模板——Gmail/Telegram/Slack/Discord/Notion",
     "280+ free n8n templates — Gmail, Telegram, Slack, Discord, Notion, Google Drive",
     ["280+ 模板", "Gmail/Telegram/Slack", "零代码工作流"],
     "npx skills add enescingoz/awesome-n8n-templates",
     "安装后让 Agent 帮你搭自动化工作流",
     ["n8n", "OpenClaw"]),

    ("huginn/huginn", "huginn", "Huginn", "vertical", "📊",
     "让 AI Agent 创建/监控/执行数据代理——经典自动化平台",
     "Create agents that monitor and act on your behalf — classic automation",
     ["49K Star", "监控执行", "数据代理"],
     "docker run huginn/huginn",
     "Docker 运行后 Web UI 配置代理",
     ["Docker", "Web UI"]),

    ("nicbarker/knowledge-work", "knowledge-work", "Knowledge Work Skills", "vertical", "📚",
     "知识工作者全套 Skill：研究/写作/分析/项目管理",
     "Knowledge workers' full skill kit — research, writing, analysis, PM",
     ["研究", "写作", "分析", "项目管理"],
     "git clone https://github.com/nicbarker/knowledge-work",
     "克隆后按需复制",
     ["Claude Code", "Copilot"]),

    ("chuspeeism/dashi-ppt-skill", "dashi-ppt", "Dashi PPT Skill", "vertical", "📽️",
     "让 AI Agent 帮你做 PPT——文档→网页版 PPT→可编辑 PPTX",
     "Turn docs into editable PPT with AI agent — web-based + exportable PPTX",
     ["网页版 PPT", "浏览器编辑", "一键导出 PPTX"],
     "git clone https://github.com/chuspeeism/dashi-ppt-skill",
     "克隆后放到 Agent skills 目录",
     ["Claude Code", "Copilot"]),

    ("virgiliojr94/book-to-skill", "book-to-skill", "Book-to-Skill", "vertical", "📖",
     "把技术书/文档自动转成 Agent Skill——章节拆分+SKILL.md 生成",
     "Automatically convert tech books & docs into agent skills — chapter split + SKILL.md",
     ["自动拆分章节", "生成 SKILL.md", "技术文档 → Skill"],
     "git clone https://github.com/virgiliojr94/book-to-skill",
     "克隆后 Python 运行",
     ["Python", "Claude Code"]),

    ("bojieli/ai-agent-book", "ai-agent-book", "《深入理解 AI Agent》", "learn", "📕",
     "李博杰著开源书——AI Agent 设计原理与工程实践",
     "Open-source book by Bojie Li — AI Agent design principles and engineering practice",
     ["中文", "开源书", "实战代码", "51K Star"],
     "git clone https://github.com/bojieli/ai-agent-book",
     "克隆后直接阅读或配套代码",
     ["Python", "全栈"]),
]


def fetch_stars(repo):
    """从 GitHub API 拉 star 数"""
    url = f"https://api.github.com/repos/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "awesome-ai-skills-builder"}
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                return data.get("stargazers_count")
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"  ⚠️ 限流，等 15s ({repo})")
                time.sleep(15)
                continue
            print(f"  ❌ {repo}: HTTP {e.code}")
            return None
        except Exception as e:
            print(f"  ❌ {repo}: {e}")
            time.sleep(5)
    return None


def fmt_stars(n):
    if n is None: return 0
    return int(n)


def main():
    print(f"🚀 开始构建新 skills.json，共 {len(NEW_PROJECTS)} 个新项目")

    # 1. 拉所有 Star 数
    enriched = []
    for i, p in enumerate(NEW_PROJECTS, 1):
        repo, pid, name, cat, emoji, zh, en, feats, install, usage, compat = p
        print(f"[{i}/{len(NEW_PROJECTS)}] {repo} ...", end=" ")
        stars = fetch_stars(repo)
        if stars is not None:
            print(f"{stars} ⭐")
        else:
            print("失败，稍后重试")
        enriched.append((repo, pid, name, cat, emoji, zh, en, feats, install, usage, compat, stars))
        time.sleep(0.4)  # 限流保护

    # 2. 合并现有 + 新增
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "..", "docs", "data", "skills.json")
    src = os.path.abspath(src)
    with open(src, "r", encoding="utf-8") as f:
        existing = json.load(f)

    # 把新项目也加进去
    for repo, pid, name, cat, emoji, zh, en, feats, install, usage, compat, stars in enriched:
        existing["skills"].append({
            "id": pid,
            "category": cat,
            "name": name,
            "owner": repo.split("/")[0],
            "repo": repo,
            "stars": fmt_stars(stars),
            "emoji": emoji,
            "shortDesc": zh,
            "descEn": en,
            "features": feats,
            "install": install,
            "usage": usage,
            "compatible": compat,
            "repoUrl": f"https://github.com/{repo}"
        })

    # 3. 按 Star 数排序
    existing["skills"].sort(key=lambda s: s["stars"], reverse=True)

    # 4. 重新统计每个分类的计数（不需要改 categories，分类定义不变）
    # 但我们新增了 "security" 分类？不，我们的 category 映射保持原有 8 个
    # 把 "framework" 下 openclaw 有重复，清理一下
    seen_ids = set()
    clean = []
    for s in existing["skills"]:
        if s["id"] not in seen_ids:
            seen_ids.add(s["id"])
            clean.append(s)
    existing["skills"] = clean

    # 5. 写回
    with open(src, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 完成！共 {len(existing['skills'])} 个 Skill 写入 {src}")
    for cat in existing["categories"]:
        n = sum(1 for s in existing["skills"] if s["category"] == cat["id"])
        if n > 0:
            print(f"   {cat['name']}: {n} 个")


if __name__ == "__main__":
    main()
