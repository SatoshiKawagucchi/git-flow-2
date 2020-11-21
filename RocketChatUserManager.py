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

# 個別ライブラリ
from UserManager import BaseUserManager

################################################
# パラメータ：yamlから取得するのでいったんこれで
################################################
#
#HEADERS ={
#    'X-Auth-Token': 'zYGeveBMm79longHcJTwFi425FB6qyLxXDuRXUHAXDS',
#    'X-User-Id': 'sny2QJnFfBHBK4Prc',
#    'Content-Type': 'application/json'}
#
#URL = 'http://192.168.10.104:3000'
#INIT_PASS = 'p@ssw0rd'
#

################################################
# RocketChatUserManager 
################################################

class RocketChatUserManager(BaseUserManager):
    '''RocketChatユーザ管理Class
     
    目的別にAPIを生成するので
    HEADERSとURLはインスタンス変数として扱う

     RocketChatのユーザ管理を行う。
       ユーザ追加、削除、変更
    ''' 
    
    def __init__(self, HEADERS, URL):

        # 引数チェック 型    
        if not isinstance(HEADERS, dict):
            print(f'引数：HEADERSの型が正しくありません dict <-> {type(HEADERS)}')
            raise TypeError

        # 引数チェック 型    
        if not isinstance(URL, str):
            print(f'引数：URLの型が正しくありません str <-> {type(URL)}')
            raise TypeError
    
        # インスタンス生成
        self.HEADERS = HEADERS
        self.URL = URL
            

    def userAdd(self, userid, first_name, last_name, mail, INIT_PASS):
        '''ユーザ登録

        引数情報を元にRocketChatにIDを追加する 
        roleはuser,次回ログイン時にパスワード変更を要求設定とする

        Args:
           userid(str): 登録するユーザID
           first_name(str): 名前
           last_name(str): 姓
           mail(str): 割り当てられたメールアドレス

        Returns:

        Raises:
            TypeError: 引数型の不備
            Exception: ID登録時の例外

        Examples:
            >>>  self.userAdd('PIT00000', 'Satoshi', 'Suzuki', 'satoshi_10_suzuki@mufg.jp', INIT_PASS)

        Note:
            /api/v1/users.create'

            あまりこまごまとした入力チェックをやっていませんので
            利用の際には慎重に w

        ''' 

        # 引数チェック 型    
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str  <-> {type(userid)}')
            raise TypeError

        if not isinstance(first_name, str):
            print(f'引数：first_nameの型が正しくありません str  <-> {type(first_name)}')
            raise TypeError

        if not isinstance(last_name, str):
            print(f'引数：last_nameの型が正しくありません str  <-> {type(last_name)}')
            raise TypeError

        if not isinstance(mail, str):
            print(f'引数：mailの型が正しくありません str  <-> {type(mail)}')
            raise TypeError

        if not isinstance(INIT_PASS, str):
            print(f'引数：INIT_PASSの型が正しくありません str  <-> {type(INIT_PASS)}')
            raise TypeError

        # すでにIDを作成済であれば何もしない
        if self.is_user(userid):
            print(f'すでにIDは登録済です：{userid}')
            return True

        # UserID登録API定義
        API = f'{self.URL}/api/v1/users.create'

        # メッセージ構築
        user = {
            'email':    mail,
            'name' :    f'{last_name} {first_name}',
            'password': INIT_PASS,
            'username': userid,
#            'roles':    'user',
            'requirePasswordChange': True,
        }

        # 登録処理
        try:
            response = requests.post(
                API,
                data=json.dumps(user),
                headers=self.HEADERS,)
        except Exception as e:
            print(f'API error: {e}')
            print(f'RocketChatユーザ登録に失敗しました： {userid}')
            return False
        else:
            print(f'RocketChatユーザ登録が完了しました： {userid}')
            return True
        

    def userDelete(self, userid):
        '''ユーザ削除処理

        引数情報を元にRocketChatからIDを削除する 

        Args:
           userid(str): 削除するユーザID

        Returns:

        Raises:
            TypeError: 引数型の不備
            Exception: ID削除時の例外

        Examples:
            >>> self.userDelete('PIT00000') 

        Note:
            あまりこまごまとした入力チェックをやっていませんので
            利用の際には慎重に w

            /api/v1/users.delete

        '''

        # 引数チェック 型    
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str  <-> {type(userid)}')
            raise TypeError

        # UserID登録API定義
        API = f'{self.URL}/api/v1/users.delete'

        # メッセージ構築
        user = {
            'username': userid
        }

        # すでにIDなければ何もしない
        if not self.is_user(userid):
            print(f'すでにIDは削除済です：{userid}')
            return True

        
        # 登録処理
        try:
            response = requests.post(
                API,
                data=json.dumps(user),
                headers=self.HEADERS,)
        except Exception as e:
            print(f'API error: {e}')
            print(f'RocketChatユーザ削除に失敗しました： {userid}')
            return False
        else:
            print(f'RocketChatユーザ削除が完了しました： {userid}')
            return True


    def getAllUserList(self):
        '''RocketChatに登録してあるすべてのIDリストを取得する
        
        RocketChatに登録している全IDをリストで取得する

        Args:

        Returns:
           list: ユーザ一覧を格納したlist 

        Raises:
           API実行時のエラー 

        Examples:
            >>> list_AllUser = R.getAllUserList() 

        Note:

        '''

        # 結果格納
        _list = []

        # API定義
        API = f'{self.URL}/api/v1/users.list'

        # 取得処理
        try:
            response = requests.get(
                API,
                headers=self.HEADERS,)
        except Exception as e:
            print(f'API error: {e}')
            print(f'RocketChatユーザ一覧取得に失敗しました')
        else:
            for u in response.json()['users']:
                _list.append(u["username"])

        # 結果を返す
        finally:
            return _list
        

