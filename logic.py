# aca se implementa la logica del juego
import random
import urwid

class Juego:

    def __init__ (self, preguntas):
        self.preguntas = preguntas
        self.puntuacion = 0
        self.preg_actual_indice = 0
        self.terminado = False
        self.indices_disponibles = list(range(len(preguntas)))
        random.shuffle(self.indices_disponibles)

    def obtener_preg_actual(self):
        if self.preg_actual_indice < len(self.indices_disponibles):
            indice_real = self.indices_disponibles[self.preg_actual_indice]
            return self.preguntas[indice_real]
        return None

    def verificar_resp(self, resp_selec):
        pregunta = self.obtener_preg_actual()
        if pregunta and resp_selec == pregunta["respuesta_correcta"]:
            self.puntuacion +=1
            return True
        return False

    def sig_preg(self):
        self.preg_actual_indice +=1
        if self.preg_actual_indice >= len(self.indices_disponibles):
            self.terminado = True

class App:

    def __init__(self, preguntas, game_loop, return_to_menu_callback):
        self.juego = Juego(preguntas)
        self.loop = game_loop
        self.return_to_menu_callback = return_to_menu_callback
        self.widget_preg = urwid.Text("")
        self.widget_opc = urwid.Pile([])
        self.widget_mensaje = urwid.Text("")
        self.widget_puntuacion = urwid.Text("")
        self.main_widget = self._crear_interfaz_principal()
        self.actualizar_interfaz()

    def _crear_interfaz_principal(self):
        # Unir todos los elementos en un layout
        return urwid.Frame(
            body=urwid.Pile([
                ("fixed", 1, urwid.Divider("-")),
                ("fixed", 1, self.widget_preg),
                ("fixed", 1, urwid.Divider("-")),
                self.widget_opc,
                ("fixed", 1, urwid.Divider("-")),
                ("fixed", 1, self.widget_mensaje),
                ("fixed", 1, self.widget_puntuacion),
            ]),
            header=urwid.Text("ya tu sabe, mi loco", align="center"),
            footer=urwid.Text("Presiona q para salir", align="center")
        )

    def actualizar_interfaz(self):
        self.widget_mensaje.set_text("")
        if self.juego.terminado:
            self.widget_preg.set_text("y se terminó")
            self.widget_opc.contents = []
            self.widget_opc.contents.append((urwid.Text("Gracias totales", align='center'), ('pack',None)))
            self.widget_puntuacion.set_text(f"Puntuacion final: {self.juego.puntuacion}")
            return_button = urwid.Button("Volver al menu")
            urwid.connect_signal(return_button, 'click', self.return_to_menu_callback)
            self.widget_opc.contents.append((urwid.AttrMap(return_button, 'button', 'focus button'), ('pack', None)))
        else:
            pregunta_actual = self.juego.obtener_preg_actual()
            if pregunta_actual:
                self.widget_preg.set_text(("question", pregunta_actual['pregunta']))
                self.widget_puntuacion.set_text(("status",f"Puntuacion: {self.juego.puntuacion} / {self.juego.preg_actual_indice + 1}"))
                opciones_widgets = []
                opciones_mezcladas = random.sample(pregunta_actual['opciones'], len(pregunta_actual['opciones']))
                for opcion in opciones_mezcladas:
                    button = urwid.Button(opcion)
                    urwid.connect_signal(button, 'click', self.manejar_respuesta, opcion)
                    opciones_widgets.append((urwid.AttrMap(button, 'button', 'focus button'),('pack', None)))
                self.widget_opc.contents = opciones_widgets
            else:
                self.juego.terminado = True
                self.actualizar_interfaz()

    def manejar_respuesta(self,button, res_selec):
        es_correcta = self.juego.verificar_resp(res_selec)
        if es_correcta:
            self.widget_mensaje.set_text("Bien, loco")
        else:
            preg_actual = self.juego.obtener_preg_actual()
            self.widget_mensaje.set_text(f"moqueaste. La Respuesta era {preg_actual['respuesta_correcta']}")
        # se puede esperar un tiempo, o pedirle al usuario que toque una tecla.
        # se decide de que el usuario espere xq es loco
        self.loop.set_alarm_in(1.5, self.continuar_juego) # espera 1.5 seg

    def continuar_juego(self, loop, data):
        self.juego.sig_preg()
        self.actualizar_interfaz()

    def unhandled_input(self, key):
        if key in ('q','Q'):
            self.return_to_menu_callback()
            return True
        return False

    def run(self):
        self.loop = urwid.MainLoop(self.main_widget, unhandled_input=self.unhandled_input)
        self.loop.run()

