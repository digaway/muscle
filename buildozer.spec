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

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

icon.filename = %(source.dir)s/icon.png

android.permissions =

[buildozer]
log_level = 2
warn_on_root = 1
