from nicegui import ui
from nicegui import events
import logging

left = True, False 
right = False, True
both = True, True
none = False, False

class Page():
    def __init__(self, title, icon, position, sibling_page=None, short_cut=""):
        self.title        = title
        self.icon         = icon
        self.is_left      = position[0]
        self.is_right     = position[1]
        self.sibling_page = sibling_page
        self.short_cut    = short_cut
        self.on_click     = None
        self.page         = None

    def set_visibility(self, visible):
        if self.page:
            self.page.set_visibility(visible)
    
    def create_page(self, object, on_click):
        self.page = object
        self.on_click = on_click

# [Variable]
g__pages = {    # https://fonts.google.com/icons?icon.query=stop
    'Ctrl+1':    Page('Gallery',    'folder',     left,  "Ctrl+1",    "Meta+1"),
    'Alt+1' :    Page('Notes',      'info',       right, "Ctrl+1",    "Meta+1"),
    'Meta+2':    Page('Customizer', 'plumbing',   both,  "Meta+4",    "Meta+2"),
    'Meta+3':    Page('Editor',     'code',       both,  "Meta+4",    "Meta+3"),
    'Meta+4':    Page('Viewer',     'view_in_ar', both,  "Meta+1",    "Meta+4"),
    'Ctrl+5':    Page('Settings',   'settings',   left,  "Ctrl+5",    "Meta+5"),
    'Alt+5' :    Page('Help',       'help',       right, "Ctrl+3",    "Meta+5"),
   #'settings'   Page('Settings',   'settings',   none,  ""),
}

size_splitter = None

def set_zoom_left():
    if size_splitter.value == 100:
        size_splitter.value = 50
    elif size_splitter.value < 50:
        size_splitter.value = 50
    elif size_splitter.value >= 50:
        size_splitter.value = 100
    else:
        pass # impossible

def set_zoom_right():
    if size_splitter.value == 0:
        size_splitter.value = 50
    elif size_splitter.value > 50:
        size_splitter.value = 50
    elif size_splitter.value <= 50:
        size_splitter.value = 0
    else:
        pass # impossible

left_cards = []
right_cards = []

class PageSwitcher():
    def __init__(self, pages = g__pages, add_zoom=True):
        ui.colors(accent='#6A0000', info='#555555')
        self.pages = pages
        self.add_zoom = add_zoom
        # TODO: move default to a yaml file
        self.left_page   = 'Meta+3'
        self.right_page  = 'Meta+4'
        self.show_left_and_right(self.left_page, self.right_page)
  
    def setup_left_button_bar(self, cards : list):
        cards.reverse()

        with ui.button_group() as bar:	
            self.left_button_bar = bar
            for page in self.pages:
                if self.pages[page].is_left:
                    active = self.pages[page]
                    active.page = cards.pop()
                    button = ui.button('', icon=active.icon, on_click=active.on_click)
                    if 'Meta' in active.short_cut:
                        short_cut = active.short_cut.replace('Meta', 'Ctrl')
                    else: 
                        short_cut = active.short_cut
                    button.tooltip(f'{active.title} `{short_cut}`')
                    if active.title == self.left_page:
                        button.props('fab color=accent')
            if self.add_zoom:
                z = ui.button('', icon='zoom_out_map', on_click=set_zoom_left).tooltip('Zoom left `Meta+0`')
                z.props('fab color=info')

        return self.left_button_bar

    def setup_right_button_bar(self, cards : list):
        cards.reverse()
        
        with ui.button_group() as bar:	
            self.right_button_bar = bar
            for page in self.pages:
                if self.pages[page].is_right:
                    active = self.pages[page]                    
                    active.page = cards.pop()
                    button = ui.button('', icon=active.icon, on_click=active.on_click)
                    if 'Meta' in active.short_cut:
                        short_cut = active.short_cut.replace('Meta', 'Alt')
                    else: 
                        short_cut = active.short_cut
                    button.tooltip(f'{active.title} {short_cut}')
                    if active.title == self.right_page:
                        button.props('fab color=accent')
        
            if self.add_zoom:
                z = ui.button('', icon='zoom_out_map', on_click=set_zoom_right).tooltip('Zoom right `Meta+0`')
                z.props('fab color=info')

        return self.right_button_bar

    def hide_other_pages(self, left_page, right_page):
        # Hide all other pages
        for page in self.pages:
            if page != left_page and page != right_page:
                self.pages[page].set_visibility(False)

    def show_left_and_right(self, left_page, right_page):
        if self.pages[left_page ]:
            self.pages[left_page ].set_visibility(True)
        if self.pages[right_page ]:
            self.pages[right_page].set_visibility(True)
        
        self.hide_other_pages(left_page, right_page)
        
    def show_left(self, left_page):
        # move right page to left page and activate sibling page
        if self.right_page == left_page:
            self.right_page = self.pages[left_page].sibling_page
            self.left_page  = left_page
        else: # only switch left page
            self.left_page = left_page

        self.update_visibility()

    def show_right(self, right_page):
        # move left page to right page and activate sibling page
        if self.left_page == right_page:
            self.left_page  = self.pages[right_page].sibling_page
            self.right_page = right_page
        else: # only switch right page
            self.right_page = right_page

        self.update_visibility()

    def update_visibility(self):
        self.pages[self.left_page ].set_visibility(True)
        self.pages[self.right_page].set_visibility(True)
        # TODO: button bar on active pages
        self.hide_other_pages(self.left_page, self.right_page)


