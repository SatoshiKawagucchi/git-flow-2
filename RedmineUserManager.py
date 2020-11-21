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
import redminelib
import requests
import sys

from pprint import pprint
from redminelib import Redmine

# 個別ライブラリ
from UserManager import BaseUserManager

################################################
# 独自例外定義 
################################################
#class MaxRetryError(Exception):
#    pass
#
################################################
# RedmineUserManager 
################################################

class RedmineUserManager(BaseUserManager):
    """Redmineユーザ管理Class

     Redmineのユーザ管理を行う。
       ユーザ追加、削除、変更
       グループへユーザ追加、削除

    Attributes:
        API_KEY (int)   : Redmineのadmin API key
        HOST (bool)     : Redmineのホスト 

    """
    
    def __init__(self, HOST, API_KEY):
        """Redmineインスタンス生成

        API_KEY,HOSTからRedmineインスタンスを返す

        Args:
            HOST (str):      Redmine Host 
            API_KEY (str):   adminに応じたAPI_KEY

        Returns:

        Raises:
            TypeError: 引数型の不備
            Exception: Redmineインスタンス生成不備

        Examples:
            >>> redmine = RedmineUserManager(HOST, API_KEY) 

        Note:
            Redmineのグループは事前に存在する必要があります。
            新しいグループが記載されたとしても自動でRedmine上で作成しません。
            __init__ではboolを返してはならないので留意

        """ 

        # 引数チェック 型    
        if not isinstance(HOST, str):
            print(f'引数：HOSTの型が正しくありません str <-> {type(HOST)}')
            raise TypeError

        if not isinstance(API_KEY, str):
            print(f'引数：API_KEYの型が正しくありません str <-> {type(API_KEY)}')
            raise TypeError
            
        # Redmineインスタンス生成（self.redmine）
        self.redmine = None
        try:
            self.redmine = Redmine(HOST, key=API_KEY)
        except exception as e: 
            print(f'Redmine Instance生成に失敗しました')
            print(f'エラー詳細：{e}')
        else:
            if not isinstance(self.redmine, redminelib.Redmine):
                print(f'Redmine Instance生成に失敗しました')
                raise Exception
            
            # Group ResouceMap生成（都度生成は無駄なので共有できる資源として最初に生成／維持する）
            # Redmineインスタンス生成はデタラメなHOSTでも生成できてしまう仕様
            # 生成したRedmineインスタンスに対し情報取得アクションにより正常？を判定する
            try:
                # 生成したRedmineインスタンスに対しアクション
                self.groupmap = self.getGroupMap()
            except Exception as e:
                print(f'正常にインスタンス生成できていません： {e}')
            else:  
                # 初期処理完了
                print(f'ユーザ管理初期処理が完了しました')
            
            
    ########################################################    
    # ユーザID関連処理
    ########################################################
    def userAdd(self, userid, first_name, last_name, mail, INIT_PASS):
        '''ユーザID登録

        引数情報を元にRedmineにIDを追加する 
        次回ログイン時はパスワード変更を求められます

        Args:
           userid(str): 登録するユーザID
           first_name(str): 名前
           last_name(str): 姓
           mail(str): 割り当てられたメールアドレス
           INIT_PASS(str): 初期パスワード

        Returns:

        Raises:
            TypeError: 引数型の不備
            Exception: ID登録時の例外

        Examples:
            >>> self.userAdd('PIT00000', 'Satoshi', 'Suzuki', satoshi_10_suzuki@mufg.jp, INIT_PASS) 

        Note:
            あまりこまごまとした入力チェックをやっていませんので
            利用の際には慎重に w

        '''

        # 引数チェック 型    
        #TODO NULLチェックとか文字列フォーマットチェックとか
 
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError
            
        if not isinstance(first_name, str):
            print(f'引数：first_nameの型が正しくありません str <-> {type(first_name)}') 
            raise TypeError
            
        if not isinstance(last_name, str):
            print(f'引数：last_nameの型が正しくありません str <-> {type(last_name)}')
            raise TypeError
            
        if not isinstance(mail, str):
            print(f'引数：mailの型が正しくありません str <-> {type(mail)}')
            raise TypeError
            
        if not isinstance(INIT_PASS, str):
            print(f'引数：INIT_PASSの型が正しくありません str <-> {type(INIT_PASS)}')
            raise TypeError
           
        # 登録処理
        print(f'ユーザIDを登録します： {userid}')
        try:
            # ユーザ登録実施：API
            u = self.redmine.user.create(login=userid,
                                         firstname=first_name,
                                         lastname=last_name,
                                         mail=mail,
                                         password=INIT_PASS,
                                         must_change_passwd=True,
                                         send_information=False)
        except Exception as e:
            print(f'ユーザ登録に失敗しました：{userid}')
            print(f'エラー詳細：{e}')
            print()
        else:
            # 登録完了チェック
            if u.id:
                print(f'ユーザID登録が完了しました： ID.No {u.id} : {userid}')
                return True 
            else:
                print(f'すでにユーザIDは登録済です： ID.No {u.id} : {userid}')
                return False

        
    def userDelete(self, userid):
        '''ユーザ削除処理

        引数情報を元にRedmineからIDを削除する 

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

        '''
        # 引数チェック 型    
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError
            
        # 存在チェック
        if self.is_user(userid):
            # 削除対処ID情報取得
            try:
                obj_user = self.redmine.user.filter(name=userid)
            except Exception as e:
                print(f'ユーザ情報取得エラー: {userid}: {e}')
            else:
                # 削除処理実施
                try:
                    obj_user.delete()
                except Exception as e:
                    print(f'ユーザ削除エラー：{userid} {e}')
                    return False
                else:
                    print(f'ユーザ削除完了しました：{userid}')
                    return True
        else:
            print(f'削除対象IDが存在しません：{userid}')
            return False
        

    def userUpdate(self, userid, INIT_PASS):
        '''ユーザ情報をUpdateする。
        
        ここではパスワード初期化を想定する。
        機能拡張する場合は頑張ってください。
         

        Args:
           userid(str): 削除するユーザID

        Returns:

        Raises:
            TypeError: 引数型の不備
            Exception: ID情報更新時の例外

        Examples:
            >>> self.userDelete('PIT00000') 

        Note:
            あまりこまごまとした入力チェックをやっていませんので
            利用の際には慎重に w

        '''
        # 引数チェック 型    
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError

        if not isinstance(INIT_PASS, str):
            print(f'引数：INIT_PASSの型が正しくありません str <-> {type(INIT_PASS)}')
            raise TypeError
            
        if self.is_user(userid):
            # 更新対処ID情報取得
            try:
                self.redmine.user.filter(name=userid).update(
                    password = INIT_PASS,
                    must_change_passwd = True,)
            except Exception as e:
                print(f'ユーザ情報更新エラー：{userid} {e}')
                return False
            else:
                print(f'ユーザ情報更新完了しました／パスワード初期化：{userid}')
                return True
        else:
            print(f'更新対象IDが存在しません：{userid}')
            return False


    ########################################################    
    # グループ関連処理
    ########################################################
    def userGroupAdd(self, group, userid):
        '''ユーザIDをグループに追加する
        
        指定したグループ名にユーザIDを追加する。 
        

        Args:
           group(str): 追加するグループ名
           userid(str): 追加するユーザID

        Returns:

        Raises:
            TypeError: 引数型の不備
            Exception: ID登録時の例外

        Examples:
            >>> self.userGroupAdd('開発推進チーム', 'PIT00000') 

        Note:
            あまりこまごまとした入力チェックをやっていませんので
            利用の際には慎重に w

        '''        

        # 引数チェック 型    
        if not isinstance(group, str):
            print(f'引数：groupの型が正しくありません str <-> {type(group)}')
            raise TypeError
            
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError
        
        # そもそもRedmineに指定IDが存在しない
        if not self.is_user(userid):
            print(f'指定ユーザIDがRedmineに存在しません: {userid}')           
            return False

        # 指定グループが存在しない
        if not self.is_userGroup(group):
            print(f'登録グループは存在しません: {group}')
            return False

        # 既に登録済か？
        (result, obj_group, obj_user) = self.is_userInTheGroup(group, userid)
            
        # 指定グループ（存在する）にIDが存在しない場合にのみ実施
        if not result:
            try:
                obj_group.user.add(obj_user)
            except Exception as e:
                print(f'{e}')
            else:
                print(f'グループへID登録が完了しました: {group}: {userid}')
                return True
        else:
            print(f'ユーザIDはすでにグループに登録済です: {group}:{userid}')
            return False
        

    def userGroupDelete(self, group, userid):
        '''ユーザIDをグループから削除する
        
        指定したグループ名からユーザID削除する。 

        Args:
           group(str): 追加するグループ名
           userid(str): 追加するユーザID

        Returns:

        Raises:
            TypeError: 引数型の不備
            Exception: ID削除時の例外

        Examples:
            >>> self.userGroupDelete('開発推進チーム', 'PIT00000') 

        Note:
            あまりこまごまとした入力チェックをやっていませんので
            利用の際には慎重に w
        '''        
        # 引数チェック 型    
        if not isinstance(group, str):
            print(f'引数：groupの型が正しくありません str <-> {type(group)}')
            raise TypeError
            
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError

        # そもそもRedmineに指定IDが存在しない
        if not self.is_user(userid):
            print(f'指定ユーザIDがRedmineに存在しません: {userid}')           
            return False

        # 指定グループが存在しない
        if not self.is_userGroup(group):
            print(f'登録グループは存在しません: {group}')
            return False

        # 既に登録済か？
        (result, obj_group, obj_user) = self.is_userInTheGroup(group, userid)
        # 指定グループにIDが存在する場合にのみ実施
        if result:
            try:
                obj_group.user.remove(obj_user)
            except Exception as e:
                print(f'{e}')
                return False
            else:
                print(f'グループからID削除処理が完了しました: {group}: {userid}')
                return True
        else:
            print(f'ユーザIDはすでにグループに削除済です: {group}:{userid}')        
            return False
        

    ########################################################    
    # チェック処理
    ########################################################
    def is_user(self, userid):
        '''Redmine ユーザID存在チェック
        
        Redmineに指定ユーザIDが存在するかチェックする

        Args:
           userid(str): 確認するユーザID

        Returns:
           true: 存在する
           false: 存在しない

        Raises:
            TypeError: 引数型の不備
            Exception: 存在チェック事の例外

        Examples:
            >>> self.is_user('PIT00000') 

        Note:
            あまりこまごまとした入力チェックをやっていませんので
            利用の際には慎重に w
               
        '''
        # 引数チェック 型    
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError
            
        # 探索ループ初期処理
        is_account = False

        # 登録IDがすでに存在しているかチェック    
        for _ in self.redmine.user.filter(name=userid):
            if _.login == userid:
                is_account = True
                break

        return is_account


    def is_userGroup(self, group):
        '''Redmine グループ存在チェック
        
        Redmineに指定グループ名が存在するかチェックする

        Args:
           group(str): 確認するグループ名

        Returns:
           true: 存在する
           false: 存在しない

        Raises:
            TypeError: 引数型の不備
            Exception: 存在チェック事の例外

        Examples:
            >>> self.is_userGroup('開発推進チーム') 

        Note:
            あまりこまごまとした入力チェックをやっていませんので
            利用の際には慎重に w

        '''

        # 引数チェック 型    
        if not isinstance(group, str):
            print(f'引数：groupの型が正しくありません str <-> {type(group)}')
            raise TypeError
            
        # チェックフラグ
        is_extend = False

        # 存在チェック
        try:
            self.groupmap[group]        
        except Exception as e:
            '''存在しないとExceptionが発生する'''
        else:
            is_extend = True
        finally:
            return is_extend      


    def is_userInTheGroup(self, group, userid):
        '''グループにそのユーザが存在するか
        
        指定グループに指定ユーザIDが存在するかチェックする

        Args:
           group(str): 確認するグループ名
           userid(str): 確認するユーザID

        Returns:
           true: 存在する
           false: 存在しない

        Raises:
            TypeError: 引数型の不備
            Exception: 存在チェック事の例外

        Examples:
            >>> self.is_userInTheGroup('開発推進チーム', 'PIT00000') 

        Note:
            あまりこまごまとした入力チェックをやっていませんので
            利用の際には慎重に w
        '''
        # 引数チェック 型    
        if not isinstance(group, str):
            print(f'引数：groupの型が正しくありません str <-> {type(group)}')
            raise TypeError
            
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError
        
        # グループのUser一覧を取得する
        obj_group = self.redmine.group.get(self.getGroupResourceID(group), include='users')
        
        # その中にユーザIDが存在するか→どっちの結果の戻り値も使うことに留意
        obj_id = self.getUserResourceID(userid)
        for g in list(obj_group.users):
            # ID存在チェック
            if g.id == obj_id:
                # すでにグループ登録済判定
                # 結果とすでに得たグループオブジェクト、ターゲットリソースIDを返す
                return True, obj_group, obj_id
        
        # グループに登録未済
        # 結果とすでに得たグループオブジェクト、ターゲットリソースIDを返す
        return False, obj_group, obj_id

    ########################################################    
    # リリースID取得処理 groupに仕様制約多い
    ########################################################
    def getGroupMap(self):
        '''グループ名とリソースIDのmapを作る        
        イニシャル処理でmap生成してください。呼び出しの都度Map生成は無駄なので。
        
        Args:

        Returns:
           g_map(map): グループ名とグループIDのマップ、グループ全量 

        Raises:
            TypeError: 引数型の不備
            Exception: グループ一覧取得時の例外

        Examples:
            >>> self.getGroupMap() 

        Note:
            あまりこまごまとした入力チェックをやっていませんので

        '''

        # 結果入れ物用意
        g_map = {}
        # 情報取得
        try:
            g_all = self.redmine.group.all()
        except Exception as e:
            print(f'Redmineグループ一覧取得に失敗しました： {e}')
        else:
            # map生成
            try:
                for g in g_all:
                    g_map[g.name]= g.id
            except Exception as e:
                print(f'Redmineグループ一覧取得に失敗しました： {e}')
                return False
            else:
                print(f'Redmineグループ一覧取得に成功しました')
                # 結果を返す
                return g_map
        

    def getGroupResourceID(self, group):
        '''グループ名とリソースIDのmapからリソースIDを取得する
        '''
        # 引数チェック 型    
        if not isinstance(group, str):
            print(f'引数：groupの型が正しくありません str <-> {type(group)}')
            raise TypeError
            
        # 指定グループ名存在＆グループリソースIDを返す
        if self.is_userGroup(group):
            return self.groupmap[group]
        else:
            False
    

    def getUserResourceID(self, userid):
        '''loginIDからユーザリソースIDを取得する
        '''
        # 引数チェック 型    
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError
        
        # 指定ユーザID存在＆ユーザリソースIDを返す
        if self.is_user(userid):
            # 探索方法が少々特殊
            for u in list(self.redmine.user.filter(name=userid)):
                id = u.id
            return id
        else:
            return False


    def judgeTargetGroupname(self, VENDER_MAP, company, manager, lycheeUser):
        """引数情報から所属グループ名を返す
    
         所属会社、業遂、Lychee利用有無から追加するグループ名を決定する
    
        Args:
            company (str):     ユーザIDから自動的に決定する4文字の所属会社識別子
            manager (bool):    業遂か非業遂か
            LycheeUser (bool): Lychee利用許可者か否か
    
        Returns:
           str: 所属グループ名
    
        Raises:
            TypeError: 引数型の不備
    
        Examples:
            >>> judgeTargetGroupname('PHSL',True,True)
               一括（業遂）
        Note:
            Redmineのグループは事前に存在する必要があります。
            新しいグループが記載されたとしても自動でRedmine上で作成しません。

        """    

        # 引数チェック 型    
        if not isinstance(VENDER_MAP, dict):
            print(f'引数：VENDER_MAPの型が正しくありません map <-> {type(VENDER_MAP)}')
            raise TypeError
        
        if not isinstance(company, str):
            print(f'引数：companyの型が正しくありません str <-> {type(company)}')
            raise TypeError
        
        if not isinstance(manager, bool):
            print(f'引数：managerの型が正しくありません bool <-> {type(manager)}')
            raise TypeError
        
        if not isinstance(lycheeUser, bool):
            print(f'引数：lycheeUserの型が正しくありません bool <-> {type(lycheeUser)}')
            raise TypeError
    
        if not VENDER_MAP:
            print(f'VENDER_MAPオブジェクトが存在しません')
            raise NameError
            
        # 業遂／非業遂／Lychee利用判定
        try:
            # 業遂でLychee利用有無判定
            if manager:
                if not lycheeUser:
                    return f'{VENDER_MAP[company]}（業遂）（Lycheeなし）'
                else:
                    return f'{VENDER_MAP[company]}（業遂）'
            else:
            # 非業遂でLychee利用有無判定
                if not lycheeUser:
                    return f'{VENDER_MAP[company]}（非業遂）'
                else:
                    return f'{VENDER_MAP[company]}（非業遂）（Lycheeあり）'
        except Exception as e:
            print(f'Error: 指定したベンダーコードは存在しません {e}')
            return False
        else:
            return False
    
