# -*- coding: utf-8 -*-
from django.db import models

class Blacklists(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField("Nome", max_length=50)
    descricao = models.CharField("Descrição", max_length=750) # Field renamed to remove unsuitable characters.
    created = models.DateTimeField("Data de Criação")
    modified = models.DateTimeField("Data de Modificação")

    def __unicode__(self):
        return self.descricao

    class Meta:
        managed = False
        db_table = 'blacklists'
        verbose_name = "Blacklist"
        verbose_name_plural = "Blacklists"
        ordering = ('id',)

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField("Usuário",max_length=50, blank=True)
    password = models.CharField("Senha",max_length=50, blank=True)
    email = models.CharField("E-Mail",max_length=100, blank=True)
    role = models.CharField("Regra",max_length=20, blank=True)
    created = models.DateTimeField("Data de Criação",blank=True, null=True)
    modified = models.DateTimeField("Data de Modificação",blank=True, null=True)

    def __unicode__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = "Cadastro de Usuário"
        verbose_name_plural = "Cadastro de Usuários"
        ordering = ('username',)

class Controls(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Users)
    mac = models.CharField("MAC Address", max_length=20)
    created = models.DateTimeField("Data de Criação")
    modified = models.DateTimeField("Data de Modificação")
    
    def __unicode__(self):
        return "%s -> %s" % (self.user, self.mac)
    
    class Meta:
        managed = False
        db_table = 'controls'
        verbose_name = "Controle"
        verbose_name_plural = "Controles"
        ordering = ('id',)

class Hour(models.Model):
    id = models.IntegerField(primary_key=True)
    hour_start = models.TimeField("Hora Inicial")
    hour_stop = models.TimeField("Hora Inicial")
    controls = models.ForeignKey(Controls)
    description = models.CharField("Descrição", max_length=45)

    def __unicode__(self):
        return "%s" % (self.description)

    class Meta:
        managed = False
        db_table = 'hour'
        verbose_name = u'Horário de Acesso'
        verbose_name_plural = u'Horarios de Acesso'
        ordering = ('id','controls',)

class ControlsBlacklists(models.Model):
    id = models.IntegerField(primary_key=True)
    blacklist = models.ForeignKey(Blacklists)
    controls = models.ForeignKey(Controls)
    created = models.DateTimeField("Data de Criação")
    modified = models.DateTimeField("Data de Modificação")

    def __unicode__(self):
        return "%s -- %s" % (self.blacklist, self.controls)

    class Meta:
        managed = False
        db_table = 'controls_blacklists'
        verbose_name = u"Blacklist e Controle"
        verbose_name_plural = u"Blacklists e Controles"
        ordering = ('controls',)

class Ips(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.CharField("IPv4 Address",max_length=20)
    blacklist = models.ForeignKey(Blacklists)
    created = models.DateTimeField("Data de Criação")
    modified = models.DateTimeField("Data de Modificação")

    def __unicode__(self):
        return self.ip

    class Meta:
        managed = False
        db_table = 'ips'
        verbose_name = u"Cadastro de IP"
    	verbose_name_plural = u"Cadastro de IPs"
    	ordering = ('blacklist', 'ip',)
