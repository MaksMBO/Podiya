from django.contrib import admin
from .models import User, UserProfile, ContentMakerRequest, IssueRequest

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(ContentMakerRequest)
admin.site.register(IssueRequest)
