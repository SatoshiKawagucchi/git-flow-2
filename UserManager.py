#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-

"""案件で使用するOSSツールのID／グループ管理

  各種OSSのユーザID管理、グループ管理をまとめて行う

  Todo:
     * まだRedmineとRocketChatのみ。他のOSSに対しても同様に作る

"""

################################################
# library
################################################

import json
import requests
import sys

from pprint import pprint
from redminelib import Redmine


################################################
# Basic Class
################################################

class BaseUserManager(object):
    """メソッド実装強制
    
    ユーザID及びグループメンテナンスメソッド定義。
    各OSS向けの共通メソッド定義。
    
    Attributes:
        object(object): class最上位 

    """
 
    # ユーザ管理
    def userAdd(self):
        '''ユーザを追加する'''
        raise NotImplementedError()
    
    def userDelete(self):
        '''ユーザを削除する'''
        raise NotImplementedError()

    def userUpdate(self):
        '''ユーザ情報をUpdateする（おそらくパスワード初期化ぐらい）'''
        raise NotImplementedError()

    # グループ管理    
    def userGropuAdd(self):
        '''グループにユーザを追加する'''
        raise NotImplementedError()
    
    def userGropuDelete(self):
        '''グループからユーザを削除する'''
        raise NotImplementedError()
        
    # チェック処理
    def is_user(self):
        '''ユーザが存在するか'''
        raise NotImplementedError()        
        
    def is_userGroup(self):
        '''グループが存在するか'''
        raise NotImplementedError()
        
    def is_userInTheGroup(self):
        '''グループにそのユーザが存在するか'''
        raise NotImplementedError()
