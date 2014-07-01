from django.contrib import admin
from cpof.pools.models import Users, Ips, Blacklists, Controls, ControlsBlacklists

class UsersAdmin(admin.ModelAdmin):
	fields = ('username', 'password')
	list_display = ('id','username', 'password')
	list_filter = ('id','username')
	search_fields = ('username',)

class IpsAdmin(admin.ModelAdmin):
	fields = ('ip', 'blacklist', 'created','modified')
	list_display = ('id','ip', 'blacklist', 'created','modified')
	list_filter = ('id','ip')
	search_fields = ('ip',)

class ControlsAdmin(admin.ModelAdmin):
	fields = ('user', 'mac', 'created' ,'modified')
	list_display = ('id', 'user', 'mac', 'created' ,'modified')
	list_filter = ('id','mac')
	search_fields = ('mac',)

class ControlsBlacklistsAdmin(admin.ModelAdmin):
	fields = ('blacklist', 'controls', 'created' ,'modified')
	list_display = ('id', 'blacklist', 'controls', 'created' ,'modified')
	list_filter = ('blacklist', 'controls')
	search_fields = ('blacklist_id',)

class BlacklistsAdmin(admin.ModelAdmin):
	fields = ('name', 'descricao', 'created' ,'modified')
	list_display = ('id', 'name', 'descricao', 'created' ,'modified')
	list_filter = ('name',)
	search_fields = ('descricao',)

admin.site.register(Blacklists, BlacklistsAdmin)
admin.site.register(ControlsBlacklists, ControlsBlacklistsAdmin)
admin.site.register(Controls, ControlsAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Ips, IpsAdmin)
# Register your models here.