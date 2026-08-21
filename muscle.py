# muscle.py
# ==================== 配置区（修改这里即可控制动作与图片） ====================
# 动作名称列表：顺序即为卡片显示顺序、数据 id 顺序，同时决定图片文件名为 "动作.jpg"
LABELS = [
    "杠铃卧推", "杠铃斜推", "杠铃实力推", "杠铃划船", "杠铃深蹲", "杠铃硬拉","杠铃臀推" ,
     "哑铃卧推","哑铃斜推","哑铃坐推", "哑铃飞鸟", "哑铃俯身臂屈伸","哑铃交替弯举", "哑铃侧平举","哑铃俯身反向飞鸟",
     "引体向上",
]

IMAGE_EXT = ".jpg"      # 图片扩展名，可按实际改为 .png
MAX_WEIGHT = 200.0      # 重量上限(kg)，用于计算遮罩深浅，重量越大图片越暗
# ==============================================================================

import os
import json
import platform
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image as KivyImage
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior

Window.size = (400, 700)

# ==================== 字体安全加载 ====================
def find_chinese_font():
    for f in ["msyh.ttc", "simhei.ttf", "simsun.ttc", "MiSans-Regular.ttf"]:
        if os.path.exists(f):
            return os.path.abspath(f)
    if platform.system() == "Windows":
        for f in [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/msyhbd.ttc",
        ]:
            if os.path.exists(f):
                return f
    for f in [
        "/usr/share/fonts/truetype/misans/MiSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansSC-Regular.otf",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]:
        if os.path.exists(f):
            return f
    return None

_font_path = find_chinese_font()
FONT = None
if _font_path:
    from kivy.core.text import LabelBase
    LabelBase.register(name="CN", fn_regular=_font_path)
    FONT = "CN"

def fnt():
    return FONT if FONT else "Roboto"

# ==================== 剪贴板 ====================
def copy_to_clipboard(text):
    """跨平台复制文本到剪贴板，返回 (ok, msg)"""
    if platform.system() == "Windows":
        try:
            import ctypes
            from ctypes import wintypes
            CF_UNICODETEXT = 13
            kernel32 = ctypes.windll.kernel32
            user32 = ctypes.windll.user32
            if not user32.OpenClipboard(0):
                return False, "无法打开剪贴板"
            user32.EmptyClipboard()
            hMem = kernel32.GlobalAlloc(0x0042, (len(text) + 1) * 2)
            pMem = kernel32.GlobalLock(hMem)
            ctypes.c_wchar_p.from_address(pMem).value = text
            kernel32.GlobalUnlock(hMem)
            user32.SetClipboardData(CF_UNICODETEXT, hMem)
            user32.CloseClipboard()
            return True, "已复制到剪贴板"
        except Exception as e:
            return False, f"复制失败: {e}"
    # Linux / macOS 走命令行
    try:
        import subprocess
        if platform.system() == "Linux":
            for cmd in [
                ["xclip", "-selection", "clipboard"],
                ["wl-copy"],
            ]:
                try:
                    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                    p.communicate(text.encode("utf-8"))
                    return True, "已复制到剪贴板"
                except FileNotFoundError:
                    continue
            return False, "未找到 xclip/wl-copy"
        if platform.system() == "Darwin":
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            p.communicate(text.encode("utf-8"))
            return True, "已复制到剪贴板"
    except Exception as e:
        return False, f"复制失败: {e}"
    return False, "不支持的平台"

# ==================== 数据模型 ====================
class HistoryRecord:
    def __init__(self, sets, reps, weight):
        self.sets = sets
        self.reps = reps
        self.weight = weight
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {"sets": self.sets, "reps": self.reps, "weight": self.weight, "timestamp": self.timestamp}

    @staticmethod
    def from_dict(d):
        r = HistoryRecord(d.get("sets", 0), d.get("reps", 0), d.get("weight", 0))
        r.timestamp = d.get("timestamp", "")
        return r


