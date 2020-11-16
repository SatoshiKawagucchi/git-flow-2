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

##########################################
# テスト実施
##########################################
# テスト対象ライブラリインポート
import UserManager 
'''Abstruct機能確認

UserManagerはAbstructの役割を担っている。
overrideなしの使用ではNotImplementedErrorが発生する。

'''
@pytest.mark.xfail(raises=NotImplementedError)
def test_userAdd():
    UM = UserManager.BaseUserManager() 
    UM.userAdd()

@pytest.mark.xfail(raises=NotImplementedError)
def test_userDelete():
    UM = UserManager.BaseUserManager() 
    UM.userDelete()

@pytest.mark.xfail(raises=NotImplementedError)
def test_userUpdate():
    UM = UserManager.BaseUserManager() 
    UM.userUpdate()

@pytest.mark.xfail(raises=NotImplementedError)
def test_userGroupAdd():
    UM = UserManager.BaseUserManager() 
    UM.userGroupAdd()

@pytest.mark.xfail(raises=NotImplementedError)
def test_userGroupDelete():
    UM = UserManager.BaseUserManager() 
    UM.userGroupDelete()

@pytest.mark.xfail(raises=NotImplementedError)
def test_is_user():
    UM = UserManager.BaseUserManager() 
    UM.is_user()

@pytest.mark.xfail(raises=NotImplementedError)
def test_is_userInTheGroup():
    UM = UserManager.BaseUserManager() 
    UM.is_userInTheGroup()

@pytest.mark.xfail(raises=NotImplementedError)
def test_is_userGroup():
    UM = UserManager.BaseUserManager() 
    UM.is_userGroup()
