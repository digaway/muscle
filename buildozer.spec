[app]
title = 训练数据记录器
package.name = muscletracker
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = python3,kivy,pillow
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.permissions =
android.accept_sdk_license = True
android.sdk_repo = https://mirrors.cloud.tencent.com/android/repository/
android.ndk_repo = https://mirrors.cloud.tencent.com/android/repository/

# 强制使用本地已克隆的 p4a 目录，禁止去网上拉取
android.p4a_fork = mirrors
android.p4a_branch = main
android.p4a_source_dir = /home/runner/work/muscle/muscle/.buildozer/android/platform/python-for-android
android.p4a_update = False

[buildozer]
log_level = 1
pip_index_url = https://pypi.tuna.tsinghua.edu.cn/simple
