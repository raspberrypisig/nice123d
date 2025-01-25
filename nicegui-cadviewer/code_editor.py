from nicegui import ui
import os 
from datetime import datetime
import time


class CodeEditor(ui.element):
    def __init__(self, editor_width="100%", editor_height="400px", code_file=None):
        """Initialize the Python editor component."""
        super().__init__()
        self.time_start()

        with ui.splitter(horizontal=True) as splitter:
            with splitter.before:
                # Create a toolbar with buttons
                self.toolbar = ui.row().classes('w-full')

                with self.toolbar:
                    ui.button("New",      icon="star", on_click=self.on_new)
                    ui.button("Load",     icon="upload-file", on_click=self.on_load)
                    ui.button("Save",     icon="download-file", on_click=self.on_save)
                    ui.button("Undo",     icon="undo", on_click=self.on_undo)
                    ui.button("Redo",     icon="redo", on_click=self.on_redo)
                    ui.button("Run Code", icon="send", on_click=self.on_run)

                # Setup editor
                self.editor = ui.codemirror(language='python', theme='dracula')
                self.editor.classes('w-full h-full')
                if code_file is not None and code_file.exists():
                    with code_file.open() as f:
                        self.editor.value = f.read()
        
            with splitter.after:
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
        content = self.editor.value
        with open('my_python_script.py', 'w') as f:
            f.write(content)
        print("File saved successfully")

    def on_load(self):
        """Load code from a file into the editor."""
        with open('my_python_script.py', 'r') as f:
            content = f.read()
        self.editor.set_value(content)

    def on_undo(self):
        """Undo the last action in the editor."""
        self.editor.exec('editor.undo()')

    def on_redo(self):
        """Redo the last undone action in the editor."""
        self.editor.exec('editor.redo()')

    def on_new(self):
        """Clear the editor."""
        self.editor.set_value('')

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

