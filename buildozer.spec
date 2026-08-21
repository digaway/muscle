[app]
title = 训练数据记录器
package.name = muscletracker
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 0.1
requirements = python3,kivy,pillow
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 0

[app]
# 安卓配置
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# 关键：自动接受 SDK 许可，避免云端卡在 y/N 确认
android.accept_sdk_license = True

# 如果你有 icon.png 放在项目根目录，取消下一行注释
# icon.filename = %(source.dir)s/icon.png

# 你的应用是纯本地存储，不需要网络等权限，保持最小权限
android.permissions =

# 避免旧缓存导致构建异常
android.skip_update = False
