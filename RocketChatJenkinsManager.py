#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-

'''RocketChat Jenkins情報取得

  Jenkins情報をRocketChatのチャンネルに提供する 

  Jenkinsの設定によりCSRF対策が行われている
  そのためauth情報だけでなくJenkins-Crumb情報が必要となる。

  1.adminのTOKEN情報
    → adminユーザコンソールからパーソナルアクセストークンを生成する。
      都度生成なのでメモるのを忘れないようにする。

  2.Jenkins-Crumb情報取得方法
    → コマンドを発行する必要がる。以下実行してその戻りにより得られる
      adminのTOKEN設定が設定になっている。
    curl -u 'admin:ADMINS_TOKEN' 'http://xxxxxxx/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'

  3.結果送信は自前ライブラリを使用する様にして下さい。ここでは実装しません。
    RocketChatChannelManager -> sendMessageToRocketChat(channel, msg)1


  Todo:

'''

################################################
# library
################################################

import json
import requests
import pandas as pd
import sys

from datetime import datetime
from dateutil import parser
from pprint import pprint
from pytz import timezone

################################################
# 環境変数取得 
################################################
#
#
# HEADERS定義
# headers = {
#     'Jenkins-Crumb': '4d0e2b6e2f75aff392422caa2fb7b1f924a4c518c4561743273953b05c0cabdb'}
# 認証定義
# AUTH = ('admin', '11062c796463d71a04e56e5c2cf49a26fa')
#
# URL = 'http://192.168.179.3:3000'
# 

