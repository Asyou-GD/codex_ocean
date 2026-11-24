---
name: codex-ocean-theme
description: 在 macOS 上预览、定制或迁移 Codex 的 Ocean Shallows Live 动态海景主题。适用于调整水面、自动鱼群、聊天气泡透明度，以及在另一台 Mac 恢复已定稿的主题。
---

# 定制和迁移 Codex 海景

**先交付可在浏览器打开的 HTML，让用户改到满意，再把定稿应用到 Codex。** 第一次展示预览时就说明，Codex 里的海景只播放动画。水面和鱼群会自动运动，点水、拖鱼和海景快捷键都不可用。鼠标和键盘留给聊天、文字选择和「显示更多」。如果只是把已经定稿的版本搬到新 Mac，直接走换机流程。

## 先预览，再定稿

1. 找到 `codex_ocean` 工作副本，读取当前的 `themes/preset-ocean-shallows/theme.json`、`background.webp` 和 `assets/` 下的两份渲染文件。新建或复用工作区中的单文件 HTML 作为设计稿，把需要的样式、动画和图片内嵌，使文件可直接在本地浏览器打开。
2. 在预览里用示例对话显示用户气泡、回复和输入框，让用户能同时看清水色、鱼群和文字。用自动播放演示最终背景；预览工具若带调色或调速控件，把它们留在浏览器。提供 HTML 本地路径，让用户既能直接编辑，也能逐轮描述想改的地方。
3. 每轮更新同一份 HTML，打开核对实际效果。用户确认“按这个版本应用到 Codex”后，再把最终差异移入下表对应的文件。编辑 HTML 本身只会改变预览。

| 想改的效果 | 将定稿改到哪里 |
| --- | --- |
| 沙滩位置、海床和礁石 | 更新 `themes/preset-ocean-shallows/background.webp`。换图名时同步修改 `theme.json` 的 `image`。 |
| 聊天文字、强调色和面板配色 | 编辑同目录 `theme.json` 的 `colors.text`、`colors.accent`、`colors.panel` 等字段。保留主题 ID `preset-ocean-shallows`，海景动画用它识别当前主题。 |
| 水面节奏、鱼群数量或游姿 | 将预览采用的绘制参数移到 `assets/renderer-inject.js` 的海景代码。例如，`drawSchools` 中的 `perSchool` 控制每群小鱼的数量，`swimCadences` 控制大型生物的动作节奏。 |
| 自己发出的消息有多透明 | 在 `assets/dream-skin.css` 的海景样式里调 `--ocean-user-bubble-alpha`。取 `0` 时气泡底色完全透明，可调到 `0.15` 保留一层淡底。只改变底色的 alpha，保持文字、链接和按钮清晰。 |

两个渲染文件由各主题共用。新增海景样式要限定在 `body[data-ocean-scene]` 下，动画沿用现有的主题 ID 判断和切走时的清理逻辑。使用本地预览和公开示例文案复核效果即可。

## 应用到当前 Mac 或迁移到新 Mac

1. 在目标 Mac 上取得用户选定的仓库版本。首次安装时，解压 `app/Codex-Dream-Skin-1.5.21-macOS.zip`，把 **Codex Dream Skin.app** 移到「应用程序」并打开，再在菜单栏选择「安装 / 升级引擎…」。仓库配套的是 1.5.21。[私有仓库](https://github.com/Asyou-GD/codex_ocean)
2. 在 Finder 中按 ⇧⌘G 打开下表中的目标目录。首次安装或迁移时复制全部三项；在同一台 Mac 上继续 DIY 时，只同步这轮定稿改过的项目。替换前将已有同名文件和主题目录备份到目标目录之外，供回退使用。

   | 从仓库复制 | 目标位置 |
   | --- | --- |
   | `themes/preset-ocean-shallows/` 整个目录 | `~/Library/Application Support/CodexDreamSkinStudio/themes/preset-ocean-shallows/`，其中直接包含 `theme.json`、`background.webp` |
   | `assets/renderer-inject.js` | `~/.codex/codex-dream-skin-studio/assets/renderer-inject.js` |
   | `assets/dream-skin.css` | `~/.codex/codex-dream-skin-studio/assets/dream-skin.css` |

3. 初次启用或更新了主题目录里的图片、配色后，在 Dream Skin 菜单的「已保存的主题」中选择 **Ocean Shallows Live**。海景已运行时，安装目录中的 JS 和 CSS 保存后会自动刷新；需要手动刷新时，可选「重新应用皮肤」。打开已有聊天，观察水面和鱼群是否运动，检查亮色海面上的文字是否可读，以及长消息能否展开和收起。切到另一 App，确认露出的 Codex 区域仍能看到海景。
4. 日常更换背景，直接在「已保存的主题」里选择目标主题。要撤销文件层面的定制，先切走海景，再恢复第 2 步备份的资源和原主题目录，并重新选择原主题。若这台 Mac 原先没有海景目录，回退时可将新增目录移到主题库之外。

要在新 Mac 继续用本技能，把仓库的 `skills/codex-ocean-theme/` 整个复制到 `~/.codex/skills/`（如自定义了 `CODEX_HOME`，使用其下的 `skills/`）。在新会话里输入 `$codex-ocean-theme 把每群小鱼减半，先给我看 HTML`，即可从本机这版接着改。
