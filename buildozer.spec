[app]
title = 训练数据记录器
package.name = muscletracker
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0.0
requirements = python3,kivy,pillow
orientation = portrait

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.permissions =
android.accept_sdk_license = True

[buildozer]
log_level = 1
