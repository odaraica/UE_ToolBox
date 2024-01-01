#coding=utf-8
import unreal
import os
import SaveGetData as SG



class ImportAnimAsset():
    def __init__(self):
        self.SG = SG.DataOperation()
        self.skeletonMeshList = []
        self.sequenceDict = {}
        self.configDict = self.SG.getConfig()
        self.fbxPathDict = []
        self.sequenceList = []
        self.projectList = []
        self.epsodeList = []
        self.epsodeDict = {}
        self.shotList = []
        self.shotDict = {}
        self.basePath = '/Game/'




    def getSkeletonPath(self):
        #JS_name  JS_XiongMao    skefilename    JS_XiongMao_mat_forUE_skeletion
        assetList = unreal.EditorAssetLibrary.list_assets(self.basePath + 'JS/BangDing/')
        for asset in assetList:
            if asset.endswith('_skeleton'):
                self.skeletonMeshList.append(asset)

    def getSequencePath(self,project_name,epsode_name,shotList):
        for shotNam in shotList:
            sequencePath = self.basePath + '/shot/' + 'SHOT/' + project_name + '/' + epsode_name + '/' + shotNam
            for each_pipe in list(self.configDict['shot_num'].keys()):
                sequence_asset_path = sequencePath + '/' + shotNam + '_' + each_pipe + '_sequence'
                if self.assetExist(sequence_asset_path):
                    self.sequenceDict[shotNam] = sequence_asset_path


    def importAnimFBX(self,project_name,epsode_name,shotList):
        for shotNam in shotList:
            cgtw_path_dict = self.SG.get_CGTW_SHOT_dir(project_name,epsode_name,shotNam)
            fbx_path = cgtw_path_dict['animation'] + '/fbx/'
            files = os.listdir(fbx_path)
            for file in files:
                if file.endswith('.fbx'):
                    save_path = self.basePath + 'SHOT/' + project_name + '/' + epsode_name + '/' + shotNam + '/'
                    sequence_path = save_path + shotNam + '_animation' + '_sequence'
                    level_path    = save_path + shotNam + '_animation' + '_level'
                    if '_cam' in file or '_CAM' in file:
                        fbx_file_path = fbx_path + file
                        if self.import_fbx_onto_sequence(level_path,sequence_path,fbx_file_path):
                            pass
                        else:
                            print('fbx:{0} add on sequence:{1} failed,please check'.format(fbx_file_path,sequence_path))

                    else:
                        fbx_file_path = fbx_path + file
                        filename = file.rsplit('.', 1)[0]
                        fbx_save_path = save_path + filename +'_animation'
                        for skeletonPath in self.skeletonMeshList:
                            JS_name = skeletonPath.rsplit('/', 1)[1]
                            JS_name = JS_name[:-9]
                            if JS_name in filename:
                                if self.importAnimAsset(fbx_file_path,fbx_save_path,skeletonPath):

                                    self.addToLevel(fbx_save_path,level_path)
                                else:
                                    print('animation file fbx:{0] import failed,please check'.format(fbx_file_path))

    def importAnimAsset(self,fbx_path,save_asset_path,skeleton_path):
        task = self.SG.importAnimationAssets(fbx_path,save_asset_path,skeleton_path)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(task)
        if self.assetExist(save_asset_path):
            return True
        else:
            return False

    def import_fbx_onto_sequence(self,map_asset_path, sequence_asset_path, input_fbx_file):
        # Load the map, get the world
        world = unreal.EditorLoadingAndSavingUtils.load_map(map_asset_path)
        sequence = unreal.load_asset(sequence_asset_path, unreal.LevelSequence)
        bindings = sequence.get_bindings()
        # Set Options
        import_options = unreal.MovieSceneUserImportFBXSettings()
        import_options.set_editor_property("create_cameras",True)
        import_options.set_editor_property("match_by_name_only ", True)
        import_options.set_editor_property("reduce_keys", False)
        # Import
        result = unreal.SequencerTools.import_level_sequence_fbx(world, sequence, bindings, import_options,input_fbx_file)
        return result
    def importCamAsset(self):
        pass

    def addToLevel(self,fbx_asset_path,level_asset_path):
        pass

    def assetExist(self, assPath):
        if unreal.EditorAssetLibrary.does_asset_exist(assPath):
            return True
        else:
            return False

    def directoryExist(self, dirpath):
        if unreal.EditorAssetLibrary.does_directory_exist(dirpath):
            return True
        else:
            return False
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



