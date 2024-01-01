# coding=utf-8
import unreal


class ImportAnimAsset():
    def __init__(self):
        self.fbxPath = ''
        self.CreatelevelPath = ''

    def MainExecu(self):
        pass

    def importCam(self):
        pass


    def setFbxPath(self,path):
        self.fbxPath = path

    def setLevelPath(self,path):
        self.CreatelevelPath = path

    def import_fbx(self,map_asset_path, sequencer_asset_name, package_path, actor_label_list, input_fbx_file):

        # Load the map, get the world
        world = unreal.EditorLoadingAndSavingUtils.load_map(map_asset_path)
        # Get Actors from passed in names
        level_actors = unreal.EditorLevelLibrary.get_all_level_actors()
        actor_list = []
        for label in actor_label_list:
            filtered_list = unreal.EditorFilterLibrary.by_actor_label(level_actors, label,
                                                                      unreal.EditorScriptingStringMatchType.EXACT_MATCH)
            actor_list.extend(filtered_list)
        # Create the sequence asset
        sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(sequencer_asset_name, package_path,
                                                                           unreal.LevelSequence,
                                                                           unreal.LevelSequenceFactoryNew())
        # Create Bindings
        for actor in actor_list:
            sequence.add_possessable(actor)
        bindings = sequence.get_bindings()
        # Set Options
        import_options = unreal.MovieSceneUserImportFBXSettings()
        import_options.set_editor_property("create_cameras",True)
        import_options.set_editor_property("reduce_keys", False)

        # Import
        unreal.SequencerTools.import_level_sequence_fbx(world, sequence, bindings, import_options, input_fbx_file)

        return sequence

    def create_level_sequence(self,asset_name, package_path='/Game/'):

        level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name, package_path,
                                                                           unreal.LevelSequence,
                                                                           unreal.LevelSequenceFactoryNew())

        floor = unreal.find_object(level_editor.get_current_level(), "Floor")
        sm_component = unreal.find_object(floor, "StaticMeshComponent0")

        floor_binding = sequence.add_possessable(floor)
        floor_binding.add_track(unreal.MovieScene3DTransformTrack)
        self.populate_binding(sequence, floor_binding, 1, 5)

        print("Floor {0} is bound as {1}".format(floor, floor_binding.get_id()))

        sm_component_binding = sequence.add_possessable(sm_component)
        sm_component_binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)
        self.populate_binding(sequence, sm_component_binding, 1, 5)

        print("Static mesh component {0} is bound as {1}".format(sm_component, sm_component_binding.get_id()))

        # Create a spawnable from the floor instance
        spawnable_floor_binding = sequence.add_spawnable_from_instance(floor)
        transform_track = spawnable_floor_binding.add_track(unreal.MovieScene3DTransformTrack)
        self.populate_track(sequence, transform_track, 1, 5)

        # Create a spawnable from an actor class
        spawnable_camera_binding = sequence.add_spawnable_from_class(unreal.CineCameraActor)
        # add an infinite transform track
        transform_section = spawnable_camera_binding.add_track(unreal.MovieScene3DTransformTrack).add_section()
        transform_section.set_start_frame_bounded(0)
        transform_section.set_end_frame_bounded(0)

        return sequence

    def create_sequence_from_selection(self,asset_name, length_seconds=5, package_path='/Game/'):

        sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name, package_path,
                                                                           unreal.LevelSequence,
                                                                           unreal.LevelSequenceFactoryNew())

        for actor in unreal.SelectedActorIterator(unreal.EditorLevelLibrary.get_editor_world()):
            binding = sequence.add_possessable(actor)

            # Add a transform track for the actor
            transform_track = binding.add_track(unreal.MovieScene3DTransformTrack)
            transform_section = transform_track.add_section()
            transform_section.set_start_frame_seconds(0)
            transform_section.set_end_frame_seconds(length_seconds)

            # Add a visibility track for the actor
            visibility_track = binding.add_track(unreal.MovieSceneVisibilityTrack)
            visibility_track.set_property_name_and_path('bHidden', 'bHidden')
            visibility_section = visibility_track.add_section()
            visibility_section.set_start_frame_seconds(0)
            visibility_section.set_end_frame_seconds(length_seconds)

            # Add a bool simulate physics property track to the root component
            root_component_binding = sequence.add_possessable(actor.root_component)
            root_component_binding.set_parent(binding)

            simulate_physics_track = root_component_binding.add_track(unreal.MovieSceneBoolTrack)
            simulate_physics_track.set_property_name_and_path('bSimulatePhysics', 'BodyInstance.bSimulatePhysics')
            simulate_physics_section = simulate_physics_track.add_section()
            simulate_physics_section.set_start_frame_seconds(0)
            simulate_physics_section.set_end_frame_seconds(length_seconds)

            # Add a dummy vector track for 2 channels
            vector_track = root_component_binding.add_track(unreal.MovieSceneVectorTrack)
            vector_track.set_property_name_and_path('Dummy2Vector', 'Dummy2Vector')
            vector_track.set_num_channels_used(2)
            vector_section = vector_track.add_section()
            vector_section.set_start_frame_seconds(0)
            vector_section.set_end_frame_seconds(length_seconds)

            try:
                camera = unreal.CameraActor.cast(actor)
                camera_cut_track = sequence.add_track(unreal.MovieSceneCameraCutTrack)

                # Add a camera cut track for this camera
                camera_cut_section = camera_cut_track.add_section()
                camera_cut_section.set_start_frame_seconds(0)
                camera_cut_section.set_end_frame_seconds(length_seconds)

                camera_binding_id = unreal.MovieSceneObjectBindingID()
                camera_binding_id.set_editor_property("Guid", binding.get_id())
                camera_cut_section.set_editor_property("CameraBindingID", camera_binding_id)

                # Add a current focal length track to the cine camera component
                camera_component = actor.get_cine_camera_component()
                camera_component_binding = sequence.add_possessable(camera_component)
                camera_component_binding.set_parent(binding)
                focal_length_track = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)
                focal_length_track.set_property_name_and_path('CurrentFocalLength', 'CurrentFocalLength')
                focal_length_section = focal_length_track.add_section()
                focal_length_section.set_start_frame_bounded(0)
                focal_length_section.set_end_frame_bounded(0)

            except TypeError:
                pass

            print("{0} is bound as {1}".format(actor, binding.get_id()))

        return sequence

    def populate_track(self,sequence, track, num_sections=1, section_length_seconds=1):

        for i in range(num_sections):
            section = track.add_section()
            section.set_start_frame_seconds(i * section_length_seconds)
            section.set_end_frame_seconds(section_length_seconds)

    '''
    	Summary:
    		Populates the specified sequence and object binding with some test sections.
    	Params:
    		track - The UMovieScene to populate
    		binding - The FMovieSceneObjectBindingID to create sections for.
    		num_sections - The number of sections to create.
    		section_length_seconds - The length of each section it is creating.
    '''

    def populate_binding(self,sequence, binding, num_sections=1, section_length_seconds=1):

        for track in binding.get_tracks():
            self.populate_track(sequence, track, num_sections, section_length_seconds)