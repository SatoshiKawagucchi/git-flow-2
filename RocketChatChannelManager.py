#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-

'''RocketChat Channelメンテナンス

  RocketChatのチャンネル管理を行う 

  Todo:
     * まだRedmineとRocketChatのみ。他のOSSに対しても同様に作る

'''

################################################
# library
################################################

import json
import requests
import sys

from datetime import datetime
from dateutil import parser
from pprint import pprint
from pytz import timezone

################################################
# 環境変数取得 
################################################
#
#HEADERS ={
#'X-Auth-Token': 'zYGeveBMm79longHcJTwFi425FB6qyLxXDuRXUHAXDS',
#'X-User-Id': 'sny2QJnFfBHBK4Prc',
#'Content-Type': 'application/json'}
#
#URL = 'http://192.168.179.3:3000'
#INIT_PASS = 'p@ssw0rd'
#

################################################
# RocketChatChannelManager 
################################################
class RocketChatChannelManager(object):
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
    
    
    def getChannelPublicMap(self):
        '''パブリックチャネルのリストと最終更新時間のマップ
        
        パブリックチャンネル名とチャンネル最終更新時間のマップを作成する。

        Args:

        Returns:
           map:  パブリックチャンネル名と最終更新時間のマップ 

        Raises:
           API実行時のエラー 

        Examples:
            >>> map = self.getChannelPublicMap() 

        Note:
            publicとprivateで取得関数が異なるという。。。

        '''

        # 結果格納
        _map = {}

        # API定義
        API = f'{self.URL}/api/v1/channels.list'

        # 取得処理
        try:
            response = requests.get(
                API,
                headers=self.HEADERS,)    
        except Exception as e:
            print(f'API実行エラー: {API}')
            print(f'Error: {e}')
            return False
        else:
            for l in response.json()['channels']:
                _map[l['name']] = l['_updatedAt']

            # mapを返す
            return _map

        
    def getChannelPrivateMap(self):
        '''プライベートチャネルのリストと最終更新時間のマップ

        プライベート名とチャンネル最終更新時間のマップを作成する。

        Args:

        Returns:
           map:  プライベートチャンネル	名と最終更新時間のマップ 

        Raises:
           API実行時のエラー 

        Examples:
            >>> map = self.getChannelPrivateMap() 

        Note:
            publicとprivateで取得関数が異なるという。。。

        '''

        # 結果格納
        _map = {}

        # API定義
        API = f'{self.URL}/api/v1/groups.listAll'
       
        # 取得処理
        try:
            response = requests.get(
                API,
                headers=self.HEADERS,)    
        except Exception as e:
            print(f'API実行エラー: {API}')
            print(f'Error: {e}')
            return False
        finally:
            for l in response.json()['groups']:
                _map[l['name']] = l['_updatedAt']

            # mapを返す
            return _map    

    def exchangeMapkeyToList(self, map):
        '''mapのkeyからlistを生成する

        ちょっとめんどい変換ヘルパー関数

        '''
        # 引数チェック 型    
        if not isinstance(map, dict):
            print(f'引数：mapの型が正しくありません dict <-> {type(map)}')
            raise TypeError

        # 入れ物
        _list = []

        # mapループ
        for key in map.keys():
            _list.append(key)
        
        return _list
          

    def getChannelMap(self):
        '''チャンネル一覧およびチャンネルの最終更新時間を取得する

        パブリック、プライベート両方のチャンネルをまとめて処理する

        Args:

        Returns:
           map: チャンネル名と所属ユーザリストのマップ 

        Raises:
           API実行時のエラー 

        Examples:
            >>> map_ = R.getChannelMap()

        Note:
            getChannelPubliclist()やgetChannelPrivatelist()と併用する感じ
            パブリック、プライベートまとめて取得

        '''

        # public,privateそれぞれ取得
        _map_public = self.getChannelPublicMap()
        _map_private = self.getChannelPrivateMap()

        # mapを結合して返す
        #TODO Falseでも結合できる？戻り値を見直す必要あり？
        if ((_map_public) and (_map_private)):
            _map_public.update(_map_private)
            return _map_public
        else:
            return {}
              
            
    def getChannelUserMap(self, list_channelname):
        '''指定チャンネルの登録ID一覧
        
        listに格納したチャンネルに所属するユーザ一覧を
        チャンネル名と参加しているユーザリストのマップを返す
        パブリック、プライベートをまとめて実施

        Args:
           list_channelname(list): 探索対象のチャンネル名リスト

        Returns:
           map: チャンネル名と所属ユーザリストのマップ 

        Raises:
           API実行時のエラー 

        Examples:
            >>> map = getChannelUserMap(['aaaa','bbbb'])

        Note:

        '''

        # 引数チェック 型    
        if not isinstance(list_channelname , list):
            print(f'引数：list_channelnameの型が正しくありません list  <-> {type(list_channelname)}')
            raise TypeError

        # 結果全体格納するMap
        _map = {}
       
        # MSG送信API定義
        # パブリックもプライベートもまとめて実施
        APIS = [f'{self.URL}/api/v1/channels.members',
                f'{self.URL}/api/v1/groups.members']
        
        # 1000人は超えないだろう。。。から
        COUNT = '1000'
        
        # 対象チャンネル名リストでループ
        for channel in list_channelname:

            # MSG組み立て 
            msg = (('roomName', channel),('count',COUNT),) 
            
            # API発行
            for api in APIS:
                try:
                    response = requests.get(
                        api,
                        params=msg,
                        headers=self.HEADERS,)
                except Exception as e:
                    print(f'API実行エラー: {API}')
                    print(f'Error: {e}')
                    return False
                else:
                    # ユーザたちを格納するList
                    _list = []
                    
                    # 結果を得られた場合のみ格納
                    if response:
                        for l in response.json()['members']:
                            _list.append(f'{l["username"]}')
                        _map[channel] = _list

        # mapを返す
        return _map
    

    def getDifftimeLastUpdateSec(self, _targetTime):
        '''最終更新時間からの経過秒を返す
        
        Public,Privateそれぞれ指定が可能
        
        Args:
           _targetTime(str): 比較したい時間 ISO時間フォーマット

        Returns:
           list: ユーザ一覧を格納したlist 

        Raises:
           API実行時のエラー 

        Examples:
            >>> list_AllUser = R.getAllUserList() 

        Note:

        '''

        # 引数チェック 型    
        if not isinstance(_targetTime, str):
            print(f'引数：_targetTimeの型が正しくありません str  <-> {type(_targetTime)}')
            raise TypeError

        # 今時間生成
        jst_now = datetime.now(timezone('Asia/Tokyo'))
        target = parser.parse(_targetTime).astimezone(timezone('Asia/Tokyo'))

        # いま時間とターゲット時間の差分を秒で返す
        return (jst_now - target).total_seconds()

            
    def getChannel_id(self, channelname):
        '''Channel名の _id情報を取得する
        
        チャンネル名からチャンネルIDを取得する 

        Args:
           channelname: チャンネル名

        Returns:
           str: チャンネル名に対するチャンネルID 

        Raises:
           API実行時のエラー 

        Examples:
            >>> R.getChannel_id('general') 

        Note:

        '''
        
        # 引数チェック 型    
        if not isinstance(channelname, str):
            print(f'引数：channelの型が正しくありません str  <-> {type(channelname)}')
            raise TypeError

        # ユーザ情報取得API定義
        API = f'{self.URL}/api/v1/rooms.info'

        # MSG組み立て
        msg = {'roomName': channelname,}
        
        # MSG送信
        try:
            response = requests.get(
                API,
                params=msg,
                headers=self.HEADERS,)
        except Exception as e:
            print(f'API実行エラー: {API}')
            print(f'Error: {e}')
            return False
        else:
            if response.json()['success']:
                return response.json()['room']['_id']
            else:
                return False

            
    def sendMessageToRocketChat(self, channel, msg):
        '''指定チャネルにメッセージを送る
        
        指定チャンネルにメッセージを送信する        

        Args:
           channel: チャンネル名
           msg:     送信メッセージ 

        Returns:
           処理結果, HTTP ステータスコード

        Raises:
           API実行時のエラー 

        Examples:
            '>>> R.getUser_id('geneal', 'こんにちわ') 

        Note:

        '''

        # 引数チェック 型    
        if not isinstance(channel, str):
            print(f'引数：channelの型が正しくありません str  <-> {type(channel)}')
            raise TypeError
        
        if not isinstance(msg, str):
            print(f'引数：msgの型が正しくありません str  <-> {type(msg)}')
            raise TypeError
        
        # MSG送信API定義
        API = f'{self.URL}/api/v1/chat.postMessage'
        
        # MSG組み立て
        msg = {'channel': channel,
               'text'   : msg,}
        
        # 指定チャンネルが存在する場合のみ実行 
        if self.getChannel_id(channel):

            # MSG送信
            try:
                response = requests.post(
                    API,
                    data=json.dumps(msg),
                    headers=self.HEADERS,)
            except Exception as e:
                print(f'API実行エラー: {API}')
                print(f'Error: {e}')
                return False
            else:
                pprint(f'Status code: {response.status_code}') 
                return True
        else:
            print(f'指定したチャンネルが存在しません: {channel}')
            return False


    def closeTargetChannel(self, roomname):
        '''パブリック、プライベート区別なくチャンネルを削除する
        
        指定したチャンネル名を削除する 

        Args:
           roomname(str): 削除するチャンネル名

        Returns:

        Raises:
           API実行時のエラー 

        Examples:
            >>> R.closeTargetChannel('テストチャンネル')

        Note:
            まとめて消す仕様ではない、1チャンネルづつターゲットで

        ''' 

        # 引数チェック 型    
        if not isinstance(roomname, str):
            print(f'引数：roomnameの型が正しくありません str  <-> {type(roomname)}')
            raise TypeError
        
        # 削除API定義
        # パブリックもプライベートも区別なくまとめて実施
        APIS = [f'{self.URL}/api/v1/channels.delete',
                f'{self.URL}/api/v1/groups.delete']

        # MSG組み立て
        msg = {'roomId': self.getChannel_id(roomname)}

        # まとめてチャンネル削除を遂行
        for API in APIS:
            try:
                response = requests.post(
                    API,
                    data=json.dumps(msg),
                    headers=self.HEADERS,)
                print(response)
            except Exception as e:
                print(f'API実行エラー: {API}')
                print(f'Error: {e}')
            else:
                # 結果をログっぽく返す
                # 結果を得られた場合のみログを返す
                if response:
                    return response.json()['success']

