#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-

''' UserManager.pyのテストクラス
'''

##########################################
# library テスト実行環境構築向け
##########################################
import pytest
import sys
from pathlib2 import Path
from pprint import pprint
import redminelib

import requests
import urllib3

##########################################
# 環境構築 
# test対象ライブラリPath設定
#   Pathオブジェクトそのものでなく
#   str変換した文字列を渡す
##########################################
__DEBUG__ = True
LIBPATH = Path('/home/satoshi/work/jenkins_script/app/python/bin')
if __DEBUG__: print(LIBPATH)
sys.path.append(str(LIBPATH))

# テスト固定パラメータ設定
HOST = 'http://192.168.179.3:3100'
API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
INIT_PASS = "p@ssw0rd"
VENDER_MAP = {
    'PHSE': '一括',
    'PHSL': '一括',
    'PHTC': '一括',
    'PINC': 'INC（常駐）',
    'PNSD': 'NSD（常駐）',
    'PNDS': 'NDS（常駐）',
    'PIT0': 'MUIT'
}

if __DEBUG__:
    pprint(HOST)
    pprint(API_KEY)
    pprint(INIT_PASS)
    pprint(VENDER_MAP)

##########################################
# テスト実施
##########################################
#class MaxRetryError(Exception):
#    pass
class ConnectionError(Exception):
    pass
#
##########################################
# テスト実施
##########################################
# テスト対象ライブラリインポート
from RedmineUserManager import RedmineUserManager

##########################################
# テスト実施 __init__
##########################################
'''RedmineUserManger Test
!pytest -s -x -l %
'''
def test___init__Normal1():
    '''__init__によるRedmineインスタンス生成が正常にできることを確認する

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    RUM = RedmineUserManager(HOST, API_KEY)
    pprint(type(RUM))
    assert type(RUM) == RedmineUserManager

@pytest.mark.xfail(raises=TypeError)
def test__init__Error1():
    '''__init__で引数エラー 引数1型エラー'''
    RUM = RedmineUserManager([], API_KEY)

@pytest.mark.xfail(raises=TypeError)
def test__init__Error2():
    '''__init__で引数エラー 引数2型エラー'''
    RUM = RedmineUserManager(HOST, [])

@pytest.mark.xfail(raises=TypeError)
def test__init__Error3():
    '''__init__で引数エラー 引数1、2型エラー'''
    RUM = RedmineUserManager([], [])

@pytest.mark.xfail(raises=TypeError)
def test__init__Error4():
    '''__init__で引数エラー 引数指定漏れ'''
    RUM = RedmineUserManager()

@pytest.mark.xfail(raises=TypeError)
def test__init__Error5():
    '''__init__で引数エラー 引数個数エラー1つ'''
    RUM = RedmineUserManager(HOST)

@pytest.mark.xfail(raises=TypeError)
def test__init__Error6():
    '''__init__で引数エラー 引数個数超過'''
    RUM = RedmineUserManager(HOST, API_KEY,[])

@pytest.mark.xfail(raises=Exception)
def test__init__Error7():
    '''__init__で引数エラー HOST適当に'''
    #HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    HOST = 'http://999.999.999.999' 
    RUM = RedmineUserManager(HOST, API_KEY)

@pytest.mark.xfail(raises=Exception)
def test__init__Error8():
    '''__init__で引数エラー API_KEYを適当に'''
    HOST = 'http://192.168.179.3:3100'
    #API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    API_KEY =  '9999999999999999999999999999999999999999'
    RUM = RedmineUserManager(HOST, API_KEY)


##########################################
# テスト実施 userAdd 
##########################################

def test___userAdd__Normal1():
    '''userAddによるRedmine ID作成テスト
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)
    # RedmineUserID削除
    RC = RUM.userDelete('PIT00000')

    # RedmineUserID作成
    RC = RUM.userAdd('PIT00000', 'Satoshi0', 'Suzuki', 'satoshi_00_suzuki@mufg.jp',INIT_PASS)
    assert RC == True

