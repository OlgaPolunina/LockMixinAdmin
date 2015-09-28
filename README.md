# LockMixinAdmin
Примесь для запрета удаления и редактирования записей в административном интерфейсе.

Пример использования:

    class StatusAdmin(LockMixinAdmin, admin.ModelAdmin):
        """
        Статус.
        
        """
        lock_id_list = [1, 2]
        lock_readonly_fields = ['title']
        
    admin.site.register(models.Status, StatusAdmin)

