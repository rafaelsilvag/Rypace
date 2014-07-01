import xadmin
from xadmin import views
from cpof.pools.models import Users, Ips, Blacklists, Controls, ControlsBlacklists, Hour
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction

class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "Controle Parental OpenFlow", "content": "<h3> Bem Vindo ao Controle Parental OpenFlow</h3><p>Powered By: Ryu OpenFlow Controller</p>"},
            {"type": "chart", "model": "app.accessrecord", 'chart': 'user_count', 'params': {'_p_date__gte': '2013-01-08', 'p': 1, '_p_date__lt': '2013-01-29'}},
            {"type": "list", "model": "app.host", 'params': {
                'o':'-guarantee_date'}},
        ],
        [
            {"type": "qbutton", "title": "Acesso Expresso", "btns": [{'model': Controls}, {'model':Ips}, {'model':Blacklists}, {'model':Users}]},
            {"type": "addform", "model": ControlsBlacklists},
        ]
    ]

xadmin.site.register(views.website.IndexView, MainDashboard)

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    site_title = u"Controle Parental OpenFlow"
    global_search_models = [Ips, Users, Blacklists, Controls, ControlsBlacklists, Hour]
    global_models_icon = {
        Ips: 'globe',
        Users: 'user',
        Blacklists: 'upload',
        Controls: 'map-marker',
        ControlsBlacklists: 'key',
	Hour: 'time'
    }

xadmin.site.register(views.CommAdminView, GlobalSetting)

class UsersAdmin(object):
	fields = ('username', 'password')
	list_display = ('id','username', 'password')
	list_filter = ('id','username')
	search_fields = ('username',)

class IpsAdmin(object):
	fields = ('ip', 'blacklist', 'created','modified')
	list_display = ('id','ip', 'blacklist', 'created','modified')
	list_filter = ('id','ip')
	search_fields = ('ip',)

class ControlsAdmin(object):
	fields = ('user', 'mac', 'created' ,'modified')
	list_display = ('id', 'user', 'mac', 'created' ,'modified')
	list_filter = ('id','mac')
	search_fields = ('mac',)

class ControlsBlacklistsAdmin(object):
	fields = ('blacklist', 'controls', 'created' ,'modified',)
	list_display = ('id', 'blacklist', 'controls', 'created' ,'modified')
	list_filter = ('blacklist', 'controls')
	search_fields = ('blacklist_id',)

class BlacklistsAdmin(object):
	fields = ('name', 'descricao', 'created' ,'modified')
	list_display = ('id', 'name', 'descricao', 'created' ,'modified')
	list_filter = ('name',)
	search_fields = ('descricao',)

class HoursAdmin(object):
	fields = ('hour_start','hour_stop','controls','description')
	list_display = ('id','hour_start','hour_stop','controls','description')
	list_filter = ('description',)
	search_fields = ('description','controls',)


xadmin.site.register(Blacklists, BlacklistsAdmin)
xadmin.site.register(ControlsBlacklists, ControlsBlacklistsAdmin)
xadmin.site.register(Controls, ControlsAdmin)
xadmin.site.register(Users, UsersAdmin)
xadmin.site.register(Ips, IpsAdmin)
xadmin.site.register(Hour, HoursAdmin)
# Register your models here.