class AddQuestionForm:
    """
    gestiona la interfaz para agregar nuevas preguntas a la db
    """

    def __init__(self, db_instance, return_to_menu_callback):
        self.db = db_instance
        self.return_to_menu_callback = return_to_menu_callback
        # campos de entrada de texto
        # edit_text es la opcion que se muestra por defecto
        self.edit_question = urwid.Edit(edit_text="Escribe tu pregunta Aqui: ")
        self.edit_correct = urwid.Edit("Respuesta correcta: ")
        self.edit_option2 = urwid.Edit("Opcion incorrecta 1: ")
        self.edit_option3 = urwid.Edit("Opcion incorrecta 2: ")
        self.edit_option4 = urwid.Edit("Opcion incorrecta 3: ")
        # botones
        self.save_button = urwid.Button("Guardar")
        urwid.connect_signal(self.save_button, 'click', self._save_question)
        self.cancel_button = urwid.Button("Cancelar")
        urwid.connect_signal(self.cancel_button, 'click', lambda button: self.return_to_menu_callback())
        self.message_widget = urwid.Text("", align='center')
        # Organizar los widgets en un pile
        pile = urwid.Pile([
            urwid.AttrMap(urwid.Text("---Agregar nueva pregunta---", align='center'), 'header'),
            urwid.Divider(),
            urwid.AttrMap(self.edit_question, 'edit_field', 'focus edit_field'),
            urwid.AttrMap(self.edit_correct, 'edit_field', 'focus edit_field'),
            urwid.AttrMap(self.edit_option2, 'edit_field', 'focus edit_field'),
            urwid.AttrMap(self.edit_option3, 'edit_field', 'focus edit_field'),
            urwid.AttrMap(self.edit_option4, 'edit_field', 'focus edit_field'),
            self.message_widget,
            urwid.Divider(),
            urwid.AttrMap(self.save_button, 'button', 'focus button'),
            urwid.AttrMap(self.cancel_button, 'button', 'focus button'),
        ])
        # Centrar el contenido y crear el Frame principal para la vista
        body_widget = urwid.Filler(pile, valign='middle')
        self.main_widget = urwid.Frame(
            body=urwid.Padding(body_widget, left=2, right=2, width=('relative', 80)),
            header=urwid.AttrMap(urwid.Text("Formulario de preguntas", align='center'), 'header'),
            footer=urwid.AttrMap(urwid.Text("Completa y  guarda, loco", align='center'),'footer')
        )

    def _save_question(self, button):
        question_text = self.edit_question.edit_text.strip()
        correct_answer = self.edit_correct.edit_text.strip()
        option2 = self.edit_option2.edit_text.strip()
        option3 = self.edit_option3.edit_text.strip()
        option4 = self.edit_option4.edit_text.strip()
        # chequeo basico para no romperme la base
        if not all([question_text, correct_answer, option2, option3, option4]):
            self.message_widget.set_text(("Error: todos los campos son obligatorios"))
            return
        # elimino duplicados
        options = [correct_answer, option2, option3, option4]
        if len(set(options)) < len(options):
            self.message_widget.set_text(("Error: todas las opciones tienen que ser distintas"))
            return
        try:
            success = self.db.add_question(question_text, correct_answer, option2, option3, option4, correct_answer)
            if success:
                self.message_widget.set_text(("Pregunta guardada con exito"))
                self.edit_question.set_edit_text("")
                self.edit_correct.edit_text("")
                self.edit_option2.edit_text("")
                self.edit_option3.edit_text("")
                self.edit_option4.edit_text("")
            # mover el foco al primer campo despues de guardiar
                self.main_widget.body.original_widget.set_focus(self.edit_question)
            else:
                self.message_widget.set_text(("error","Error al guardar la pregunta en la db"))
        except Exception as e:
            self.message_widget.set_text(("Error",f"Error al guardar: {e}"))
    
    def unhandled_input(self, key):
        if key in ('q','Q'):
            self.return_to_menu_callback()
            return True
        return False

    def get_widget(self):
        return self.main_widget
