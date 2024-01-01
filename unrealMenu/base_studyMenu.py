#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import unreal


def get_current_folder():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'perforce')
    if not sys.modules.get('__file__'):
        import inspect
        __file__ = os.path.abspath(inspect.getfile(inspect.currentframe()))
    return os.path.dirname(__file__).replace('\\', '/')


def init_python_path():
    _current_folder = get_current_folder()
    vendor_path = os.path.join(_current_folder, 'vendor', 'python{}'.format(sys.version_info.major))
    print(vendor_path)
    sys.path.append(vendor_path)


def build_menu():
    menus = unreal.ToolMenus.get()
    main_menu = menus.find_menu("LevelEditor.MainMenu")
    assemble_entry = unreal.ToolMenuEntry(
        name="ZMMainTools",
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.DEFAULT))
    # laberl name
    assemble_entry.set_label("ZMMainTools")
    # command
    assemble_entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type="Python",
        string=("from sequenceAssemble import MainTools;from imp import reload;reload(MainTools);MainTools.do()")
    )
    script_menu = main_menu.add_sub_menu(main_menu.get_name(), "ZMMainTools", "ZMMainTools", "ZMMainTools")
    script_menu.add_menu_entry("Scripts", assemble_entry)


    assemble_entry1 = unreal.ToolMenuEntry(
        name="AssembleLauncer",
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.DEFAULT)
    )
    # laberl name
    assemble_entry1.set_label("Shot_Assemble")
    # command
    assemble_entry1.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type="Python",
        string=(
            "from sequenceAssemble import sequenceAssembleLauncer;from imp import reload;reload(sequenceAssembleLauncer);sequenceAssembleLauncer.do()"
        )
    )
    # script_menu1 = main_menu.add_sub_menu(main_menu.get_name(), "AssembleLauncer", "AssembleLauncer", "ZMMainTools")
    script_menu.add_menu_entry("Scripts1", assemble_entry1)

    menus.refresh_all_widgets()


def main():
    init_python_path()
    build_menu()


if __name__ == '__main__':
    main()
