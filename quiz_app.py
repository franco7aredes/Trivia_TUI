import urwid
import logic
import database

class Trivia:
    def __init__(self):
        self.database = database.TriviaDatabase()
        self.current_view = None
        self.main_loop = None
        self.database._create_table()
        self.show_main_menu()

    def start_game(self, button = None):
        game_instance = logic.App(self.database, self.main_loop, self.return_to_menu)
        self.set_view(game_instance.get_widget(), game_instance.unhandled_input)

    def return_to_menu(self):
        self.show_main_menu()

    def exit_program(self,button = None):
        raise urwid.ExitMainLoop()

    def show_main_menu(self):
        """crea y muestra el menu principal del juego"""
        # un creador de texto simnple
        text_header = urwid.Text("--Creador de la Trivia--", align ='center')
        # crea un widget de boton
        # urwid.AttrMap es para aplicar estilos
        # ur2.Button('texto del boton')
        # urwid.WidgetMap convierte el boton en un widget mapable para urwifd
        # urwid.on_press es el evento que se dispara cuando se aprieta
        play_button = urwid.Button('jugar')
        urwid.connect_signal(play_button, 'click', self.start_game)
        add_question_button = urwid.Button('Agregar preg')
        urwid.connect_signal(add_question_button, 'click',self.add_question_form)
        exit_button = urwid.Button('Salir')
        urwid.connect_signal(exit_button, 'click', self.exit_program)
        # Agrupa los widgets en una pila
        pile_content = urwid.Pile([
            urwid.AttrMap(text_header, 'header'),
            urwid.Divider(),
            urwid.AttrMap(urwid.Padding(play_button, left=2, right=2, width=('relative', 80)), 'menu_item', 'focus menu_item'),
            urwid.AttrMap(urwid.Padding(add_question_button, left=2, right=2, width=('relative', 80)), 'menu_item', 'focus menu_item'),
            urwid.AttrMap(urwid.Padding(exit_button, left=2, right=2, width=('relative', 80)), 'menu_item', 'focus menu_item'),
            ])
        # Crea la vista que mostrará los widgets
        # urwid.ListBox permite scroll si el contenido es grande 
        # urwid.Filler centra verticalmente
        # urwid.Frame permite cabecera, pie de pagina y cuerpo
        body_widget = urwid.Filler(pile_content, valign='middle')
        #list_walker = urwid.SimpleListWalker([pile_content])
        #list_box = urwid.ListBox(list_walker)
        # Añade padding para que no ocupe todo el ancho
        menu_frame = urwid.Frame(
            body=body_widget,
            header=urwid.AttrMap(urwid.Text("menu principal", align='center'), 'header'),
            footer=urwid.AttrMap(urwid.Text("te mueves con las flechas", align='center'), 'footer')
        )
        #padding = urwid.Padding(menu_frame, align='center', width=('relative', 80))
        # background = urwid.Overlay(padding, urwid.SolidFill(), 'center', ('relative', 80)
        #self.current_view = urwid.Filler(padding, valign='middle')
        self.set_view(menu_frame, self.unhandled_input_default)

    def set_view(self, new_widget, unhandled_input_handler=None):
        if self.main_loop:
            self.main_loop.widget = new_widget
            self.main_loop.unhandled_input = unhandled_input_handler if unhandled_input_handler else self.unhandled_input_default
        else:
            palete = [
                ('button', 'black', 'dark green'),
                ('focus button', 'white', 'dark blue'),
                ('header', 'white', 'dark red', 'bold'),
                ('question', 'light cyan', 'black', 'bold'),
                ('status', 'yellow', 'black'),
                ('game_over', 'light red', 'black', 'bold'),
                ('status_message', 'light magenta', 'black'),
            ]
            self.main_loop = urwid.MainLoop(new_widget, palette=palete, unhandled_input=unhandled_input_handler if unhandled_input_handler else self.unhandled_input_default)
            self.main_loop.screen.set_terminal_properties(colors=256)

    def unhandled_input_default(self, key):
	    if key in ('q', 'Q'):
		    exit_program()

    def run(self):
	    self.main_loop.run()

    def add_question_form(self, button = None):
        form_instance = logic.AddQuestionForm(self.main_loop, self.return_to_menu)
        self.set_view(form_instance.get_widget(), form_instance.unhandled_input)

if __name__ == "__main__":
    app = Trivia()
    app.run()
