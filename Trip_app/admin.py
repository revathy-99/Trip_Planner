from django.contrib import admin
from django.apps import apps

# Dynamically register all models
app = apps.get_app_config('Trip_app')  # Replace 'Trip_app' with your app name
for model_name, model in app.models.items():
    admin.site.register(model)
