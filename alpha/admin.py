from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import*

admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Replies)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(News)
admin.site.register(NewsComment)
admin.site.register(PaymentSwitch)
admin.site.register(PaymentMethod)
admin.site.register(SubmitPayment)
admin.site.register(SavedQuestion)





# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff', 'status')  # Exclude username
    list_filter = ('is_staff', 'status')  # Exclude username
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_pic', 'department','status')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('phone_number', 'first_name', 'last_name')  # Exclude username
    ordering = ('phone_number',)  # Exclude username

admin.site.register(CustomUser, CustomUserAdmin)
