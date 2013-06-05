from django.contrib import admin

from wevolve.project_parts.models import Document, File, Post, Comment


class DocumentAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    pass


class FileAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Document, DocumentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Comment, CommentAdmin)
