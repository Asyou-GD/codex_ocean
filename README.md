# Ocean Shallows Live

用于 macOS Codex 聊天窗口的动态浅海背景。选中 **Ocean Shallows Live** 后，海面会流动，鱼群会自动出现。背景不接收鼠标输入，可以照常选中文字和聊天。

| 文件 | 用途 |
| --- | --- |
| [Codex Dream Skin 1.5.21](app/Codex-Dream-Skin-1.5.21-macOS.zip) | 本机使用的原版 macOS 菜单栏 App，支持 Apple Silicon 和 Intel。 |
| [海景主题](themes/preset-ocean-shallows/) | 主题配置、配色和海床底图。 |
| [renderer-inject.js](assets/renderer-inject.js) | 与本机引擎相同的定制渲染文件，包含海面和鱼群的绘制代码。 |
| [dream-skin.css](assets/dream-skin.css) | 与本机引擎相同的样式文件，包含海景图层和窗口失焦时的背景修正。 |
| [海景定制技能](skills/codex-ocean-theme/SKILL.md) | 从单文件 HTML 预览开始调整效果，定稿后同步到聊天窗口，也可用于换机和回退。 |

## 在另一台 Mac 上使用

1. 解压 App，移入「应用程序」并打开。首次使用 Dream Skin 时，在菜单栏选择「安装 / 升级引擎…」，完成 1.5.21 引擎安装。
2. 在 Finder 中按 ⇧⌘G，前往 `~/.codex/codex-dream-skin-studio/assets/`。先把现有的 `renderer-inject.js` 和 `dream-skin.css` 备份到其他目录，再用仓库 `assets/` 中的同名文件替换。
3. 前往 `~/Library/Application Support/CodexDreamSkinStudio/themes/`，把仓库中的整个 `preset-ocean-shallows` 文件夹放进去。确认 `theme.json` 和 `background.webp` 都直接位于这个文件夹中。
4. 打开 Dream Skin 菜单，在「已保存的主题」中选择 **Ocean Shallows Live**。

App 压缩包保留了 1.5.21 的出厂资源。修复或重装引擎后，如果能看到海床却没有鱼群，请重新核对第 2 步的两个文件。

## 切换主题时的行为

两个渲染文件由所有主题共用。只有主题 ID 为 `preset-ocean-shallows` 时，引擎才会创建海景画布、绘制水面并生成鱼群。切换到其他主题时，海景动画和画布会一起移除。切换到其他 App 时保持海景可见的样式，也只在海景图层存在时生效。

通用的标题栏识别和浅色输入框样式会在其他匹配的主题中生效。

## 来源

菜单栏 App 来自 [Codex Dream Skin v1.5.21](https://github.com/Fei-Away/Codex-Dream-Skin/releases/tag/v1.5.21)。上游软件许可证见 [LICENSE](LICENSE)，随 App 分发的第三方素材说明位于应用包内的 `Contents/Resources/NOTICE.md`。
