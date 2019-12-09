from django.contrib import admin
from Slife.models import Category,Option,Vote,Comment,Contact
# Register your models here.

class OptionInline(admin.TabularInline):
    model = Option
    readonly_fields = ['votes']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','created','modified','views','active','details']
    search_fields = ['name','details']
    list_filter = ['created','views','created','modified']
    readonly_fields = ['views']
    inline = [OptionInline]    

admin.site.register(Category, CategoryAdmin)

admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Option)
admin.site.register(Vote)
#Opt & Vote was not in Ranker