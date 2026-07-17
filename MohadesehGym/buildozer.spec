[app]

# (str) Title of your application
title = Mohadeseh Gym

# (str) Package name
package.name = mohadesehgym

# (str) Package domain
package.domain = org.mohadeseh

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# (str) Application version
version = 1.0

# (list) Supported orientations
orientation = portrait

# (bool) fullscreen mode
fullscreen = 0


# (str) Requirements
requirements = python3,kivy==2.1.0,arabic-reshaper,python-bidi


# (str) Android API
android.api = 33

# (str) Minimum API
android.minapi = 24

# (str) Android NDK version
android.ndk = 25b


# (list) Architectures
android.archs = arm64-v8a,armeabi-v7a


# (bool) Allow backup
android.allow_backup = True


# (str) Presplash
# presplash.filename = %(source.dir)s/data/presplash.png


# (str) Icon
# icon.filename = %(source.dir)s/icon.png


# (list) Permissions
android.permissions = INTERNET


# (str) Python-for-android branch
p4a.branch = master


# (bool) Copy library files
android.copy_libs = 1
