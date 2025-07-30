import urwid
import logic
import database

#Noneleta de colores, centralizada aquí ya que Trivia es tu controlador principal
PALETTE = [
    ('body', 'black', 'light gray'),
    ('header', 'white', 'dark blue', 'bold'),
    ('footer', 'white', 'dark green', 'bold'),
    ('button', 'black', 'dark cyan'),
    ('focus button', 'white', 'dark blue', 'bold'),
    ('question', 'yellow', 'default', 'bold'),
    ('status', 'white', 'dark red', 'bold'),
    ('edit_field', 'black', 'light green'),
    ('focus edit_field', 'black', 'dark green', 'bold'),
    ('error', 'white', 'dark red', 'bold'),
    ('success', 'white', 'dark green', 'bold'),
    ('menu_item', 'black', 'light gray'),
    ('focus menu_item', 'white', 'dark blue'),
    ('list_item', 'black', 'white'), # Para la vista de preguntas
    ('focus list_item', 'white', 'dark red', 'bold') # Para la vista de preguntas
]
                                                            

class Trivia:
    def __init__(self):
        self.database = database.TriviaDatabase()
        self.current_view = None
        self.main_loop = urwid.MainLoop(urwid.WidgetPlaceholder(urwid.SolidFill()), PALETTE, unhandled_input=self.unhandled_input_default)
        self.main_loop.screen.set_terminal_properties(colors=256)
        self.create_main_menu()

    def start_game(self, button = None):
        preguntas = self.database.get_random_questions(10)
        if not preguntas:
            self.show_message("No hay suficientes preguntas en la db")
            self.main_loop.set_alarm_in(2, lambda loop, data: self.return_to_menu())
        game_instance = logic.App(self.database, self.main_loop, self.return_to_menu)
        self.set_view(game_instance.get_widget(), game_instance.unhandled_input)

    def return_to_menu(self, button=None):
        self.set_view(self.menu_frame, self.unhandled_input_default)

    def exit_program(self,button = None):
        raise urwid.ExitMainLoop()

    def create_main_menu(self):
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
        view_questions_button = urwid.Button('Ver preguntas')
        urwid.connect_signal(view_questions_button, 'click', self.show_all_questions)
        # Agrupa los widgets en una pila
        pile_content = urwid.Pile([
            urwid.AttrMap(text_header, 'header'),
            urwid.Divider(),
            urwid.AttrMap(urwid.Padding(play_button, left=2, right=2, width=('relative', 80)), 'menu_item', 'focus menu_item'),
            urwid.AttrMap(urwid.Padding(add_question_button, left=2, right=2, width=('relative', 80)), 'menu_item', 'focus menu_item'),
            urwid.AttrMap(urwid.Padding(exit_button, left=2, right=2, width=('relative', 80)), 'menu_item', 'focus menu_item'),
            urwid.AttrMap(urwid.Padding(view_questions_button, left=2, right=2, width=('relative', 80)), 'menu_item', 'focus menu_item'),
            urwid.Divider(),
            urwid.AttrMap(urwid.Text("Se maneja con las flechas y enter", align='center'), 'footer')
            ])
        # Crea la vista que mostrará los widgets
        # urwid.ListBox permite scroll si el contenido es grande 
        # urwid.Filler centra verticalmente
        # urwid.Frame permite cabecera, pie de pagina y cuerpo
        body_widget = urwid.Filler(pile_content, valign='middle')
        #list_walker = urwid.SimpleListWalker([pile_content])
        #list_box = urwid.ListBox(list_walker)
        # Añade padding para que no ocupe todo el ancho
        self.menu_frame = urwid.Frame(
            body=body_widget,
            header=urwid.AttrMap(urwid.Text("menu principal", align='center'), 'header'),
            footer=urwid.AttrMap(urwid.Text("Bienvenido a esta basofia", align='center'), 'footer')
        )
        #padding = urwid.Padding(menu_frame, align='center', width=('relative', 80))
        # background = urwid.Overlay(padding, urwid.SolidFill(), 'center', ('relative', 80)
        #self.current_view = urwid.Filler(padding, valign='middle')
        self.set_view(self.menu_frame, self.unhandled_input_default)

    def set_view(self, new_widget, unhandled_input_handler=None):
        self.main_loop.widget = new_widget
        self.main_loop.unhandled_input = unhandled_input_handler if unhandled_input_handler else self.unhandled_input_default

    def unhandled_input_default(self, key):
        if key in ('q', 'Q'):
            self.exit_program()
            return True
        return False

    def run(self):
	    self.main_loop.run()

    def add_question_form(self, button = None):
        form_instance = logic.AddQuestionForm(self.database, self.return_to_menu)
        self.set_view(form_instance.main_widget, form_instance.unhandled_input)


    def show_all_questions(self, button=None):
        questions = self.database.get_all_questions()
        if not questions:
            self.show_message("No hay preguntas para mostrar.", 'info')
            self.main_loop.set_alarm_in(2, lambda loop, data: self.return_to_menu())
            return

        list_widgets = []
        for i, q_data in enumerate(questions):
            list_widgets.append(urwid.AttrMap(urwid.Text(f"Pregunta {i+1}: {q_data['pregunta']}"), 'list_item'))
            list_widgets.append(urwid.AttrMap(urwid.Text(f"  Opciones: {', '.join(q_data['opciones'])}"), 'list_item'))
            list_widgets.append(urwid.AttrMap(urwid.Text(f"  Correcta: {q_data['respuesta_correcta']}"), 'list_item'))
            list_widgets.append(urwid.Divider())

        # Añadir un botón para volver
        back_button = urwid.Button("Volver al Menú")
        urwid.connect_signal(back_button, 'click', self.return_to_menu)
        list_widgets.append(urwid.AttrMap(back_button, 'button', 'focus button'))

        list_box = urwid.ListBox(urwid.SimpleListWalker(list_widgets))
        frame = urwid.Frame(
            body=urwid.Padding(list_box, left=2, right=2, width=('relative', 90)),
            header=urwid.AttrMap(urwid.Text("Todas las Preguntas", align='center'), 'header'),
            footer=urwid.AttrMap(urwid.Text("Presiona 'q' para volver al menú", align='center'), 'footer')
        )
        self.set_view(frame, self._unhandled_input_for_list_view)
    
    def show_message(self, message, message_type='info'):
        # Muestra un mensaje temporal en la parte inferior de la pantalla
        message_widget = urwid.AttrMap(urwid.Text(message, align='center'), message_type)

        # Guardar el footer original y reemplazarlo
        original_footer = self.main_loop.widget.footer if isinstance(self.main_loop.widget, urwid.Frame) else None
        if isinstance(self.main_loop.widget, urwid.Frame):
            self.main_loop.widget.footer = message_widget
        else:
        # Si el widget actual no es un Frame, envuélvelo temporalmente
            current_body = self.main_loop.widget
            self.main_loop.widget = urwid.Frame(body=current_body, footer=message_widget)

if __name__ == "__main__":
    app = Trivia()
    app.run()
    app.database.close()
