/* ============================================================
 *  Awesome AI Skills - 前端交互逻辑
 *  从 data/skills.json 加载数据，渲染首页和详情页
 * ============================================================ */

const DATA_URL = 'data/skills.json';

// 格式化 Star 数
function fmtStars(n) {
  if (n >= 10000) {
    const v = n / 1000;
    return (v % 1 === 0 ? v.toFixed(0) : v.toFixed(1)) + 'K';
  }
  return n.toString();
}

// 从 GitHub URL 提取 owner/repo
function repoName(repo) {
  return repo;
}

// 加载数据
async function loadData() {
  const res = await fetch(DATA_URL);
  return await res.json();
}

/* ==================== 首页逻辑 ==================== */
function renderHome(data) {
  const { categories, skills } = data;
  let activeCat = 'all';
  let searchTerm = '';

  // 渲染分类按钮
  const catContainer = document.getElementById('categoryFilters');
  catContainer.innerHTML = [
    `<button class="cat-btn active" data-cat="all">🌟 全部 (${skills.length})</button>`,
    ...categories.map(c => {
      const count = skills.filter(s => s.category === c.id).length;
      return `<button class="cat-btn" data-cat="${c.id}">${c.name} (${count})</button>`;
    })
  ].join('');

  // 分类切换
  catContainer.addEventListener('click', (e) => {
    const btn = e.target.closest('.cat-btn');
    if (!btn) return;
    catContainer.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeCat = btn.dataset.cat;
    renderSkills();
  });

  // 搜索
  const searchInput = document.getElementById('searchInput');
  searchInput.addEventListener('input', (e) => {
    searchTerm = e.target.value.toLowerCase().trim();
    renderSkills();
  });

  // 渲染卡片
  function renderSkills() {
    const grid = document.getElementById('skillGrid');
    const empty = document.getElementById('emptyState');
    const filtered = skills.filter(s => {
      const matchCat = activeCat === 'all' || s.category === activeCat;
      if (!searchTerm) return matchCat;
      const t = searchTerm;
      return matchCat && (
        s.name.toLowerCase().includes(t) ||
        s.shortDesc.toLowerCase().includes(t) ||
        s.descEn.toLowerCase().includes(t) ||
        (s.features || []).some(f => f.toLowerCase().includes(t))
      );
    });

    if (filtered.length === 0) {
      grid.innerHTML = '';
      empty.classList.remove('hidden');
      return;
    }
    empty.classList.add('hidden');

    grid.innerHTML = filtered.map(s => {
      const catName = categories.find(c => c.id === s.category)?.name || '';
      return `
        <a href="skill.html?id=${s.id}" class="skill-card" data-id="${s.id}">
          <div class="flex items-start justify-between mb-3">
            <span class="text-4xl">${s.emoji}</span>
            <span class="badge badge-star">
              <i class="fa-solid fa-star"></i>
              ${fmtStars(s.stars)}
            </span>
          </div>
          <h3 class="text-lg font-bold mb-1.5 text-slate-100">${s.name}</h3>
          <p class="text-slate-400 text-sm leading-relaxed line-clamp-2 mb-3">${s.shortDesc}</p>
          <div class="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-700/30">
            <span>${catName}</span>
            <span class="text-indigo-400">点击查看 →</span>
          </div>
        </a>
      `;
    }).join('');
  }

  renderSkills();
}

