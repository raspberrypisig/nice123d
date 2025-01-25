"""
nicegui cadviewer

name: cadviewer.py
by:   jdegenstein
date: January 24, 2025

desc:

This module creates a graphical window with a text editor and CAD viewer (based on ocp_vscode). 
The graphical user interface is based on nicegui and spawns the necessary subprocess and allows
for re-running the user-supplied script and displaying the results.

Key Features:
  - Has a run button for executing user code
  - Has a keyboard shortcut of CTRL-Enter to run the user code

license:

    Copyright 2025 jdegenstein

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
# [Imports]
from nicegui import app, ui
from nicegui.events import KeyEventArguments
import subprocess
from pathlib import Path
from code_editor import CodeEditor
import platform

# [Variables]
models_path = Path(__file__).parent / ".." / "models"
code_file = models_path / "basic.py"
editor = None 
# get the operating system
active_os = platform.system()
    

app.native.window_args["resizable"] = True
app.native.start_args["debug"] = True
# app.native.settings['ALLOW_DOWNLOADS'] = True # export "downloads" ?
app.native.settings["MATPLOTLIB"] = False

editor_fontsize = 18
# TODO: consider separate editor execution thread from nicegui thread

button_frac = 0.05

with ui.splitter().classes(
    "w-full h-full no-wrap items-stretch border"
) as splitter:
    with splitter.before:

        with ui.tabs().classes('w-full h-full items-stretch border') as tabs:
            page_editor     = ui.tab('Editor', icon='code')
            page_parameters = ui.tab('Parameters', icon='plumbing')
            page_settings   = ui.tab('Settings', icon='settings')
         
        with ui.tab_panels(tabs, value=page_editor).classes('w-full h-full items-stretch border'):
            with ui.tab_panel(page_editor):
                editor = CodeEditor(code_file=code_file)

            with ui.tab_panel(page_parameters):
                ui.label('Parameters')

            with ui.tab_panel(page_settings):
                ui.label('Settings')

            
    with splitter.after:
        with ui.column().classes("w-full items-stretch border"):
            ocpcv = (
                ui.element("iframe")
                .props('src="http://127.0.0.1:3939/viewer"')
                .classes("h-[calc(100vh-3rem)]")
            )


# handle the CTRL + Enter run shortcut:
def handle_key(e: KeyEventArguments):
    if active_os == "Windows":
        main_modifier = e.modifiers.ctrl
    elif active_os == "Mac":
        main_modifier = e.modifiers.cmd
    else:
        main_modifier = e.modifiers.meta

    if e.modifiers.ctrl and e.action.keydown:
        if e.key.enter:
            editor.on_run()         
        elif main_modifier and e.action.keydown:
            if e.key.s:
                editor.on_save()
            elif e.key.o:
                editor.on_load()
            elif e.key.z:
                editor.on_undo()
            elif e.key.y:
                editor.on_redo()

# TODO: consider separating this module and how best to organize it (if name == main, etc.)

# ui.run(native=True, window_size=(1800, 900), fullscreen=False, reload=True) #use reload=True when developing rapidly, False helps exit behavior

# layout info https://github.com/zauberzeug/nicegui/discussions/1937

# [Functions]

# run ocp_vscode in a subprocess
def startup_all():
    global ocpcv_proc
    # spawn separate viewer process
    ocpcv_proc = subprocess.Popen(["python", "-m", "ocp_vscode"])
    # pre-import build123d and ocp_vscode in main thread
    exec("from build123d import *\nfrom ocp_vscode import *")



def shutdown_all():
    ocpcv_proc.kill()
    # ocpcv_proc.terminate() # TODO: investigate best cross-platform solution
    editor.save()
    app.shutdown()



def main():
    
    # Startup
    app.on_startup(startup_all)
    app.on_shutdown(shutdown_all)  # register shutdown handler
    keyboard = ui.keyboard(on_key=handle_key)

    # Execution
    ui.run(
        native=True,
        window_size=(1800, 900),
        title="nicegui-cadviewer",
        fullscreen=False,
        reload=False,
    )

# [Main]
if __name__ == '__main__':
    main()
