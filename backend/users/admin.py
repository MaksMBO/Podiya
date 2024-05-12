from django.contrib import admin
from .models import User, UserProfile, ContentMakerRequest, IssueRequest


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_content_maker',)
    list_display_links = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_content_maker',)
    search_fields = ('id', 'username', 'email',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    list_display_links = ('id', 'user',)
    search_fields = ('id', 'user',)


class IssueRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'request_date',)
    list_display_links = ('id', 'user', 'text', 'request_date',)
    search_fields = ('id', 'text', 'user',)


class ContentMakerRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'is_approved', 'request_date',)
    list_display_links = ('id', 'user', 'text', 'is_approved', 'request_date',)
    search_fields = ('id', 'text', 'user',)


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ContentMakerRequest, ContentMakerRequestAdmin)
admin.site.register(IssueRequest, IssueRequestAdmin)
