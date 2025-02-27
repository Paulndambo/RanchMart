from django.contrib import admin
from shop.models import Animal, AnimalImage, Category

# Register your models here.
@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'quantity')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(AnimalImage)
class AnimalImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'animal', 'image')
    list_filter = ('animal',)
    search_fields = ('animal__name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)