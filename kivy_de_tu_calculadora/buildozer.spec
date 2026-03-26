[app]

# (str) Title of your application
title = Calculadora

# (str) Package name
package.name = calculadora

# (str) Package domain (needed for android/ios packaging)
package.domain = org.calculadora

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
# source.include_patterns = assets/*, images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
# source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
# source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
# source.exclude_patterns = license, images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0,requests==2.31.0,pyBCV

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = kivy

# (list) Garden requirements
# garden_requirements =

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
# services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# (str) iOS bundle identifier
# ios.bundle_identifier = %(package.domain)s.%(package.name)s

# (list) iOS supported orientations
# ios.orientation = portrait

# (list) iOS ui files
# ios.ui_files = Main.storyboard

# (list) iOS plist entries
# ios.plist_entries = CFBundleDevelopmentRegion:English

#
# Android Specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 30

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version used for compilation
android.sdk = 30

# (str) Android NDK version used for compilation
android.ndk = 23b

# (str) Android NDK directory (if empty, it will be downloaded)
# android.ndk_path =

# (str) Android SDK directory (if empty, it will be downloaded)
# android.sdk_path =

# (str) ANT directory (if empty, it will be downloaded)
# android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or to save time
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# android.accept_sdk_license = True

# (str) Android entry point, default is 'org.kivy.android.PythonActivity'
# android.entrypoint = org.renpy.android.PythonActivity

# (list) Android additionnal directories to add to the manifest
# android.add_manifest_entries =

# (list) Python packages for android (if empty, buildozer will search for requirements)
# android.python_packages = []

# (list) Android AAR archives to add (leave empty to not add anything)
# android.add_aars =

# (list) Gradle dependencies to add (leave empty to not add anything)
# android.gradle_dependencies =

# (list) Java classes to add (leave empty to not add anything)
# android.add_src =

# (str) android logcat filters to use
# android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (bool) Turn on/off the armeabi-v7a arch
# android.armeabi_v7a = True

# (bool) Turn on/off the arm64-v8a arch
# android.arm64_v8a = True

# (bool) Turn on/off the x86 arch
# android.x86 = True

# (bool) Turn on/off the x86_64 arch
# android.x86_64 = True

# (list) Android application meta-data to set
# android.meta_data =

# (list) Android library to include (if empty, it will be generated)
# android.library_references =

# (list) Android services
# android.services =

# (str) Android broadcast receivers
# android.broadcast_receivers =

# (bool) Indicate whether the screen should stay on
# android.wakelock = False

# (list) Android activity to add to the manifest
# android.add_activities =

# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (bool) Enable AndroidX
# android.enable_androidx = True

# (list) Android additional Java code to add to the project
# android.add_src =

# (bool) Use the default presplash for Android
# android.use_default_presplash = True