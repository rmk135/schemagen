from django.contrib import admin

from .models import User, Field, Schema, Schema_Field

admin.site.register(User)
admin.site.register(Field)
admin.site.register(Schema)
admin.site.register(Schema_Field)