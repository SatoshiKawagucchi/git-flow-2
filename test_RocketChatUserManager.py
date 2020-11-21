#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-

''' RocketChatUserManager.pyのテストクラス
'''

##########################################
# library テスト実行環境構築向け
##########################################
import pytest
import sys
from pathlib2 import Path
from pprint import pprint

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
HEADERS ={
    'X-Auth-Token': 'zYGeveBMm79longHcJTwFi425FB6qyLxXDuRXUHAXDS',
    'X-User-Id': 'sny2QJnFfBHBK4Prc',
    'Content-Type': 'application/json',
}
URL = 'http://192.168.10.104:3000'
INIT_PASS = 'p@ssw0rd'

if __DEBUG__:
    pprint(HEADERS)
    pprint(URL)
    pprint(INIT_PASS)


##########################################
# テスト実施
##########################################
# テスト対象ライブラリインポート
from RocketChatUserManager import RocketChatUserManager


##########################################
# テスト実施 __init__
##########################################
'''RocketChatUserManger Test
!pytest -s -x -l %
'''

def test___init__Normal1():
    '''__init__によるRocketChatインスタンス生成が正常にできることを確認する

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___init__Normal1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatUserManager(HEADERS, URL)
    pprint(type(RCM))
    assert type(RCM) == RocketChatUserManager

@pytest.mark.xfail(raises=TypeError)
def test___init__Error1():
    '''__init__で引数エラー 引数1型エラー'''
    print()
    print('-'*50)
    print(test___init__Error1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatUserManager([], URL)

@pytest.mark.xfail(raises=TypeError)
def test___init__Error2():
    '''__init__で引数エラー 引数1型エラー'''
    print()
    print('-'*50)
    print(test___init__Error2.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatUserManager(HEADERS, [])

def test___userAdd__Normal1():
    '''userAddによるRocket ID作成テスト
    RocketChatインスタンスを正常作成を前提に検証を進める 
    '''
    print()
    print('-'*50)
    print(test___userAdd__Normal1.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID = 'PIT00000'
    PREFIX = '00'
    FIRST_NAME = f'Satoshi_{PREFIX}'
    LAST_NAME = f'Suzuki'
    MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'

    # いったん強制的にIDを消す 
    # RocketChatUserID削除
    RC = RCM.userDelete(ID)

    # RocketChatUserID作成
    RC = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)
    assert RC == True

def test___userAdd__Normal2():
    '''userAddによるRocket ID作成テスト すでにある状態で同じIDを追加
    RocketChatインスタンスを正常作成を前提に検証を進める 
    '''
    print()
    print('-'*50)
    print(test___userAdd__Normal2.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID = 'PIT00000'
    PREFIX = '00'

    # 固定でいいかと
    FIRST_NAME = f'Satoshi_{PREFIX}'
    LAST_NAME = f'Suzuki'
    MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'

    # いったん強制的にIDを消す 
    # RocketChatUserID削除
    RC = RCM.userDelete(ID)

    # RocketChatUserID作成 IDがある状態で再度作成する
    RC1 = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)
    RC2 = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)
    assert RC2 == True

@pytest.mark.xfail(raises=TypeError)
def test___userAdd__Error1():
    '''userAdd パラメータ型エラー
    RocketChatインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Error1.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID = 00000000 
    PREFIX = '00'

    # 固定でいいかと
    FIRST_NAME = f'Satoshi_{PREFIX}'
    LAST_NAME = f'Suzuki'
    MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'

    # いったん強制的にIDを消す 
    # RocketChatUserID削除
    #RC = RCM.userDelete(ID)

    # RocketChatUserID作成 IDがある状態で再度作成する
    RC1 = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)
    assert RC1 == False

@pytest.mark.xfail(raises=TypeError)
def test___userAdd__Error2():
    '''userAdd パラメータ型エラー
    RocketChatインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Error2.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID ='PIT00000' 
    PREFIX = '00'

    # 固定でいいかと
    FIRST_NAME = 00000000 
    #FIRST_NAME = f'Satoshi_{PREFIX}'
    LAST_NAME = f'Suzuki'
    MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'

    # いったん強制的にIDを消す 
    # RocketChatUserID削除
    #RC = RCM.userDelete(ID)

    # RocketChatUserID作成 IDがある状態で再度作成する
    RC1 = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)
    assert RC1 == False

@pytest.mark.xfail(raises=TypeError)
def test___userAdd__Error3():
    '''userAdd パラメータ型エラー
    RocketChatインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Error3.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID ='PIT00000' 
    PREFIX = '00'

    # 固定でいいかと
    FIRST_NAME = f'Satoshi_{PREFIX}'
    #LAST_NAME = f'Suzuki'
    LAST_NAME = 00000000 
    MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'

    # いったん強制的にIDを消す 
    # RocketChatUserID削除
    #RC = RCM.userDelete(ID)

    # RocketChatUserID作成 IDがある状態で再度作成する
    RC1 = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)
    assert RC1 == False

