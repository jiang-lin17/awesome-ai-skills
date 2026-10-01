# 🚀 Awesome AI Skills

> 一个精选的 GitHub AI Agent Skills 与工具集合，帮助 AI 使用者快速找到适合的技能包 / A curated collection of GitHub AI Agent Skills & tools, helping AI users find the right skill packs fast.

<div align="center">

<!-- 🎯 网站入口横幅 -->
<table>
<tr>
<td align="center" width="100%" style="padding:20px;border-radius:12px;background:linear-gradient(135deg,#6366f1,#8b5cf6,#ec4899);color:#fff;">

### 👀 想看？点击进入网站浏览！

**👉 [https://jiang-lin17.github.io/awesome-ai-skills/](https://jiang-lin17.github.io/awesome-ai-skills/)**

搜索 · 分类筛选 · 点击看说明书 · 一键复制安装命令

</td>
</tr>
</table>

<br>

[![GitHub stars](https://img.shields.io/github/stars/jiang-lin17/awesome-ai-skills?style=social)](https://github.com/jiang-lin17/awesome-ai-skills/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/jiang-lin17/awesome-ai-skills?style=social)](https://github.com/jiang-lin17/awesome-ai-skills/network/members)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/jiang-lin17/awesome-ai-skills/graphs/commit-activity)
[![Auto-update](https://img.shields.io/badge/Auto--Update-Enabled-brightgreen.svg)](https://github.com/jiang-lin17/awesome-ai-skills/actions)

**🤖 AI Agent Skills · 🛠️ 工具框架 · 💡 安装即用**
**30+ Curated Projects · 8 Categories · Auto-updated Stars**

</div>

---

## 📖 简介 / Introduction

这个仓库收集了 GitHub 上最热门的 **AI Agent Skills** 和相关工具，涵盖从纯技能包到完整 Agent 框架的各类项目。每个条目都附带：

- 🌟 **Star 数量** — 判断项目热度
- 📝 **一句话简介** — 快速了解用途
- ⚡ **安装/加载命令** — 一键试用

适合谁？

- 🧑‍💻 使用 Claude Code / Cursor / Copilot / Trae 等 AI 编码助手的开发者
- 🤖 正在搭建 AI Agent 应用的工程师
- 📚 想了解 AI Agent 生态的学习者

---

## 🏆 精选项目 Top 30

根据 GitHub Star 数、活跃度和实用性筛选（数据更新于 2026 年 10 月）。

---

### 🧠 1. Agent Skills 技能库（纯 Skill 包，可直接加载）

> 可直接放入 `.claude/skills/` 或 GitHub Copilot 的 `.github/agents/` 目录下的技能包

| # | 项目 | ⭐ Stars | 简介 / Description | 安装 / Install |
|---|------|----------|---------------------|----------------|
| 1 | [**superpowers**](https://github.com/obra/superpowers) | 293.6K | 🧩 Agentic skills 框架，教 Agent 先规划再执行，减少混乱代码。An agentic skills framework that teaches agents to plan before coding. | `git clone https://github.com/obra/superpowers` → 放到 Agent skills 目录 |
| 2 | [**caveman**](https://github.com/JuliusBrussee/caveman) | 108.6K | 🪨 "洞穴人"极简 token Skill，砍掉 65% token，让 AI 像老派程序员一样高效。Cuts 65% tokens by speaking in caveman style. | `go install github.com/JuliusBrussee/caveman@latest` |
| 3 | [**addyosmani/agent-skills**](https://github.com/addyosmani/agent-skills) | 100.2K | 🔧 Google 出品，生产级 AI coding agent 工程技能包。Production-grade engineering skills by Google's Addy Osmani. | `git clone https://github.com/addyosmani/agent-skills` → 复制 skill 文件夹 |
| 4 | [**scientific-agent-skills**](https://github.com/K-Dense-AI/scientific-agent-skills) | 47.2K | 🔬 把 AI 变成科学家！170+ skills，25 万+ 科研人员在用，覆盖生物/化学/医药。Turn AI agents into scientists with 170+ validated skills. | `git clone https://github.com/K-Dense-AI/scientific-agent-skills` |
| 5 | [**anthropics/skills**](https://github.com/anthropics/skills) | 179.2K | 🎯 Anthropic 官方开源 Skill 库，含浏览器操作、数据分析等。Official open-source Agent Skills from Anthropic. | `git clone https://github.com/anthropics/skills` → 放到 `.claude/skills/` |
| 6 | [**Vercel find-skills**](https://github.com/vercel-labs/skills) | 32.9K | 🔍 帮你"找适合的 Skill"的 Skill！描述任务，自动推荐并安装。Meta-skill that finds and installs the right skill for your task. | `npx skills add https://github.com/vercel-labs/skills -skill find-skills` |

---

### 🔧 2. Agent 框架与平台（构建/运行 AI Agent 的基础设施）

> 用来搭建自己的 AI Agent 应用的框架，适合想自己造轮子的开发者

| # | 项目 | ⭐ Stars | 简介 / Description | 安装 / Install |
|---|------|----------|---------------------|----------------|
| 7 | [**hermes-agent**](https://github.com/NousResearch/hermes-agent) | 250.4K | 🧠 会"成长"的 Agent！持久化运行，自动学习你的习惯，内置 memory 和 skills。The agent that grows with you, persistent + self-learning. | `curl -fsSL https://hermes-agent.dev/install.sh \| bash` |
| 8 | [**AutoGPT**](https://github.com/Significant-Gravitas/AutoGPT) | 187.6K | 🎯 自主 Agent 先驱！给 AI 一个目标，它自动规划、执行、循环。The OG autonomous AI agent — give it a goal, it plans & executes. | `pip install autogpt` 或 Docker：`docker run -it autogpt/autogpt` |
| 9 | [**dify**](https://github.com/langgenius/dify) | 157.6K | 🎨 开源 Agent 工作流平台，拖拽式构建 Agent，支持云/自建。Open-source platform for building agentic workflows, drag & drop. | `git clone https://github.com/langgenius/dify && cd dify/docker && docker compose up -d` |
| 10 | [**langflow**](https://github.com/langflow-ai/langflow) | 155.4K | 🧊 LangChain 官方可视化构建器，拖拽搭建 RAG 和 Agent 流程。Visual builder for LangChain, drag-and-drop RAG & agents. | `pip install langflow && langflow run` |
| 11 | [**agency-agents**](https://github.com/msitarzewski/agency-agents) | 155.6K | 🏢 一整个 AI "代理公司"！每个 Agent 是某个领域的专家（前端、社区运营…）。A complete AI agency — each agent a domain expert. | `git clone https://github.com/msitarzewski/agency-agents` |
| 12 | [**langchain**](https://github.com/langchain-ai/langchain) | 147.3K | 🔗 Agent 工程标准框架，最大的 Agent 生态系统。The standard framework for building LLM-powered agents. | `pip install langchain` 或 `npm install langchain` |

---

### 💾 3. 持久化记忆系统（让 Agent 跨会话"记住"东西）

> 解决 AI Agent "失忆"问题，跨 session 保留上下文和经验

| # | 项目 | ⭐ Stars | 简介 / Description | 安装 / Install |
|---|------|----------|---------------------|----------------|
| 13 | [**claude-mem**](https://github.com/thedotmack/claude-mem) | 95.0K | 🧠 给 Claude Code 加持久记忆！自动捕捉操作、压缩摘要、智能注入。Persistent memory for Claude Code — captures, compresses, injects context. | `cd ~ && npm install -g claude-mem && claude-mem init` |
| 14 | [**MemPalace**](https://github.com/MemPalace/mempalace) | 59.4K | 🏰 开源 Agent 记忆系统，多模型支持，RAG 友好。Best-benchmarked open-source AI memory system. | `pip install mempalace` |

---

### 🌐 4. 网络访问与数据获取（让 Agent 能上网）

> 给 AI Agent 装上"眼睛"，能搜索网页、抓取数据

| # | 项目 | ⭐ Stars | 简介 / Description | 安装 / Install |
|---|------|----------|---------------------|----------------|
| 15 | [**firecrawl**](https://github.com/firecrawl/firecrawl) | 187.3K | 🔥 给 Agent 喂网页数据的 API，搜索+抓取+清洗一条龙。Turns websites into LLM-ready data for agents. | `npm install @mendable/firecrawl-js` 或 `pip install firecrawl-py` |
| 16 | [**browser-use**](https://github.com/browser-use/browser-use) | 116.9K | 🌐 让 LLM 控制浏览器！自动化网页操作。Make AI agents control browsers autonomously. | `pip install browser-use` + `playwright install` |
| 17 | [**Agent-Reach**](https://github.com/Panniantong/Agent-Reach) | 86.8K | 👁️ 给 Agent 装上全网"眼睛"——Twitter/Reddit/YouTube/B站/小红书，一个 CLI 搞定。Give agents eyes across Twitter, Reddit, YouTube, Bilibili, Xiaohongshu. | `pip install agent-reach` |
| 18 | [**crawl4ai**](https://github.com/unclecode/crawl4ai) | 84.6K | 🕷️ AI 友好的爬虫，一键把网页变成 LLM 可用的 Markdown。Converts any URL into LLM-ready Markdown in seconds. | `pip install crawl4ai && crawl4ai-setup` |

---

### 🎨 5. 代码开发辅助（让 Coding Agent 更专业）

> 专门提升 AI 编码助手能力的技能包和工具

| # | 项目 | ⭐ Stars | 简介 / Description | 安装 / Install |
|---|------|----------|---------------------|----------------|
| 19 | [**ponytail**](https://github.com/DietrichGebert/ponytail) | 149.5K | 🐴 让 Agent 像"最懒的资深工程师"一样思考——不写多余代码。Makes AI agents think like the laziest senior dev. | `git clone https://github.com/DietrichGebert/ponytail` → Skill 加载 |
| 20 | [**gemini-cli**](https://github.com/google-gemini/gemini-cli) | 107.2K | 💎 Google 开源的 Gemini CLI Agent，多模态，直接在终端用。Open-source multimodal Gemini agent in your terminal. | `npm install -g @google/gemini-cli` |
| 21 | [**pi**](https://github.com/earendil-works/pi) | 110.8K | 🍰 轻量 AI Agent 工具箱，统一 LLM API + agent loop + TUI + coding CLI. Lightweight AI agent toolkit: unified API, loop, TUI, coding CLI. | `curl -fsSL https://pi.dev/install.sh \| bash` |
| 22 | [**rtk**](https://github.com/rtk-ai/rtk) | 82.1K | ⚡ CLI 代理，砍掉 60-90% LLM token 消耗。CLI proxy that cuts LLM token usage 60-90%. | `cargo install rtk` 或下载 release binary |

---

### 🔍 6. System Prompts & Agent 内幕

> 顶级 AI 工具的 System Prompt 和内部机制大揭秘

| # | 项目 | ⭐ Stars | 简介 / Description | 安装 / Install |
|---|------|----------|---------------------|----------------|
| 23 | [**system-prompts-and-models-of-ai-tools**](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | 144.0K | 🔐 Cursor/Claude Code/Devin/Trae 等 30+ 顶级 AI 工具的 System Prompt 和内部 tools 全集。System prompts & internal tools of 30+ top AI coding tools. | 直接浏览或 `git clone` 研究 |

---

### 📚 7. Awesome Lists & 学习资源

> 更广泛的 AI Agent 项目合集和学习教程

| # | 项目 | ⭐ Stars | 简介 / Description | 安装 / Install |
|---|------|----------|---------------------|----------------|
| 24 | [**awesome-llm-apps**](https://github.com/Shubhamsaboo/awesome-llm-apps) | 140.4K | 📚 100+ 免费开源 AI Agent、Agent Skills 和 RAG 应用。100+ free AI agents, agent skills & RAG apps. | 直接浏览 |
| 25 | [**Hello-Agents**](https://github.com/datawhalechina/Hello-Agents) | 81.4K | 🎓 Datawhale 社区出品，从零构建 AI Native Agent 的完整教程。Complete course for building AI agents from scratch. | `git clone https://github.com/datawhalechina/Hello-Agents` |
| 26 | [**GitHub awesome-copilot**](https://github.com/github/awesome-copilot) | — | 🌟 GitHub 官方 Copilot 自定义 Agent 和 Skill 合集。Official collection of GitHub Copilot custom agents & skills. | 直接浏览 |

---

### ⚙️ 8. 垂直领域 & 工作流工具

> 特定场景下的 Agent 工具和自动化平台

| # | 项目 | ⭐ Stars | 简介 / Description | 安装 / Install |
|---|------|----------|---------------------|----------------|
| 27 | [**n8n**](https://github.com/n8n-io/n8n) | 206.4K | 🔄 开源工作流自动化 + AI 能力，400+ 集成。Open-source workflow automation with native AI. | `npm run n8n` 或 Docker：`docker run n8nio/n8n` |
| 28 | [**ragflow**](https://github.com/infiniflow/ragflow) | 91.6K | 📑 开源 RAG 引擎，深度文档理解 + Agent 能力融合。Open-source RAG engine with deep doc understanding + agent fusion. | `git clone https://github.com/infiniflow/ragflow && docker compose up -d` |
| 29 | [**career-ops**](https://github.com/career-ops-hq/career-ops) | 73.2K | 💼 开源 AI 求职 Agent——自动扫描招聘站、筛选职位、生成简历。Open-source AI job search agent. | `pip install career-ops` |
| 30 | [**autoresearch**](https://github.com/karpathy/autoresearch) | 97.1K | 🧪 Karpathy 出品，自动运行 AI 研究实验。AI agents running research experiments autonomously. | `pip install autoresearch` |

---

## 🛠️ 如何使用这些 Skills

### Claude Code / Anthropic 标准 Skill 格式
```bash
# 1. 克隆 Skill 仓库
git clone https://github.com/addyosmani/agent-skills

# 2. 把想要的 skill 文件夹复制到你的项目
cp -r agent-skills/skills/* .claude/skills/

# 3. 重启或刷新 Agent，skill 自动加载
```

### GitHub Copilot Agent Skills
```bash
# 放到仓库里
mkdir -p .github/agents
cp your-skill.md .github/agents/
# 或者放到组织级 .github 仓库
```

### 通用加载方式
大多数现代 AI Agent（Claude Code、Cursor、Trae、OpenClaw）都支持类似的 skills 目录机制：

| Agent | Skill 目录 |
|-------|-----------|
| Claude Code | `.claude/skills/` |
| GitHub Copilot | `.github/agents/` |
| Trae | 插件市场加载 |
| OpenClaw | `~/.openclaw/skills/` |
| 通用标准 | 每个 skill 文件夹含 `SKILL.md` + 脚本 + 资源 |

---

## 📊 生态趋势（2026 Q4）

- **Agent Skills 标准化** — Anthropic 推动的 Agent Skills 规范正在被 Copilot、Cursor、Trae 等广泛采用
- **持久化记忆成刚需** — claude-mem 等项目爆发式增长，Agent 跨会话连续性成核心痛点
- **"Personal Agent" 赛道爆发** — Meta Muse、OpenAI Dots、大厂 Handy Bot/Spell 等 2026 年 Q3 集中推出
- **AI + 浏览器** — browser-use、Agent-Reach 让 Agent 真正"看得见"互联网

---

## 🤝 贡献指南 / Contributing

欢迎提交你发现的热门 AI Skill！

1. Fork 本仓库
2. 在 README.md 对应分类下添加项目条目
3. 确保格式：`| # | [项目名](链接) | ⭐ Stars | 简介 | 安装命令 |`
4. 提交 PR

---

## 📄 License

[MIT](./LICENSE) — 自由使用、修改、分发。

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请 Star 支持一下！**

</div>
