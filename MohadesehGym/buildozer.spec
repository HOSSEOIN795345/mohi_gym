[app]

title = Mohadeseh Gym
package.name = mohadesehgym
package.domain = org.mohadeseh

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json

version = 1.0

orientation = portrait
fullscreen = 0

# 🔥 مهم
requirements = python3==3.10.11,kivy==2.1.0,arabic-reshaper,python-bidi

# 🔥 مهم
android.api = 31
android.minapi = 21
android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

android.permissions = INTERNET

# سرعت بهتر
android.copy_libs = 1

# جلوگیری از باگ
p4a.branch = master
