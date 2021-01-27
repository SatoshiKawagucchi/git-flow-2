def mapFromProjectIDtoProjectName(self):
    _map = {}
  
    projects = self.gitlab.projects.list(all=True)
    for _ in projects:
        _map[_.attributes['id']] = _.attributes['name']
    
    return _map


def getCommitList(self):
    # self.gitlabにインスタンス生成結果が入っている
    
    # DataFrameカラム定義
    ## class内で定義するとことにする
    columns = ['commited_date','project_id', 'project_name', 'hexsha', 'Commiter', '追加行', '削除行', 'filename', 'CommitMessage']
    
    # コミット情報格納リスト
    _list = []

    # project一覧を取得
    try:
        projects = self.gitlab.projects.list(all=True)
    except Exception as e2:
        print(f'{e2}')

    # プロジェクト単位に情報取得
    for project in projects:

        # コミット毎の情報を取得する
        # プロジェクト：コミット = 1:n
        try:
            commits = project.commits.list()
        except Exception as e3:
            print(f'{e3}')        

        for commit in commits:
            # コミット単位に情報を得る
            try:
                commit_id = project.commits.get(commit.attributes['id'])
            except Exception as e4:
                print(f'{e4}')        

            # コミット毎のdiff情報を取得する
            ## コミット:差分モジュール数 = 1:n
            for commit_id_diff in commit_id.diff():

                # 選別処理を行う
                _map = {}
                _list_add = []
                _list_del = []

                # コード分離
                ## 差分検出した固まりを1行単位に分割する
                _list_temps = commit_id_diff['diff'].split('\n')

                # 追加、削除をカウント（対象コードも溜めてみる）
                ## 追加行：先頭 +で始まる
                ## 追加行：先頭 -で始まる
                for _list_temp in _list_temps:
                    if _list_temp.startswith('+'):
                        _list_add.append(commit_id_diff)
                    if _list_temp.startswith('-'):
                        _list_del.append(commit_id_diff)
                    _map[commit_id_diff['new_path']] = [_list_add, _list_del]

                # 結果を蓄積
                for filename, changeline in _map.items():
                    # 追加、削除がないものは対象外とする
                    ## changeline[0]:追加行
                    ## changeline[1]:削除行                
                    if len(changeline[0]) != 0 or  len(changeline[1]) != 0:
                        # 蓄積
                        _list.append([commit.attributes['committed_date'],
                                      commit.attributes['project_id'],
                                      map_ProjectIDtoProjectName[commit.attributes['project_id']],
                                      commit.attributes['id'],
                                      commit.attributes['committer_name'],
                                      len(changeline[0]),
                                      len(changeline[1]),
                                      filename,                              
                                      commit.attributes['title'],
                                     ])

    # DataFrame化
    df = pd.DataFrame(_list)
    df.columns = columns

    # タイムゾーンがばらばらなので一旦UTCで統一する
    # datetime64[ns, UTC]になっている。
    # tz統一なく to_datetime()を行ってもdatetime64型にならない
    df['commited_date'] = pd.to_datetime(df['commited_date'],utc=True)
    df['commited_date'] = df['commited_date'].dt.tz_convert('Asia/Tokyo')
    df.set_index('commited_date', inplace=True)
    pprint(df.head())

    return df
