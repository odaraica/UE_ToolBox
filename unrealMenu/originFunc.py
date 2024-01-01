#coding=utf-8
import unreal


class ImportAsset():
    def __init__(self):
        self.fbxPath = ''
        self.buildPosition = ''
        self.skeletonMeshPath = ''
        self.staticMeshPath = ''
        self.texturepath = ''
        self.soundpath = ''
        self.animFilePath = ''

        self.contentSkeletonPath = ''   #skeletonMesh导入之后 skeleton骨架在content里的路径

    # unreal.LevelSequence unreal.LevelSequenceFactoryNew()
    # unreal.Material      unreal.MaterialFactoryNew()
    # unreal.World         unreal.WorldFactory()

    def create_generic_asset(self,asset_path='',unique_name=True,asset_class=None,asset_factory=None):
        if unique_name:
            asset_path,asset_name = unreal.AssetToolsHelpers.get_asset_tools().create_unique_asset_name(
                base_package_name = asset_path,suffix = ''
            )
        if not unreal.EditorAssetLibrary.does_asset_exist(asset_path = asset_path):
            path = asset_path.rsplit('/',1)[0]
            name = asset_path.rsplit('/',1)[1]
            return unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                asset_name = name,
                asset_path = path,
                asset_class = asset_class,
                factory = asset_factory
            )
        return unreal.load_asset(asset_path)

    def importAnimationAssets(self):
        animation_task = self.buildImportTask(self.animFilePath,'/Game/Animations',self.buildAnimationImportOptions(self.contentSkeletonPath))

        self.execuImportTasks([animation_task])

    def importMeshAssets(self):
        staticMesh_task = self.buildImportTask(self.staticMeshPath,'/Game/StaticMeshes',self.buildStaticMeshImportOptions())
        skeletonMesh_task = self.buildImportTask(self.skeletonMeshPath,'/Game/SkeletonMeshes',self.buildSkeletonMeshImportOptions())

        self.execuImportTasks([staticMesh_task,skeletonMesh_task])

    def importSimpleAssets(self):
        texture_task = self.buildImportTask(self.texturepath,'/Game/Textures')
        sound_task = self.buildImportTask(self.soundpath,'/Game/Sounds')

        self.execuImportTasks([texture_task,sound_task])

    def execuImportTasks(self,tasks):
        # fbx_task = unreal.buildImportTask(self.fbxPath,
        #                                   self.buildPosition,
        #                                   unreal.buildAni)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
        for task in tasks:
            for path in task.get_editor_property('imported_object_paths'):
                print('imported:{}'.format(path))

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

    def buildStaticMeshImportOptions(self):
        options = unreal.FbxImportUI()
        options.set_editor_property('import_mesh',True)
        options.set_editor_property('import_textures', False)
        options.set_editor_property('import_materials', True)
        options.set_editor_property('import_as_skeletal', False)

        options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(50.0,0.0,0.0))
        options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0,0.0,0.0))
        options.static_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)

        options.static_mesh_import_data.set_editor_property('combine_meshes', True)
        options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
        options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)

        return options

    def buildSkeletonMeshImportOptions(self):
        options = unreal.FbxImportUI()
        options.set_editor_property('import_mesh', True)
        options.set_editor_property('import_textures', False)
        options.set_editor_property('import_materials', True)
        options.set_editor_property('import_as_skeletal', True)

        options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(50.0, 0.0, 0.0))
        options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
        options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)

        options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
        options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', True)
        return options

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



    #查询目录是否存在
    def directoryExist(self,dirpath):
        if unreal.EditorAssetLibrary.does_directory_exist(dirpath):
            return True
        else:
            return False
    #创建目录
    def createDirectory(self,dirpath):
        if not self.directoryExist(dirpath):
            unreal.EditorAssetLibrary.make_directory(dirpath)
    #复制目录及内容
    def duplicateDirectory(self,dirpath,newpath):
        #复制的意思是 newpath会被创建  同时dirpath里的东西会被复制到newpath里
        if self.directoryExist(dirpath) and not self.directoryExist(newpath):
            unreal.EditorAssetLibrary.duplicate_directory(dirpath,newpath)
    #删除目录
    def deleteDirectory(self,dirpath):
        if self.directoryExist(dirpath):
            unreal.EditorAssetLibrary.delete_directory(dirpath)
    #重命名目录 注意newNam也是一个完整路径带着最后的文件夹名
    def renameDirectory(self,dirpath,newNam):
        if self.directoryExist(dirpath):
            unreal.EditorAssetLibrary.rename_directory(dirpath,newNam)

    #查询某资源是否存在
    def assetExist(self,assPath):
        if unreal.EditorAssetLibrary.does_asset_exist(assPath):
            return True
        else:
            return False
    #复制资源
    def duplicateAsset(self,assPath,newPath):
        if self.assetExist(assPath) and not self.assetExist(newPath):
            unreal.EditorAssetLibrary.duplicate_asset(assPath,newPath)

    #删除资源
    def deleteAsset(self,assPath):
        if self.assetExist(assPath):
            unreal.EditorAssetLibrary.delete_asset(assPath)

    #重命名资源
    def renameAsset(self,assPath,newNam):
        if self.assetExist(assPath) and not self.assetExist(newNam):
            unreal.EditorAssetLibrary.rename_asset(assPath,newNam)


    #保存某个文件
    def saveAsset(self,path='',force_save = True):
        return unreal.EditorAssetLibrary.save_asset(asset_to_save = path,only_if_is_dirty = not force_save)
    #保存某个content目录下的所有文件
    def saveDiractory(self,path = '',force_save=True,rec=True):
        return unreal.EditorAssetLibrary.save_directory(directory_path = path,only_if_is_dirty = not force_save,recursive = rec)


    def getPackageFromPath(self,path):
        return unreal.load_package(path)

    #获得所有 未保存（带星）的内容和地图(umap) 的list
    def getAllDirtyPackages(self):
        packages = []
        for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
            packages.append(x)
        for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages():
            packages.append(x)
        return packages

    def savePackages(self,packages=[],show_dialog=False):
        if show_dialog:
            return unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(packages=[],show_dialog=show_dialog)

    def saveAllDirtyPackages(self,show_dialog=False):
        if show_dialog:
            return unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(save_map_packages=True,save_content_packages=True)
        else:
            return unreal.EditorLoadingAndSavingUtils.save_dirty_packages(save_map_packages=True,save_content_packages=True)

    # return: str List : The asset paths that are currently selected
    def getSelectedAssets(self):
        return unreal.CppLib.get_selected_assets()

    # asset_paths: str List : The asset paths to select,将列表里的资源全选中
    def setSelectedAssets(self,asset_paths=[]):
        unreal.CppLib.set_selected_assets(asset_paths)

    # return: str List : The folder paths that are currently selected
    def getSelectedFolders(self):
        return unreal.CppLib.get_selected_folders()

    # folder_paths: str List : The asset paths to select
    def setSelectedFolders(self,folder_paths=[]):
        unreal.CppLib.set_selected_folders(folder_paths)

    # return: obj List : The asset objects that are currently opened in the editor
    def getAllOpenedAssets(self):
        return unreal.CppLib.get_assets_opened_in_editor()

    # asset_objects: obj List : The asset objects to close
    def closeAssets(self,asset_objects=[]):
        unreal.CppLib.close_editor_for_assets(asset_objects)

    # active_viewport_only: bool : If True, will only affect the active viewport
    # actor: obj unreal.Actor : The actor you want to snap to
    def focusViewportOnActor(self,active_viewport_only=True, actor=None):
        command = 'CAMERA ALIGN'
        if active_viewport_only:
            command += ' ACTIVEVIEWPORTONLY'
        if actor:
            command += ' NAME=' + actor.get_name()
        self.executeConsoleCommand(command)

    # Note: This is the real Python function but it does not work in editor : unreal.SystemLibrary.execute_console_command(unreal.EditorLevelLibrary.get_editor_world(), 'stat unit')
    # console_command: str : The console command
    def executeConsoleCommand(self,console_command=''):
        unreal.CppLib.execute_console_command(console_command)

    # return: int : The index of the active viewport
    def getActiveViewportIndex(self):
        return unreal.CppLib.get_active_viewport_index()

    # viewport_index: int : The index of the viewport you want to affect
    # location: obj unreal.Vector : The viewport location
    # rotation: obj unreal.Rotator : The viewport rotation
    def setViewportLocationAndRotation(self,viewport_index=1, location=unreal.Vector(), rotation=unreal.Rotator()):
        unreal.CppLib.set_viewport_location_and_rotation(viewport_index, location, rotation)

    # viewport_index: int : The index of the viewport you want to affect
    # actor: obj unreal.Actor : The actor you want to snap to
    def snapViewportToActor(self,viewport_index=1, actor=None):
        self.setViewportLocationAndRotation(viewport_index, actor.get_actor_location(), actor.get_actor_rotation())
    #*******************************************************************************
    # object_to_cast: obj unreal.Object : The object you want to cast
    # object_class: obj unreal.Class : The class you want to cast the object into
    def cast(self,object_to_cast=None, object_class=None):
        try:
            return object_class.cast(object_to_cast)
        except:
            return None

    # Note: Also work using the command : help(unreal.StaticMesh)
    # unreal_class: obj : The class you want to know the properties
    # return: str List : The available properties (formatted the way you can directly use them to get their values)
    def getAllProperties(self,unreal_class=None):
        return unreal.CppLib.get_all_properties(unreal_class)


    #sequnce**********************************************************
    # sequence_path: str : The level sequence asset path
    # actor: obj unreal.Actor : The actor you want to add into (or get from) the sequence asset
    # return: obj unreal.SequencerBindingProxy : The actor binding
    def getOrAddPossessableInSequenceAsset(self,sequence_path='', actor=None):
        sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path))
        possessable = sequence_asset.add_possessable(object_to_possess=actor)
        return possessable

    # animation_path: str : The animation asset path
    # possessable: obj unreal.SequencerBindingProxy : The actor binding you want to add the animation on
    # return: obj unreal.SequencerBindingProxy : The actor binding
    def addSkeletalAnimationTrackOnPossessable(self,animation_path='', possessable=None):
        # Get Animation
        animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animation_path))
        params = unreal.MovieSceneSkeletalAnimationParams()
        params.set_editor_property('Animation', animation_asset)
        # Add track
        animation_track = possessable.add_track(track_type=unreal.MovieSceneSkeletalAnimationTrack)
        # Add section
        animation_section = animation_track.add_section()
        animation_section.set_editor_property('Params', params)
        #animation_section.set_range_seconds(0, animation_asset.get_editor_property('sequence_length'))
        animation_section.set_range_seconds(0, animation_asset.sequence_length)

    def addSkeletalAnimationTrackOnActor_EXAMPLE(self):
        sequence_path = '/Game/ExampleAssets/Sequences/SEQ_Test'
        animation_path = '/Game/ExampleAssets/Animations/AN_Tutorial_Idle'
        actor_in_world = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(),
                                                                        unreal.SkeletalMeshActor)()[0]
        possessable_in_sequence = self.getOrAddPossessableInSequenceAsset(sequence_path, actor_in_world)
        self.addSkeletalAnimationTrackOnPossessable(animation_path, possessable_in_sequence)

    # use_selection: bool : True if you want to get only the selected actors
    # actor_class: class unreal.Actor : The class used to filter the actors. Can be None if you do not want to use this filter
    # actor_tag: str : The tag used to filter the actors. Can be None if you do not want to use this filter
    # world: obj unreal.World : The world you want to get the actors from. If None, will get the actors from the currently open world.
    # return: obj List unreal.Actor : The actors
    def getAllActors(self,use_selection=False, actor_class=None, actor_tag=None, world=None):
        world = world if world is not None else unreal.EditorLevelLibrary.get_editor_world()  # Make sure to have a valid world
        if use_selection:
            selected_actors = self.getSelectedActors()
            class_actors = selected_actors
            if actor_class:
                class_actors = [x for x in selected_actors if self.cast(x, actor_class)]
            tag_actors = class_actors
            if actor_tag:
                tag_actors = [x for x in selected_actors if x.actor_has_tag(actor_tag)]
            return [x for x in tag_actors]
        elif actor_class:
            actors = unreal.GameplayStatics.get_all_actors_of_class(world, actor_class)
            tag_actors = actors
            if actor_tag:
                tag_actors = [x for x in actors if x.actor_has_tag(actor_tag)]
            return [x for x in tag_actors]
        elif actor_tag:
            tag_actors = unreal.GameplayStatics.get_all_actors_with_tag(world, actor_tag)
            return [x for x in tag_actors]
        else:
            actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)
            return [x for x in actors]

    # path: str : Blueprint class path
    # actor_location: obj unreal.Vector : The actor location
    # actor_rotation: obj unreal.Rotator : The actor rotation
    # actor_location: obj unreal.Vector : The actor scale
    # world: obj unreal.World : The world in which you want to spawn the actor. If None, will spawn in the currently open world.
    # properties: dict : The properties you want to set before the actor is spawned. These properties will be taken into account in the Construction Script
    # return: obj unreal.Actor : The spawned actor
    def spawnBlueprintActor(self,path='', actor_location=None, actor_rotation=None, actor_scale=None, world=None,
                            properties={}):
        actor_class = unreal.EditorAssetLibrary.load_blueprint_class(path)
        actor_transform = unreal.Transform(actor_location, actor_rotation, actor_scale)
        world = world if world is not None else unreal.EditorLevelLibrary.get_editor_world()  # Make sure to have a valid world
        # Begin Spawn
        actor = unreal.GameplayStatics.begin_spawning_actor_from_class(world_context_object=world,
                                                                       actor_class=actor_class,
                                                                       spawn_transform=actor_transform,
                                                                       no_collision_fail=True)
        # Edit Properties
        for x in properties:
            actor.set_editor_property(x, properties[x])
        # Complete Spawn
        unreal.GameplayStatics.finish_spawning_actor(actor=actor, spawn_transform=actor_transform)
        return actor


    # return: obj List unreal.Actor : The selected actors in the world
    def getSelectedActors(self):
        return unreal.EditorLevelLibrary.get_selected_level_actors()

    # Note: Will always clear the selection before selecting.
    # actors_to_select: obj List unreal.Actor : The actors to select.
    def selectActors(self,actors_to_select=[]):
        unreal.EditorLevelLibrary.set_selected_level_actors(actors_to_select)