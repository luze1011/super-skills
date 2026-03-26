#!/usr/bin/env python3
"""
PyAutoGUI 桌面控制脚本
提供鼠标、键盘、屏幕操作的封装函数
"""

import pyautogui
import sys
import json
import time
from typing import Optional, Tuple, List
from datetime import datetime

# 安全设置：鼠标移到屏幕角落会触发异常
pyautogui.FAILSAFE = True

# 默认延迟
DEFAULT_DURATION = 0.3
DEFAULT_INTERVAL = 0.05

def output_result(success: bool, command: str, data: dict = None, error: str = None):
    """输出 JSON 格式的结果"""
    result = {
        "success": success,
        "command": command,
        "timestamp": datetime.now().isoformat(),
        "data": data or {},
        "error": error
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

# ==================== 鼠标控制 ====================

def mouse_move(x: int, y: int, duration: float = DEFAULT_DURATION):
    """移动鼠标到指定坐标"""
    try:
        pyautogui.moveTo(x, y, duration=duration)
        output_result(True, "mouse.move", {"x": x, "y": y, "duration": duration})
    except Exception as e:
        output_result(False, "mouse.move", error=str(e))

def mouse_click(x: Optional[int] = None, y: Optional[int] = None, 
                button: str = 'left', clicks: int = 1):
    """点击鼠标"""
    try:
        if x is not None and y is not None:
            pyautogui.click(x, y, button=button, clicks=clicks)
        else:
            pyautogui.click(button=button, clicks=clicks)
        output_result(True, "mouse.click", {"x": x, "y": y, "button": button, "clicks": clicks})
    except Exception as e:
        output_result(False, "mouse.click", error=str(e))

def mouse_double_click(x: Optional[int] = None, y: Optional[int] = None):
    """双击鼠标"""
    mouse_click(x, y, clicks=2)

def mouse_right_click(x: Optional[int] = None, y: Optional[int] = None):
    """右键点击"""
    mouse_click(x, y, button='right')

def mouse_drag(x: int, y: int, duration: float = 1.0, button: str = 'left'):
    """拖拽鼠标"""
    try:
        pyautogui.dragTo(x, y, duration=duration, button=button)
        output_result(True, "mouse.drag", {"x": x, "y": y, "duration": duration})
    except Exception as e:
        output_result(False, "mouse.drag", error=str(e))

def mouse_scroll(clicks: int, x: Optional[int] = None, y: Optional[int] = None):
    """滚轮滚动（正数向上，负数向下）"""
    try:
        if x is not None and y is not None:
            pyautogui.scroll(clicks, x, y)
        else:
            pyautogui.scroll(clicks)
        output_result(True, "mouse.scroll", {"clicks": clicks, "x": x, "y": y})
    except Exception as e:
        output_result(False, "mouse.scroll", error=str(e))

def mouse_position():
    """获取鼠标当前位置"""
    try:
        x, y = pyautogui.position()
        output_result(True, "mouse.position", {"x": x, "y": y})
    except Exception as e:
        output_result(False, "mouse.position", error=str(e))

# ==================== 键盘控制 ====================

def keyboard_write(text: str, interval: float = DEFAULT_INTERVAL):
    """输入文本"""
    try:
        pyautogui.write(text, interval=interval)
        output_result(True, "keyboard.write", {"text": text, "length": len(text)})
    except Exception as e:
        output_result(False, "keyboard.write", error=str(e))

def keyboard_press(key: str, presses: int = 1, interval: float = 0.1):
    """按下按键"""
    try:
        pyautogui.press(key, presses=presses, interval=interval)
        output_result(True, "keyboard.press", {"key": key, "presses": presses})
    except Exception as e:
        output_result(False, "keyboard.press", error=str(e))

def keyboard_hotkey(*keys: str):
    """按下组合键"""
    try:
        pyautogui.hotkey(*keys)
        output_result(True, "keyboard.hotkey", {"keys": list(keys)})
    except Exception as e:
        output_result(False, "keyboard.hotkey", error=str(e))

def keyboard_keydown(key: str):
    """按下按键不释放"""
    try:
        pyautogui.keyDown(key)
        output_result(True, "keyboard.keydown", {"key": key})
    except Exception as e:
        output_result(False, "keyboard.keydown", error=str(e))

def keyboard_keyup(key: str):
    """释放按键"""
    try:
        pyautogui.keyUp(key)
        output_result(True, "keyboard.keyup", {"key": key})
    except Exception as e:
        output_result(False, "keyboard.keyup", error=str(e))

# ==================== 屏幕操作 ====================

def screen_screenshot(filename: str, region: Optional[Tuple[int, int, int, int]] = None):
    """截屏"""
    try:
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        output_result(True, "screen.screenshot", {"filename": filename, "region": region})
    except Exception as e:
        output_result(False, "screen.screenshot", error=str(e))

def screen_size():
    """获取屏幕尺寸"""
    try:
        width, height = pyautogui.size()
        output_result(True, "screen.size", {"width": width, "height": height})
    except Exception as e:
        output_result(False, "screen.size", error=str(e))

def screen_locate(image_path: str, confidence: float = 0.9):
    """定位图像"""
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            output_result(True, "screen.locate", {
                "found": True,
                "left": location.left,
                "top": location.top,
                "width": location.width,
                "height": location.height
            })
        else:
            output_result(True, "screen.locate", {"found": False})
    except Exception as e:
        output_result(False, "screen.locate", error=str(e))

def screen_locate_center(image_path: str, confidence: float = 0.9):
    """定位图像中心点"""
    try:
        center = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if center:
            output_result(True, "screen.locate_center", {"found": True, "x": center.x, "y": center.y})
        else:
            output_result(True, "screen.locate_center", {"found": False})
    except Exception as e:
        output_result(False, "screen.locate_center", error=str(e))

def screen_pixel(x: int, y: int):
    """获取像素颜色"""
    try:
        color = pyautogui.pixel(x, y)
        output_result(True, "screen.pixel", {"x": x, "y": y, "rgb": color})
    except Exception as e:
        output_result(False, "screen.pixel", error=str(e))

# ==================== 工具函数 ====================

def wait(seconds: float):
    """等待"""
    time.sleep(seconds)
    output_result(True, "wait", {"seconds": seconds})

def alert(text: str, title: str = "Alert"):
    """显示警告框"""
    pyautogui.alert(text, title)
    output_result(True, "alert", {"text": text, "title": title})

def confirm(text: str, title: str = "Confirm") -> bool:
    """显示确认框"""
    result = pyautogui.confirm(text, title)
    output_result(True, "confirm", {"text": text, "response": result})
    return result == "OK"

def prompt(text: str, title: str = "Prompt", default: str = "") -> str:
    """显示输入框"""
    result = pyautogui.prompt(text, title, default)
    output_result(True, "prompt", {"text": text, "response": result})
    return result or ""

# ==================== 命令行接口 ====================

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python pyautogui-control.py <command> [args...]")
        print("Commands: move, click, double-click, right-click, drag, scroll, position")
        print("          write, press, hotkey, keydown, keyup")
        print("          screenshot, size, locate, locate-center, pixel")
        print("          wait, alert, confirm, prompt")
        sys.exit(1)
    
    command = sys.argv[1].lower().replace('-', '_')
    args = sys.argv[2:]
    
    # 鼠标命令
    if command == 'move':
        mouse_move(int(args[0]), int(args[1]), float(args[2]) if len(args) > 2 else DEFAULT_DURATION)
    elif command == 'click':
        mouse_click(int(args[0]) if args else None, int(args[1]) if len(args) > 1 else None)
    elif command == 'double_click':
        mouse_double_click(int(args[0]) if args else None, int(args[1]) if len(args) > 1 else None)
    elif command == 'right_click':
        mouse_right_click(int(args[0]) if args else None, int(args[1]) if len(args) > 1 else None)
    elif command == 'drag':
        mouse_drag(int(args[0]), int(args[1]), float(args[2]) if len(args) > 2 else 1.0)
    elif command == 'scroll':
        mouse_scroll(int(args[0]))
    elif command == 'position':
        mouse_position()
    
    # 键盘命令
    elif command == 'write':
        keyboard_write(args[0] if args else "", float(args[1]) if len(args) > 1 else DEFAULT_INTERVAL)
    elif command == 'press':
        keyboard_press(args[0], int(args[1]) if len(args) > 1 else 1)
    elif command == 'hotkey':
        keyboard_hotkey(*args)
    elif command == 'keydown':
        keyboard_keydown(args[0])
    elif command == 'keyup':
        keyboard_keyup(args[0])
    
    # 屏幕命令
    elif command == 'screenshot':
        screen_screenshot(args[0])
    elif command == 'size':
        screen_size()
    elif command == 'locate':
        screen_locate(args[0], float(args[1]) if len(args) > 1 else 0.9)
    elif command == 'locate_center':
        screen_locate_center(args[0], float(args[1]) if len(args) > 1 else 0.9)
    elif command == 'pixel':
        screen_pixel(int(args[0]), int(args[1]))
    
    # 工具命令
    elif command == 'wait':
        wait(float(args[0]))
    elif command == 'alert':
        alert(args[0] if args else "", args[1] if len(args) > 1 else "Alert")
    elif command == 'confirm':
        confirm(args[0] if args else "", args[1] if len(args) > 1 else "Confirm")
    elif command == 'prompt':
        prompt(args[0] if args else "", args[1] if len(args) > 1 else "Prompt", args[2] if len(args) > 2 else "")
    
    else:
        output_result(False, command, error=f"Unknown command: {command}")

if __name__ == "__main__":
    main()