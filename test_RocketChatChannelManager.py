#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-

'''RocketChatChannelManager.pyのテストクラス
'''

##########################################
# library テスト実行環境構築向け
##########################################
import pytest
import sys
from datetime import datetime
from pathlib2 import Path
from pprint import pprint
from pytz import timezone

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
from RocketChatChannelManager import RocketChatChannelManager


##########################################
# テスト実施 __init__
##########################################
'''RocketChatChannelManger Test
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

    RCM = RocketChatChannelManager(HEADERS, URL)
    pprint(type(RCM))
    assert type(RCM) == RocketChatChannelManager

@pytest.mark.xfail(raises=TypeError)
def test___init__Error1():
    '''__init__で引数エラー 引数1型エラー'''
    print()
    print('-'*50)
    print(test___init__Error1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager([], URL)

@pytest.mark.xfail(raises=TypeError)
def test___init__Error2():
    '''__init__で引数エラー 引数1型エラー'''
    print()
    print('-'*50)
    print(test___init__Error2.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, [])



def test___getChannelPublicMap__Normal1():
    '''getChannelPublicMapによるパブリックチャンネル取得

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannelPublicMap__Normal1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    _map = RCM.getChannelPublicMap()
    pprint(_map)

    # チャンネル操作すると冪等が飛んでしまう。。。
#    assert _map == {'general': '2020-11-21T06:35:55.288Z'}
#    for k, v in _map.items():
#        print(k,v) 
#        assert k == 'general'
#        assert v == '2020-11-21T06:35:55.288Z'
#


def test___getChannelPrivateMap__Normal1():
    '''getChannelPublicMapによるプライベートチャンネル取得

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannelPrivateMap__Normal1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    _map = RCM.getChannelPrivateMap()
    pprint(_map)

    # チャンネル操作すると冪等が飛んでしまう。。。
#    assert _map == {'ひとりことをつぶやく': '2020-11-03T04:59:00.376Z', '根の深い問題': '2020-11-03T04:59:00.376Z'}
#    assert [k for k, v in _map.items()] == ['ひとりことをつぶやく', '根の深い問題']


def test___exchangeMapKeyToList__Normal1():
    '''exchangeMapKeyToListによるkey取得

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___exchangeMapKeyToList__Normal1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    _map = RCM.getChannelPrivateMap()
    pprint(_map)
    _list = RCM.exchangeMapkeyToList(_map)

    assert [k for k, v in _map.items()] == _list 
    assert _list == ['ひとりことをつぶやく', '根の深い問題']


@pytest.mark.xfail(raises=TypeError)
def test___exchangeMapKeyToList__Error1():
    '''exchangeMapKeyToListで引数エラー 引数1型エラー'''
    print()
    print('-'*50)
    print(test___exchangeMapKeyToList__Error1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    _list = RCM.exchangeMapkeyToList([])


def test___getChannelMap__Normal1():
    '''getChannelMapによる一括取得

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannelMap__Normal1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    _map = RCM.getChannelMap()
    pprint(_map)

    # チャンネル操作すると冪等が飛んでしまう。。。
#    assert _map == {'general': '2020-11-21T06:35:55.288Z',
#                    'ひとりことをつぶやく': '2020-11-03T04:59:00.376Z',
#                    '根の深い問題': '2020-11-03T04:59:00.376Z'}


def test___getChannelUserMap__Normal1():
    '''getChannelUserMapによるmap取得 チャンネル指定 パブリック 

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannelUserMap__Normal1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    _map = RCM.getChannelUserMap(['general'])
    pprint(_map)
    assert _map == {'general': ['admin']}


def test___getChannelUserMap__Normal2():
    '''getChannelUserMapによるmap取得 チャンネル指定 プライベート

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannelUserMap__Normal2.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    _map = RCM.getChannelUserMap(['ひとりことをつぶやく'])
    pprint(_map)
    assert _map == {'ひとりことをつぶやく': ['admin']}


def test___getChannelUserMap__Normal3():
    '''getChannelUserMapによるmap取得 チャンネル複数指定 

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannelUserMap__Normal3.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    _map = RCM.getChannelUserMap(['general', 'ひとりことをつぶやく'])
    pprint(_map)
    assert _map == {'general': ['admin'], 'ひとりことをつぶやく': ['admin']}


def test___getChannelUserMap__Normal4():
    '''getChannelUserMapによるmap取得 全体取得

     全量を対象に調査
     getChannelMap 全体のmap
     exchangeMapkeyToList mapをlistに変換 

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannelUserMap__Normal4.__doc__)
    print('-'*50)
    print()

    # 全量を対象に調査
    ## getChannelMap 全体のmap
    ## exchangeMapkeyToList mapをlistに変換 
    RCM = RocketChatChannelManager(HEADERS, URL)
    _map = RCM.getChannelUserMap(RCM.exchangeMapkeyToList(RCM.getChannelMap()))
    pprint(_map)
#    assert _map == {'general': ['admin'], 'ひとりことをつぶやく': ['admin'], '根の深い問題': ['admin']}


def test___getChannelUserMap__Normal5():
    '''getChannelUserMapによるmap取得 存在しないチャンネル指定 

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannelUserMap__Normal5.__doc__)
    print('-'*50)
    print()

    # 検証
    RCM = RocketChatChannelManager(HEADERS, URL)
    _map = RCM.getChannelUserMap([])
    pprint(_map)
    assert _map == {} 
