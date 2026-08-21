# -*- coding: utf-8 -*-
"""
imaging.py  —— 纯逻辑模块（无 Kivy 依赖）
- 查找系统中文字体
- 图片主色提取 / 生成居中裁切的缩略图路径
"""
import os
from PIL import Image

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)


def find_chinese_font():
    """按优先级返回系统里第一个存在的中文字体文件路径"""
    candidates = [
        "/usr/share/fonts/truetype/misans/MiSans-Regular.ttf",
        "/usr/share/fonts/truetype/misans/MiSans-Medium.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-VF.otf.ttc",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    # 兜底：遍历常见目录
    for root, _, files in os.walk("/usr/share/fonts"):
        for f in files:
            if f.startswith("MiSans") and f.endswith(".ttf"):
                return os.path.join(root, f)
    return None


def extract_dominant_color(path, size=40):
    """提取图片主色 (R,G,B)，用于数字徽标等辅助配色"""
    try:
        im = Image.open(path).convert("RGB").resize((size, size))
        px = list(im.getdata())
        # 按亮度加权，避免大面积暗色主导
        r = g = b = 0.0
        total = 0.0
        for R, G, B in px:
            lum = 0.299 * R + 0.587 * G + 0.114 * B
            w = max(lum, 30)
            r += R * w; g += G * w; b += B * w
            total += w
        if total <= 0:
            return (120, 140, 170)
        return (int(r / total), int(g / total), int(b / total))
    except Exception:
        return (120, 140, 170)


def make_thumb(path, target_w, target_h):
    """生成一张居中裁切到 (target_w x target_h) 的缩略图，返回路径"""
    if not os.path.exists(path):
        return None
    key = os.path.basename(path)
    out = os.path.join(CACHE_DIR, f"thumb_{key}")
    try:
        im = Image.open(path).convert("RGBA")
        # 居中裁切
        iw, ih = im.size
        tr = target_w / float(target_h)
        if iw / float(ih) > tr:
            new_h = ih
            new_w = int(new_h * tr)
            left = (iw - new_w) // 2
            im = im.crop((left, 0, left + new_w, ih))
        else:
            new_w = iw
            new_h = int(new_w / tr)
            top = (ih - new_h) // 2
            im = im.crop((0, top, iw, top + new_h))
        im = im.resize((target_w, target_h), Image.LANCZOS)
        im.save(out)
        return out
    except Exception as e:
        print("[imaging] thumb failed:", e)
        return None
