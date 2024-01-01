#coding=utf-8
import sys
import os
import json
import unreal
sys.path.append(r'c:/CgTeamWork_v6/bin/base')
import cgtw2


class DataOperation:
    def __init__(self):
        self.cgtw = cgtw2.tw()
        self.projectDict = {}
        self.isDebug = False
        self.configDict = self.getConfig()
        self.laucherData = ['192.168.1.246:8383','TDDATA','abc123456']

    def importAnimationAssets(self,fbx_path,save_asset_path,skeleton_path):
        animation_task = self.buildImportTask(fbx_path, save_asset_path,self.buildAnimationImportOptions(skeleton_path))


    def buildImportTask(self, filename, destination_path, options=None):
        task = unreal.AssetImportTask()
        task.set_editor_property('automated', True) #avoid dialogs
        task.set_editor_property('destination_name', '') #optional new custom name to import as
        task.set_editor_property('destination_path', destination_path) #content path
        task.set_editor_property('filename', filename) #filename to import
        task.set_editor_property('replace_existing', True)
        task.set_editor_property('save', True)
        #task.set_editor_property('result',returnObj)   return imported object
        task.set_editor_property('option', options) #import options specific to the type of asset
        return task

    def buildAnimationImportOptions(self,skeletonPath):
        options = unreal.FbxImportUI()

        options.set_editor_property('import_animations',True)
        options.skeleton = unreal.load_asset(skeletonPath)

        options.anim_sequence_import_data.set_editor_property('import_translate',unreal.Vector(50.0, 0.0, 0.0))
        options.anim_sequence_import_data.set_editor_property('import_rotation', unreal.Vector(0.0, 0.0, 0.0))
        options.anim_sequence_import_data.set_editor_property('import_uniform_scale', 1.0)

        options.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
        options.anim_sequence_import_data.set_editor_property('remove_redundant_key', False)
        return options

    def setupCGTW(self,IP=None,account=None,password=None):
        if self.isDebug:
            print(self.cgtw.login.http_sever_ip())
        else:
            if not IP:
                self.cgtw = cgtw2.tw(self.laucherData[0],self.laucherData[1],self.laucherData[2])
            else:
                self.cgtw = cgtw2.tw(IP,account,password)

    def get_CGTW_Data(self,IP=None,account=None,password=None):
        if not self.isDebug:
            self.setupCGTW(IP,account,password)
            idList = self.cgtw.info.get_id('public', 'project', [])
            tempList = self.cgtw.info.get('public', 'project', idList, ['project.entity', 'project.database'])
            if tempList:
                for project in tempList:
                    self.projectDict[project['project.entity']] = project['project.database']
        else:
            self.projectDict = {'ZW':'proj_zw'}
        return self.projectDict

    def get_CGTW_eps(self,database_name):
        if not self.isDebug:
            epsDict = {}
            epsIDs = self.cgtw.info.get_id(database_name,'eps',[])
            epsDataList = self.cgtw.info.get(database_name,'eps',epsIDs,['eps.id','eps.entity'])
            if epsDataList:
                for epsInfo in epsDataList:
                    epsDict[epsInfo['eps.entity']] = epsInfo['eps.id']
        else:
            epsDict = {'J01': '27480F90-5566-686B-74F1-0D72CE377211', 'J02': '84B6B7EF-9503-4117-61EB-929CD75B5507', 'J03': '4729C79F-4286-1E90-9055-61EC335AA54E', 'J04': '304B9DCE-5A8E-CD3E-088A-840492917D88', 'J05': '94D0FB95-C6A1-FF35-9DC3-35494FCAA794', 'PV': 'CDCFBB3A-5F9D-FCEC-7CCE-A7582A10286C', 'J06': 'F48AD2D8-942D-4E43-63B9-6F93E86CF2C8', 'J07': '2D92D621-A706-4B03-8C8E-78A8E146EB36', 'J08': '91C7E2BB-14E8-AEDE-7090-B17FEC35C9D7', 'J09': '0B9B22B1-2A74-3863-2804-3FEE70D7F6BF', 'J10': 'CF2BBC96-EF85-A115-7B07-AD73590ED1E6', 'PV02': '1E092760-A409-3644-2E39-B4B7415E3929'}

        return epsDict

    def get_CGTW_shot(self,database_name,epsDict):
        if not self.isDebug:
            shotDict = {}
            for key in epsDict.keys():
                shotDict[key] = []

            shotIDs = self.cgtw.info.get_id(database_name, 'shot', [])
            shotDataList = self.cgtw.info.get(database_name, 'shot', shotIDs, ['shot.link_eps', 'shot.entity'])
            if shotDataList:
                for shotInfo in shotDataList:
                    for eps in list(epsDict.keys()):
                        if shotInfo['shot.link_eps'] == eps:
                            shotDict[shotInfo['shot.link_eps']].append(shotInfo['shot.entity'])
        else:
            shotDict = {'J01': [], 'J02': [], 'J03': [], 'J04': [], 'J05': [], 'PV': ['PV_021', 'PV_001', 'PV_007-008', 'PV_005', 'PV_006', 'PV_009-011', 'PV_004', 'PV_019', 'PV_002', 'PV_003', 'PV_020', 'PV_016', 'PV_014-015', 'PV_017', 'PV_012', 'PV_012A', 'PV_013', 'PV_017A', 'PV_018'], 'J06': [], 'J07': [], 'J08': [], 'J09': [], 'J10': [], 'PV02': ['PV02_035', 'PV02_020', 'PV02_031', 'PV02_024', 'PV02_026', 'PV02_014', 'PV02_036', 'PV02_039', 'PV02_042', 'PV02_022', 'PV02_048', 'PV02_017', 'PV02_015', 'PV02_003A', 'PV02_005', 'PV02_030', 'PV02_027', 'PV02_046', 'PV02_047', 'PV02_028', 'PV02_038', 'PV02_012', 'PV02_011', 'PV02_020C', 'PV02_018', 'PV02_032', 'PV02_049', 'PV02_019', 'PV02_041', 'PV02_037', 'PV02_020E', 'PV02_040', 'PV02_033', 'PV02_029', 'PV02_021', 'PV02_044', 'PV02_045', 'PV02_003', 'PV02_010', 'PV02_013', 'PV02_016', 'PV02_001', 'PV02_043', 'PV02_050', 'PV02_002', 'PV02_006', 'PV02_009', 'PV02_004', 'PV02_016A', 'PV02_020F', 'PV02_008A', 'PV02_020G', 'PV02_017B', 'PV02_017A', 'PV02_020D', 'PV02_020A', 'PV02_008C', 'PV02_025', 'PV02_034', 'PV02_011A', 'PV02_007', 'PV02_023', 'PV02_008', 'PV02_008B', 'PV02_020B']}
        return shotDict

    def get_CGTW_SHOT_dir(self,database_name,epsode_name,shot_name):
        if not self.isDebug:
            shot_Namdir_Dict= []
            shotIDs = self.cgtw.task.get_id(database_name, 'shot', [['eps.entity','=',epsode_name],'and',['shot.entity','=',shot_name]])
            for eachPipe in list(self.configDict['shot_num'].keys()):
                eachPipe_name = self.configDict['shot_num'][eachPipe]
                tempresult = self.cgtw.task.get_field_and_dir(database_name,'shot',shotIDs,['task.entity'],[self.configDict['shot_num'][eachPipe_name]])
                tempDir = tempresult[0][eachPipe_name]
                shot_Namdir_Dict[eachPipe] = tempDir

            # [{'task.entity': '简模', 'id': '8C1EFA37-7107-ECC0-67C8-875EDCA4C0A8', '分镜': 'H:/Projects/ZW/Shot/Layout'}, {'task.entity': '群集', 'id': '2D2D4FF1-0D53-1194-8401-B93AEBE5AC01', '分镜': 'H:/Projects/ZW/Shot/Layout'}, {'task.entity': '动画一审', 'id': '68F95AF5-7777-0AE5-3B17-B49D3D625AEA', '分镜': 'H:/Projects/ZW/Shot/Layout'}, {'task.entity': '灯光', 'id': 'E7745A69-BFFA-A793-407D-7DEA766DF1D3', '分镜': 'H:/Projects/ZW/Shot/Layout'}, {'task.entity': '特效', 'id': 'A72F7CDF-875F-E33C-1A00-2BD1205BE8F7', '分镜': 'H:/Projects/ZW/Shot/Layout'}, {'task.entity': '解算', 'id': '42926BAC-F6C2-20F4-B464-0E0F13E3AF35', '分镜': 'H:/Projects/ZW/Shot/Layout'}, {'task.entity': '动画', 'id': '1727B208-E449-5313-45D1-DEE95882F547', '分镜': 'H:/Projects/ZW/Shot/Layout'}, {'task.entity': '合成', 'id': '155EC4EF-74F8-7EE0-B35F-A17A5D60C6A5', '分镜': 'H:/Projects/ZW/Shot/Layout'}]
            # tempresult_light = self.cgtw.task.get_field_and_dir(database_name, 'shot', shotIDs, ['task.entity'], [self.configDict['shot_num']['Light']])
            # [{'task.entity': '简模', 'id': '8C1EFA37-7107-ECC0-67C8-875EDCA4C0A8', '灯光': 'H:/Projects/ZW/Shot/Lighting'}, {'task.entity': '群集', 'id': '2D2D4FF1-0D53-1194-8401-B93AEBE5AC01', '灯光': 'H:/Projects/ZW/Shot/Lighting'}, {'task.entity': '动画一审', 'id': '68F95AF5-7777-0AE5-3B17-B49D3D625AEA', '灯光': 'H:/Projects/ZW/Shot/Lighting'}, {'task.entity': '灯光', 'id': 'E7745A69-BFFA-A793-407D-7DEA766DF1D3', '灯光': 'H:/Projects/ZW/Shot/Lighting'}, {'task.entity': '特效', 'id': 'A72F7CDF-875F-E33C-1A00-2BD1205BE8F7', '灯光': 'H:/Projects/ZW/Shot/Lighting'}, {'task.entity': '解算', 'id': '42926BAC-F6C2-20F4-B464-0E0F13E3AF35', '灯光': 'H:/Projects/ZW/Shot/Lighting'}, {'task.entity': '动画', 'id': '1727B208-E449-5313-45D1-DEE95882F547', '灯光': 'H:/Projects/ZW/Shot/Lighting'}, {'task.entity': '合成', 'id': '155EC4EF-74F8-7EE0-B35F-A17A5D60C6A5', '灯光': 'H:/Projects/ZW/Shot/Lighting'}]
        else:
            shot_Namdir_Dict= {'layout':'H:/Projects/ZW/Shot/Layout','animation':'H:/Projects/ZW/Shot/animation','CFX':'H:/Projects/ZW/Shot/CFX','VFX':'H:/Projects/ZW/Shot/VFX',
                                'Light':'H:/Projects/ZW/Shot/Lighting','Comp':'H:/Projects/ZW/Shot/comp'}
        return shot_Namdir_Dict


    def getCurrentPath(self):

        if not sys.modules.get('__file__'):
            import inspect
            __file__ = os.path.abspath(inspect.getfile(inspect.currentframe()))
            return  os.path.dirname(__file__).replace('\\', '/')
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def saveConfig(self, folderDict):

        self.saveData(folderDict, self.getCurrentPath() + '/bin/config.txt')

    def getConfig(self):
        config = self.getData(self.getCurrentPath() + '/bin/config.txt')

        return config

    def getData(self, path):
        try:
            with open(path, 'r') as fin:
                Data = json.load(fin)
                return Data
        except:
            print(u'数据读取出错')




    def saveData(self, data, savePath):
        try:
            dataPath = savePath
            with open(dataPath, 'w') as fout:
                json.dump(data, fout)
            return 1
        except:
            print(u'数据写入出错')
            return 0

if __name__ == '__main__':
    DO = DataOperation()
    # print(DO.getCurrentPath())

    # DO.setupCGTW()
    # DO.get_CGTW_SHOT_dir('proj_zw','PV','PV_001')

    #print(DO.testCGTW())

    # configData = {'JS':['MeiBangDing','BangDing','BP'],'DJ': ['MeiBangDing','BangDing','BP'],'CJ': ['MeiBangDing','Map'],'SHOT': [],'shot_num':{'layout':'分镜','Animation':u'动画','CFX':u'解算','VFX':u'特效','Light':u'灯光','Effect':u'','Comp':u'合成'}}
    # DO.saveConfig(configData)