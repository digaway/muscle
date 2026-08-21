# -*- coding: utf-8 -*-
import os, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imaging import find_chinese_font, extract_dominant_color

# 最小化 ImageItem（与主程序一致），避免导入 main 拉入 Kivy
class HistoryRecord:
    def __init__(self, text, number):
        self.text = text; self.number = number
        from datetime import datetime
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
class ImageItem:
    def __init__(self, idx, filename, label):
        self.idx = idx; self.filename = filename; self.label = label
        self.text = label; self.number = 0; self.history = []
    def update(self, text, number):
        self.text = text; self.number = number
        self.history.append(HistoryRecord(text, number))
    def to_dict(self):
        return {"idx": self.idx, "filename": self.filename, "label": self.label,
                "text": self.text, "number": self.number,
                "history": [{"text": h.text, "number": h.number, "timestamp": h.timestamp} for h in self.history]}
    @staticmethod
    def from_dict(d):
        it = ImageItem(d["idx"], d["filename"], d.get("label", ""))
        it.text = d.get("text", it.label); it.number = d.get("number", 0)
        it.history = [HistoryRecord(h.get("text",""), h.get("number",0)) for h in d.get("history", [])]
        return it

presets = [("pix1.png","卧推"),("pix2.png","深蹲"),("pix3.png","硬拉"),
           ("pix4.png","引体向上"),("pix5.png","俯卧撑"),("pix6.png","臂弯举")]

print("=== 1. 中文字体 ===")
fp = find_chinese_font()
print("font path:", fp)
assert fp and os.path.exists(fp), "中文字体未找到"

print("=== 2. 图片文件 ===")
for fn, lb in presets:
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), fn)
    print(f"{fn} ({lb}): exists={os.path.exists(p)}")
    assert os.path.exists(p), fn + " 不存在"

print("=== 3. 主色提取 ===")
for fn, lb in presets:
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), fn)
    print(f"{fn}: dominant={extract_dominant_color(p)}")

print("=== 4. 数据模型 + 遮罩alpha逻辑 ===")
def mask_alpha(n): return 0.08 + 0.55 * (n / 100.0)
it = ImageItem(0, "pix1.png", "卧推")
it.update("卧推", 30)
it.update("卧推", 80)
print("current:", it.text, it.number, "| history条数:", len(it.history))
print("alpha: n=0 -> %.3f, n=30 -> %.3f, n=80 -> %.3f, n=100 -> %.3f" % (
    mask_alpha(0), mask_alpha(30), mask_alpha(80), mask_alpha(100)))
assert mask_alpha(80) > mask_alpha(30) > mask_alpha(0)
assert it.history[0].text == "卧推" and it.history[1].number == 80

print("=== 5. 持久化读写(含中文) ===")
items = [ImageItem(i, fn, lb) for i, (fn, lb) in enumerate(presets)]
items[0].update("卧推", 75)
items[3].update("引体向上", 90)
data = [it.to_dict() for it in items]
test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data.json")
with open(test_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
with open(test_file, "r", encoding="utf-8") as f:
    loaded = [ImageItem.from_dict(d) for d in json.load(f)]
print("load back: pix1.text=%s pix1.num=%d pix4.num=%d" % (
    loaded[0].text, loaded[0].number, loaded[3].number))
assert loaded[0].text == "卧推" and loaded[0].number == 75 and loaded[3].number == 90
os.remove(test_file)

print("\nALL CHECKS PASSED")
