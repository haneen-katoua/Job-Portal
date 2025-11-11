# admin.py
from django.contrib import admin
from .models import User, Profile

# Inline لعرض البروفايل مع المستخدم
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# تخصيص UserAdmin بسيط
class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'email', 'user_type')  # عرض الحقول الأساسية
    list_filter = ('user_type',)                        # فلترة حسب نوع المستخدم
    search_fields = ('username', 'email')              # البحث حسب الاسم أو الإيميل
    inlines = [ProfileInline]                           # ربط البروفايل

# تسجيل الموديلات في الأدمن
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
