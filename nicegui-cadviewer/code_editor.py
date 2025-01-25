from nicegui import ui
import os 
from datetime import datetime
import time


class CodeEditor(ui.element):
    def __init__(self, editor_width="100%", editor_height="400px", code_file=None, new_file=None):
        """Initialize the Python editor component."""
        super().__init__()
        self.time_start()
        self.file_name = ''
        # Create a toolbar with buttons
        with ui.row().classes('w-full h-10'):
            self.toolbar = ui.row().classes('w-full')
            with self.toolbar:
                ui.button("New",      icon="star", on_click=self.on_new)
                ui.button("Load",     icon="upload", on_click=self.on_load)
                ui.button("Save",     icon="download    ", on_click=self.on_save)
                ui.button("Undo",     icon="undo", on_click=self.on_undo).props('color="grey"')
                ui.button("Redo",     icon="redo", on_click=self.on_redo).props('color="grey"')
                ui.button("Run Code", icon="send", on_click=self.on_run)

        with ui.row().classes('w-full h-full'):


            if code_file and code_file.exists():
                with code_file.open() as f:
                    code = f.read()
                    self.file_name = code_file.name
            else:
                self.on_new()

            ui.label(self.file_name)

            # Setup editor
            self.editor = ui.codemirror(language='python', theme='dracula')
            self.editor.classes('w-full h-full')
            self.editor.value = code
            self.new_file = None 
            if new_file and new_file.exists():
                self.new_file = new_file
    
        with ui.row().classes('w-full h-20'):
            self.log = ui.log(max_lines=10).classes('w-full h-20')
    
        self.log.push(self.info('init', 'Code editor initialized'))

    def time_start(self):
        self.start_time = time.time()

    def info(self, function, message, do_time=True):
        timestamp = datetime.now().strftime('%X.%f')[:-5]
        use_time = ''
        if do_time:
            used_time = f'in {time.time() - self.start_time:0.2}s'
        return f'{timestamp}: [{function}] {message} {used_time}'
    
    def on_save(self):
        """Save the current code to a file."""
        self.time_start()
        content = self.editor.value
        with open('my_python_script.py', 'w') as f:
            f.write(content)
        self.info('file', 'saved successfully')

    def on_load(self):
        """Load code from a file into the editor."""
        self.time_start()
        with open('my_python_script.py', 'r') as f:
            content = f.read()
        self.editor.set_value(content)
        self.info('file', 'loaded successfully')

    def on_undo(self):
        """Undo the last action in the editor."""
        self.log.push("TODO: `undo` needs to be implemented")
        self.editor.run_method('undo')

    def on_redo(self):
        """Redo the last undone action in the editor.
           see https://github.com/codemirror/codemirror5/blob/master/src/edit/commands.js"""
        self.log.push("TODO: `redo` needs to be implemented")
        self.editor.run_method('redo')

    def on_new(self):
        """Clear the editor."""
        self.time_start()
        if self.new_file:
            with self.new_file.open('r') as f:
                self.editor.value = f.read()
            self.log.push(self.info('file', f'loaded template {self.new_file}'))
        else:
            self.log.push(self.info('file', 'No template file specified (`new.py` in `models`). Using minimal default code'))
            self.editor.set_value('from build123d import *\nfrom ocp_vscode import *\n\n\nshow_all()')

    def on_run(self):
        """Execute the code from the editor."""
        self.time_start()
        result = self.execute_code(self.editor.value)
        self.log.push(self.info('on_run', result))
        

    def execute_code(self, code: str):
        """Execute the Python code in the editor."""
        try:
            exec(code)
            return "Code executed successfully"
        except Exception as e:
            return f"Error: {str(e)}"