class ImageItem:
    def __init__(self, item_id, label, image_path):
        self.id = item_id
        self.label = label
        self.image_path = image_path
        self.sets = 0
        self.reps = 0
        self.weight = 0.0
        self.history = []

    def update(self, sets, reps, weight):
        self.sets = sets
        self.reps = reps
        self.weight = float(weight)
        self.history.append(HistoryRecord(sets, reps, self.weight))

    def clear_all(self):
        """清除所有数据与历史"""
        self.sets = 0
        self.reps = 0
        self.weight = 0.0
        self.history = []

    def get_mask_alpha(self):
        if self.weight <= 0:
            return 0.0
        return min(self.weight / MAX_WEIGHT, 1.0) * 0.6

    def display_text(self):
        if self.sets > 0 or self.reps > 0 or self.weight > 0:
            return f"{self.sets}组 × {self.reps}次 × {self.weight:.0f}kg"
        return ""

    def is_filled(self):
        """三项是否至少填写了（用于复制时判断）"""
        return self.sets > 0 and self.reps > 0 and self.weight > 0

# ==================== 卡片 Widget ====================
class ImageItemWidget(ButtonBehavior, FloatLayout):
    def __init__(self, item, main_screen, **kwargs):
        super().__init__(**kwargs)
        self.item = item
        self.main_screen = main_screen
        self.size_hint = (0.48, None)
        self.height = 180

        self.img = KivyImage(
            source=item.image_path,
            allow_stretch=True, keep_ratio=False,
            size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}
        )
        self.add_widget(self.img)

        with self.canvas:
            self.mask_color = Color(0, 0, 0, 0)
            self.mask_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.lbl = Label(
            text="", font_size='15sp', bold=True, color=(1, 1, 1, 1),
            halign='center', valign='middle',
            outline_color=(0, 0, 0, 1), outline_width=2.5,
            font_name=fnt(),
            size_hint=(0.9, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        self.lbl.bind(size=self.lbl.setter('text_size'))
        self.add_widget(self.lbl)
        self.update_appearance()

    def _update_rect(self, *args):
        self.mask_rect.size = self.size
        self.mask_rect.pos = self.pos

    def update_appearance(self):
        self.mask_color.rgba = (0, 0, 0, self.item.get_mask_alpha())
        self.lbl.text = self.item.display_text()

    def on_press(self):
        self.show_input_popup()

    def show_input_popup(self):
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        content.add_widget(Label(
            text=self.item.label, font_size='18sp', bold=True,
            color=(0.1, 0.2, 0.5, 1), size_hint=(1, 0.15), font_name=fnt(),
        ))

        input_box = BoxLayout(size_hint=(1, 0.25), spacing=8)
        sets_input = TextInput(text=str(self.item.sets) if self.item.sets else "",
                               hint_text="组数", multiline=False, input_type='number',
                               font_size='16sp', font_name=fnt(), halign='center')
        reps_input = TextInput(text=str(self.item.reps) if self.item.reps else "",
                               hint_text="次数", multiline=False, input_type='number',
                               font_size='16sp', font_name=fnt(), halign='center')
        weight_input = TextInput(text=str(int(self.item.weight)) if self.item.weight else "",
                                 hint_text="重量(kg)", multiline=False, input_type='number',
                                 font_size='16sp', font_name=fnt(), halign='center')
        input_box.add_widget(sets_input)
        input_box.add_widget(Label(text="-", font_size='18sp', bold=True, font_name=fnt(), size_hint=(0.1, 1)))
        input_box.add_widget(reps_input)
        input_box.add_widget(Label(text="-", font_size='18sp', bold=True, font_name=fnt(), size_hint=(0.1, 1)))
        input_box.add_widget(weight_input)
        content.add_widget(input_box)

        btn_box = BoxLayout(size_hint=(1, 0.2), spacing=10)
        save_btn = Button(text="保存", background_color=(0.2, 0.6, 0.2, 1), font_name=fnt())
        history_btn = Button(text="历史记录", background_color=(0.2, 0.4, 0.8, 1), font_name=fnt())
        cancel_btn = Button(text="取消", background_color=(0.6, 0.2, 0.2, 1), font_name=fnt())
        btn_box.add_widget(save_btn); btn_box.add_widget(history_btn); btn_box.add_widget(cancel_btn)
        content.add_widget(btn_box)

        popup = Popup(title="", content=content, size_hint=(0.9, 0.5), separator_height=0)

        def save_data(instance):
            try: sets_val = int(sets_input.text) if sets_input.text.strip() else 0
            except ValueError: sets_val = 0
            try: reps_val = int(reps_input.text) if reps_input.text.strip() else 0
            except ValueError: reps_val = 0
            try: weight_val = float(weight_input.text) if weight_input.text.strip() else 0.0
            except ValueError: weight_val = 0.0
            self.item.update(sets_val, reps_val, weight_val)
            self.update_appearance()
            self.main_screen._save_data()
            popup.dismiss()

        save_btn.bind(on_press=save_data)
        history_btn.bind(on_press=lambda inst: (popup.dismiss(), self.show_history_popup()))
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    def show_history_popup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=8)
        scroll = ScrollView()
        hist_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=6)
        hist_box.bind(minimum_height=hist_box.setter('height'))

        if not self.item.history:
            hist_box.add_widget(Label(text="暂无历史记录", size_hint_y=None, height=50,
                                      font_size='15sp', font_name=fnt()))
        else:
            for record in reversed(self.item.history):
                entry = BoxLayout(orientation='vertical', size_hint_y=None, height=65, padding=[10, 5])
                with entry.canvas.before:
                    Color(0.93, 0.93, 0.93, 1); Rectangle(size=entry.size, pos=entry.pos)
                entry.bind(size=lambda obj, val: obj.canvas.before.clear() or (
                    Color(0.93, 0.93, 0.93, 1), Rectangle(size=obj.size, pos=obj.pos)
                ))
                hist_box.add_widget(Label(text=f"🕐 {record.timestamp}", font_size='12sp',
                                          color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=20,
                                          halign='left', font_name=fnt()))
                hist_box.add_widget(Label(text=f"{record.sets}组 × {record.reps}次 × {record.weight:.0f}kg",
                                          font_size='14sp', size_hint_y=None, height=30, halign='left',
                                          color=(0.1, 0.1, 0.1, 1), font_name=fnt()))
                hist_box.add_widget(entry)

        scroll.add_widget(hist_box)

        # 底部按钮：关闭 + 清除所有数据
        bottom = BoxLayout(size_hint=(1, 0.15), spacing=10)
        close_btn = Button(text="关闭", background_color=(0.4, 0.4, 0.4, 1), font_name=fnt())
        clear_btn = Button(text="🗑 清除所有数据", background_color=(0.7, 0.2, 0.2, 1), font_name=fnt())
        bottom.add_widget(close_btn); bottom.add_widget(clear_btn)
        content.add_widget(scroll); content.add_widget(bottom)

        hist_popup = Popup(title=f"📋 {self.item.label} 的历史记录", content=content,
                           size_hint=(0.92, 0.72), separator_height=1, title_font=fnt())

        def do_clear(instance):
            self.item.clear_all()
            self.update_appearance()
            self.main_screen._save_data()
            hist_popup.dismiss()
            Popup(title="✅ 已清除", content=Label(text=f"{self.item.label} 的所有数据已清除",
                                                  font_size='14sp', font_name=fnt()),
                  size_hint=(0.75, 0.25), title_font=fnt()).open()

        def ask_clear(instance):
            confirm = BoxLayout(orientation='vertical', padding=15, spacing=12)
            confirm.add_widget(Label(text=f"确定要清除【{self.item.label}】\n全部数据与历史记录吗？",
                                     font_size='15sp', font_name=fnt()))
            bb = BoxLayout(size_hint=(1, 0.4), spacing=10)
            yes = Button(text="确认清除", background_color=(0.7, 0.2, 0.2, 1), font_name=fnt())
            no = Button(text="取消", background_color=(0.4, 0.4, 0.4, 1), font_name=fnt())
            bb.add_widget(yes); bb.add_widget(no)
            confirm.add_widget(bb)
            cp = Popup(title="⚠ 二次确认", content=confirm, size_hint=(0.8, 0.4), title_font=fnt())
            yes.bind(on_press=lambda inst: (cp.dismiss(), do_clear(inst)))
            no.bind(on_press=cp.dismiss)
            cp.open()

        close_btn.bind(on_press=hist_popup.dismiss)
        clear_btn.bind(on_press=ask_clear)
        hist_popup.open()

