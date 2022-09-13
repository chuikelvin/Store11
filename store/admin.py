import os
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin
# from .models import *

# Register all models in app.
dirname = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
# print(dirname)
# from django.apps import apps

app_models = apps.get_app_config(dirname).get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass


# models = apps.get_models()

# for model in models:
#     print(model)
#     # admin.site.register(model)

# from django.apps import apps
# from django.contrib import admin
# from django.contrib.admin.sites import AlreadyRegistered

# # app_models = apps.get_app_config('store').get_models()
# app_models = apps.get_models()
# for model in app_models:
#     try:
#         admin.site.register(model)
#     except AlreadyRegistered:
#         pass
    
# # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # print(os.path.dirname(Path))
# # print(BASE_DIR)

# print("Path at terminal when executing this file")
# print(os.getcwd() + "\n")

# print("This file path, relative to os.getcwd()")
# print(__file__ + "\n")

# print("This file full path (following symlinks)")
# full_path = os.path.realpath(__file__)
# print(full_path + "\n")

# print("This file directory and name")
# path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")

# print("This file directory only")
# print(os.path.dirname(full_path))