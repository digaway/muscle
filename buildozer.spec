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
android.sdk_repo = https://mirrors.cloud.tencent.com/android/repository/
android.ndk_repo = https://mirrors.cloud.tencent.com/android/repository/

# 仅指定本地目录和分支，不指定 fork，防止 Buildozer 判定为旧版本而删除
android.p4a_branch = master
android.p4a_source_dir = /home/runner/work/muscle/muscle/.buildozer/android/platform/python-for-android
android.p4a_update = False

icon.filename = %(source.dir)s/icon.jpg

[buildozer]
log_level = 1
pip_index_url = https://pypi.tuna.tsinghua.edu.cn/simple
