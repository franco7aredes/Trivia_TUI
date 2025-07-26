# acá se va a implementar las funciones que relacionan el juego con la base de datos
import sqlite3
import random
import os

class TriviaDatabase:
	def __init__(self, db_name='datos/triv.db'):
		self.db_name = db_name
		self.conn = None
		self.cursor = None
		self._ensure_dir_exists()
		self._connect()
		self._create_table()
	
	def _ensure_dir_exists(self):
		db_dir = os.path.dirname(self.db_name)
		if db_dir and not os.path.exists(db_dir):
			try:
				os.makedirs(db_dir)
				print(f"Directorio '{db_dir}' creado.")
			except OSError as e:
				print("Error al crear directorio '{db_dir}' : '{e}'")
				self.db_name = None
	
	def _connect(self):
		if not self.db_name:
			print("No se puede conectar: ruta de DB no valida")
			return
		try:
			self.conn = sqlite3.connect(self.db_name)
			self.cursor = self.conn.cursor()
			print("Conectado a DB '{self.db_name}'")
		except sqlite3.Error as e:
			print("Error al conectar a '{self.db_name}' : '{e}' ")
			self.conn = None
			self.cursor = None
	
	def _create_table(self):
		if not self.conn:
			print("no se esta conectado a la DB como para crear la tabla")
			return
		try:
			self.cursor.execute('''
				CREATE TABLE IF NOT EXISTS preguntas (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					pregunta TEXT NOT NULL,
					opcion_a TEXT NOT NULL,
					opcion_b TEXT NOT NULL,
					opcion_c TEXT NOT NULL,
					opcion_d TEXT NOT NULL,
					correcta TEXT NOT NULL
				)
			''')
			self.conn.commit()
			print("Tabla 'preguntas' verificada/creada")
		except sqlite3.Error as e:
			print("Error al crear la tabla: '{e}' ")
	
	def add_question(self, preg, op_a, op_b, op_c, op_d, res_correcta):
		if not self.conn:
			print("No hay conexion a la DB como para agregar la pregunta")
			return
		opc_validas = [op_a, op_b, op_c, op_d]
		if res_correcta not in opc_validas:
			print(f"Error: la respuesta correcta no esta en las opciones validas")
			return
		try:
			self.cursor.execute('''
				INSERT INTO preguntas(preg, op_a, op_b, op_c, op_d, res_correcta)
				VALUES (?, ?, ?, ?, ?, ?)
			''', (preg, op_a, op_b, op_c, op_d, res_correcta))
			self.conn.commit()
			print(f"pregunta agregada: '{preg}'")
		except sqlite3.Error as e:
			print(f"Error al agregar la pregunta: '{e}'")
	
	def get_all_questions(self):
		if not self.conn:
			print("No hay conexion a DB, no se puede devolver las preguntas")
			return []
		try:
			self.cursor.execute("SELECT preg, op_a, op_b, op_c, op_d , res_correcta FROM preguntas")
			rows = self.cursor.fetchall()
			preguntas = []
			for row in rows:
				pregunta_dict = {
					'pregunta': row[0],
					'opciones': [row[1], row[2], row[3], row[4]],
					'respuesta_correcta': row[5]
				}
				preguntas.append(pregunta_dict)
			return preguntas
		except sqlite3.Error as e:
			print(f"Error al obtener las preguntas: '{e}'")
			return []
	
	def get_random_questions(self, cantidad):
		all_questions = self.get_all_questions()
		if not all_questions:
			print("No hay preguntas en la base de datos")
			return []
		if len(all_questions) <= count:
			return all_questions
		return random.sample(all_questions, cantidad)
	
	def close(self):
		if self.conn:
			self.conn.close()
			print("Conexion a BD cerrada.")
	
	def clear_all_questions(self):
		if not self.conn:
			print("No se puede borrar las preguntas porque no se esta conectado a la DB")
			return
		try:
			self.cursor.execute("DELETE FROM preguntas")
			self.conn.commit()
			print("Todas las preguntas han sido eliminadas")
		except sqlite3.Error as e:
			print("Error al intentar borrar las preguntas: '{e}'")