#    assert _map == {'general': ['admin'], 'ひとりことをつぶやく': ['admin'], '根の深い問題': ['admin']}

@pytest.mark.xfail(raises=TypeError)
def test___getChannelUserMap__Error1():
    '''getChannelUserMapで引数エラー 引数1型エラー'''
    print()
    print('-'*50)
    print(test___getChannelUserMap__Error1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC1 = RCM.getChannelUserMap({})



def test___getDifftimeLastUpdateSec__Normal1():
    '''getDifftimeLastUpdateSecによる値算出実施確認

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getDifftimeLastUpdateSec__Normal1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    _time = '2020-11-03T04:59:00.376Z' 
    pprint(datetime.now(timezone('Asia/Tokyo')))
    pprint(_time)
    print(RCM.getDifftimeLastUpdateSec(_time)) 


@pytest.mark.xfail(raises=TypeError)
def test___getDifftimeLastUpdateSec__Error1():
    '''getDifftimeLastUpdateSecで引数エラー 引数1型エラー
    '''
    print()
    print('-'*50)
    print(test___getDifftimeLastUpdateSec__Error1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC1 = RCM.getDifftimeLastUpdateSec(9999999999999999999)


def test___getChannel_id__Normal1():
    '''getChannel_idによるID取得 チャンネルID取得

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannel_id__Normal1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC = RCM.getChannel_id('general')
    assert RC == 'GENERAL'


def test___getChannel_id__Normal2():
    '''getChannel_idによるID取得 チャンネルID取得

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannel_id__Normal2.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC = RCM.getChannel_id('ひとりことをつぶやく')
    assert RC == '8q7AijAC9CiurqGFG'

def test___getChannel_id__Normal3():
    '''getChannel_idによるID取得 存在しないチャンネルを指定

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___getChannel_id__Normal3.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC = RCM.getChannel_id('ひとりことをつぶやくx')
    assert RC == False


@pytest.mark.xfail(raises=TypeError)
def test___getChannel_id__Error1():
    '''getChannel_idで引数エラー 引数1型エラー
    '''
    print()
    print('-'*50)
    print(test___getChannel_id__Error1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC1 = RCM.getChannel_id(9999999999999999999)


def test___sendMessageToRocketChat__Normal1():
    '''sendMessageToRocketChatによる指定チャンネルにメッセージを送信

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___sendMessageToRocketChat__Normal1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC = RCM.sendMessageToRocketChat('general', 'テストメッセージです_OK')
    assert RC == True


def test___sendMessageToRocketChat__Normal2():
    '''sendMessageToRocketChatによる指定チャンネルにメッセージを送信、存在しないチャンネル

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___sendMessageToRocketChat__Normal2.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC = RCM.sendMessageToRocketChat('generalx', 'テストメッセージです_Error')
    assert RC == False

@pytest.mark.xfail(raises=TypeError)
def test___sendMessageToRocketChat__Error1():
    '''sendMessageToRocketChatで引数エラー 引数1型エラー
    '''
    print()
    print('-'*50)
    print(test___sendMessageToRocketChat__Error1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC1 = RCM.sendMessageToRocketChat([],'テストメッセージ')

@pytest.mark.xfail(raises=TypeError)
def test___sendMessageToRocketChat__Error2():
    '''sendMessageToRocketChatで引数エラー 引数1型エラー
    '''
    print()
    print('-'*50)
    print(test___sendMessageToRocketChat__Error2.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC1 = RCM.sendMessageToRocketChat('general',[])


def test___closeTargetChannel__Normal1():
    '''closeTargetChannelによるチャンネル削除 存在するチャンネルを指定

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）

    '''
    print()
    print('-'*50)
    print(test___closeTargetChannel__Normal1.__doc__)
    print('-'*50)
    print()

    # 消す予定のチャンネルに書き込み
    RCM = RocketChatChannelManager(HEADERS, URL)
    RC1 = RCM.sendMessageToRocketChat('削除テスト用チャンネル', 'テストメッセージです_OK')


    # チャンネル操作すると冪等が飛んでしまう。。。
    # チャンネル削除
#    RC2 = RCM.closeTargetChannel('削除テスト用チャンネル')
#    assert RC2 == True

def test___closeTargetChannel__Normal2():
    '''closeTargetChannelによるチャンネル削除 存在しないチャンネルを指定

    __init__は値を返さないのでRCチェックはないです。例外捉えるまで。
    （捕らえた上でのRCハンドリングはしない）
    '''
    print()
    print('-'*50)
    print(test___closeTargetChannel__Normal2.__doc__)
    print('-'*50)
    print()

    # チャンネル削除
    RCM = RocketChatChannelManager(HEADERS, URL)
    RC2 = RCM.closeTargetChannel('削除テスト用チャンネル')
    assert RC2 == None

@pytest.mark.xfail(raises=TypeError)
def test___closeTargetChannel__Error1():
    '''closeTargetChannelで引数エラー 引数1型エラー
    '''
    print()
    print('-'*50)
    print(test___sendMessageToRocketChat__Error1.__doc__)
    print('-'*50)
    print()

    RCM = RocketChatChannelManager(HEADERS, URL)
    RC1 = RCM.closeTargetChannel([])


