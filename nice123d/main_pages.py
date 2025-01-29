from nicegui import ui
from nicegui import events
import logging
from enum import Enum

left = True, False 
right = False, True
both = True, True
none = False, False


class Side(Enum):
    LEFT = 1
    RIGHT = 2


# [Variable]


size_splitter   = None

left_container  = None
right_container = None
left_cards      = []
right_cards     = []

class Views():
    gallery = None
    customizer = None
    editor = None
    viewer = None
    settings = None
    notes = None
    help = None

    views_left  = None
    views_right = None

    def __init__(self):
        self.pages = [self.gallery, self.customizer, self.editor, self.viewer, self.settings, self.notes, self.help]
        self.show_left = None
        self.show_right = None
    
    def update_pages(self):
        self.pages = [self.gallery, self.customizer, self.editor, self.viewer, self.settings, self.notes, self.help]
        self.show_left = self.gallery
        self.show_right = self.notes
    
        self.views_left  = [self.gallery, self.customizer, self.editor, self.settings]
        self.views_right = [self.notes,   self.viewer,     self.help]


    def show_all(self):
        print(f'show_views {self.show_left} {self.show_right}')	

        count = 0
        for page in self.pages:
            if page:
                count += 1
                page.set_visibility(True)


    def update_views(self):
        print(f'update_views {self.show_left} {self.show_right}')	
        self.show_left.set_visibility(True)
        self.show_right.set_visibility(True)

        count = 0
        for page in self.pages:
            if page != self.show_left and page != self.show_right:
                if page:
                    count += 1
                    page.set_visibility(False)
        print(f'- hidden pages {count}')

    def already_shown_on_side(self, page, side):
        if side == Side.LEFT:
            return self.show_left == page
        elif side == Side.RIGHT:
            return self.show_right == page
        else:
            return False

    def is_on_other(self, page, side):
        if side == Side.LEFT:
            return page in self.views_right
        elif side == Side.RIGHT:
            return page in self.views_left
        else:
            return False

    def modify_size(self, side):
        if side == Side.LEFT:

            if size_splitter.value < 50:
                size_splitter.value = 50
            elif size_splitter.value < 100:
                size_splitter.value = 100
            else:
                size_splitter.value = 50
                
        elif side == Side.RIGHT:

            if size_splitter.value > 50:
                size_splitter.value = 50
            elif size_splitter.value == 50:
                size_splitter.value = 0
            else:
                size_splitter.value = 50

        else:
            pass # impossible

    def make_visible(self, side):
        if side == Side.LEFT:
            if size_splitter.value < 50:
                size_splitter.value = 50
            else:
                pass # no change necessary
                
        elif side == Side.RIGHT:
            if size_splitter.value > 50:
                size_splitter.value = 50
            else:
                pass # no change necessary
            
        else:
            pass # impossible

    def show_gallery(self):
        """Show the gallery page it is restricted to the left page."""

        page = self.gallery
        side = Side.LEFT
        if self.already_shown_on_side(page, side):
            self.modify_size(side)
        else:
            page.set_visibility(True)
            self.show_left = self.gallery
            if not self.show_right:
                self.show_right = self.notes

        self.update_views()

    def show_settings(self):
        """Show the settings page - it is restricted to the left side."""

        page = self.settings
        side = Side.LEFT
        if self.already_shown_on_side(page, side):
            print(f'   - already_shown_on_side {page} {side}')
            self.modify_size(side)
        else:
            print(f'   - else {page} {side}')
            size_splitter.value = 100
            page.set_visibility(True)
            self.show_left = page

        self.update_views()

    def show_notes(self):
        """Show the notes page - it is restricted to the right side."""

        page = self.notes
        side = Side.RIGHT
        if self.already_shown_on_side(page, side):
            self.modify_size(side)
        else:
            page.set_visibility(True)
            self.show_right = page
            if not self.show_left:
                self.show_left = self.gallery

        self.update_views()

    def show_help(self):
        """Show the help page - it is restricted to the right side."""

        side = Side.RIGHT
        if self.already_shown_on_side(self.help, side):
            self.modify_size(side)
        else:
            self.gallery.set_visibility(True)
            self.show_right = self.help
            if not self.show_left:
                self.show_left = self.editor

        self.update_views()

    def other(self, side):
        if side == Side.LEFT:
            return Side.RIGHT
        else:
            return Side.LEFT

    def move_to_side(self, page, side):
        code = ''
        if page == self.editor:
            print(f'editor {page} {side} - {page.value}')
            code = page.value

        if side == Side.LEFT and page in self.views_right:
            self.views_right.remove(page)
            self.views_left.append(page)
            page.move(left_container)
        elif side == Side.RIGHT and page in self.views_left:
            self.views_left.remove(page)
            self.views_right.append(page)
            page.move(right_container)
        else:
            pass # impossible

        page.value = code
        page.update()

    def show_left_or_right(self, page, side, page_sibling_left=None, page_sibling_right=None):
        if side == Side.LEFT:
            page_sibling = page_sibling_right
        
        elif side == Side.RIGHT:
            page_sibling = page_sibling_left
        else:
            pass # impossible

        if not page_sibling:
            page_sibling = self.help

        if self.is_on_other(page_sibling, self.other(side)):
            self.move_to_side(page_sibling, self.other(side))


        if self.already_shown_on_side(page, side):
            self.modify_size(side)

        elif self.is_on_other(page, side):
            print(f'is_on_other {page} print {type(page)} to {side}')
            if side == Side.LEFT:                 
                self.show_left  = page
                if self.show_right == page:
                    self.show_right = page_sibling
            elif side == Side.RIGHT:
                self.show_right = page
                if self.show_left == page:
                    self.show_left  = page_sibling

            self.move_to_side(page, side)

            self.make_visible(side)

        else:
            page.set_visibility(True)
            if side == Side.LEFT:
                self.show_left = page
                if not self.show_right:
                    self.show_right = page_sibling

            elif side == Side.RIGHT:
                self.show_right = page
                
                if not self.show_left:
                    self.show_left = page_sibling
                    
            else:
                pass # impossible
                
        self.update_views()

    def show_customizer(self, side=Side.LEFT):

        self.show_left_or_right(self.customizer, side, self.viewer, self.editor)

        
    def show_editor(self, side):

        self.show_left_or_right(self.editor, side, self.customizer, self.viewer)
        
    def show_viewer(self, side):

        self.show_left_or_right(self.viewer, side, self.editor, self.customizer)

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

    pages.views.show_all()

    if size_splitter.value == 0:
        size_splitter.value = 50
    elif size_splitter.value > 50:
        size_splitter.value = 50
    elif size_splitter.value <= 50:
        size_splitter.value = 0
    else:
        pass # impossible

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

