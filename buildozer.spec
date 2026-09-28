[app]
title = MINE
package.name = mine
package.domain = org.mine
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,cryptography,plyer,pyttsx3,SpeechRecognition
orientation = portrait
fullscreen = 0
android.permissions = RECORD_AUDIO,INTERNET
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
