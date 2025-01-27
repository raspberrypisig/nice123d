from nicegui import ui
from nicegui.events import KeyEventArguments
import logging

from app_logging import NiceGUILogHandler
from project_gallery import ProjectGallery, models_path, code_file, new_file
from code_editor import CodeEditor
from ocp_viewer import OcpViewer

import platform
active_os = platform.system()       # get the operating system



class MainWindow(ui.element):
    
    def __init__(self, app, models_path=models_path, code_file=code_file, new_file=new_file):
        self.app = app
        self.width =1800
        self.height= 900
        self.title="nicegui-cadviewer"

        self.model_path = models_path
        self.code_file = models_path / code_file
        self.new_file = models_path / new_file

        ui.add_css('''
            :root {
                --nicegui-default-padding: 0.5rem;
                --nicegui-default-gap: 0.5rem;
            }
        ''')
        # TODO: move buttons from editor to main window
        if 0:       
            with ui.row().classes('w-full items-center'):
                result = ui.label().classes('mr-auto')
                with ui.button(icon='menu'):
                    with ui.menu() as menu:
                        ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))
                        ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))
                        ui.menu_item('Menu item 3 (keep open)',
                                    lambda: result.set_text('Selected item 3'), auto_close=False)
                        ui.separator()
                        ui.menu_item('Close', menu.close)

        # TODO: (maybe solved) layout info https://github.com/zauberzeug/nicegui/discussions/1937
        with ui.tabs().classes('w-full h-10 items-stretch border') as left_tabs:
            page_gallery = ui.tab('Gallery', icon='folder')
            page_parameters = ui.tab('Parameters', icon='plumbing')
            page_editor = ui.tab('Editor', icon='code')

        with ui.tab_panels(left_tabs, value=page_editor).classes('w-full h-full items-stretch border') as left_tab_panels:
            with ui.tab_panel(page_gallery):
                self.gallery = ProjectGallery(models_path)
            with ui.tab_panel(page_parameters):
                ui.label('Parameters')
            with ui.tab_panel(page_editor):
                self.editor = CodeEditor(code_file=code_file, new_file=new_file)

        with ui.expansion('Logger', icon='work').classes('w-full'):
            self.logger_ui = ui.log().classes('w-full h-10')
            self.logger = NiceGUILogHandler(self.logger_ui)


        with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
            ui.label('HEADER')
            ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
        with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4') as left_drawer:
            ui.label('LEFT DRAWER')
        with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
            with ui.tabs().classes('w-full h-10 items-stretch border') as right_tabs:

                page_viewer = ui.tab('Viewer', icon='view_in_ar')
                page_help = ui.tab('Help', icon='help')
                page_settings   = ui.tab('Settings', icon='settings')
            
            with ui.tab_panels(right_tabs, value=page_viewer).classes('w-full h-full items-stretch border') as right_tab_panels:
                with ui.tab_panel(page_viewer):
                    self.viewer = OcpViewer(port=3940)

                with ui.tab_panel(page_help):
                    ui.label('Help')

                with ui.tab_panel(page_settings):
                    ui.label('Settings')

        with ui.footer().style('background-color: #3874c8'):
            ui.label('FOOTER')

                

        # connect logger to sub elements
        self.gallery.set_logger(self.logger)
        self.editor.set_logger(self.logger)
        self.viewer.set_logger(self.logger)

    @property
    def size(self):
        return (self.width, self.height)

    def startup(self):
        self.viewer.startup()
        ui.keyboard(on_key=self.handle_key)

    def handle_key(self, e: KeyEventArguments):
        if active_os == "Windows":
            main_modifier = e.modifiers.ctrl
        elif active_os == "Mac":
            main_modifier = e.modifiers.cmd
        else:
            main_modifier = e.modifiers.meta

        if main_modifier and e.action.keydown:
            if e.key.enter:
                self.editor.on_run()             # TODO: fix editor
            elif e.key.name == "s":
                self.editor.on_save()
            elif e.key.name == "o":
                self.editor.on_load()
            elif e.key.name == "t":
                self.editor.on_new()

    def on_close_window(self, event):
        self.viewer.shutdown()
        self.editor.on_save()
        self.close()
        self.app.shutdown()