def test___userAdd__Normal2():
    '''userAddによるRedmine ID作成テスト IDを重複登録
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Normal2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)
    # RedmineUserID削除
    RC = RUM.userDelete('PIT00000')

    # RedmineUserID作成 2連発
    RC = RUM.userAdd('PIT00000', 'Satoshi1', 'Suzuki', 'satoshi_suzuki@mufg.jp',INIT_PASS)
    RC = RUM.userAdd('PIT00000', 'Satoshi1', 'Suzuki', 'satoshi_suzuki@mufg.jp',INIT_PASS)
    assert RC == None 



@pytest.mark.xfail(raises=TypeError)
def test___userAdd__Error1():
    '''userAdd パラメータ型エラー
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Error1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)
    # RedmineUserID削除
    RC = RUM.userDelete('PIT00000')

    # RedmineUserID作成
    login = 999999999 
    RC = RUM.userAdd(login, 'Satoshi1', 'Suzuki', 'satoshi_suzuki@mufg.jp',INIT_PASS)
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___userAdd__Error2():
    '''userAdd パラメータ型エラー
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Error2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)
    # RedmineUserID削除
    RC = RUM.userDelete('PIT00000')

    # RedmineUserID作成
    first_name = 999999999 
    RC = RUM.userAdd('PIT00000', first_name, 'Suzuki', 'satoshi_suzuki@mufg.jp',INIT_PASS)
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___userAdd__Error3():
    '''userAdd パラメータ型エラー
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Error3.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)
    # RedmineUserID削除
    RC = RUM.userDelete('PIT00000')

    # RedmineUserID作成
    last_name = 999999999 
    RC = RUM.userAdd('PIT00000', 'Satoshi', last_name, 'satoshi_suzuki@mufg.jp',INIT_PASS)
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___userAdd__Error4():
    '''userAdd パラメータ型エラー
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Error4.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)
    # RedmineUserID削除
    RC = RUM.userDelete('PIT00000')

    # RedmineUserID作成
    mail = 999999999 
    RC = RUM.userAdd('PIT00000', 'Satoshi', 'Suzuki', mail ,INIT_PASS)
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___userAdd__Error5():
    '''userAdd パラメータ型エラー
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Error5.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)
    # RedmineUserID削除
    RC = RUM.userDelete('PIT00000')

    # RedmineUserID作成
    INIT_PASS= 999999999 
    RC = RUM.userAdd('PIT00000', 'Satoshi', 'Suzuki', 'satoshi_suzuki@mufg.jp', INIT_PASS)
    assert RC == False


##########################################
# テスト実施 userDelete
##########################################

def test___userDelete__Normal1():
    '''userDeleteによるRedmine ID削除テスト
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userDelete__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    INIT_PASS = "p@ssw0rd"
    RUM = RedmineUserManager(HOST, API_KEY)

    # RedmineUserID作成
    RC = RUM.userAdd('PIT00000', 'Satoshi1', 'Suzuki', 'satoshi_suzuki@mufg.jp', INIT_PASS)

    # RedmineUserID削除
    RC = RUM.userDelete('PIT00000')
    assert RC == True

def test___userDelete__Normal2():
    '''userDeleteによるRedmine ID削除テスト 削除IDをさらに削除する
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userDelete__Normal2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    INIT_PASS = "p@ssw0rd"
    RUM = RedmineUserManager(HOST, API_KEY)

    # RedmineUserID作成
    RC = RUM.userAdd('PIT00000', 'Satoshi1', 'Suzuki', 'satoshi_suzuki@mufg.jp', INIT_PASS)

    # RedmineUserID削除
    RC = RUM.userDelete('PIT00000')
    RC = RUM.userDelete('PIT00000')
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___userDelete__Error1():
    '''userDeleteによるRedmine ID削除テスト パラメータ型エラー
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userDelete__Error1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    INIT_PASS = "p@ssw0rd"
    RUM = RedmineUserManager(HOST, API_KEY)

    # RedmineUserID作成
    RC = RUM.userAdd('PIT00000', 'Satoshi1', 'Suzuki', 'satoshi_suzuki@mufg.jp', INIT_PASS)

    # RedmineUserID削除
    login = 999999999
    RC = RUM.userDelete(login)
    assert RC == False


##########################################
# テスト実施 userDelete
##########################################

def test___userUpdate__Normal1():
    '''userUpdateによるRedmine パスワード変更 
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userUpdate__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    INIT_PASS = 'p@ssw0rd'
    RUM = RedmineUserManager(HOST, API_KEY)

    # RedmineUserパスワード変更
    RC = RUM.userDelete('PIT00002')
    RC = RUM.userAdd('PIT00002', 'Satoshi2', 'Suzuki', 'satoshi_2_suzuki@mufg.jp', INIT_PASS)
    RC = RUM.userUpdate('PIT00002', INIT_PASS)
    assert RC == True