#    def userUpdate(self, userid):
#    #####################################################        
#    # うまくいっていない
#    #####################################################        
#        '''Pxxxxxxxxのパスワードを初期化する
#        '''
#        # 引数チェック 型    
#        if not isinstance(userid, str):
#            print(f'引数：useridの型が正しくありません str  <-> {type(userid)}')
#            raise TypeError
#
#        # ユーザ情報更新API定義
#        API = f'{self.URL}/api/v1/users.update'
#
#        # MSG組み立て
#        msg = {'userId': self.getUser_id(userid),
#                'data' :{
#                    "name": userid,
#                    "password": self.INIT_PASS,}
#              }
#        #if __DEBUG__: print(msg)
#
#        # MSG送信
#        try:
#            response = requests.post(
#                API,
#                data=json.dumps(msg),
#                headers=self.HEADERS,)
#        except Exception as e:
#            print(f'API error: {e}')
#        finally:
#            return response.json()
#
#        
    ########################################################    
    # グループ関連処理
    ########################################################
    # RocketChatのグループは管理者からどうこうする話ではない。
    # グループ処理は何もしない。
    def userGroupAdd(self, group, userid):
        pass
        
    def userGroupDelete(self, group, userid):
        pass
        
    ########################################################    
    # チェック処理
    ########################################################
    def is_user(self, userid):
        '''User名のid情報を取得する
        
        指定したユーザIDがRocketChatに存在するか判定する

        Args:
           userid: ユーザ名

        Returns:
           True:  ユーザIDが存在する
           False: ユーザIDが存在しない

        Raises:
           API実行時のエラー 

        Examples:
            >>> R.getUser_id('PIT00000') 

        Note:
            self.getAllUserList()を使用しユーザ一覧listを判定に使用する

        '''
         
        # Redmineに登録してあるユーザID一覧を取得する
        _list = self.getAllUserList()

        # 引数にしていたユーザ存在を判定
        if userid in _list:
            print(f'指定IDは存在します: {userid}')
            return True
        else:
            print(f'指定IDは存在しません: {userid}')
            return False
 

    def is_userGroup(self, group):
        '''RocketChatではユーザグループを設定しない予定'''
        pass
        

    def is_userInTheGroup(self, group, userid):
        '''RocketChatではユーザグループを設定しない予定'''
        pass


    ########################################################    
    # リリースID取得処理 groupに仕様制約多い
    ########################################################
    def getGroupMap(self):
        pass

    def getGroupResourceID(self, group):
        pass
    
    def getUserResouceID(self, userid):
        pass
