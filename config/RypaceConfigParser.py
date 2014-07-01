'''
Created on 28/11/2013

@author: Rafael S. Guimaraes
'''
from ConfigParser import ConfigParser, Error

class RypaceConfigParser(object):
    def __init__(self):
        """
            Metodo construtor da instancia para todas as
            configuracoes.
        """
        self.__filePath = "config/"
        self.__fileName = "database.ini"
        self.__parser = ConfigParser()
        print(self.__filePath + self.__fileName)
        try:
            self.__parser.read(self.__filePath + self.__fileName)
            self.__configSections = self.__parser.sections()
            try:
                self.__generalConfig = self.__parser.items('general')
                self.__localDBConfig = self.__parser.items('database')
            except Error, e:
                print("Erro: " + e)
        except Error, e:
            print("Erro: " + e)

    def readGeneralConfig(self):
        """
            Retorna  uma tupla com todas as configuracores em general.
        """
        return dict(self.__generalConfig)

    def readDBConfig(self):
        """
            Retorna uma tupla com todas as configuracoes do banco de dados local.
        """
        return dict(self.__localDBConfig)
