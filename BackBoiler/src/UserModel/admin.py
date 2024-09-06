from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display=('id', 'is_active' , 'username',  'email', 'password', 'date_joined', 'last_login')

    fieldsets = (
        ('New User', {'fields': ('is_active', 'username', 'email', 'password',)}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'is_active')}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('id',)


admin.site.register(User,UserAdmin)
