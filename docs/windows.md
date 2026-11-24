# Windows 安装 Ocean Shallows Live

适用于 Windows 10 / 11 x64，使用 Microsoft Store 注册到当前用户的官方 Codex 桌面应用。安装分为三个部分，上游 Windows 引擎、本仓库的海景资源、托盘里的主题选择。

本流程对应 Dream Skin 1.5.21。海景 JavaScript 与 macOS 使用同一份文件，Windows 另有适配样式。当前已核对文件、加载入口和安装路径，Windows 的实际显示与启动结果在目标电脑上验证。

## 1. 下载并安装 Windows 引擎

下载 `CodexDreamSkin-Setup-v1.5.21.exe`，正常退出 Codex 后运行安装器。它按当前用户安装，附带 Node.js 运行时。安装完成后，开始菜单会出现 Codex Dream Skin 的启动和托盘入口。[上游 v1.5.21 下载](https://github.com/Fei-Away/Codex-Dream-Skin/releases/tag/v1.5.21)

该版本安装器的 SHA-256 为 `80e6fb4d6e0b96df84d5cd324d419c1cfc97aba6e4a4b62b83b29c3f1de62c42`。在安装器所在目录可以用 `Get-FileHash -Algorithm SHA256 .\CodexDreamSkin-Setup-v1.5.21.exe` 核对。[上游安装器与校验值](https://github.com/Fei-Away/Codex-Dream-Skin/releases/expanded_assets/v1.5.21)

确认本机已注册官方 Codex，可在 PowerShell 运行

```powershell
Get-AppxPackage -Name OpenAI.Codex |
    Select-Object Name, Version, PackageFullName
```

如果结果为空，先在当前 Windows 用户下安装并启动一次官方 Codex，再继续安装引擎。

## 2. 下载本仓库

在 GitHub 选择 **Code → Download ZIP** 并解压，也可以只按下面的结构下载四个海景文件。已有 Git 工作副本时，先更新到需要的版本。

解压后的仓库根目录应包含以下文件

```text
assets/
  renderer-inject.js
  windows/
    dream-skin.css
themes/
  preset-ocean-shallows/
    theme.json
    background.webp
```

## 3. 备份并复制海景资源

先右键任务栏托盘里的 Dream Skin 图标，选择「打开主题文件夹」。这个菜单打开的实际目录就是本机的主题库，先记下它的位置。

Windows 1.5.21 中，从这个主题文件夹返回上一层，进入 `engine → assets`，找到引擎正在使用的两份文件。引擎目录同层应有 `VERSION` 和 `scripts`。修改过安装或启动方式时，按下方的引擎核对方法确认实际位置。

找到两个目录后，退出 Dream Skin 托盘并正常关闭 Codex。把原有的两个引擎文件及同名海景目录备份到其他文件夹，再按下表复制。

| 仓库中的文件 | 复制到哪里 |
| --- | --- |
| `assets\renderer-inject.js` | 当前引擎的 `assets` 文件夹，替换同名文件 |
| `assets\windows\dream-skin.css` | 同一个引擎的 `assets` 文件夹，替换 `dream-skin.css` |
| `themes\preset-ocean-shallows\` 整个目录 | 软件菜单打开的主题文件夹 |

复制后，`theme.json` 和 `background.webp` 直接位于 `preset-ocean-shallows` 内。保留配置中的主题 ID `preset-ocean-shallows`，引擎用它启用海景。

JavaScript 和 Windows 样式使用同一仓库版本，并放在同一个实际运行的引擎中。不同电脑使用各自的软件目录。底图与配置作为受信任的已保存预设加载。[菜单示意与默认目录参考](../README.md#找到软件实际使用的文件夹)

<details>
<summary>需要 AI 核对实际引擎时</summary>

让 Dream Skin 托盘运行，在 PowerShell 查看相关进程的脚本位置

```powershell
Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -in @('powershell.exe', 'pwsh.exe', 'node.exe') -and
        $_.CommandLine -match '\\scripts\\(tray-dream-skin\.ps1|start-dream-skin\.ps1|injector\.mjs)'
    } |
    Select-Object ProcessId, CommandLine
```

脚本所在的 `scripts` 文件夹上一级是引擎目录。核对它与准备替换的 `assets` 位于同一引擎中，再退出托盘进行替换。

安装器快捷方式可能先启动 `setup-bootstrap.ps1`，再转到受管引擎。核对时使用实际运行的 Dream Skin 脚本路径。

</details>

## 4. 启用主题

1. 从开始菜单打开 **Codex Dream Skin** 和它的托盘入口。
2. 在托盘菜单的「已保存主题」里选择 **Ocean Shallows Live**。
3. 如果启动器要求重启正在运行的 Codex，保存当前输入后按提示操作。
4. 打开一条聊天，观察海面和鱼群是否自动运动。检查用户消息的透明描边、文字选择、输入框以及长消息的展开与收起。
5. 切换到另一应用，再回到 Codex，检查海景是否仍能正常显示。

海景仅播放动画。海面、鱼群的鼠标交互和快捷键不可用，聊天输入与原生控件照常使用。

## 5. 验证安装结果

以下命令确认选中的主题 ID，并调用已安装引擎自带的验证流程

```powershell
$themes = Read-Host '粘贴软件菜单实际打开的主题文件夹路径'
$state = Split-Path -Parent $themes
$engine = Read-Host '粘贴已经核对的引擎目录，其中应包含 VERSION 和 scripts'

Get-Content -LiteralPath (Join-Path $state 'active-theme\theme.json') -Raw |
    ConvertFrom-Json |
    Select-Object id, name

powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File "$engine\scripts\verify-dream-skin.ps1"
```

主题 ID 应为 `preset-ocean-shallows`。同时核对第 4 节的可见效果，记录验证脚本的退出码和失败时的具体错误。

重新安装或升级 Dream Skin 会重新部署引擎资源。升级后再次核对第 3 节的 JavaScript 和 Windows 样式。

## 排查具体问题

| 实际现象 | 检查或处理 |
| --- | --- |
| 找不到 `engine\assets` | 确认 Windows 安装器已经执行成功，查看安装日志。 |
| 托盘没有海景选项 | 检查主题目录是否多嵌套了一层，两个预设文件是否齐全，然后重新打开托盘菜单。 |
| 能看到海床，水面和鱼群不动 | 核对活动主题 ID，以及安装目录中的 JavaScript 是否与仓库同名文件一致。 |
| 消息框、标题栏或输入框样式异常 | 核对实际复制的是 `assets\windows\dream-skin.css`，并重新应用主题。 |
| 启动器报告找不到端点或 `access-denied` | 记录 Codex Store 版本和完整错误，按上游的启动兼容说明排查。部分官方客户端版本会限制该启动方式，实际错误决定是否能继续。[上游 Windows 兼容说明](https://github.com/Fei-Away/Codex-Dream-Skin/blob/v1.5.21/windows/README.md) |

日志位于软件主题文件夹的上一级，包括 `injector.log`、`injector-error.log` 和 `verify.log`。使用自定义引擎时，从其实际启动参数确认日志位置。反馈时只提供相关错误片段。

## 切换与回退

日常切换，在托盘的「已保存主题」中选择其他主题。恢复定制前的状态时，关闭 Codex 和托盘，将第 3 节备份的引擎文件与预设目录放回原处，再打开 Dream Skin。

恢复原生外观可使用 **Codex Dream Skin - Restore** 快捷方式，并完成它提示的重启。[上游恢复说明](https://github.com/Fei-Away/Codex-Dream-Skin/blob/v1.5.21/windows/README.md)

## 交给 AI 执行时

让 AI 在当前 Windows 电脑完成环境检查、下载、安装、资源复制、主题选择和验证，并报告完成到哪一步。Windows 10 x64 属于上游声明的运行范围，按本文检查本机 Store 包和引擎条件后执行。

本仓库的 Windows 入口是本文和 `assets/windows/dream-skin.css`。Mac 安装包对应另一平台；Windows 的引擎从第 1 节取得，海景资源按第 3 节复制。

成功结论应包括实际启用的主题 ID、验证结果和可见动画。遇到失败时，给出失败命令、退出码和错误，继续处理能恢复的问题。需要用户完成系统安装对话框或客户端重启时，说明具体操作，并在完成后接着验证。