################################################
# RocketChatJenkinsManager 
################################################
class RocketChatJenkinsManager(object):
    def __init__(self, HEADERS, AUTH, URL):

        # 引数チェック 型    
        if not isinstance(HEADERS, dict):
            print(f'引数：HEADERSの型が正しくありません dict <-> {type(HEADERS)}')
            raise TypeError

        # 引数チェック 型    
        if not isinstance(AUTH, tuple):
            print(f'引数：AUTHの型が正しくありません tuple <-> {type(AUTH)}')
            raise TypeError

        # 引数チェック 型    
        if not isinstance(URL, str):
            print(f'引数：URLの型が正しくありません str <-> {type(URL)}')
            raise TypeError

        # インスタンス生成
        self.HEADERS = HEADERS
        self.AUTH = AUTH
        self.URL = URL


    def exchangeUnixtimeToTimestamp(self, unixtime):
        '''unixtimeをtimestampに変換する

        Args:
          unixtime: float

        Returns:
          timestamp: str

        Raises:
          TypeError

        Examples:
          >>> jenkins = RocketChatJenkinsManager(HEADERS, AUTH, URL)
          >>> jenkins.exchangeUnixtimeToTimestamp(1610870939803)
             -> '2021/01/17 17:08:59'
        Note:

        '''

        # 引数チェック 型    
        #if not isinstance(unixtime, int):
        #    print(f'引数：unixtimeの型が正しくありません int <-> {type(unixtime)}')
        #    raise TypeError

        timestamp_succsessful = float(unixtime)
        return datetime.fromtimestamp(timestamp_succsessful/1000.).strftime('%Y/%m/%d %H:%M:%S')
    
    
    def getJenkinsJobList(self):
        '''Jenkins 利用可能JOB一覧を取得する

        利用可能JenkinsJOB一覧をPandas DataFrameで返す。

        Args:
          無し

        Returns:
          pd.DataFrame
             Jobname, Params, JobDescription, ExecCount, URL

        Raises:
          API実行時のエラー 

        Examples:
          >>> jenkins = RocketChatJenkinsManager(HEADERS, AUTH, URL)
          >>> df = jenkins.getJenkinsJobList()

        Note:

        '''

        # Columns定義（データ取得）
        columns_in_df = ['JobName', 'JobDescription', 'ExecCount', 'URL','Params']
        # Columns定義（データ出力） 
        columns_out_df = ['JobName', 'Params', 'JobDescription', 'ExecCount', 'URL']

        # API定義
        ENDPOINT = '/api/json'
        QUERY = '?depth=1&tree=jobs[displayName,description,lastCompletedBuild[number,url],actions[parameterDefinitions[name]]]'
        API = f'{self.URL}{ENDPOINT}{QUERY}' 

        # 取得処理
        try:
            response = requests.post(
                API,
                auth=self.AUTH,)    
        except Exception as e:
            print(f'API実行エラー: {API}')
            print(f'Error: {e}')
            return False
        else:
            # 仮の入れ物を用意
            _list1 = []
            _list2 = []

            # 取得responseから情報取得
            ## Job基本情報取得
            for _ in response.json()['jobs']:
                _list1.append([_['displayName'], 
                               _['description'], 
                               _['lastCompletedBuild']['number'], 
                               _['lastCompletedBuild']['url']])
                
                ## 可変であるパラメータ取得
                _list3 = []
                for __ in _['actions']:
                    if (__ != {}) & (__ != {'_class': 'com.cloudbees.plugins.credentials.ViewCredentialsAction'}):
                        _key = ''
                        for ___ in __['parameterDefinitions']:
                            _key += f"param: {___['name']} "
                        _list3.append(_key)
                _list2.append(_list3)

            ## 出力フォーマット処理
            df1 = pd.DataFrame(_list1)
            df2 = pd.DataFrame(_list2)
            df = pd.concat([df1, df2], axis=1)
            df.columns = columns_in_df

            # 出力微調整
            return df[columns_out_df]
             

    def execJenkinsJobListNoParameters(self, jobname):
        '''指定したJenkinsJOB（パラメータなし）をリモート実行する
        
        ここでの役割はJenkinsJobをリモート実行するのみであり
        そのJob実行結果はハンドリングしていない。
        そもそも非同期実行の仕組みになっている。

        Args:
          jobname: str JenkinsJob名、ただしパラメータ定義のないJob 

        Return:
          response: <Response [201]>  実行スケジュールに渡しました

        Raises:
          API実行時のエラー 

        Examples:
          >>> jenkins = RocketChatJenkinsManager(HEADERS, AUTH, URL)
          >>> jenkins.execJenkinsJobListNoParameters('test_hubot')

        Note:

        '''
        # 引数チェック 型    
        if not isinstance(jobname, str):
            print(f'引数：jobnameの型が正しくありません str <-> {type(jobname)}')
            raise TypeError

        # API定義
        ENDPOINT = f'/job/{jobname}/build'
        API = f'{self.URL}{ENDPOINT}'

        # Job投入
        try:
            response = requests.post(
                API,
                headers=self.HEADERS,
                auth=self.AUTH,)    
        except Exception as e:
            print(f'API実行エラー: {API}')
            print(f'Error: {e}')
            return False
        else:
            # Jobリモート投入成功を伝える
            print(f'{jobname}をリモート実行しました')
            print(response) 
            return '201'


    def execJenkinsJobListWithParameters(self, jobname):
        '''指定したJenkinsJOB（パラメータ設定あり）をリモート実行する
        
        ここでの役割はJenkinsJobをリモート実行するのみであり
        そのJob実行結果はハンドリングしていない。
        そもそも非同期実行の仕組みになっている。

        Args:
          jobname: str JenkinsJob名、ただしパラメータ定義のないJob 

        Return:
          response: <Response [201]>  実行スケジュールに渡しました

        Raises:
          API実行時のエラー 

        Examples:
          >>> jenkins = RocketChatJenkinsManager(HEADERS, AUTH, URL)
          >>> jenkins.execJenkinsJobListWithParameters('test_hubot')

        Note:

        '''
        # 引数チェック 型    
        if not isinstance(jobname, str):
            print(f'引数：jobnameの型が正しくありません str <-> {type(jobname)}')
            raise TypeError

        # API定義
        ENDPOINT = f'/job/{jobname}/buildWithParameters'
        API = f'{self.URL}{ENDPOINT}'

        # Job投入
        try:
            response = requests.post(
                API,
                headers=self.HEADERS,
                auth=self.AUTH,)    
        except Exception as e:
            print(f'API実行エラー: {API}')
            print(f'Error: {e}')
            return False
        else:
            # Jobリモート投入成功を伝える
            print(f'{jobname}をリモート実行しました')
            print(response) 
            return '201'


    def _lastBuildTimestamp(self, jobname):
        '''指定したJenkinsJOB（パラメータ設定あり）の最終実行時間を取得する
        

        Args:
          jobname: str JenkinsJob名、ただしパラメータ定義のないJob 

        Retur:
          timestamp: str 最後の成功Build時間 YYYY/MM/DD HH:MM:SS 

        Raises:
          API実行時のエラー 

        Examples:
          >>> jenkins = RocketChatJenkinsManager(HEADERS, AUTH, URL)
          >>> jenkins.lastSuccessfulBuildTimestamp('test_hubot')

        Note:

        '''
        # 引数チェック 型    
        if not isinstance(jobname, str):
            print(f'引数：jobnameの型が正しくありません str <-> {type(jobname)}')
            raise TypeError

        # API定義
        ENDPOINT = f'/job/{jobname}/lastBuild/api/json'
        API = f'{self.URL}{ENDPOINT}'

        # JOBパラメータ定義
        params = (
            ('pretty', 'true'),
        )

        # Job投入
        try:
            response = requests.post(
                API,
                headers=self.HEADERS,
                params=params,
                auth=self.AUTH,)    
        except Exception as e:
            print(f'API実行エラー: {API}')
            print(f'Error: {e}')
            return False
        else:
            # unixtimeをtimestampへ変換して戻す
            return(self.exchangeUnixtimeToTimestamp(response.json()['timestamp']))


    def _lastSuccessfulBuildTimestamp(self, jobname):
        '''指定したJenkinsJOB（パラメータ設定あり）の最終成功時間を取得する
        

        Args:
          jobname: str JenkinsJob名、ただしパラメータ定義のないJob 

        Retur:
          timestamp: str 最後の成功Build時間 YYYY/MM/DD HH:MM:SS 

        Raises:
          API実行時のエラー 

        Examples:
          >>> jenkins = RocketChatJenkinsManager(HEADERS, AUTH, URL)
          >>> jenkins.lastSuccessfulBuildTimestamp('test_hubot')

        Note:

        '''
        # 引数チェック 型    
        if not isinstance(jobname, str):
            print(f'引数：jobnameの型が正しくありません str <-> {type(jobname)}')
            raise TypeError

        # API定義
        ENDPOINT = f'/job/{jobname}/lastSuccessfulBuild/api/json'
        API = f'{self.URL}{ENDPOINT}'

        # JOBパラメータ定義
        params = (
            ('pretty', 'true'),
        )

        # Job投入
        try:
            response = requests.post(
                API,
                headers=self.HEADERS,
                params=params,
                auth=self.AUTH,)    
        except Exception as e:
            print(f'API実行エラー: {API}')
            print(f'Error: {e}')
            return False
        else:
            # unixtimeをtimestampへ変換して戻す
            return(self.exchangeUnixtimeToTimestamp(response.json()['timestamp']))


    def _lastFailedBuildTimestamp(self, jobname):
        '''指定したJenkinsJOB（パラメータ設定あり）の最終失敗時間を取得する
        

        Args:
          jobname: str JenkinsJob名、ただしパラメータ定義のないJob 

        Retur:
          timestamp: str 最後の成功Build時間 YYYY/MM/DD HH:MM:SS 

        Raises:
          API実行時のエラー 

        Examples:
          >>> jenkins = RocketChatJenkinsManager(HEADERS, AUTH, URL)
          >>> jenkins.lastFailedBuildTimestamp('test_hubot')

        Note:

        '''
        # 引数チェック 型    
        if not isinstance(jobname, str):
            print(f'引数：jobnameの型が正しくありません str <-> {type(jobname)}')
            raise TypeError

        # API定義
        ENDPOINT = f'/job/{jobname}/lastFailedBuild/api/json'
        API = f'{self.URL}{ENDPOINT}'

        # JOBパラメータ定義
        params = (
            ('pretty', 'true'),
        )

        # Job投入
        try:
            response = requests.post(
                API,
                headers=self.HEADERS,
                params=params,
                auth=self.AUTH,)    
        except Exception as e:
            print(f'API実行エラー: {API}')
            print(f'Error: {e}')
            return False
        else:
            # unixtimeをtimestampへ変換して戻す
            return(self.exchangeUnixtimeToTimestamp(response.json()['timestamp']))


    def getJobInformation(self, jobname):
        '''指定したJenkinsJOB（パラメータ設定あり）の実行情報を取得する
        

        Args:
          jobname: str JenkinsJob名、ただしパラメータ定義のないJob 

        Return:
          joburl:  str
          job情報: DataFrame

        Raises:
          API実行時のエラー 

        Examples:
          >>> jenkins = RocketChatJenkinsManager(HEADERS, AUTH, URL)
          >>> jenkins.getJobInformation('test_hubot')

        Note:

        '''
        # 引数チェック 型    
        if not isinstance(jobname, str):
            print(f'引数：jobnameの型が正しくありません str <-> {type(jobname)}')
            raise TypeError

        # API定義
        ENDPOINT = f'/job/{jobname}/api/json'
        API = f'{self.URL}{ENDPOINT}'

        # JOBパラメータ定義
        params = (
            ('pretty', 'true'),
        )

        # Job投入
        try:
            response = requests.post(
                API,
                headers=self.HEADERS,
                params=params,
                auth=self.AUTH,)    
        except Exception as e:
            print(f'API実行エラー: {API}')
            print(f'Error: {e}')
            return False
        else:
            # JobLinkPath生成
            joburl = f"{response.json()['url']}"

            # 基本情報をまとめる
            _list = []
            _list.append([f"Job名",                  f"{response.json()['displayName']}"])
            _list.append([f"Job詳細",                f"{response.json()['description']}"])
            _list.append([f"HealthReport",           f"{response.json()['healthReport'][0]['description']}"])
            _list.append([f"JobStatus Color",        f"{response.json()['color']}"])
#            _list.append([f"Job最新実行:失敗判定",   f"{response.json()['lastUnstableBuild']}"])
            _list.append([f"Job最終BuildNo.",        f"{response.json()['lastBuild']['number']}"])
            _list.append([f"Job最終Build時間",       f"{self._lastBuildTimestamp(jobname)}"]) 
            _list.append([f"Job最終成功BuildNo.",    f"{response.json()['lastSuccessfulBuild']['number']}"])
            _list.append([f"Job最終成功Build時間",   f"{self._lastSuccessfulBuildTimestamp(jobname)}"]) 
            _list.append([f"Job最終失敗BuildNo.",    f"{response.json()['lastFailedBuild']['number']}"])
            _list.append([f"Job最終失敗Build時間",   f"{self._lastFailedBuildTimestamp(jobname)}"]) 
            
            # DataFrame生成
            df = pd.DataFrame(_list)
            df.columns = ['項目', 'ステータス']
            return joburl, df
 
