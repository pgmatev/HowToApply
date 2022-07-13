from django.contrib import admin
from .models import Post, University, Student, StudentExam, Program, ProgramExam, Exam, Subject


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    # list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_username',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user_username'


admin.site.register(Post, PostAdmin)
admin.site.register(University)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentExam)
admin.site.register(Program)
admin.site.register(ProgramExam)
admin.site.register(Exam)
admin.site.register(Subject)
