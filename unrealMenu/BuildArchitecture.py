import unreal
import SaveGetData as SG


class Build_Architecture:
    def __init__(self):
        self.SG = SG.DataOperation()
        self.projectList = []
        self.projectDict = {}
        self.epsodeList = []
        self.epsodeDict = {}
        self.shotList = []
        self.shotDict = []
        self.newSequenceDirDict = {}
        self.newLevelDirDict = {}
        self.configData = {}
        self.basePath = '/Game/'


    def setConfig(self):
        self.configData = self.SG.getConfig()


    def create_folder(self):
        self.setConfig()
        if self.configData:
            for firstFolder in self.configData.keys():
                if not firstFolder == 'shot_num':
                    self.createDirectory(self.basePath + firstFolder)
                    if self.configData[firstFolder]:
                        for secondFolder in self.configData[firstFolder]:
                            self.createDirectory(self.basePath + firstFolder + '/' + secondFolder)

    def createShotFolderAndSequence(self,project_name,epsode_name,shotList):
        for shotNam in shotList:
            if self.directoryExist(self.basePath + 'SHOT/'):
                shot_path = self.basePath + 'SHOT/' + project_name + '/' + epsode_name + '/' + shotNam
                self.newSequenceDirDict[shot_path] = []
                self.newLevelDirDict[shot_path] = []
                for each_pipe in list(self.configData['shot_num'].keys()):
                    sequence_path = shot_path + '/' + each_pipe
                    self.createDirectory(sequence_path)
                    if self.directoryExist(sequence_path):
                    #     #创建sequence
                        assetPath = sequence_path + '/' + shotNam + '_' + each_pipe + '_sequence'   #J01_animaion_sequence
                        self.newSequenceDirDict[shot_path].append(assetPath)
                        assetClass = unreal.LevelSequence
                        assetClassFactory = unreal.LevelSequenceFactoryNew()
                        self.create_generic_asset(assetPath,True,assetClass,assetClassFactory)
                        self.saveAsset(assetPath)
                    #     #创建level
                        levelPath = sequence_path + '/' + shotNam + '_' + each_pipe + '_level'
                        self.newLevelDirDict[shot_path].append(levelPath)
                        levelClass = unreal.World
                        levelClassFactory = unreal.WorldFactory()
                        self.create_generic_asset(levelPath,True,levelClass,levelClassFactory)
                        self.saveAsset(levelPath)

    def connectSequenceAsset(self):
        for index in range(len(self.newSequenceDirDict.keys())):
            sequences_path = self.newSequenceDirDict[list(self.newSequenceDirDict.keys())[index]]
            level_path = self.newLevelDirDict[list(self.newLevelDirDict.keys())[index]]
            maxind = len(list(self.configData['shot_num'].keys()))  #7
            if maxind > 1:
                for tempindex  in range(maxind -1 ):  #6
                    sub_sequence  = sequences_path[tempindex]  #0-5
                    main_sequence = sequences_path[maxind - 1]     #6
                    display_name = sub_sequence.rsplit('/', 1)[1]
                    sub_sequence_asset = unreal.load_asset(sub_sequence)
                    main_sequence_asset = unreal.load_asset(main_sequence)
                    if self.assetExist(sub_sequence) and self.assetExist(main_sequence):
                        # print('subseq:{0}  add in to mainseq:{1}'.format(sub_sequence,main_sequence))
                        sub_sequence_track = main_sequence_asset.add_track(unreal.MovieSceneSubTrack)
                        sub_sequence_track.set_display_name(display_name)
                        sub_sequence_section = sub_sequence_track.add_section()
                        sub_sequence_section.set_sequence(sub_sequence_asset)

    def testBuild(self):
        # 创建sequence1
        self.newSequenceDirDict[self.basePath] = []
        self.newLevelDirDict[self.basePath] = []
        assetPath = self.basePath + 'dick_sequence'
        self.newSequenceDirDict[self.basePath].append(assetPath)
        assetClass = unreal.LevelSequence
        assetClassFactory = unreal.LevelSequenceFactoryNew()
        self.create_generic_asset(assetPath, True, assetClass, assetClassFactory)
        self.saveAsset(assetPath)
        # # 创建sequence2
        # assetPath1 = self.basePath + 'dick_sequence1'
        #
        # self.newSequenceDirDict[self.basePath].append(assetPath1)
        # assetClass1 = unreal.LevelSequence
        # assetClassFactory1 = unreal.LevelSequenceFactoryNew()
        # self.create_generic_asset(assetPath1, True, assetClass1, assetClassFactory1)
        # self.saveAsset(assetPath1)
        # 创建level1
        levelPath = self.basePath + 'dick_level'
        self.newLevelDirDict[self.basePath].append(levelPath)
        levelClass = unreal.World
        levelClassFactory = unreal.WorldFactory()
        self.create_generic_asset(levelPath, True, levelClass, levelClassFactory)
        self.saveAsset(levelPath)
        #创建level2
        levelPath1 = self.basePath + 'dick_level1'
        self.newLevelDirDict[self.basePath].append(levelPath1)
        levelClass = unreal.World
        levelClassFactory = unreal.WorldFactory()
        self.create_generic_asset(levelPath1, True, levelClass, levelClassFactory)
        self.saveAsset(levelPath1)

    def testConn(self):
        main_seq_path = '/Game/main_sequence'
        sub_seq_path = '/Game/sub_sequence'
        main_sequence_asset = unreal.load_asset(main_seq_path)
        sub_sequence_asset = unreal.load_asset(sub_seq_path)
        sub_sequence_track = main_sequence_asset.add_track(unreal.MovieSceneSubTrack)
        sub_sequence_track.set_display_name('dick_sequence')
        sub_sequence_section = sub_sequence_track.add_section()
        sub_sequence_section.set_sequence(sub_sequence_asset)
        # for index in range(len(self.newLevelDirDict.keys())):
        #     sequences_path = self.newSequenceDirDict[list(self.newSequenceDirDict.keys())[index]]
        #     levels_path = self.newLevelDirDict[list(self.newLevelDirDict.keys())[index]]
        #     if self.assetExist(sequences_path[0]) and self.assetExist(levels_path[0]) and self.assetExist(levels_path[1]):
        #         sequence_asset = unreal.load_asset(sequences_path[0])
        #         main_world = unreal.EditorAssetLibrary.load_asset(levels_path[0])
        #         main1_world = unreal.load_asset(levels_path[1])
        # for index in range(len(self.newSequenceDirDict.keys())):
            #{'/Game/': ['/Game/dick_sequence', '/Game/dick_sequence1']}
            #AttributeError: 'Build_Architecture' object has no attribute 'newlevelDirDict'
            # sequences_path = self.newSequenceDirDict[list(self.newSequenceDirDict.keys())[index]]
            # level_path = self.newLevelDirDict[list(self.newLevelDirDict.keys())[index]]
            # if self.assetExist(sequences_path[0])and self.assetExist(sequences_path[1]) and self.assetExist(level_path):
            #     sequence_asset = unreal.load_asset(sequences_path[0])
            #     sequence1_asset = unreal.load_asset(sequences_path[1])

                # level_asset = unreal.load_asset(level_path)
                # #add subsequence1  MovieSceneSubTrack  MovieSceneCinematicShotTrack
                # subseq_track = sequence_asset.add_track(unreal.MovieSceneSubTrack)
                # subseq_track.set_display_name('subsequence1_asset')
                # subsection = subseq_track.add_section()
                # subsection.set_sequence(sequence1_asset)
            #
            #     #add subsequence2
            #     bind1 = sequence_asset.add_spawnable_from_instance(level_asset)
            #     level_track = bind1.add_track(unreal.MovieScene3DTransformTrack)
            #     level_track.set_display_name('level_asset')

    # loss  level connect function      temp unuse
    def connectAssets(self,sub_asset_path,main_asset_path,sequence_display_name,type = None):

        if self.assetExist(sub_asset_path) and self.assetExist(main_asset_path):
            if type == 'level':
                main_level = unreal.EditorLoadingAndSavingUtils.load_map(main_asset_path)
                sub_level = unreal.EditorLoadingAndSavingUtils.load_map(sub_asset_path)
                main_datalayer_manager = main_level.get_data_layer_manager()
                datalayer_name = sub_asset_path.rsplit('/', 1)[1]
                # main_datalayer = unreal.datalayer


            elif type == 'sequence':
                temptrack = unreal.load_asset(main_asset_path).add_track(unreal.MovieSceneSubTrack)
                temptrack.set_display_name(sequence_display_name)
                tempsection = temptrack.add_section()
                tempsection.set_sequence(unreal.load_asset(sub_asset_path))
            else:
                pass

    # 查询目录是否存在
    def directoryExist(self, dirpath):
        if unreal.EditorAssetLibrary.does_directory_exist(dirpath):
            return True
        else:
            return False

    # 创建目录
    def createDirectory(self, dirpath):
        if not self.directoryExist(dirpath):
            unreal.EditorAssetLibrary.make_directory(dirpath)

    def saveAsset(self, path='', force_save=True):
        return unreal.EditorAssetLibrary.save_asset(asset_to_save=path, only_if_is_dirty=not force_save)
    # 查询某资源是否存在
    def assetExist(self, assPath):
        if unreal.EditorAssetLibrary.does_asset_exist(assPath):
            return True
        else:
            return False

    def create_generic_asset(self, asset_path='', unique_name=True, asset_class=None, asset_factory=None):
        #建立sequence或其他用
        if unique_name:
            asset_path, asset_name = unreal.AssetToolsHelpers.get_asset_tools().create_unique_asset_name(
                asset_path, suffix=''
            )
        if not unreal.EditorAssetLibrary.does_asset_exist(asset_path=asset_path):
            path = asset_path.rsplit('/', 1)[0]
            name = asset_path.rsplit('/', 1)[1]
            return unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                name,
                path,
                asset_class,
                asset_factory
            )
        return unreal.load_asset(asset_path)

    def getOrAddPossessableInSequenceAsset(self, sequence_path='', actor=None):
        sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path))
        possessable = sequence_asset.add_possessable(object_to_possess=actor)
        return possessable

    def getProjectData(self):
        self.projectDict = self.SG.get_CGTW_Data()
        if self.projectDict:
            for pro in self.projectDict.keys():
                self.projectList.append(pro)

    def getEpsodeData(self,project_name):
        database_name = self.projectDict[project_name]
        self.epsodeDict = self.SG.get_CGTW_eps(database_name)
        self.epsodeList = list(self.epsodeDict.keys())

    def getShotData(self,project_name,epsode_name):
        database_name = self.projectDict[project_name]
        self.shotDict = self.SG.get_CGTW_shot(database_name,self.epsodeDict)
        if self.shotDict:
            self.shotList = self.shotDict[epsode_name]
            self.shotList.sort()