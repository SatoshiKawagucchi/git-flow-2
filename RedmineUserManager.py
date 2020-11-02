# library
import json
import requests

from pprint import pprint
from redminelib import Redmine

# BaseClass
class BaseUserManager(object):
    '''メソッド実装強制
    
    ユーザID及びグループメンテナンスメソッド定義
    
    '''
    
    '''ユーザ自体の保守はLDAPになる予定のため暫定処理'''
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


# インスタンス生成情報
# TODO:yaml化        
API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
HOST = 'http://192.168.179.3:3100'
INIT_PASS = "p@ssw0rd"
DEBUG = True



class RedmineUserManager(BaseUserManager):

    def __init__(self, API_KEY, HOST, INIT_PASS):
 
        # インスタンス変数生成
        self.API_KEY = API_KEY
        self.HOST = HOST
        self.INIT_PASS = INIT_PASS
        

        # Redmineインスタンス生成（self.redmine）
        try:
            self.redmine = Redmine(self.HOST, key=self.API_KEY)
        
        except Exception as e:
            print(f'Redmine インスタンス生成に失敗しました')
            print(f'詳細：{e}')
        
        finally:
            print(f'{self.redmine}')
            
        # Group ResouceMap生成（都度生成は無駄なので共有できる資源として最初に生成／維持する）
        self.groupmap = self.getGroupMap()
            
            
    ########################################################    
    # ユーザID関連処理
    ########################################################
    def userAdd(self, userid, first_name, last_name, mail):
        '''ユーザID登録
        
        '''
        print(f'ユーザIDを登録します： {userid}')
        try:
            # ユーザ登録実施：API
            print(f'init pass {self.INIT_PASS}')
            u = self.redmine.user.create(login=userid,
                                         firstname=first_name,
                                         lastname=last_name,
                                         mail=mail,
                                         password=self.INIT_PASS,
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

        
    def userDelete(self, userid):
        '''ユーザ削除処理
        
        '''
        # 存在チェック
        #print(self.is_user(userid))
        if self.is_user(userid):
            # 削除対処ID情報取得
            try:
                user = self.redmine.user.filter(name=userid)
            except Exception as e:
                print(f'ユーザ情報取得エラー: {userid}: {e}')
            else:
                # 削除処理実施
                try:
                    user.delete()
                
                except Exception as e:
                    print(f'ユーザ削除エラー：{userid} {e}')
                
                else:
                    print(f'ユーザ削除完了しました：{userid}')
        else:
            print(f'削除対象IDが存在しません：{userid}')
        

    def userUpdate(self, userid):
        '''
        ユーザ登録情報をUpdateする機会／／／たぶんない
        と思ったが、パスワード初期化があるかも。        
        '''
        if self.is_user(userid):
            # 更新対処ID情報取得
            try:
                self.redmine.user.filter(name=userid).update(
                password = self.INIT_PASS,
                must_change_passwd = True,)
                
            except Exception as e:
                print(f'ユーザ情報更新エラー：{userid} {e}')

            else:
                print(f'ユーザ情報更新完了しました／パスワード初期化：{userid}／{self.INIT_PASS}')

        else:
            print(f'更新対象IDが存在しません：{userid}')


    ########################################################    
    # グループ関連処理
    ########################################################
    def userGropuAdd(self, group, userid):
        '''ユーザIDをグループに追加する
        
        扱いやすいようにグループ及びユーザIDのリソースマップを作成しそれを活用する。

        ↓リソースIDでなくても扱えるようにしている。
          group: グループ名称
          userid: PXXXXXXX ユーザ名
        
        '''
        group = self.redmine.group.get(self.getGroupResourceID(group), include='users')
        print(group)
        user = self.getUserResouceID(userid)
        print(user)
        
        # 判定（指定グループにIDが存在しない場合にのみ実施）
        if self.is_userInTheGroup(group, userid):
            group.user.add(user)
        else:
            print(f'ユーザIDはすでにグループに登録済です: {group}:{userid}')
        

    def userGropuDelete(self, group, userid):
        group = self.redmine.group.get(self.getGroupResourceID(group), include='users')
        print(group)
        user = self.getUserResouceID(userid)
        print(user)
        
        group.user.remove(user)
        
        
    ########################################################    
    # チェック処理
    ########################################################
    def is_user(self, userid):
        '''Redmine ユーザID存在チェック

        Args:
            userid   : 探索対象ユーザID

        Returns:
            True/False： 存在する/存在しない

        Example:
            >>> redmine = RedmineUserManager(API_KEY, HOST, INIT_PASS)
            >>> redmine.is_user('PIT00554')

        Notes:

        '''
        # 探索ループ初期処理
        is_account = False

        # 登録IDがすでに存在しているかチェック    
        for _ in self.redmine.user.filter(name=userid):
            if _.login == userid:
                is_account = True
                break
                
        # ID存在結果判定
        if is_account:
            print(f'{userid} は登録されています')
        
        return is_account

    def is_userGroup(self,group):
        '''グループが存在するか'''
        try:
            print(self.groupmap[group])        
            return True
        except Exception as e:
            '''存在しないとExceptionが発生する'''
            return False
        
    def is_userInTheGroup(self, group, userid):
        '''グループにそのユーザが存在するか'''
        # まずそのグループが存在するか
        if self.is_userGroup(group):
            # グループのUser一覧を取得する
            group = self.redmine.group.get(self.getGroupResourceID(group), include='users')
            # その中にユーザIDが存在するか
            target_resouce_id = self.getUserResouceID(userid)
            for g in list(group.users):
                print(g.id, target_resouce_id)
                if g.id == target_resouce_id:
                    return True
            return False
                
        else:
            return False

    ########################################################    
    # リリースID取得処理 groupに仕様制約多い
    ########################################################
    def getGroupMap(self):
        '''グループ名とリソースIDのmapを作る        
        イニシャル処理でmap生成してください。呼び出しの都度Map生成は無駄なので。
        '''
        if self.is_userGroup:
            g_all = self.redmine.group.all()
            g_map = {}
            for g in g_all:
                #print(list(g))
                g_map[g.name]= g.id

            return g_map

    def getGroupResourceID(self, group):
        '''グループ名とリソースIDのmapからリソースIDを取得する
        '''
        if self.is_userGroup:
            return self.groupmap[group]

    
    def getUserResouceID(self, userid):
        '''loginIDからユーザリソースIDを取得する
        '''
        if self.is_user(userid):        
            for u in list(r.user.filter(name=userid)):
                id = u.id

            return id
