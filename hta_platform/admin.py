from django.contrib import admin
from .models import Post, University, Student, StudentExam, Program, ProgramExam, Exam, Subject


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    # list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('user.name',)


admin.site.register(Post, PostAdmin)
admin.site.register(University)
admin.site.register(Student)
admin.site.register(StudentExam)
admin.site.register(Program)
admin.site.register(ProgramExam)
admin.site.register(Exam)
admin.site.register(Subject)
