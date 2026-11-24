#!/usr/bin/env python3
"""Find a visible macOS Codex window and record it as an animated GIF."""

import argparse
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime


WINDOW_DISCOVERY = r"""
import AppKit
import CoreGraphics
import Foundation

let applications = NSWorkspace.shared.runningApplications.filter {
    $0.bundleIdentifier == "com.openai.codex"
}
let processIDs = Set(applications.map { $0.processIdentifier })
let windows = CGWindowListCopyWindowInfo(
    [.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID
) as? [[String: Any]] ?? []
var candidates = [[String: Int]]()
for window in windows {
    guard let processID = window[kCGWindowOwnerPID as String] as? Int32,
          processIDs.contains(processID),
          let layer = window[kCGWindowLayer as String] as? Int, layer == 0,
          let number = window[kCGWindowNumber as String] as? Int,
          let bounds = window[kCGWindowBounds as String] as? [String: Any],
          let width = bounds["Width"] as? Double,
          let height = bounds["Height"] as? Double,
          width >= 400, height >= 300 else { continue }
    candidates.append(["id": number, "width": Int(width), "height": Int(height)])
}
let data = try JSONSerialization.data(withJSONObject: candidates)
print(String(decoding: data, as: UTF8.self))
"""


def positive_number(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("请输入大于 0 的数值")
    return number


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="自动找到桌面上可见的 Codex 窗口，将实际窗口录成循环 GIF。"
    )
    parser.add_argument("--seconds", type=positive_number, default=6, help="录制秒数，默认 6")
    parser.add_argument("--fps", type=positive_number, default=12, help="动图帧率，默认 12")
    parser.add_argument("--width", type=int, help="输出宽度，默认保留录屏原生分辨率（含 Retina 像素）")
    parser.add_argument("--output", type=Path, help="输出 GIF 路径，默认保存到桌面")
    parser.add_argument("--window-id", type=int, help="多个窗口时指定要录制的 Codex 窗口编号")
    parser.add_argument("--list", action="store_true", help="列出可录制的 Codex 窗口")
    args = parser.parse_args()
    if args.width is not None and args.width < 160:
        parser.error("--width 至少为 160")
    return args


def discover_windows():
    result = subprocess.run(
        [shutil.which("swift"), "-"],
        input=WINDOW_DISCOVERY,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError("无法查询 Codex 窗口。请检查 Swift 命令行工具是否可用。\n" + result.stderr[-2000:])
    return json.loads(result.stdout)


def capture_window(window, directory, seconds):
    video = directory / "window.mov"
    result = subprocess.run(
        [
            "/usr/sbin/screencapture", "-x", "-v", "-V", f"{seconds:g}",
            "-l", str(window["id"]), str(video),
        ],
        capture_output=True,
        text=True,
        timeout=seconds + 30,
    )
    if result.returncode or not video.is_file() or video.stat().st_size == 0:
        raise RuntimeError(
            "窗口录制失败。请保持 Codex 窗口打开，并为运行脚本的应用开启 macOS 屏幕录制权限。\n"
            + result.stderr.strip()
        )
    return video


def encode_gif(ffmpeg, video, output, width, fps, window):
    resize = ""
    if width is not None:
        height = max(2, round(width * window["height"] / window["width"] / 2) * 2)
        resize = (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x0a283b,"
        )
    filters = (
        f"[0:v]fps={fps:g},{resize}"
        "split[a][b];[a]palettegen=max_colors=256:stats_mode=full[p];"
        "[b][p]paletteuse=dither=bayer:bayer_scale=3"
    )
    result = subprocess.run(
        [
            ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin",
            "-i", str(video),
            "-filter_complex", filters, "-fps_mode", "vfr",
            "-loop", "0", "-n", str(output),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError("GIF 编码失败。\n" + result.stderr[-2000:])


def main():
    args = parse_arguments()
    if platform.system() != "Darwin":
        raise RuntimeError("此脚本适用于 macOS。")
    if not shutil.which("swift"):
        raise RuntimeError("需要 Swift 命令行工具，可运行 xcode-select --install 安装。")
    windows = discover_windows()
    if args.list:
        print(json.dumps(windows, ensure_ascii=False, indent=2))
        return
    if not windows:
        raise RuntimeError("桌面上没有找到可见的 Codex 窗口，请先打开并显示 Codex。")
    window = windows[0]
    if args.window_id is not None:
        window = next((item for item in windows if item["id"] == args.window_id), None)
        if window is None:
            raise RuntimeError("指定编号不在可见 Codex 窗口中，可用 --list 查看。")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("需要 FFmpeg。已安装 Homebrew 时可运行 brew install ffmpeg。")
    output = args.output
    if output is None:
        filename = "codex-ocean-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".gif"
        output = Path.home() / "Desktop" / filename
    output = output.expanduser().resolve()
    if output.suffix.lower() != ".gif":
        raise RuntimeError("--output 请使用 .gif 扩展名。")
    if output.exists():
        raise RuntimeError("输出文件已存在，请换一个文件名。")
    output.parent.mkdir(parents=True, exist_ok=True)
    print(
        f"已找到 Codex 窗口 {window['id']}，{window['width']}×{window['height']}。"
        f"录制 {args.seconds:g} 秒，输出 {args.fps:g} FPS。",
        flush=True,
    )
    with tempfile.TemporaryDirectory(prefix=".codex-gif-", dir=output.parent) as temporary:
        directory = Path(temporary)
        video = capture_window(window, directory, args.seconds)
        print("窗口录制完成，正在生成 GIF…", flush=True)
        encoded = directory / "result.gif"
        encode_gif(ffmpeg, video, encoded, args.width, args.fps, window)
        # Publish the complete GIF without overwriting an existing destination.
        os.link(encoded, output)
    print(f"已保存 {output}（{output.stat().st_size / 1024 / 1024:.1f} MB）")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n录制已停止。", file=sys.stderr)
        sys.exit(130)
    except (RuntimeError, OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
