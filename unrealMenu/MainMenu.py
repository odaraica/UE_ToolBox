import unreal
import sys
import os


class UnrealMenu:
    def __init__(self):
        self.curPath = ''

    def execuPlugin(self):

        self.getCurrentPath()
        if self.curPath:
            sys.path.append(self.curPath)
            sys.path.append(self.curPath + '/unrealMenu/')
            sys.path.append(self.curPath + '/unrealMenu/lib')
            print(self.curPath + '/unrealMenu/')
            self.constructMenu()


    def getCurrentPath(self):

        if not sys.modules.get('__file__'):
            import inspect
            __file__ = os.path.abspath(inspect.getfile(inspect.currentframe()))
            self.curPath =  os.path.dirname(__file__).replace('\\','/')
        else:
            self.curPath =  os.path.dirname(os.path.abspath(__file__))

    def constructMenu(self):
        Base_Menus = unreal.ToolMenus.get()
        main_menu = Base_Menus.find_menu('LevelEditor.MainMenu')
        #setup Entry
        ToolBox_MenuEntry = unreal.ToolMenuEntry(
            name = 'XNYYToolBox',
            type=unreal.MultiBlockType.MENU_ENTRY,
            insert_position=unreal.ToolMenuInsert('',unreal.ToolMenuInsertType.DEFAULT))
        #label name
        ToolBox_MenuEntry.set_label(u'虚拟影业工具箱')
        #command
        ToolBox_MenuEntry.set_string_command(
            type=unreal.ToolMenuStringCommandType.PYTHON,
            custom_type='Python',
            string=('import ToolBoxUI;ToolBoxUI.execu();')
        )

        ToolBox_menu = main_menu.add_sub_menu(main_menu.get_name(),u'XNYYToolBox',u'XNYYToolBox',u'虚拟影业工具箱')
        ToolBox_menu.add_menu_entry('Scripts',ToolBox_MenuEntry)

        Base_Menus.refresh_all_widgets()


UM = UnrealMenu()
UM.execuPlugin()











