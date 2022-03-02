from django.contrib import admin
from .models import Post, University, Student


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_posted')
    # list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('user.name',)


admin.site.register(Post, PostAdmin)
admin.site.register(University)
admin.site.register(Student)