def test___userUpdate__Normal2():
    '''userUpdateによるRedmine パスワード変更 
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userUpdate__Normal2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    INIT_PASS = "p@ssw0rd"
    RUM = RedmineUserManager(HOST, API_KEY)

    # RedmineUserID作成
    RC = RUM.userDelete('PIT00002')

    # RedmineUserパスワード変更
    RC = RUM.userUpdate('PIT00002', INIT_PASS)
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___userUpdate__Error1():
    '''userUpdateによるRedmine IDパスワード変更 パラメータ型エラー
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userUpdate__Error1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    INIT_PASS = "p@ssw0rd"
    RUM = RedmineUserManager(HOST, API_KEY)

    # RedmineUserID作成
    RC = RUM.userDelete('PIT00002')
    RC = RUM.userAdd('PIT00002', 'Satoshi2', 'Suzuki', 'satoshi_2_suzuki@mufg.jp', INIT_PASS)

    # RedmineUserIDパスワード変更
    login = 999999999
    RC = RUM.userUpdate(login, INIT_PASS)

@pytest.mark.xfail(raises=TypeError)
def test___userUpdate__Error2():
    '''userUpdateによるRedmine IDパスワード変更 パラメータ型エラー
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userUpdate__Error2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    INIT_PASS = "p@ssw0rd"
    RUM = RedmineUserManager(HOST, API_KEY)

    # RedmineUserID作成
    RC = RUM.userDelete('PIT00002')
    RC = RUM.userAdd('PIT00002', 'Satoshi2', 'Suzuki', 'satoshi_2_suzuki@mufg.jp', INIT_PASS)

    # RedmineUserIDパスワード変更
    INIT_PASS = 999999999
    RC = RUM.userUpdate('PIT00002', INIT_PASS)
    assert RC == False


##########################################
# テスト実施 userGroupAdd 
##########################################

def test___userGroupAdd__Normal1():
    '''userGroupAddによるグループへID追加
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupAdd__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # 指定グループに指定IDを追加する 
    RC = RUM.userGroupAdd('MUIT（業遂）','PIT00002')
    assert RC == True

def test___userGroupAdd__Normal2():
    '''userGroupAddによるグループへID追加 重複追加
    userGroupAdd__Normal1で既に追加したIDをさらに同じグループへ追加する
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupAdd__Normal2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # 指定グループに指定IDを追加する 
    RC = RUM.userGroupAdd('MUIT（業遂）','PIT00002')
    assert RC == False

def test___userGroupAdd__Normal3():
    '''userGroupAddによるグループへID追加 存在しないグループを指定 
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupAdd__Normal3.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # テスト用ユーザIDを作成する 
    RC = RUM.userDelete('PIT00003')
    RC = RUM.userAdd('PIT00003', 'Satoshi3', 'Suzuki', 'satoshi_3_suzuki@mufg.jp', INIT_PASS)

    # 存在しないグループを指定する、IDは実在する
    RC = RUM.userGroupAdd('XXXX（業遂）', 'PIT00003')
    assert RC == False 

def test___userGroupAdd__Normal4():
    '''userGroupAddによるグループへ すでにグループに登録済のIDを指定する
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupAdd__Normal4.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # 指定グループに指定IDを追加する 
    RC = RUM.userDelete('PIT00003')
    RC = RUM.userAdd('PIT00003', 'Satoshi3', 'Suzuki', 'satoshi_3_suzuki@mufg.jp', INIT_PASS)
    RC = RUM.userGroupAdd('MUIT（業遂）', 'PIT00003')

    # すでに所属するグループにIDを追加する 
    RC = RUM.userGroupAdd('MUIT（業遂）', 'PIT00003')
    assert RC == False 

def test___userGroupAdd__Normal5():
    '''userGroupAddによるグループへ 存在しないIDを指定する
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupAdd__Normal5.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # テスト対象IDを消す 
    RC = RUM.userDelete('PIT00003')
    # 存在するグループに消したIDを登録する
    RC = RUM.userGroupAdd('MUIT（業遂）', 'PIT00003')
    assert RC == False 