# ==================== 主界面 ====================
class MainScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', padding=12, spacing=10, **kwargs)
        self.app = app

        self.add_widget(Label(text="训练数据记录器", font_size='22sp', bold=True,
                              color=(0.1, 0.2, 0.5, 1), size_hint=(1, 0.08), font_name=fnt()))
        self.add_widget(Label(text=f"点击图片输入数据（组数-次数-重量），重量越大图片越暗（上限{MAX_WEIGHT:.0f}kg）",
                              font_size='12sp', color=(0.5, 0.5, 0.5, 1), size_hint=(1, 0.05), font_name=fnt()))

        self.grid = GridLayout(cols=2, spacing=12, padding=8, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.items = []
        self.widgets = []
        for i, label in enumerate(LABELS):
            item = ImageItem(i, label, f"{label}{IMAGE_EXT}")
            self.items.append(item)
            w = ImageItemWidget(item, self)
            self.widgets.append(w)
            self.grid.add_widget(w)

        scroll = ScrollView()
        scroll.add_widget(self.grid)
        self.add_widget(scroll)

        # 底部：一键复制最新数据（替代原导出按钮）
        btn_box = BoxLayout(size_hint=(1, 0.08), spacing=12)
        copy_btn = Button(text="📋 复制最新数据", background_color=(0.1, 0.5, 0.7, 1),
                          font_size='15sp', font_name=fnt())
        copy_btn.bind(on_press=self.copy_latest)
        btn_box.add_widget(copy_btn)
        self.add_widget(btn_box)

        self._load_data()

    def copy_latest(self, instance):
        """复制所有已填写动作的最新一次数据，跳过未填项"""
        lines = []
        for item in self.items:
            if item.is_filled():
                lines.append(f"{item.label} {item.sets}-{item.reps}-{item.weight:.0f}kg")
        if not lines:
            Popup(title="ℹ 暂无数据", content=Label(text="没有已填写的项目可复制",
                                                   font_size='14sp', font_name=fnt()),
                  size_hint=(0.75, 0.25), title_font=fnt()).open()
            return
        text = "\n".join(lines)
        ok, msg = copy_to_clipboard(text)
        print(f"[复制到剪贴板]\n{text}")
        Popup(title="📋 复制结果", content=Label(text=f"{msg}\n已复制 {len(lines)} 项最新数据",
                                                 font_size='13sp', font_name=fnt()),
              size_hint=(0.8, 0.28), title_font=fnt()).open()

    def _save_data(self):
        data = [{
            'id': item.id, 'label': item.label,
            'sets': item.sets, 'reps': item.reps, 'weight': item.weight,
            'history': [h.to_dict() for h in item.history]
        } for item in self.items]
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for item_data in data:
                iid = item_data.get('id', 0)
                if iid < len(self.items):
                    item = self.items[iid]
                    item.sets = item_data.get('sets', 0)
                    item.reps = item_data.get('reps', 0)
                    item.weight = item_data.get('weight', 0.0)
                    item.history = [HistoryRecord.from_dict(h) for h in item_data.get('history', [])]
                    self.widgets[iid].update_appearance()
        except Exception as e:
            print(f"加载数据失败: {e}")

DATA_FILE = "data.json"

# ==================== App ====================
class MuscleApp(App):
    kv_file = None
    def build(self):
        self.title = "训练数据记录器"
        return MainScreen(self)
    def on_stop(self):
        self.root._save_data()

if __name__ == '__main__':
    MuscleApp().run()
