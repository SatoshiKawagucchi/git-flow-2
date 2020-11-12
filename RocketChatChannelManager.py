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
from pprint import pprint
from pytz import timezone


################################################
# Basic Class
################################################

class RocketChatManager(object):
    def __init__(self):

        #TODO yaml化
        self.HEADERS ={
            'X-Auth-Token': 'zYGeveBMm79longHcJTwFi425FB6qyLxXDuRXUHAXDS',
            'X-User-Id': 'sny2QJnFfBHBK4Prc',
            'Content-Type': 'application/json'}
        
        self.URL = 'http://192.168.179.3:3000'
        self.INIT_PASS = 'p@ssw0rd'


################################################
# RocketChatChannelManager 
################################################
class RocketChatChannelManager(RocketChatManager):
    def __init__(self):
        super().__init__()
#        if __DEBUG__: print(self.HEADERS, self.URL)
    
    
    def getChannelPubliclist(self):
        '''パブリックチャネルのリストと最終更新時間のマップ
        
        パブリックチャンネル名とチャンネル最終更新時間のマップを作成する。
        ついでにパブリックチャネル名一覧リストを作成する。

        Args:

        Returns:
           list: パブリックチャンネル一覧
           map:  パブリックチャンネル名と最終更新時間のマップ 

        Raises:
           API実行時のエラー 

        Examples:
            >>> list, map = self.getChannelPubliclist() 

        Note:

        '''

        # 結果格納
        _list = []
        _map = {}

        # API定義
        API = f'{self.URL}/api/v1/channels.list'

        # 取得処理
        try:
            response = requests.get(
                API,
                headers=self.HEADERS,)    
        except Exception as e:
            print(f'{e}')
        finally:
            for l in response.json()['channels']:
                _map[l['name']] = l['_updatedAt']
                _list.append(l['name'])

            # listとmapを返す
            return _list, _map

        
    def getChannelPrivatelist(self):
        '''プライベートチャネルのリストと最終更新時間のマップ

        プライベート名とチャンネル最終更新時間のマップを作成する。
        ついでにプライベート名一覧リストを作成する。

        Args:

        Returns:
           list: プライベート一覧
           map:  プライベート名と最終更新時間のマップ 

        Raises:
           API実行時のエラー 

        Examples:
            >>> list, map = self.getChannelPrivatelist() 

        Note:

        '''

        # 結果格納
        _list = []
        _map = {}

        # API定義
        API = f'{self.URL}/api/v1/groups.listAll'
       
        # 取得処理
        try:
            response = requests.get(
                API,
                headers=self.HEADERS,)    
        except Exception as e:
            print(f'{e}')
        finally:
            for l in response.json()['groups']:
                _map[l['name']] = l['_updatedAt']
                _list.append(l['name'])

            # listとmapを返す
            return _list, _map    
          

    def getChannellist(self):
        '''チャンネル一覧およびチャンネルの最終更新時間を取得する

        パブリック、プライベート両方のチャンネルをまとめて処理する

        Args:

        Returns:
           list: チャンネル一覧のリスト
           map: チャンネル名と所属ユーザリストのマップ 

        Raises:
           API実行時のエラー 

        Examples:
            >>> list_, map_ = R.getChannellist()

        Note:
            getChannelPubliclist()やgetChannelPrivatelist()と併用する感じ
            パブリック、プライベートまとめて取得

        '''

        # public,privateそれぞれ取得
        _list_public, _map_public = self.getChannelPubliclist()
        _list_private, _map_private = self.getChannelPrivatelist()

        # listとmapを結合して返す
        _list_public.extend(_list_private)
        _map_public.update(_map_private)

        return _list_public, _map_public
              
            
    def getChannelUserlist(self, list_channelname):
        '''チャネル毎の登録ID一覧
        
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
            >>> list_Public, map_Public = R.getChannelPubliclist()
            >>> _map = R.getChannelUserlist(list_Public)

            >>> list_Private, map_Private = R.getChannelPrivatelist()
            >>> _map = R.getChannelUserlist(list_Private)

        Note:
            getChannelPubliclist()やgetChannelPrivatelist()と併用する感じ

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
        
        # MSG発信チャンネル定義
        CHANNEL_LIST = list_channelname 
        
        # 1000人は超えないだろう。。。から
        COUNT = '1000'
        
        # 対象チャンネル名リストでループ
        for channel in CHANNEL_LIST:

            # MSG組み立て 
            msg = (('roomName', channel),('count',COUNT),) 
#            if __DEBUG__: print(msg)
            
            # API発行
            for api in APIS:
                try:
                    response = requests.get(
                        api,
                        params=msg,
                        headers=self.HEADERS,)
                except Exception as e:
                    print(f'{e}')
                finally:
                    # ユーザたちを格納するList
                    _list = []
                    
                    # 結果を得られ場合のみ格納
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
#        if __DEBUG__: print(jst_now, target)

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
#        if __DEBUG__: print(msg)
        
        # MSG送信
        try:
            response = requests.get(
                API,
                params=msg,
                headers=self.HEADERS,)
        except Exception as e:
            print(f'{e}')
        finally:
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
#        if __DEBUG__: print(msg)
        
        # 指定チャンネルが存在する場合のみ実行 
        if getChannel_id(channel):

            # MSG送信
            try:
                response = requests.post(
                    API,
                    data=json.dumps(msg),
                    headers=self.HEADERS,)
            except Exception as e:
                print(f'{e}')
            finally:
                pprint(response.status_code) 
        else:
            print(f'指定したチャンネルが存在しません: {channel}')


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
#        if __DEBUG__: print(msg)

        # まとめてチャンネル削除を遂行
        for api in APIS:
            try:
                response = requests.post(
                    API,
                    data=json.dumps(msg),
                    headers=self.HEADERS,)
                print(response)
            except Exception as e:
                print(f'{e}')
            finally:
                # 結果をログっぽく返す
                # 結果を得られた場合のみログを返す
                if response:
                    return response.json()        