@pytest.mark.xfail(raises=TypeError)
def test___userGroupAdd__Error1():
    '''userGroupAddによるグループへID追加 型チェック
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupAdd__Error1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # 指定グループに指定IDを追加する 
    GROUP = 9999999
    RC = RUM.userGroupAdd(GROUP,'PIT00002')
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___userGroupAdd__Error2():
    '''userGroupAddによるグループへID追加 型チェック
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupAdd__Error2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # 指定グループに指定IDを追加する 
    USERID = 9999999
    RC = RUM.userGroupAdd('MUIT（業遂）', USERID)
    assert RC == False



##########################################
# テスト実施 userGroupDelete
##########################################

def test___userGroupDelete__Normal1():
    '''userGroupDeleteによるグループのユーザID削除
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupDelete__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # 指定グループに指定IDを追加する 
    RC = RUM.userDelete('PIT00010')
    RC = RUM.userAdd('PIT00010', 'Satoshi10', 'Suzuki', 'satoshi_10_suzuki@mufg.jp',INIT_PASS)
    RC = RUM.userGroupAdd('MUIT（業遂）','PIT00010')
    
    # 追加したグループから追加したIDを削除する
    RC = RUM.userGroupDelete('MUIT（業遂）','PIT00010')
    assert RC == True

def test___userGroupDelete__Normal2():
    '''userGroupDeleteによるグループのユーザID削除 グループにないIDを指定 
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupDelete__Normal2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # 指定グループに指定IDを追加する 
    RC = RUM.userDelete('PIT00010')
    RC = RUM.userAdd('PIT00010', 'Satoshi10', 'Suzuki', 'satoshi_10_suzuki@mufg.jp',INIT_PASS)
    RC = RUM.userGroupAdd('MUIT（業遂）','PIT00010')
    
    # 追加したグループから追加したIDを削除する
    RC = RUM.userGroupDelete('MUIT（業遂）','PIT00010')
    
    # グループから削除したIDを指定してもう一回
    RC = RUM.userGroupDelete('MUIT（業遂）','PIT00010')
    assert RC == False

def test___userGroupDelete__Normal3():
    '''userGroupDeleteによるグループへID追加、Redmineに存在しないID
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupDelete__Normal3.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを作成する
    RC = RUM.userDelete('PIT00010')

    # Redmineに存在しないIDを指定する 
    RC = RUM.userGroupDelete('MUIT（業遂）','PIT00010')
    assert RC == False

def test___userGroupDelete__Normal4():
    '''userGroupDeleteによるグループへID追加、Redmineに存在しないグループ
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupDelete__Normal4.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを作成する
    RC = RUM.userDelete('PIT00010')
    RC = RUM.userAdd('PIT00010', 'Satoshi10', 'Suzuki', 'satoshi_10_suzuki@mufg.jp',INIT_PASS)

    # Redmineに存在しないグループを指定する 
    RC = RUM.userGroupDelete('XXXX（業遂）','PIT00010')
    assert RC == False



@pytest.mark.xfail(raises=TypeError)
def test___userGroupDelete__Error1():
    '''userGroupDeleteによるグループへID追加 型チェック
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupDelete__Error1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを作成する
    RC = RUM.userDelete('PIT00010')
    RC = RUM.userAdd('PIT00010', 'Satoshi10', 'Suzuki', 'satoshi_10_suzuki@mufg.jp',INIT_PASS)

    # グループ：型エラー 
    GROUP = 9999999
    RC = RUM.userGroupDelete(GROUP,'PIT00010')
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___userGroupDelete__Error2():
    '''userGroupDeleteによるグループへID追加 型チェック
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userGroupDelete__Error2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを作成する
    RC = RUM.userDelete('PIT00010')
    RC = RUM.userAdd('PIT00010', 'Satoshi10', 'Suzuki', 'satoshi_10_suzuki@mufg.jp',INIT_PASS)

    # ID：型エラー 
    USERID = 999999999
    RC = RUM.userGroupDelete('MUIT（業遂）', USERID)
    assert RC == False


