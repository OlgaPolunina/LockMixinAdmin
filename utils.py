from django.contrib import admin, messages
from django.contrib.admin.actions import delete_selected as delete_selected_
from django.contrib.admin.utils import model_ngettext
from django.utils.translation import ugettext_lazy as _




def delete_selected(modeladmin, request, queryset):
    """
    Переопределено множественное удаление записи.
    Добавляем в исключение lock_id_list
    
    """
    
    lock_id_list = getattr(modeladmin, 'lock_id_list', [])
  
    queryset_without_lock = queryset.exclude(id__in=lock_id_list)
    count_lock = queryset.filter(id__in=lock_id_list).count()
    if count_lock: 
        modeladmin.message_user(request, _('%(count)d %(items)s not may be deleted.') % {
            'count': count_lock, 'items': model_ngettext(modeladmin.opts, count_lock)
        }, messages.WARNING)
    return delete_selected_(modeladmin, request, queryset_without_lock)
    
delete_selected.short_description = _('Delete_selected_records')




class LockMixinAdmin(object):
    """
    Примесь для запрета удаления и редактирования записей.
    lock_id_list = [1, 2, 3] - список id полей для которых заблокировано удаление
    lock_readonly_fields = ['title', ] - список field полей для которых заблокировано редактирование
    
    """
    
    actions = [delete_selected]
    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.id in self.lock_id_list:
                return False
        return super(LockMixinAdmin, self).has_delete_permission(request, obj=obj)
            
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = getattr(self, 'readonly_fields', [])
        lock_id_list = getattr(self, 'lock_id_list', [])
        lock_readonly_fields = getattr(self, 'lock_readonly_fields', [])
        if obj:
            if obj.id in lock_id_list:
                return redonly_fields + lock_redonly_fields
        return super(LockMixinAdmin, self).get_readonly_fields(request, obj=obj)
