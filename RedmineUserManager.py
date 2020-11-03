#-------------------------------------------------
# library
import json
import requests

from pprint import pprint
from redminelib import Redmine
#-------------------------------------------------
# BaseClass
class BaseUserManager(object):
    '''メソッド実装強制
    
    ユーザID及びグループメンテナンスメソッド定義。
    Redmineだけでなく各OSS向けの共通メソッド定義。
    
    Attributes:
        なし
    '''
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
#-------------------------------------------------        
def judge_target_groupname(company, manager, lycheeUser):
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
        >>> judge_target_groupname('PHSL',True,True)
           一括（業遂）
    Note:
        Redmineのグループは事前に存在する必要があります。
        新しいグループが記載されたとしても自動でRedmine上で作成しません。
    """    
    # 引数チェック 型    
    if not isinstance(company, str):
        print(f'引数：companyの型が正しくありません str <-> {type(company)}')
        raise TypeError
    
    if not isinstance(manager, bool):
        print(f'引数：managerの型が正しくありません bool <-> {type(manager)}')
        raise TypeError
    
    if not isinstance(lycheeUser, bool):
        print(f'引数：lycheeの型が正しくありません bool <-> {type(lychee)}')
        raise TypeError

    # 非業遂判定
    if not manager:
        return f'{VENDER_MAP[company]}（非業遂）'
    else:
        # 業遂でLychee利用有無判定
        if not lycheeUser:
            return f'{VENDER_MAP[company]}（業遂）（Lycheeなし）'
        else:
            return f'{VENDER_MAP[company]}（業遂）'
        
#-------------------------------------------------        
class RedmineUserManager(BaseUserManager):
    """Redmineユーザ管理Class

     Redmineのユーザ管理を行う。
       ユーザ追加、削除、変更
       グループへユーザ追加、削除

    Attributes:
        API_KEY (int)   : Redmineのadmin API key
        HOST (bool)     : Redmineのホスト 
    """
    
    def __init__(self, API_KEY, HOST):
        """Redmineインスタンス生成

        API_KEY,HOSTからRedmineインスタンスを返す

        Args:
            API_KEY (str):   ユーザIDから自動的に決定する4文字の所属会社識別子
            HOST (str):      業遂か非業遂か

        Returns:
           str: 所属グループ名

        Raises:
            TypeError: 引数型の不備

        Examples:
            >>> judge_target_groupname('PHSL',True,True)
               一括（業遂）
        Note:
            Redmineのグループは事前に存在する必要があります。
            新しいグループが記載されたとしても自動でRedmine上で作成しません。
        """ 
        # 引数チェック 型    
        if not isinstance(API_KEY, str):
            print(f'引数：API_KEYの型が正しくありません str <-> {type(API_KEY)}')
            raise TypeError
            
        if not isinstance(HOST, str):
            print(f'引数：HOSTの型が正しくありません str <-> {type(HOST)}')
            raise TypeError
            
        # インスタンス変数生成
        self.API_KEY = API_KEY
        self.HOST = HOST

        # Redmineインスタンス生成（self.redmine）
        try:
            self.redmine = Redmine(self.HOST, key=self.API_KEY)
        except Exception as e:
            print(f'Redmine Instance生成に失敗しました')
            print(f'詳細：{e}')
        else:
            print(f'Redmine Instanceを生成しました： {self.redmine}')
            
        # Group ResouceMap生成（都度生成は無駄なので共有できる資源として最初に生成／維持する）
        self.groupmap = self.getGroupMap()
        
        # 初期処理完了
        print(f'ユーザ管理初期処理が完了しました')
            
            
    ########################################################    
    # ユーザID関連処理
    ########################################################
    def userAdd(self, userid, first_name, last_name, mail, INIT_PASS):
        '''ユーザID登録
        '''
        # 引数チェック 型    
        #TODO mail→メールフォーマットチェック
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

        
    def userDelete(self, userid):
        '''ユーザ削除処理
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
                else:
                    print(f'ユーザ削除完了しました：{userid}')
        else:
            print(f'削除対象IDが存在しません：{userid}')
        

    def userUpdate(self, userid):
        '''
        ユーザ登録情報をUpdateする機会／／／たぶんない
        と思ったが、パスワード初期化があるかも。        
        '''
        # 引数チェック 型    
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError
            
        if self.is_user(userid):
            # 更新対処ID情報取得
            try:
                self.redmine.user.filter(name=userid).update(
                    password = INIT_PASS,
                    must_change_passwd = True,)
            except Exception as e:
                print(f'ユーザ情報更新エラー：{userid} {e}')
            else:
                print(f'ユーザ情報更新完了しました／パスワード初期化：{userid}')
        else:
            print(f'更新対象IDが存在しません：{userid}')


    ########################################################    
    # グループ関連処理
    ########################################################
    def userGroupAdd(self, group, userid):
        '''ユーザIDをグループに追加する
        '''        
        # 引数チェック 型    
        if not isinstance(group, str):
            print(f'引数：groupの型が正しくありません str <-> {type(group)}')
            raise TypeError
            
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError

        # 既に登録済か？
        (result, obj_group, obj_user) = self.is_userInTheGroup(group, userid)
        # 指定グループにIDが存在しない場合にのみ実施
        if not result:
            try:
                obj_group.user.add(obj_user)
            except Exception as e:
                print(f'{e}')
            else:
                print(f'グループへID登録が完了しました: {group}: {userid}')
        else:
            print(f'ユーザIDはすでにグループに登録済です: {group}:{userid}')
        

    def userGroupDelete(self, group, userid):
        '''ユーザIDをグループから削除する
        '''        
        # 引数チェック 型    
        if not isinstance(group, str):
            print(f'引数：groupの型が正しくありません str <-> {type(group)}')
            raise TypeError
            
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError

        # 既に登録済か？
        (result, obj_group, obj_user) = self.is_userInTheGroup(group, userid)
        # 指定グループにIDが存在する場合にのみ実施
        if result:
            try:
                obj_group.user.remove(obj_user)
            except Exception as e:
                print(f'{e}')
            else:
                print(f'グループからID削除処理が完了しました: {group}: {userid}')
        else:
            print(f'ユーザIDはすでにグループに削除済です: {group}:{userid}')        
        
    ########################################################    
    # チェック処理
    ########################################################
    def is_user(self, userid):
        '''Redmine ユーザID存在チェック
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
                
        # ID存在結果判定
        if is_account:
            print(f'{userid} は登録されています')
        
        return is_account

    def is_userGroup(self, group):
        '''Redmine グループ存在チェック
        '''
        # 引数チェック 型    
        if not isinstance(group, str):
            print(f'引数：groupの型が正しくありません str <-> {type(group)}')
            raise TypeError
            
        # 存在チェック
        try:
            self.groupmap[group]        
        except Exception as e:
            '''存在しないとExceptionが発生する'''
            return False
        else:
            return True
        
    def is_userInTheGroup(self, group, userid):
        '''グループにそのユーザが存在するか
        '''
        # 引数チェック 型    
        if not isinstance(group, str):
            print(f'引数：groupの型が正しくありません str <-> {type(group)}')
            raise TypeError
            
        if not isinstance(userid, str):
            print(f'引数：useridの型が正しくありません str <-> {type(userid)}')
            raise TypeError
        
        # まずそのグループが存在するか
        if self.is_userGroup(group):
            # グループのUser一覧を取得する
            obj_group = self.redmine.group.get(self.getGroupResourceID(group), include='users')
            
            # その中にユーザIDが存在するか→どっちの結果の戻り値も使うことに留意
            obj_id = self.getUserResouceID(userid)
            for g in list(obj_group.users):
                # ID存在チェック
                if g.id == obj_id:
                    # 結果とすでに得たグループオブジェクト、ターゲットリソースIDを返す
                    return True, obj_group, obj_id
                
            # 結果とすでに得たグループオブジェクト、ターゲットリソースIDを返す
            return False, obj_group, obj_id
                
        else:
            # どうにもならん
            return False, False, False

    ########################################################    
    # リリースID取得処理 groupに仕様制約多い
    ########################################################
    def getGroupMap(self):
        '''グループ名とリソースIDのmapを作る        
        イニシャル処理でmap生成してください。呼び出しの都度Map生成は無駄なので。
        '''
        # 結果入れ物用意
        g_map = {}
        # 情報取得
        try:
            g_all = self.redmine.group.all()
        except Exception as e:
            print(f'Redmineグループ一覧取得に失敗しました： {e}')
        else:
            print(f'Redmineグループ一覧取得に成功しました')

        # map生成
        for g in g_all:
            g_map[g.name]= g.id

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
    
    def getUserResouceID(self, userid):
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
#-------------------------------------------------                
import pandas as pd
columns = ['ログインID','名前','姓','メールアドレス','所属','他部','Lychee利用者','業遂','登録種別','参加RedmineProject','対応種別','依頼責任者','実施希望日','ステータス','備考']
user_list1 = [
    ['PIT00100', '鈴木','哲A', 'satoshi_A_suzuki@mufg.jp','PIT0', "DP部",True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00110', '鈴木','哲B', 'satoshi_B_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00120', '鈴木','哲C', 'satoshi_C_suzuki@mufg.jp','PIT0', False,True,False,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00130', '鈴木','哲D', 'satoshi_D_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00140', '鈴木','哲E', 'satoshi_E_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00150', '鈴木','哲F', 'satoshi_F_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00160', '鈴木','哲G', 'satoshi_G_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00170', '鈴木','哲H', 'satoshi_H_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00180', '鈴木','哲I', 'satoshi_I_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00190', '鈴木','哲J', 'satoshi_J_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00200', '鈴木','哲K', 'satoshi_K_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00210', '鈴木','哲L', 'satoshi_L_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00220', '鈴木','哲M', 'satoshi_M_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00230', '鈴木','哲N', 'satoshi_N_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00240', '鈴木','哲O', 'satoshi_O_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00250', '鈴木','哲P', 'satoshi_P_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00260', '鈴木','哲Q', 'satoshi_Q_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00270', '鈴木','哲R', 'satoshi_R_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00280', '鈴木','哲S', 'satoshi_S_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00290', '鈴木','哲T', 'satoshi_T_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00300', '鈴木','哲U', 'satoshi_U_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","着任","やまはなさん","2020/10/31","済","特になし"],
]
user_list2 = [
    ['PIT00100', '鈴木','哲A', 'satoshi_A_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00110', '鈴木','哲B', 'satoshi_B_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00120', '鈴木','哲C', 'satoshi_C_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00130', '鈴木','哲D', 'satoshi_D_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00140', '鈴木','哲E', 'satoshi_E_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00150', '鈴木','哲F', 'satoshi_F_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00160', '鈴木','哲G', 'satoshi_G_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00170', '鈴木','哲H', 'satoshi_H_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00180', '鈴木','哲I', 'satoshi_I_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00190', '鈴木','哲J', 'satoshi_J_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00200', '鈴木','哲K', 'satoshi_K_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00210', '鈴木','哲L', 'satoshi_L_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00220', '鈴木','哲M', 'satoshi_M_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00230', '鈴木','哲N', 'satoshi_N_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00240', '鈴木','哲O', 'satoshi_O_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00250', '鈴木','哲P', 'satoshi_P_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00260', '鈴木','哲Q', 'satoshi_Q_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00270', '鈴木','哲R', 'satoshi_R_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00280', '鈴木','哲S', 'satoshi_S_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00290', '鈴木','哲T', 'satoshi_T_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
    ['PIT00300', '鈴木','哲U', 'satoshi_U_suzuki@mufg.jp','PIT0', False,True,True,"Redmine","全体WBS","離任","やまはなさん","2020/10/31","済","特になし"],
]

df_users_add = pd.DataFrame(user_list1)
df_users_del = pd.DataFrame(user_list2)

df_users_add.columns = columns
df_users_del.columns = columns

#-------------------------------------------------                
def main():
    
    __DEBUG__ = True
    
    # Redmine インスタンス生成
    redmine = RedmineUserManager(API_KEY, HOST)
    
    # 処理対象ユーザ一覧取得
    # dfに格納済とする（会社の環境に作成済）
    
    # 対象データループ
    for userid, first_name, last_name, mail, company, other_dep,is_lychee, is_manager, handle \
        in zip(df_users['ログインID'], 
               df_users['名前'], 
               df_users['姓'],
               df_users['メールアドレス'],
               df_users['所属'], 
               df_users['他部'],                
               df_users['Lychee利用者'],
               df_users['業遂'],
               df_users['対応種別']
              ):
        
        if __DEBUG__:
            print(userid, first_name, last_name, mail, company, other_dep, is_lychee, is_manager, handle)
            
        # ユーザ処理
        ## 注：ユーザ処理は何れLDAPに移行することを見越してユーザ処理とグループ処理を分離して記述する
        
        ## ユーザ追加
        if handle == "着任":
            redmine.userAdd(userid, first_name, last_name, mail, INIT_PASS)
        ## ユーザ削除
        elif handle == "離任":
            redmine.userDelete(userid)
        ## パスワード初期化
        elif handle == "パスワード初期化":
            redmine.userUpdate(userid)
        else:
            continue
        
        # グループ処理
        ## 他部に対してはマニュアル対応のためバイパス
        if not other_dep:
            print(f'{userid}はダイレクト所属のためグループ処理を行います')
            if handle == "着任":
                redmine.userGroupAdd(judge_target_groupname(company, is_manager, is_lychee), userid)
            elif handle == "離任":
                # ID削除するとグループからも自動削除されるが、、、LDAPになった時にどうなるのかなあ。。。
                redmine.userGroupDelete(judge_target_groupname(company, is_manager, is_lychee), userid)
            else:
                # 着任、離任以外はグループ処理を行わない
                continue
            
        else:
            print(f'{userid}は他部所属のためグループ処理をバイパスします')

            
#######################

# test用にInput差し替え
df_users = df_users_del.copy()
main()
print('-'*80)
df_users = df_users_add.copy()
main()
print('-'*80)
