##########################################
# テスト実施 is_xxxxx
##########################################

def test___is_user__Normal1():
    '''is_user 判定
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___is_user__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを追加する 
    RC = RUM.userDelete('PIT00020')
    RC = RUM.userAdd('PIT00020', 'Satoshi10', 'Suzuki', 'satoshi_20_suzuki@mufg.jp',INIT_PASS)
    
    # ユーザID存在チェック 
    RC = RUM.is_user('PIT00020')
    assert RC == True

def test___is_user__Normal2():
    '''is_user 判定
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___is_user__Normal2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを追加する 
    RC = RUM.userDelete('PIT00020')
    
    # ユーザID存在チェック 指定IDは存在しない 
    RC = RUM.is_user('PIT00020')
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___is_user__Error1():
    '''is_user 判定
    userGroupDeleteによるグループへID追加 型チェック
    '''
    print()
    print('-'*50)
    print(test___is_user__Error1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを作成する
    RC = RUM.userDelete('PIT00020')
    RC = RUM.userAdd('PIT00020', 'Satoshi10', 'Suzuki', 'satoshi_20_suzuki@mufg.jp',INIT_PASS)

    # グループ：型エラー 
    USER = 9999999
    RC = RUM.is_user(USER)
    assert RC == False


def test___is_userGroup__Normal1():
    '''is_userGroup 判定
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___is_userGroup__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)
    
    # グループ存在チェック 
    RC = RUM.is_userGroup('MUIT（業遂）')
    assert RC == True

def test___is_userGroup__Normal2():
    '''is_userGroup 判定
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___is_userGroup__Normal2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # グループ存在チェック 
    RC = RUM.is_userGroup('XXXX（業遂）')
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___is_userGroup__Error1():
    '''is_userGroup 判定
    userGroupDeleteによるグループへID追加 型チェック
    '''
    print()
    print('-'*50)
    print(test___is_userGroup__Error1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # グループ：型エラー 
    GROUP = 9999999
    RC = RUM.is_userGroup(GROUP)
    assert RC == False

def test___is_userInTheGroup__Normal1():
    '''is_userInTheGroup 判定
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___is_user__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを追加する 
    RC = RUM.userDelete('PIT00040')
    RC = RUM.userAdd('PIT00040', 'Satoshi4', 'Suzuki', 'satoshi_40_suzuki@mufg.jp',INIT_PASS)
    # グループに追加する
    RC = RUM.userGroupAdd('MUIT（業遂）','PIT00040')
    # 判定
    (result, obj_group, obj_id) = RUM.is_userInTheGroup('MUIT（業遂）', 'PIT00040')
    assert result == True
    
def test___is_userInTheGroup__Normal2():
    '''is_userInTheGroup 判定
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___is_user__Normal2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを追加する 
    RC = RUM.userDelete('PIT00040')
    RC = RUM.userAdd('PIT00040', 'Satoshi4', 'Suzuki', 'satoshi_40_suzuki@mufg.jp',INIT_PASS)
    # グループから削除する
    RC = RUM.userGroupDelete('MUIT（業遂）','PIT00040')
    # 判定
    (result, obj_group, obj_id) = RUM.is_userInTheGroup('MUIT（業遂）', 'PIT00040')
    assert result == False 

@pytest.mark.xfail(raises=TypeError)
def test___is_userInTheGroup__Error1():
    '''is_userGroup 判定
    userGroupDeleteによるグループへID追加 型チェック
    '''
    print()
    print('-'*50)
    print(test___is_userInTheGroup__Error1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを追加する 
    RC = RUM.userDelete('PIT00040')
    RC = RUM.userAdd('PIT00040', 'Satoshi4', 'Suzuki', 'satoshi_40_suzuki@mufg.jp',INIT_PASS)
    # グループに追加する
    RC = RUM.userGroupAdd('MUIT（業遂）','PIT00040')

    # グループ：型エラー 
    GROUP = 9999999
    RC, obj_group, obj_id = RUM.is_userInTheGroup(GROUP, 'PIT00040')
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___is_userInTheGroup__Error2():
    '''is_userGroup 判定
    userGroupDeleteによるグループへID追加 型チェック
    '''
    print()
    print('-'*50)
    print(test___is_userInTheGroup__Error2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを追加する 
    RC = RUM.userDelete('PIT00040')
    RC = RUM.userAdd('PIT00040', 'Satoshi4', 'Suzuki', 'satoshi_40_suzuki@mufg.jp',INIT_PASS)
    # グループに追加する
    RC = RUM.userGroupAdd('MUIT（業遂）','PIT00040')

    # ユーザID：型エラー 
    userid = 9999999
    RC, obj_group, obj_id = RUM.is_userInTheGroup('MUIT（業遂）', userid)
    assert RC == False


def test___getGroupMap__Normal1():
    '''getGroupMap 判定
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___getGroupMap__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # ユーザID存在チェック 
    RC = RUM.getGroupMap()
    assert RC == {'MUIT（業遂）': 6, 'MUIT（非業遂）': 18}


def test___getGroupResourceID__Normal1():
    '''getGroupResourceID取得
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___getGroupResourceID__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # ユーザID存在チェック 
    RC = RUM.getGroupResourceID('MUIT（業遂）')
    assert RC == 6

def test___getGroupResourceID__Normal2():
    '''getGroupResourceID取得
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___getGroupResourceID__Normal2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # ユーザID存在チェック 
    RC = RUM.getGroupResourceID('XXXX（業遂）')
    assert RC != True  

@pytest.mark.xfail(raises=TypeError)
def test___getGroupResourceID__Error1():
    '''getGroupResourceID取得 型チェック
    '''
    print()
    print('-'*50)
    print(test___getGroupResourceID__Error1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # グループ：型エラー 
    GROUP = 9999999
    RC, obj_group, obj_id = RUM.getGroupResourceID(GROUP)
    assert RC == False


def test___getUserResourceID__Normal1():
    '''getGroupResourceID取得
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___getGroupResourceID__Normal1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを追加する 
    RC = RUM.userDelete('PIT00050')
    RC = RUM.userAdd('PIT00050', 'Satoshi4', 'Suzuki', 'satoshi_50_suzuki@mufg.jp',INIT_PASS)

    # ユーザID存在チェック 
    RC = RUM.getUserResourceID('PIT00050')
    assert RC != False


def test___getUserResourceID__Normal2():
    '''getGroupResourceID取得
    Redmineインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___getGroupResourceID__Normal2.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # IDを削除する 
    RC = RUM.userDelete('PIT00050')

    # ユーザID存在チェック 
    RC = RUM.getUserResourceID('PIT00050')
    assert RC == False


@pytest.mark.xfail(raises=TypeError)
def test___getUserResourceID__Error1():
    '''getGroupResourceID取得 型チェック
    '''
    print()
    print('-'*50)
    print(test___getUserResourceID__Error1.__doc__)
    print('-'*50)
    print()

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # ユーザID ：型エラー 
    USERID = 9999999

    # ユーザID存在チェック 
    RC = RUM.getUserResourceID(USERID)
    assert RC == False



def test___judgeTargetGroupname__Normal1():
    '''judgeTargetGroupnameにてグループ名生成
    '''
    print()
    print('-'*50)
    print(test___judgeTargetGroupname__Normal1.__doc__)
    print('-'*50)
    pprint(VENDER_MAP)

    '''
    'PHSL': '一括',
    'PHTC': '一括',
    'PINC': 'INC（常駐）',
    'PIT0': 'MUIT',
    'PNDS': 'NDS（常駐）',
    'PNSD': 'NSD（常駐）'}
    '''

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # MUIT パターン
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PIT0', True, True)
    assert RC == 'MUIT（業遂）'
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PIT0', True, False)
    assert RC == 'MUIT（業遂）（Lycheeなし）'
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PIT0', False, True)
    assert RC == 'MUIT（非業遂）'
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PIT0', False, False)
    assert RC == 'MUIT（非業遂）'

    # 一括 パターン
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PHSL', True, True)
    assert RC == '一括（業遂）'
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PHSL', True, False)
    assert RC == '一括（業遂）（Lycheeなし）'
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PHSL', False, True)
    assert RC == '一括（非業遂）'
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PHSL', False, False)
    assert RC == '一括（非業遂）'

    # 常駐 パターン 代表してNSD
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PNSD', True, True)
    assert RC == 'NSD（常駐）（業遂）'
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PNSD', True, False)
    assert RC == 'NSD（常駐）（業遂）（Lycheeなし）'
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PNSD', False, True)
    assert RC == 'NSD（常駐）（非業遂）'
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PNSD', False, False)
    assert RC == 'NSD（常駐）（非業遂）'


@pytest.mark.xfail(raises=NameError)
def test___judgeTargetGroupname__Error1():
    '''judgeTargetGroupnameにてグループ名生成 存在しないベンダーコード指定
    '''
    print()
    print('-'*50)
    print(test___judgeTargetGroupname__Error1.__doc__)
    print('-'*50)
    pprint(VENDER_MAP)

    '''
    'PHSL': '一括',
    'PHTC': '一括',
    'PINC': 'INC（常駐）',
    'PIT0': 'MUIT',
    'PNDS': 'NDS（常駐）',
    'PNSD': 'NSD（常駐）'}
    '''

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # 空のdictを指定 
    RC = RUM.judgeTargetGroupname({}, 'PIT0', True, True)
    assert RC == False


@pytest.mark.xfail(raises=TypeError)
def test___judgeTargetGroupname__Error2():
    '''judgeTargetGroupnameにてグループ名生成 型エラー
    '''
    print()
    print('-'*50)
    print(test___judgeTargetGroupname__Error2.__doc__)
    print('-'*50)
    pprint(VENDER_MAP)

    '''
    'PHSL': '一括',
    'PHTC': '一括',
    'PINC': 'INC（常駐）',
    'PIT0': 'MUIT',
    'PNDS': 'NDS（常駐）',
    'PNSD': 'NSD（常駐）'}
    '''

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # ベンダID 型エラー
    VENDER_ID = True
    RC = RUM.judgeTargetGroupname(VENDER_MAP, VENDER_ID, True, True)
    assert RC == False


@pytest.mark.xfail(raises=TypeError)
def test___judgeTargetGroupname__Error3():
    '''judgeTargetGroupnameにてグループ名生成 型エラー
    '''
    print()
    print('-'*50)
    print(test___judgeTargetGroupname__Error3.__doc__)
    print('-'*50)
    pprint(VENDER_MAP)

    '''
    'PHSL': '一括',
    'PHTC': '一括',
    'PINC': 'INC（常駐）',
    'PIT0': 'MUIT',
    'PNDS': 'NDS（常駐）',
    'PNSD': 'NSD（常駐）'}
    '''

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # ベンダID 型エラー
    IS_MANAGER = "True"
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PIT0', IS_MANAGER, True)
    assert RC == False


@pytest.mark.xfail(raises=TypeError)
def test___judgeTargetGroupname__Error3():
    '''judgeTargetGroupnameにてグループ名生成 型エラー
    '''
    print()
    print('-'*50)
    print(test___judgeTargetGroupname__Error3.__doc__)
    print('-'*50)
    pprint(VENDER_MAP)

    '''
    'PHSL': '一括',
    'PHTC': '一括',
    'PINC': 'INC（常駐）',
    'PIT0': 'MUIT',
    'PNDS': 'NDS（常駐）',
    'PNSD': 'NSD（常駐）'}
    '''

    # Redmineインスタンス生成
    HOST = 'http://192.168.179.3:3100'
    API_KEY = '864b3f0933e8084295d47380bf07a168ba2947ac'
    RUM = RedmineUserManager(HOST, API_KEY)

    # ベンダID 型エラー
    IS_LYCHEE = "True"
    RC = RUM.judgeTargetGroupname(VENDER_MAP, 'PIT0', True, IS_LYCHEE)
    assert RC == False
