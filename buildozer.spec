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

# 使用 Gitee 镜像拉取 python-for-android 工具链，避免 GitHub 502 错误
android.p4a_fork = mirrors
android.p4a_source_dir = /home/runner/work/muscle/muscle/.buildozer/android/platform/python-for-android

[buildozer]
log_level = 1
# 使用清华镜像加速 pip 下载
pip_index_url = https://pypi.tuna.tsinghua.edu.cn/simple
