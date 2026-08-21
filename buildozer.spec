[app]
title = 训练数据记录器
package.name = muscletracker
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
requirements = python3,kivy,pillow
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.permissions =
android.accept_sdk_license = True
android.sdk_repo = https://mirrors.cloud.tencent.com/android/repository/
android.ndk_repo = https://mirrors.cloud.tencent.com/android/repository/

[buildozer]
log_level = 1
