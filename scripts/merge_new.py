#!/usr/bin/env python3
"""合并新增项目到现有 skills.json"""
import json

# 新增项目（跳过 404 的）
new = [
    {'id':'openclaw-fw','category':'framework','name':'OpenClaw','owner':'openclaw','repo':'openclaw/openclaw','stars':391075,'emoji':'🦞','shortDesc':'现象级开源个人 AI Agent 框架，本地运行+多平台消息接入','descEn':'Phenomenal open-source personal AI agent framework, local-first, multi-channel','features':['本地部署','多消息平台','内置 Skills','ClawHub 社区'],'install':'curl -fsSL https://openclaw.ai/install.sh | bash','usage':'脚本安装后 openclaw run 启动','compatible':['跨平台','Node.js'],'repoUrl':'https://github.com/openclaw/openclaw'},
    {'id':'mattpocock-skills','category':'skills','name':'mattpocock/skills','owner':'mattpocock','repo':'mattpocock/skills','stars':273284,'emoji':'🎣','shortDesc':'Vercel Matt Pocock 出品，idea 审查+Code Review 全套 Skill','descEn':'Matt Pocock skill pack: grill-me idea testing, code review, TS deep dives','features':['grill-me 创意审查','Code Review','TypeScript 深度','100万+安装'],'install':'npx skills add https://github.com/mattpocock/skills','usage':'npx 安装后 grill-me 检查你的想法','compatible':['Claude Code','Copilot','Cursor'],'repoUrl':'https://github.com/mattpocock/skills'},
    {'id':'last30days-skill','category':'skills','name':'last30days-skill','owner':'mvanhorn','repo':'mvanhorn/last30days-skill','stars':63304,'emoji':'🕒','shortDesc':'自动检索 Reddit/X/YouTube/HN 最近 30 天热点并汇总','descEn':'Research last 30 days across Reddit, X, YouTube, HN, synthesize brief','features':['跨平台','自动合成简报','零手动操作'],'install':'npx skills add mvanhorn/last30days-skill -g','usage':'全局安装后问 Agent 最近 AI 圈热点','compatible':['Claude Code','Copilot','OpenClaw'],'repoUrl':'https://github.com/mvanhorn/last30days-skill'},
    {'id':'antigravity-skills','category':'skills','name':'antigravity-awesome-skills','owner':'sickn33','repo':'sickn33/antigravity-awesome-skills','stars':47135,'emoji':'⚡','shortDesc':'500+ 通用 Agent Skills 大合集：开发/架构/安全/DevOps','descEn':'500+ foundational skills: dev, architecture, security, DevOps, cloud','features':['500+ Skill','开发全流程','安全专家'],'install':'git clone https://github.com/sickn33/antigravity-awesome-skills','usage':'克隆后按需复制到 agent skills 目录','compatible':['Claude Code','Copilot','Cursor','OpenClaw'],'repoUrl':'https://github.com/sickn33/antigravity-awesome-skills'},
    {'id':'academic-skills','category':'skills','name':'academic-research-skills','owner':'Imbad0202','repo':'Imbad0202/academic-research-skills','stars':50041,'emoji':'🎓','shortDesc':'13 Agent 深度研究团队 + 12 Agent 论文写作团队','descEn':'13-agent deep research, 12-agent paper writing, multi-perspective review','features':['深度研究','LaTeX 论文','同行评审','学术写作'],'install':'git clone https://github.com/Imbad0202/academic-research-skills','usage':'克隆后让 Agent 自动跑研究流程','compatible':['Claude Code','Copilot','Cursor'],'repoUrl':'https://github.com/Imbad0202/academic-research-skills'},
    {'id':'humanizer','category':'skills','name':'humanizer','owner':'blader','repo':'blader/humanizer','stars':53219,'emoji':'✍️','shortDesc':'让 AI 写作更像人类！去除 AI 生成痕迹','descEn':'Remove signs of AI-generated writing, sounds natural and human','features':['AI 痕迹去除','自然人类文风','学术必备'],'install':'npx skills add blader/humanizer','usage':'安装后 AI 输出自动 humanize','compatible':['Claude Code','Copilot'],'repoUrl':'https://github.com/blader/humanizer'},
    {'id':'orca','category':'framework','name':'Orca','owner':'stablyai','repo':'stablyai/orca','stars':82651,'emoji':'🐳','shortDesc':'让多个 AI Agent 并行开发的 IDE 编排工具','descEn':'Cross-platform multi-agent orchestration IDE — parallel agents, merge best','features':['多 Agent 并行','Git 工作树隔离','自动对比合并'],'install':'git clone https://github.com/stablyai/orca && pnpm install','usage':'pnpm 启动，统一管理多个 Agent','compatible':['跨平台','Node.js'],'repoUrl':'https://github.com/stablyai/orca'},
    {'id':'pi-fw','category':'framework','name':'Pi (framework)','owner':'earendil-works','repo':'earendil-works/pi','stars':110866,'emoji':'🍰','shortDesc':'轻量 AI Agent 工具箱：统一 LLM API + Agent Loop + TUI','descEn':'Lightweight toolkit: unified LLM API, agent loop, TUI, coding CLI','features':['统一 LLM API','Agent Loop','漂亮 TUI'],'install':'curl -fsSL https://pi.dev/install.sh | bash','usage':'脚本安装后终端运行 pi','compatible':['Mac','Linux','WSL'],'repoUrl':'https://github.com/earendil-works/pi'},
    {'id':'paseo','category':'framework','name':'Paseo','owner':'getpaseo','repo':'getpaseo/paseo','stars':19142,'emoji':'📱','shortDesc':'跨设备管理 AI Agent：iOS/Android/桌面/Web/CLI 全覆盖','descEn':'Cross-platform management for Claude Code, Codex — voice, multi-device','features':['多客户端','语音控制','跨设备协同'],'install':'npm install -g paseo','usage':'npm 全局安装后 paseo 启动','compatible':['iOS','Android','桌面','Web'],'repoUrl':'https://github.com/getpaseo/paseo'},
    {'id':'GenericAgent','category':'framework','name':'GenericAgent','owner':'lsdefine','repo':'lsdefine/GenericAgent','stars':14277,'emoji':'🌱','shortDesc':'自我进化 Agent：从 3.3K 行种子长出完整系统','descEn':'Self-evolving agent: grows skill tree from seed, 6x less tokens','features':['自我进化','Skill Tree','系统级控制'],'install':'npx skills add lsdefine/GenericAgent','usage':'npx 安装后 Agent 自我生长','compatible':['Claude Code','Copilot'],'repoUrl':'https://github.com/lsdefine/GenericAgent'},
    {'id':'autogen','category':'framework','name':'AutoGen (Microsoft)','owner':'microsoft','repo':'microsoft/autogen','stars':58000,'emoji':'🧬','shortDesc':'微软出品，多 Agent 对话协作框架','descEn':'Microsoft multi-agent conversation framework — agents talk to solve tasks','features':['多 Agent 对话','微软出品','Python + .NET'],'install':'pip install pyautogen','usage':'pip 安装后写 Python 脚本定义 Agent','compatible':['Python','.NET'],'repoUrl':'https://github.com/microsoft/autogen'},
    {'id':'mem0','category':'memory','name':'mem0','owner':'mem0ai','repo':'mem0ai/mem0','stars':66401,'emoji':'🧠','shortDesc':'给任何 LLM 添加持久化记忆的通用层','descEn':'Universal memory layer for LLMs — persistent memory for any LLM app','features':['多 LLM 支持','向量存储','自动摘要','MIT'],'install':'pip install mem0ai','usage':'pip 安装后 LangChain/LlamaIndex 直接 import','compatible':['Python','LangChain','LlamaIndex'],'repoUrl':'https://github.com/mem0ai/mem0'},
    {'id':'playwright-skill','category':'web','name':'Playwright (skill)','owner':'microsoft','repo':'microsoft/playwright','stars':96939,'emoji':'🎭','shortDesc':'Playwright 自动化浏览器——Anthropic 推荐 Agent Skill','descEn':'Playwright browser automation — Anthropic-recommended agent skill','features':['多浏览器','无头模式','截图/录屏','自动等待'],'install':'npx skills add anthropics/skills --skill webapp-testing','usage':'npx 安装后 Agent 自动会用 Playwright','compatible':['Claude Code','Copilot','Node.js'],'repoUrl':'https://github.com/microsoft/playwright'},
    {'id':'ts-reset','category':'code','name':'TS Reset','owner':'mattpocock','repo':'mattpocock/ts-reset','stars':8616,'emoji':'🔧','shortDesc':'TypeScript + AI Agent 工具包——类型安全深度问答和修复','descEn':'TypeScript type-safe deep fixes for AI coding agents','features':['类型安全','深度问答','自动修复'],'install':'npx skills add mattpocock/skills --skill grill-with-docs','usage':'搭配 grill-with-docs 使用','compatible':['Claude Code','Copilot','TypeScript'],'repoUrl':'https://github.com/mattpocock/ts-reset'},
    {'id':'plannotator','category':'code','name':'Plannotator','owner':'backnotprop','repo':'backnotprop/plannotator','stars':9082,'emoji':'📋','shortDesc':'AI 计划/代码的本地可视化批注工具','descEn':'Local plan/code annotation tool — feedback flows back to AI agent','features':['浏览器可视化','批注评论','自动反馈'],'install':'npm install -g plannotator','usage':'AI 输出自动打开审查界面','compatible':['Claude Code','Codex','Copilot CLI'],'repoUrl':'https://github.com/backnotprop/plannotator'},
    {'id':'oh-my-pi','category':'code','name':'oh-my-pi','owner':'can1357','repo':'can1357/oh-my-pi','stars':33911,'emoji':'💡','shortDesc':'Pi Agent 增强版——LSP 深度集成+调试器调用','descEn':'Pi agent enhanced — LSP integration + debugger invocation','features':['LSP 深度集成','重命名同步更新','调试器调用','Rust'],'install':'curl -fsSL https://oh-my-pi.dev/install.sh | bash','usage':'脚本安装后 oh-my-pi run 启动','compatible':['Mac','Linux','Windows'],'repoUrl':'https://github.com/can1357/oh-my-pi'},
    {'id':'cua','category':'code','name':'Cua','owner':'TryCua','repo':'TryCua/cua','stars':27618,'emoji':'🖥️','shortDesc':'为 AI Agent 提供高性能虚拟环境','descEn':'High-performance virtual environments for AI agents — automate computer tasks','features':['轻量虚拟机','应用操控','上网/写代码/办公'],'install':'git clone https://github.com/TryCua/cua && cargo build','usage':'克隆后 cargo build 编译','compatible':['Mac','Linux'],'repoUrl':'https://github.com/TryCua/cua'},
    {'id':'huginn','category':'vertical','name':'Huginn','owner':'huginn','repo':'huginn/huginn','stars':50016,'emoji':'📊','shortDesc':'让 AI 创建/监控/执行数据代理——经典自动化平台','descEn':'Create agents that monitor and act on your behalf — classic automation','features':['监控执行','数据代理','Docker'],'install':'docker run huginn/huginn','usage':'Docker 运行后 Web UI 配置','compatible':['Docker','Web UI'],'repoUrl':'https://github.com/huginn/huginn'},
    {'id':'dashi-ppt','category':'vertical','name':'Dashi PPT Skill','owner':'chuspeeism','repo':'chuspeeism/dashi-ppt-skill','stars':9022,'emoji':'📽️','shortDesc':'让 AI Agent 帮你做 PPT——文档→网页 PPT→可编辑 PPTX','descEn':'Turn docs into editable PPT — web-based + exportable PPTX','features':['网页版 PPT','浏览器编辑','一键导出 PPTX'],'install':'git clone https://github.com/chuspeeism/dashi-ppt-skill','usage':'克隆后放到 Agent skills 目录','compatible':['Claude Code','Copilot'],'repoUrl':'https://github.com/chuspeeism/dashi-ppt-skill'},
    {'id':'book-to-skill','category':'vertical','name':'Book-to-Skill','owner':'virgiliojr94','repo':'virgiliojr94/book-to-skill','stars':33202,'emoji':'📖','shortDesc':'把技术书/文档自动转成 Agent Skill','descEn':'Automatically convert tech books into agent skills','features':['自动拆分章节','生成 SKILL.md'],'install':'git clone https://github.com/virgiliojr94/book-to-skill','usage':'克隆后 Python 运行','compatible':['Python','Claude Code'],'repoUrl':'https://github.com/virgiliojr94/book-to-skill'},
    {'id':'ai-agent-book','category':'learn','name':'《深入理解 AI Agent》','owner':'bojieli','repo':'bojieli/ai-agent-book','stars':51973,'emoji':'📕','shortDesc':'李博杰著开源书——AI Agent 设计原理与工程实践','descEn':'Open-source book by Bojie Li — AI Agent design principles and engineering','features':['中文','开源书','实战代码'],'install':'git clone https://github.com/bojieli/ai-agent-book','usage':'克隆后直接阅读或配套代码','compatible':['Python','全栈'],'repoUrl':'https://github.com/bojieli/ai-agent-book'},
]

# 读现有
with open('docs/data/skills.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"现有 {len(data['skills'])} 个 skills")

# 合并去重
existing_ids = {s['id'] for s in data['skills']}
added = 0
for s in new:
    if s['id'] not in existing_ids:
        data['skills'].append(s)
        existing_ids.add(s['id'])
        added += 1

# 按 Star 排序
data['skills'].sort(key=lambda x: x['stars'], reverse=True)

# 写回
with open('docs/data/skills.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"新增 {added} 个，总计 {len(data['skills'])} 个 Skill")
print("Top 10:")
for s in data['skills'][:10]:
    print(f"  {s['stars']:>8,} ⭐  {s['name']} ({s['category']})")

# 每个分类的数量
print("\n分类统计:")
cats = {}
for s in data['skills']:
    c = s['category']
    cats[c] = cats.get(c, 0) + 1
for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {n}")
