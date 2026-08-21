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
# 自动接受 Android SDK 许可协议
android.accept_sdk_license = True

# 如果你在国内，网络下载 Google 资源容易失败，建议加上腾讯镜像源加速
android.sdk_repo = https://mirrors.cloud.tencent.com/android/repository/
android.ndk_repo = https://mirrors.cloud.tencent.com/android/repository/


icon.filename = %(source.dir)s/icon.jpg

android.permissions =

[buildozer]
log_level = 2
warn_on_root = 1
