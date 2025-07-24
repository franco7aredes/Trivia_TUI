# aca se implementa la logica del juego
import random
import urwid

class juego:
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
        if self.preg_actual_indice >= len(self.indices_disponibles)

class App:
    def __init__(self, trivia):
        self.juego = trivia
        self.loop = None
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
        if self.juego.juego_terminado:
            self.widget_preg.set_text("y se terminó")
            self.widget_opc.contents = []
            self.widget_opciones.set_text("Gracias totales")
            self.widget_puntuacion.set_text(f"Puntuacion final: {self.juego.puntuacion}")
        else:
            pass
    def manejar_respuesta(self,button, res_selec):
        es_correcta = self.juego.verificar_resp(res_selec)
        if es_correcta:
            self.widget_mensaje.set_text("Bien, loco")
        else:
            preg_actual = self.juego.obtener_preg_actual()
            self.widget_mensaje.set_text("moqueaste. La Respuesta era {preg_actual['respuesta_correcta']}")
        # se puede esperar un tiempo, o pedirle al usuario que toque una tecla.
        # se decide de que el usuario espere xq es loco
        self.loop.set_alarm_in(1.5, self.continuar_juego) # espera 1.5 seg
    def continuar_juego(self, loop, data):
        self.juego.sig_preg()
        self.actualizar_interfaz()
        self.loop.draw_screen() # actualiza pantalla
    def unhandled_input(self, key):
        if key in ('q','Q'):
            raise urwid.ExitMainLoop()
    def run(self):
        self.loop = urwid.MainLoop(self.main_widget, unhandled_input=self.unhandled_input)
        self.loop.run()