/* ==================== 详情页逻辑 ==================== */
function renderDetail(data) {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  const { categories, skills } = data;
  const s = skills.find(x => x.id === id);

  const container = document.getElementById('skillDetail');

  if (!s) {
    container.innerHTML = `
      <div class="text-center py-20">
        <div class="text-6xl mb-4">😕</div>
        <h2 class="text-2xl font-bold mb-2">找不到这个 Skill</h2>
        <p class="text-slate-400 mb-6">可能链接已失效或 Skill 已下架</p>
        <a href="index.html" class="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-indigo-500 hover:bg-indigo-600 transition font-medium">
          <i class="fa-solid fa-arrow-left"></i> 返回首页
        </a>
      </div>
    `;
    return;
  }

  const catName = categories.find(c => c.id === s.category)?.name || '';
  const features = s.features || [];
  const compatible = s.compatible || [];

  container.innerHTML = `
    <!-- Skill 头部 -->
    <div class="detail-section">
      <div class="flex flex-col sm:flex-row sm:items-start gap-5">
        <div class="text-6xl">${s.emoji}</div>
        <div class="flex-1">
          <div class="flex items-center gap-2 mb-2 flex-wrap">
            <span class="badge badge-star"><i class="fa-solid fa-star"></i> ${fmtStars(s.stars)}</span>
            <span class="tag">${catName}</span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-black mb-2 gradient-text">${s.name}</h2>
          <p class="text-slate-300 text-base">${s.shortDesc}</p>
          <p class="text-slate-500 text-sm mt-1 italic">${s.descEn}</p>
          <div class="mt-4 flex gap-2">
            <a href="${s.repoUrl}" target="_blank" class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 transition text-sm">
              <i class="fa-brands fa-github"></i> GitHub 仓库
            </a>
            <a href="${s.repoUrl}/stargazers" target="_blank" class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-yellow-500/10 hover:bg-yellow-500/20 border border-yellow-500/30 transition text-sm text-yellow-300">
              <i class="fa-solid fa-star"></i> Star 一下
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- 核心特点 -->
    <div class="detail-section">
      <h3><i class="fa-solid fa-sparkles text-indigo-400"></i> 核心特点</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        ${features.map((f, i) => `
          <div class="flex items-start gap-3 p-3 rounded-lg bg-slate-800/40 border border-slate-700/30">
            <span class="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-500/20 text-indigo-400 text-xs flex items-center justify-center font-bold">${i + 1}</span>
            <span class="text-slate-300 text-sm">${f}</span>
          </div>
        `).join('')}
      </div>
    </div>

    <!-- 安装命令 -->
    <div class="detail-section">
      <h3><i class="fa-solid fa-terminal text-emerald-400"></i> 安装命令</h3>
      <div class="code-block">${escapeHtml(s.install)}<button class="copy-btn" onclick="copyCode(this)">复制</button></div>
    </div>

    <!-- 使用方法 -->
    <div class="detail-section">
      <h3><i class="fa-solid fa-book-open text-amber-400"></i> 使用方法</h3>
      <p class="text-slate-300 leading-relaxed">${s.usage}</p>
    </div>

    <!-- 兼容 Agent -->
    <div class="detail-section">
      <h3><i class="fa-solid fa-plug text-cyan-400"></i> 兼容的 AI Agent</h3>
      <div class="flex flex-wrap gap-2">
        ${compatible.map(c => `<span class="tag">${c}</span>`).join('')}
      </div>
    </div>

    <!-- 相关项目 -->
    <div class="detail-section">
      <h3><i class="fa-solid fa-link text-pink-400"></i> 快速跳转</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <a href="${s.repoUrl}" target="_blank" class="p-4 rounded-lg bg-slate-800/40 border border-slate-700/30 hover:border-indigo-500/50 hover:bg-slate-800/60 transition group">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-slate-200 font-medium">GitHub 源码</div>
              <div class="text-slate-500 text-sm">${s.repo}</div>
            </div>
            <i class="fa-solid fa-arrow-up-right-from-square text-slate-500 group-hover:text-indigo-400 transition"></i>
          </div>
        </a>
        <a href="index.html" class="p-4 rounded-lg bg-slate-800/40 border border-slate-700/30 hover:border-indigo-500/50 hover:bg-slate-800/60 transition group">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-slate-200 font-medium">浏览更多 Skills</div>
              <div class="text-slate-500 text-sm">回到首页</div>
            </div>
            <i class="fa-solid fa-arrow-left text-slate-500 group-hover:text-indigo-400 transition"></i>
          </div>
        </a>
      </div>
    </div>
  `;
}

// HTML 转义
function escapeHtml(s) {
  const div = document.createElement('div');
  div.textContent = s;
  return div.innerHTML;
}

// 复制代码
window.copyCode = function(btn) {
  const codeBlock = btn.closest('.code-block');
  const code = codeBlock.textContent.replace(/复制/g, '').trim();
  navigator.clipboard.writeText(code).then(() => {
    const orig = btn.textContent;
    btn.textContent = '✓ 已复制';
    btn.style.background = 'rgba(16,185,129,0.3)';
    btn.style.color = '#6ee7b7';
    setTimeout(() => {
      btn.textContent = orig;
      btn.style.background = '';
      btn.style.color = '';
    }, 1500);
  });
};

/* ==================== 初始化 ==================== */
(async function init() {
  try {
    const data = await loadData();
    if (document.getElementById('skillGrid')) {
      renderHome(data);
    } else if (document.getElementById('skillDetail')) {
      renderDetail(data);
    }
  } catch (e) {
    console.error('加载数据失败:', e);
    document.body.innerHTML = `
      <div class="min-h-screen flex items-center justify-center">
        <div class="text-center">
          <div class="text-6xl mb-4">😵</div>
          <h2 class="text-xl font-bold mb-2">加载失败</h2>
          <p class="text-slate-400">数据文件加载失败，请刷新重试</p>
        </div>
      </div>
    `;
  }
})();