@pytest.mark.xfail(raises=TypeError)
def test___userAdd__Error4():
    '''userAdd パラメータ型エラー
    RocketChatインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Error4.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID ='PIT00000' 
    PREFIX = '00'

    # 固定でいいかと
    FIRST_NAME = f'Satoshi_{PREFIX}'
    LAST_NAME = f'Suzuki'
    #MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'
    MAIL = 00000000 

    # いったん強制的にIDを消す 
    # RocketChatUserID削除
    #RC = RCM.userDelete(ID)

    # RocketChatUserID作成 IDがある状態で再度作成する
    RC1 = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)
    assert RC1 == False

@pytest.mark.xfail(raises=TypeError)
def test___userAdd__Error5():
    '''userAdd パラメータ型エラー
    RocketChatインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userAdd__Error5.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID ='PIT00000' 
    PREFIX = '00'

    # 固定でいいかと
    FIRST_NAME = f'Satoshi_{PREFIX}'
    LAST_NAME = f'Suzuki'
    MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'

    # ちょっと微妙だが型チェックだけの目的で
    INIT_PASS = 00000000
    # いったん強制的にIDを消す 
    # RocketChatUserID削除
    #RC = RCM.userDelete(ID)

    # RocketChatUserID作成 IDがある状態で再度作成する
    RC1 = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)
    assert RC1 == False



def test___userDelete__Normal1():
    '''userDeleteによるRocket ID削除テスト
    RocketChatインスタンスを正常作成を前提に検証を進める 
    '''
    print()
    print('-'*50)
    print(test___userAdd__Normal1.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID = 'PIT00000'
    PREFIX = '00'
    FIRST_NAME = f'Satoshi_{PREFIX}'
    LAST_NAME = f'Suzuki'
    MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'

    # RocketChat ID作成をまず
    RC = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)

    # RocketChatUserID削除
    RC1 = RCM.userDelete(ID)
    assert RC1 == True


def test___userDelete__Normal2():
    '''userDeleteによるRocket ID削除テスト 存在しないIDを指定
    RocketChatインスタンスを正常作成を前提に検証を進める 
    '''
    print()
    print('-'*50)
    print(test___userAdd__Normal2.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID = 'PIT00000'
    PREFIX = '00'
    FIRST_NAME = f'Satoshi_{PREFIX}'
    LAST_NAME = f'Suzuki'
    MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'

    # RocketChat ID作成をまず
    RC = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)

    # RocketChatUserID削除
    RC1 = RCM.userDelete(ID)
    # 消したIDをもう一度消しに行く
    RC2 = RCM.userDelete(ID)
    assert RC2 == True

@pytest.mark.xfail(raises=TypeError)
def test___userDelete__Error1():
    '''userDelete パラメータ型エラー
    RocketChatインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___userDelete__Error1.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID = 00000000 

    # ID削除 
    RC1 = RCM.userDelete(ID)
    assert RC1 == False


def test___getAllUserList__Normal1():
    '''getAllUserListによるRocket ユーザ一覧取得 
    RocketChatインスタンスを正常作成を前提に検証を進める 
    '''
    print()
    print('-'*50)
    print(test___getAllUserList__Normal1.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # RocketChat ID一覧取得
    _list = RCM.getAllUserList()

    # list結果チェック 
    assert ['admin', 'rocket.cat'] == _list
    assert len(_list) == 2


def test___is_user__Normal1():
    '''is_userによるRocket ID存在テスト 存在する
    RocketChatインスタンスを正常作成を前提に検証を進める 
    '''
    print()
    print('-'*50)
    print(test___is_user__Normal1.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID = 'PIT00000'
    PREFIX = '00'
    FIRST_NAME = f'Satoshi_{PREFIX}'
    LAST_NAME = f'Suzuki'
    MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'

    # いったん強制的にIDを消す 
    # RocketChatUserID削除
    RC1 = RCM.userDelete(ID)

    # RocketChatUserID作成
    RC2 = RCM.userAdd(ID, FIRST_NAME, LAST_NAME, MAIL, INIT_PASS)

    # 存在チェック
    RC3 = RCM.is_user(ID)
    assert RC3 == True

def test___is_user__Normal2():
    '''is_userによるRocket ID存在テスト 存在しない
    RocketChatインスタンスを正常作成を前提に検証を進める 
    '''
    print()
    print('-'*50)
    print(test___is_user__Normal2.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID = 'PIT00000'
    PREFIX = '00'
    FIRST_NAME = f'Satoshi_{PREFIX}'
    LAST_NAME = f'Suzuki'
    MAIL = f'satoshi_{PREFIX}_suzuki@mufg.jp'

    # いったん強制的にIDを消す 
    # RocketChatUserID削除
    RC1 = RCM.userDelete(ID)

    # 存在チェック
    RC3 = RCM.is_user(ID)
    assert RC3 == False

@pytest.mark.xfail(raises=TypeError)
def test___is_user__Error1():
    '''is_user パラメータ型エラー
    RocketChatインスタンスを正常作成を前提に検証を進める '''
    print()
    print('-'*50)
    print(test___is_user__Error1.__doc__)
    print('-'*50)
    print()

    # インスタンス生成
    RCM = RocketChatUserManager(HEADERS, URL)

    # 対象IDを決定
    ID = 00000000 

    # ID削除 
    RC1 = RCM.userDelete(ID)
    assert RC1 == False