if __name__ in {"__main__", "__mp_main__"}:
    page_switcher = PageSwitcher()

    with ui.splitter().classes('w-full h-full items-stretch border') as main_splitter:
    
        with main_splitter.before:
            with ui.column().classes('w-full h-full items-stretch border') as main_content:
                with ui.card().classes('w-full h-full') as page_gallery:
                    Ctrl_1 = ui.label('Gallery.').classes('w-full h-full')
                with ui.card().classes('w-full h-full') as page_viewer:
                    Ctrl_2 = ui.label('Customizer.').classes('w-full h-full')  
                with ui.card().classes('w-full h-full') as page_editor:
                    Ctrl_3 = ui.label('Editor.').classes('w-full h-full')
                with ui.card().classes('w-full h-full') as page_editor:
                    Ctrl_4 = ui.label('Viewer.').classes('w-full h-full')
                with ui.card().classes('w-full h-full') as page_editor:
                    Ctrl_5 = ui.label('Settings.').classes('w-full h-full')

                left_cards = [Ctrl_1, Ctrl_2, Ctrl_3, Ctrl_4, Ctrl_5]

        with main_splitter.after:
            with ui.column().classes('w-full h-full items-stretch border'):
                with ui.card().classes('w-full h-full') as page_notes:
                    Alt_1 = ui.label('Notes.').classes('w-full h-full')
                with ui.card().classes('w-full h-full') as page_viewer:
                    Alt_2 = ui.label('Customizer.').classes('w-full h-full')  
                with ui.card().classes('w-full h-full') as page_editor:
                    Alt_3 = ui.label('Editor.').classes('w-full h-full')
                with ui.card().classes('w-full h-full') as page_customizer:
                    Alt_4 = ui.label('Viewer.').classes('w-full h-full')
                with ui.card().classes('w-full h-full') as page_help:
                    Alt_5 = ui.label('Help.').classes('w-full h-full')

                right_cards = [Alt_1, Alt_2, Alt_3, Alt_4, Alt_5]
        with main_splitter.separator:
            ui.icon('multiple_stop').classes('text-grey')  
        

    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        
        ctrl_bar = page_switcher.setup_left_button_bar(left_cards)
        ui.space()
        ui.label('model / path / file name').classes('text-xl')
        ui.space()
        size_splitter = ui.number('Value', format='%.0f', value=50, min=0, max=100, step=10)
        size_splitter.bind_value(main_splitter)  
        alt_bar = page_switcher.setup_right_button_bar(right_cards)
    

    # Run the NiceGUI app
    ui.run()