import urwid

def show_main_menu():
    """crea y muestra el menu principal del juego"""
    # un creador de texto simnple
    text_header = urwid.Text("--Creador de la Trivia--", align ='center')
    # crea un widget de boton
    # urwid.AttrMap es para aplicar estilos
    # ur2.Button('texto del boton')
    # urwid.WidgetMap convierte el boton en un widget mapable para urwifd
    # urwid.on_press es el evento que se dispara cuando se aprieta
    def exit_program(button):
        raise urwid.ExitMainLoop()
    play_button = urwid.Button('jugar')
    urwid.connect_signal(play_button, 'click', lambda button: print("Jugar a la trivia"))
    add_question_button = urwid.Button('Agregar preg')
    urwid.connect_signal(add_question_button, 'click', lambda button: print("Agregar preguntas"))
    exit_button = urwid.Button('Salir')
    urwid.connect_signal(exit_button, 'click', exit_program)
    # Agrupa los widgets en una lista
    body = [
            urwid.Divider(),
            urwid.Columns([
                ('fixed',2,urwid.Text("")), # Espacio a la izquierda
                urwid.Filler(urwid.Pile([
                    text_header,
                    urwid.Divider(),
                    urwid.Padding(play_button, left = 2, right = 2, width=('relative', 80)),
                    urwid.Padding(add_question_button, left = 2, right = 2, width=('relative', 80)),
                    urwid.Padding(exit_button, left= 2, right = 2, width=('relative', 80)),
                    ]), valign='middle'),
                ('fixed',2,urwid.Text("")),
                ]),
            urwid.Divider(),
            ]
    # Crea la vista que mostrará los widgets
    # urwid.ListBox permite scroll si el contenido es grande 
    # urwid.Filler centra verticalmente
    # urwid.Frame permite canecera, pie de pagina y cuerpo
    list_walker = urwid.SimpleListWalker(body)
    list_box = urwid.ListBox(list_walker)
    # Añade padding para que no ocupe todo el ancho
    padding = urwid.Padding(list_box, align='center', width=('relative', 80))
    # background = urwid.Overlay(padding, urwid.SolidFill(), 'center', ('relative', 80)

    # El punto de entrada principal del bucle de Urwid
    # urwid.MonitoredFocusListWalker es util para que la lista maneje el foco
    loop = urwid.MainLoop(padding, palette=[
        ('button', 'black', 'dark green'), # color del texto del boton
        ('focus button' , 'white', 'dark blue'),
        ('header', 'white', 'dark red', 'bold'), # estilo para el encabezado
        ])

    loop.run()


if __name__ == "__main__":
    show_main_menu()
