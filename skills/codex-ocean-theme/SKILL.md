---
name: codex-ocean-theme
description: 在 macOS 或 Windows 上安装、预览、定制或迁移 Codex 的 Ocean Shallows Live 动态海景主题。适用于部署已有海景、调整水面和消息样式，以及在另一台电脑恢复定稿。
---

# 定制和迁移 Codex 海景

**先交付可在浏览器打开的 HTML，让用户改到满意，再把定稿应用到 Codex。** 第一次展示预览时说明所选版本的交互范围：v1.1.0 支持消息框外点海豚起跳、落水水花和点水涟漪，水面和鱼群也会自动运动。消息框、输入框、侧栏、标题栏、按钮、链接和浮层内的操作优先交给 Codex。拖动、选字、滚动与键盘保留原生行为；拖鱼和海景快捷键未实现。旧版 v1.0.1 只播放动画。如果只是把已经定稿的版本搬到新电脑，直接走对应系统的换机流程。

## 根据当前电脑选择流程

用户请求安装或迁移已有版本时，先确认当前系统和仓库路径，直接进入对应平台的安装流程。Windows 从上游安装 Windows 引擎，再加载本仓库的共用 JavaScript、Windows 样式和预设；macOS 使用仓库里的 App 和 macOS 样式。

先从软件的「打开主题文件夹」菜单确定本机实际主题库，再定位当前运行的引擎。默认目录仅用于查找参考。复制后核对主题 ID、图片文件名，以及两份引擎资源的版本和所在目录。[菜单截图与引擎定位](https://github.com/Asyou-GD/codex_ocean#找到软件实际使用的文件夹)

开始安装后，连续完成环境检查、安装、复制、主题选择和验证。结果依据本机执行记录及显示效果。遇到失败时给出具体命令、退出码和错误，并处理可以恢复的问题。

## 先预览，再定稿

1. 找到 `codex_ocean` 工作副本，读取当前的 `themes/preset-ocean-shallows/theme.json`、`background.webp` 和 `assets/` 下的两份渲染文件。新建或复用工作区中的单文件 HTML 作为设计稿，把需要的样式、动画和图片内嵌，使文件可直接在本地浏览器打开。
2. 在预览里用示例对话显示用户气泡、回复和输入框，让用户能同时看清水色、鱼群和文字。演示自动播放和所选版本支持的点击效果，并让示例消息与输入框覆盖海豚以检查点击保护；预览工具若带调色或调速控件，把它们留在浏览器。提供 HTML 本地路径，让用户既能直接编辑，也能逐轮描述想改的地方。
3. 每轮更新同一份 HTML，打开核对实际效果。用户确认“按这个版本应用到 Codex”后，再把最终差异移入下表对应的文件。编辑 HTML 本身只会改变预览。

| 想改的效果 | 将定稿改到哪里 |
| --- | --- |
| 沙滩位置、海床和礁石 | 更新 `themes/preset-ocean-shallows/background.webp`。换图名时同步修改 `theme.json` 的 `image`。 |
| 聊天文字、强调色和面板配色 | 编辑同目录 `theme.json` 的 `colors.text`、`colors.accent`、`colors.panel` 等字段。保留主题 ID `preset-ocean-shallows`，海景动画用它识别当前主题。 |
| 水面节奏、鱼群数量或游姿 | 将预览采用的绘制参数移到 `assets/renderer-inject.js` 的海景代码。例如，`drawSchools` 中的 `perSchool` 控制每群小鱼的数量，`swimCadences` 控制大型生物的动作节奏。 |
| 点击和起跳效果 | 在共享海景代码中调整 `leapDuration`、`drawDolphins` 的抬升幅度、`splashAt` 的水花和 `disturb` 的涟漪。保留消息与控件保护、拖动取消、被动监听和切走主题时的清理。 |
| 粉色海豚的队形和大小 | 调整 `dolphinPod` 中的 `side`、`along` 和 `size`，`dolphinPath` 控制整群路线。保持整群游出画面后才重复路线。 |
| 自己发出的消息有多透明 | 在目标平台的样式文件中调 `--ocean-user-bubble-alpha`。macOS 使用 `assets/dream-skin.css`，Windows 使用 `assets/windows/dream-skin.css`。取 `0` 时气泡底色完全透明，可调到 `0.15` 保留一层淡底。保留消息文字、链接、按钮和现有描边。 |

两个渲染文件由各主题共用。新增海景样式要限定在 `body[data-ocean-scene]` 下，动画沿用现有的主题 ID 判断和切走时的清理逻辑。使用本地预览和公开示例文案复核效果即可。

## 应用到 Windows 或迁移到新 Windows 电脑

完整步骤见工作副本中的 `docs/windows.md`。[Windows 安装文档](https://github.com/Asyou-GD/codex_ocean/blob/main/docs/windows.md)

1. 用 `Get-AppxPackage -Name OpenAI.Codex` 确认当前用户已注册官方 Store 包。Windows 10 / 11 x64 使用上游 `CodexDreamSkin-Setup-v1.5.21.exe` 安装引擎，安装器附带 Node.js。已有匹配引擎时复用当前安装。
2. 右键 Dream Skin 托盘图标，选择「打开主题文件夹」，记下软件实际打开的目录。Windows 1.5.21 的引擎位于其上一级的 `engine` 中；自定义启动时按 `docs/windows.md` 核对实际脚本位置。找到目录后关闭 Codex 和托盘，备份待替换的文件，再按下表同步。

   | 仓库来源 | Windows 目标 |
   | --- | --- |
   | `assets/renderer-inject.js` | 当前引擎的 `assets/renderer-inject.js` |
   | `assets/windows/dream-skin.css` | 同一引擎的 `assets/dream-skin.css` |
   | `themes/preset-ocean-shallows/` | 软件菜单打开的主题文件夹内 |

3. 从开始菜单打开 Codex Dream Skin 和托盘，在「已保存主题」里选择 **Ocean Shallows Live**。按启动器提示处理客户端重启。
4. 在主题文件夹上一级的 `active-theme/theme.json` 中核对 ID 为 `preset-ocean-shallows`，运行已核对引擎内的 `scripts/verify-dream-skin.ps1`，并检查水面、鱼群、消息描边、文字选择、输入框及长消息展开。验证消息框外点海豚起跳、落水涟漪，消息框和输入框内点击不触发海景。
5. 启动失败时记录 Store 版本、退出码及 `injector-error.log` 中的相关错误。根据实际失败判断兼容性。当前仓库已核对 Windows 资源与路径，Windows 实机结果由这次安装验证得出。

回退时关闭 Codex 和托盘，恢复备份的引擎文件和预设，重新打开并选择原主题。日常更换背景直接使用托盘的「已保存主题」。

## 应用到当前 Mac 或迁移到新 Mac

1. 在目标 Mac 上取得用户选定的仓库版本。首次安装时，解压 `app/Codex-Dream-Skin-1.5.21-macOS.zip`，把 **Codex Dream Skin.app** 移到「应用程序」并打开，再在菜单栏选择「安装 / 升级引擎…」。仓库配套的是 1.5.21。[项目仓库](https://github.com/Asyou-GD/codex_ocean)
2. 点击菜单栏 Dream Skin 图标，通过「主题 → 打开主题文件夹」找到本机主题库，并按 README 的引擎定位说明找到当前引擎。首次安装或迁移时复制全部三项；在同一台 Mac 上继续 DIY 时，只同步这轮定稿改过的项目。替换前将已有同名文件和主题目录备份到目标目录之外，供回退使用。

   | 从仓库复制 | 目标位置 |
   | --- | --- |
   | `themes/preset-ocean-shallows/` 整个目录 | 软件菜单打开的主题文件夹内，预设中直接包含 `theme.json`、`background.webp` |
   | `assets/renderer-inject.js` | 当前引擎的 `assets/renderer-inject.js` |
   | `assets/dream-skin.css` | 同一引擎的 `assets/dream-skin.css` |

3. 初次启用或更新了主题目录里的图片、配色后，在 Dream Skin 菜单的「已保存的主题」中选择 **Ocean Shallows Live**。海景已运行时，安装目录中的 JS 和 CSS 保存后会自动刷新；需要手动刷新时，可选「重新应用皮肤」。打开已有聊天，观察水面和鱼群是否运动，检查亮色海面上的文字是否可读，以及长消息能否展开和收起。验证消息框外点海豚起跳与落水涟漪，消息框、输入框内点击及拖动选字不触发海景。切到另一 App，确认露出的 Codex 区域仍能看到海景。
4. 日常更换背景，直接在「已保存的主题」里选择目标主题。要撤销文件层面的定制，先切走海景，再恢复第 2 步备份的资源和原主题目录，并重新选择原主题。若这台 Mac 原先没有海景目录，回退时可将新增目录移到主题库之外。

## 在另一台电脑继续使用本技能

把仓库的 `skills/codex-ocean-theme/` 整个复制到技能目录。macOS 默认是 `~/.codex/skills/`，Windows 默认是 `%USERPROFILE%\.codex\skills\`。自定义了 `CODEX_HOME` 时，使用其下的 `skills` 目录。

在新会话里输入 `$codex-ocean-theme 在这台 Windows 上安装仓库里的海景并验证`，或 `$codex-ocean-theme 把每群小鱼减半，先给我看 HTML`。
