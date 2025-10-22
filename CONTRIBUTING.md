# 贡献指南 (Contributing Guide)

感谢您对 ClassTop 项目的关注！我们欢迎任何形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复或新功能
- 🌐 翻译文档

## 📋 目录

- [行为准则](#行为准则)
- [开始之前](#开始之前)
- [提交 Issue](#提交-issue)
- [提交 Pull Request](#提交-pull-request)
- [代码规范](#代码规范)
- [提交信息规范](#提交信息规范)
- [开发工作流](#开发工作流)
- [测试要求](#测试要求)
- [社区互动](#社区互动)

## 📜 行为准则

本项目遵循开源社区的基本行为准则：

- ✅ 尊重所有贡献者
- ✅ 接受建设性批评
- ✅ 专注于对项目最有利的事情
- ✅ 对新手友好，乐于分享知识
- ❌ 不使用攻击性语言或人身攻击
- ❌ 不发布与项目无关的内容

## 🚀 开始之前

### 环境准备

请确保您已经按照以下文档搭建好开发环境：

- **Windows**: [README.md](./README.md#windows-开发环境)
- **Linux**: [docs/LINUX_SETUP.md](./docs/LINUX_SETUP.md)
- **macOS**: [docs/MACOS_SETUP.md](./docs/MACOS_SETUP.md)

### IDE 配置（推荐）

- **VSCode**: [docs/VSCODE_SETUP.md](./docs/VSCODE_SETUP.md) - 全平台推荐
- **Xcode**: [docs/XCODE_SETUP.md](./docs/XCODE_SETUP.md) - macOS 调试
- **Visual Studio**: [docs/VISUAL_STUDIO_SETUP.md](./docs/VISUAL_STUDIO_SETUP.md) - Windows 调试

### 熟悉项目

在开始贡献之前，建议您：

1. 阅读 [README.md](./README.md) 了解项目功能
2. 阅读 [CLAUDE.md](./CLAUDE.md) 了解项目架构
3. 运行 `npm run tauri dev` 体验应用
4. 浏览现有的 Issues 和 Pull Requests

## 🐛 提交 Issue

### Bug 报告

发现 Bug 时，请提交 Issue 并包含以下信息：

```markdown
**Bug 描述**
简洁明了地描述 Bug

**复现步骤**
1. 执行 '...'
2. 点击 '...'
3. 滚动到 '...'
4. 出现错误

**期望行为**
描述您期望发生的事情

**实际行为**
描述实际发生的事情

**截图**
如有可能，添加截图说明问题

**环境信息**
- 操作系统: [如 Windows 11]
- 应用版本: [如 0.1.0]
- Python 版本: [如 3.10.0]
- Node.js 版本: [如 18.0.0]

**额外信息**
其他有助于理解问题的信息
```

### 功能建议

提出新功能时，请提交 Issue 并包含：

- 🎯 **问题描述**: 当前缺少什么功能？为什么需要？
- 💡 **建议方案**: 您建议如何实现？
- 🔄 **替代方案**: 是否考虑过其他解决方案？
- 📊 **影响范围**: 这个功能会影响哪些模块？

## 🔀 提交 Pull Request

### PR 流程

1. **Fork 仓库**
   ```bash
   # 在 GitHub 上点击 Fork 按钮
   git clone https://github.com/YOUR_USERNAME/classtop.git
   cd classtop
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **进行开发**
   - 编写代码
   - 遵循代码规范
   - 添加必要的测试
   - 更新相关文档

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 填写 PR 模板
   - 等待审核

### PR 要求

✅ **必须满足的条件**:

- [ ] 代码通过所有 CI 检查
- [ ] 遵循项目代码规范
- [ ] 更新了相关文档
- [ ] 添加了必要的测试（如适用）
- [ ] 提交信息符合规范
- [ ] 没有引入新的警告或错误
- [ ] 功能完整，无半成品代码

⚠️ **常见问题**:

- ❌ 不要在 PR 中包含无关的文件更改
- ❌ 不要提交包含个人配置的文件（`.env`, `.vscode/settings.json` 等）
- ❌ 不要提交构建产物（`dist/`, `target/`, `node_modules/` 等）
- ❌ 不要修改 `.gitignore` 除非有正当理由
- ❌ **不要提交测试性质的 PR 到 master 分支**（见下方 [PR #9 社死警示](#-pr-9-社死警示)）

### PR 模板

提交 PR 时，请使用以下模板：

```markdown
## 📝 变更说明

简要描述此 PR 的目的和内容

## 🔗 关联 Issue

Closes #issue_number

## 📊 变更类型

- [ ] 🐛 Bug 修复
- [ ] ✨ 新功能
- [ ] 📝 文档更新
- [ ] 🎨 样式/UI 改进
- [ ] ♻️ 代码重构
- [ ] ⚡️ 性能优化
- [ ] 🔧 配置/构建变更

## 🧪 测试

描述如何测试这些变更：

1. 测试步骤 1
2. 测试步骤 2
3. ...

## 📷 截图（如适用）

添加截图展示变更效果

## ✅ 检查清单

- [ ] 代码遵循项目规范
- [ ] 已进行自测
- [ ] 已更新相关文档
- [ ] 已添加必要注释
- [ ] 通过了所有 CI 检查
```

## 📐 代码规范

### Python 代码规范

**遵循 PEP 8 标准**:

```python
# 好的示例
def calculate_week_number(semester_start_date: str) -> int:
    """
    计算当前周数

    Args:
        semester_start_date: 学期开始日期 (YYYY-MM-DD)

    Returns:
        当前周数
    """
    from datetime import datetime

    start_date = datetime.fromisoformat(semester_start_date)
    today = datetime.now()
    days_diff = (today - start_date).days
    return (days_diff // 7) + 1
```

**关键点**:
- 使用 4 个空格缩进
- 函数名使用 `snake_case`
- 类名使用 `PascalCase`
- 添加类型提示（Type Hints）
- 编写清晰的文档字符串

### JavaScript/Vue 代码规范

**遵循 Vue 3 + Composition API 最佳实践**:

```vue
<script setup>
import { ref, onMounted, computed } from 'vue'

// 好的示例
const currentWeek = ref(1)
const semesterStartDate = ref('')

const weekNumber = computed(() => {
  if (!semesterStartDate.value) return currentWeek.value
  return calculateWeekFromDate(semesterStartDate.value)
})

onMounted(async () => {
  await loadSettings()
})
</script>
```

**关键点**:
- 使用 `<script setup>` 语法
- 使用 Composition API
- 变量名使用 `camelCase`
- 组件名使用 `PascalCase`
- 适当添加注释

### Rust 代码规范

**运行代码检查**:

```bash
# 格式检查
cargo fmt --manifest-path=src-tauri/Cargo.toml --all -- --check

# Linting（严格模式）
cargo clippy --manifest-path=src-tauri/Cargo.toml --all-targets --all-features -- -D warnings

# 构建验证
cargo build --manifest-path=src-tauri/Cargo.toml --release --features pytauri/standalone
```

## 📝 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 提交类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构（既不是新功能也不是修复）
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链相关

### 提交格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 示例

```bash
# 新功能
git commit -m "feat(schedule): add week number auto-calculation"

# Bug 修复
git commit -m "fix(topbar): fix progress bar not updating"

# 文档
git commit -m "docs: update CONTRIBUTING.md with PR guidelines"

# 重构
git commit -m "refactor(db): simplify schedule query logic"
```

## 🔄 开发工作流

### 本地开发

```bash
# 1. 拉取最新代码
git pull origin master

# 2. 创建功能分支
git checkout -b feature/my-feature

# 3. 安装依赖
npm install
uv pip install -e src-tauri

# 4. 启动开发服务器
npm run tauri dev

# 5. 进行开发...

# 6. 运行检查
cargo fmt --manifest-path=src-tauri/Cargo.toml --all -- --check
cargo clippy --manifest-path=src-tauri/Cargo.toml --all-targets -- -D warnings

# 7. 提交代码
git add .
git commit -m "feat: add my feature"

# 8. 推送分支
git push origin feature/my-feature
```

### 代码审查

提交 PR 后：

1. **自动检查**: GitHub Actions 会自动运行 CI 检查
2. **代码审查**: 维护者会审查您的代码
3. **讨论修改**: 根据反馈进行修改
4. **合并**: 通过审查后，维护者会合并 PR

## 🧪 测试要求

### 手动测试

在提交 PR 前，请确保：

- ✅ 应用可以正常启动
- ✅ 主窗口和 TopBar 窗口都能正常显示
- ✅ 您修改的功能可以正常工作
- ✅ 没有引入新的错误或警告
- ✅ 在目标平台上测试过（Windows/Linux/macOS）

### 自动化测试（未来计划）

目前项目暂无自动化测试，欢迎贡献测试相关的 PR：

- 单元测试（Python: pytest, JavaScript: Vitest）
- 集成测试
- E2E 测试

## 🤝 社区互动

### 获取帮助

- 📖 查看 [文档](./docs/)
- 💬 提交 Issue 提问
- 📧 发送邮件至：<hwllochen@qq.com>

### 贡献者列表

感谢所有为 ClassTop 做出贡献的开发者！

<!--
Contributors will be automatically added here
贡献者将会自动添加在这里
-->

---

## 🚨 PR #9 社死警示

> **⚠️ 重要提醒：请勿提交测试性质的 PR！**

为了让新贡献者吸取教训（😅），这里记录一个真实案例（而且突然冒出来一个李火旺怪惊悚的）：

### 📜 事件回顾

**PR #9**: "docs：PR Test" by @lihuowang17

- 📅 创建时间：2025-10-21 10:11:16
- ⏰ 合并时间：2025-10-21 10:34:32（存活 23 分钟）
- 🔄 结局：被 PR #10 立即 revert

**Git 历史**:
```
* 006146d Remove Claude Code github（a.k.a is anyrouter not support）
*   3f4884b Merge pull request #10 from Zixiao-System/revert-9-master
|\
| * 4547f2a Revert "docs：PR Test"
|/
*   7ae3678 Merge pull request #9 from lihuowang17/master  👈 社死现场
|\
| * d842df4 docs：PR Test
```

### 🎓 教训总结

1. **❌ 不要在 master 分支提交测试 PR**
   - 测试应该在自己的 Fork 仓库进行
   - 可以创建测试分支，但不要合并到 master

2. **❌ 不要提交无意义的内容**
   - PR 描述是 "Test PR Workflow" → 这不是有效贡献
   - 每个 PR 都应该解决实际问题

3. **✅ 正确的测试方式**
   ```bash
   # 在自己的 Fork 仓库测试
   git clone https://github.com/YOUR_USERNAME/classtop.git
   git checkout -b test/workflow-test
   # 进行测试...
   git push origin test/workflow-test
   # 在自己的仓库创建 PR 测试
   ```

4. **✅ 首次贡献的正确姿势**
   - 先从小改动开始（修正拼写错误、改进文档等）
   - 提交 PR 前仔细检查变更内容
   - 阅读 CONTRIBUTING.md（没错，就是本文档！）
   - 确保 PR 有明确的目的和价值

### 💬 社区建议

如果您想：
- 🧪 测试 PR 流程 → 在自己的 Fork 仓库测试
- 📚 学习如何贡献 → 阅读本文档和现有 PR
- 🆘 需要帮助 → 提交 Issue 询问
- 💡 有好想法 → 先提交 Issue 讨论，再动手开发

### 🎉 给 @lihuowang17 的鼓励

虽然 PR #9 被 revert 了，但我们依然：
- 🙏 感谢您对项目的兴趣
- 🌟 欢迎您继续贡献有价值的 PR
- 💪 相信您会成为优秀的贡献者

**记住**：每个伟大的开发者都经历过"社死时刻"，关键是从中学习并成长！🚀

---

## 📞 联系方式

- 💬 GitHub Issues: [提交 Issue](https://github.com/Zixiao-System/classtop/issues)
- 📧 Email: <hwllochen@qq.com>
- 🔗 Gitee (镜像): [Gitee Issues](https://gitee.com/HwlloChen/classtop/issues)

---

**再次感谢您的贡献！让我们一起让 ClassTop 变得更好！** ❤️

*Made with ❤️ by Classtop Team*
