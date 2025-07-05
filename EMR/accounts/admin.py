from django.contrib import admin
from accounts.models import User, Plans, Coverage
# Register your models here.

admin.site.register(User)
admin.site.register(Plans)
admin.site.register(Coverage)