left_buttons = ['Ctrl+1', 'Meta+2', 'Meta+3', 'Meta+4', 'Ctrl+5']
right_buttons = ['Alt+1', 'Meta+2', 'Meta+3', 'Meta+4', 'Alt+5']

class PageSwitcher():
    def __init__(self, pages = g__pages, add_zoom=False):
        ui.colors(accent='#6A0000', info='#555555')
        self.pages = pages
        self.add_zoom = add_zoom
        # TODO: move default to a yaml file

        self.left_page   = 'Meta+3'
        self.right_page  = 'Meta+4'

        self.views = Views()
        self.map_button_to_views = {
            'Ctrl+1': self.show_gallery_left,	
            'Ctrl+2': self.show_customizer_left,
            'Ctrl+3': self.show_editor_left,
            'Ctrl+4': self.show_viewer_left,
            'Ctrl+5': self.show_settings_left,
            'Alt+1': self.show_notes_right,
            'Alt+2': self.show_customizer_right,
            'Alt+3': self.show_editor_right,
            'Alt+4': self.show_viewer_right,
            'Alt+5': self.show_help_right,
        }
  
    def setup_left_button_bar(self, cards : list):
        cards.reverse()

        with ui.button_group() as bar:	
            self.left_button_bar = bar
            for page in self.pages:
                print(page)
                if self.pages[page].is_left:
                    active = self.pages[page]
                    active.page = cards.pop()
                    
                    if 'Meta' in active.short_cut:
                        short_cut = active.short_cut.replace('Meta', 'Ctrl')
                    else: 
                        short_cut = active.short_cut
                    
                    button = ui.button('', icon=active.icon, on_click=self.map_button_to_views[short_cut])
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
                    
                    if 'Meta' in active.short_cut:
                        short_cut = active.short_cut.replace('Meta', 'Alt')
                    else: 
                        short_cut = active.short_cut
                    
                    button = ui.button('', icon=active.icon, on_click=self.map_button_to_views[short_cut])
                    button.tooltip(f'{active.title} {short_cut}')
                    
                    
                    if active.title == self.right_page:
                        button.props('fab color=accent')
        
            if self.add_zoom:
                z = ui.button('', icon='zoom_out_map', on_click=set_zoom_right).tooltip('Zoom right `Meta+0`')
                z.props('fab color=info')

        return self.right_button_bar

    def show_gallery_left(self, event):
        print(f'show_gallery_left')
        self.views.show_gallery()

    def show_notes_right(self, event):
        print(f'show_notes_right')
        self.views.show_notes()

    def show_customizer_left(self, event):
        print(f'show_customizer_left')
        self.views.show_customizer(Side.LEFT)

    def show_customizer_right(self, event):
        print(f'show_customizer_right')
        self.views.show_customizer(Side.RIGHT)

    def show_editor_left(self, event):
        print(f'show_editor_left')
        self.views.show_editor(Side.LEFT)

    def show_editor_right(self, event):
        print(f'show_editor_right')
        self.views.show_editor(Side.RIGHT)
    
    def show_viewer_left(self, event):
        print(f'show_viewer_left')
        self.views.show_viewer(Side.LEFT)
    
    def show_viewer_right(self, event):
        print(f'show_viewer_right')
        self.views.show_viewer(Side.RIGHT)

    def show_settings_left(self, event):
        print(f'show_settings_left')
        self.views.show_settings()

    def show_help_right(self, event):
        print(f'show_help_right')
        self.views.show_help()

if __name__ in {"__main__", "__mp_main__"}:
    pages = PageSwitcher()

    with ui.splitter().classes('w-full h-full items-stretch border') as main_splitter:
    
        with main_splitter.before:
            with ui.column().classes('w-full h-full items-stretch border') as containter:
                left_container = containter
                pages.views.gallery = ui.label('Gallery.').classes('w-full h-full')
                pages.views.customizer = ui.label('Customizer.').classes('w-full h-full')  
                pages.views.editor = ui.codemirror(language='python', theme='dracula').classes('w-full h-full')
                pages.views.settings = ui.label('Settings.').classes('w-full h-full')

                left_cards = [pages.views.gallery, pages.views.customizer, pages.views.editor]

        with main_splitter.after:
            with ui.column().classes('w-full h-full items-stretch border') as container:
                right_container = container
                pages.views.notes = ui.label('Notes.').classes('w-full h-full')
                pages.views.viewer = ui.label('Viewer.').classes('w-full h-full')
                pages.views.help = ui.label('Help.').classes('w-full h-full')
                right_cards = [pages.views.notes, pages.views.viewer, pages.views.help]

        with main_splitter.separator:
            ui.icon('multiple_stop').classes('text-grey text-2xl')  
        
    pages.views.update_pages()

    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        
        ctrl_bar = pages.setup_left_button_bar(left_buttons)
        ui.space()
        ui.label('model / path / file name').classes('text-xl')
        ui.space()
        size_splitter = ui.number('Value', format='%.0f', value=50, min=0, max=100, step=10)
        size_splitter.bind_value(main_splitter)  
        alt_bar = pages.setup_right_button_bar(right_buttons)
    

    # Run the NiceGUI app
    ui.run()