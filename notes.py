import os, pickle
from sys import argv

class Note():
	name=''
	content = ''
	delimiters = ['.',',','!','?',':','-']
	def __init__(self,name, content):
		self.name = name
		self.content = content

	def rename(self, name):
		self.name = name

class Note_shelf():
	name = 'notes'
	catalog = {}
	path = ''
	locker = {}

	def __init__(self,name,path = os.path.dirname(__file__)):
		self.name = name
		self.path = path

	def add_notes(self,note):
		self.catalog[note.name] = note.content
		self.save_notes()


	def save_notes(self):
		with open(os.path.join(self.path,self.name)+'.dat','wb') as f:
			pickle.dump(self.catalog, f)

	def load_notes(self):
		with open(os.path.join(self.path,self.name)+'.dat', 'rb') as file:
				self.catalog = pickle.load(file)

	def get_key(self,command):
		num = command.split()[1]
		if num.isdigit():
			note_keys = list(self.catalog.keys())
			target_key = note_keys[int(num) - 1] if len(note_keys)>=int(num) - 1 else None
			return target_key

def main_menu(shelf):
	"""
	Привет! Этот консольный менеджер записок был написан Никитой Зинкевичем. Для того чтобы начать, набери 'help' для получения списка команд. Удачи в поиске новых и хранении старых идей!!!
	"""
	shelf.load_notes()

	command = input('>>> ').strip()

	if command == 'new':
		file_name = input('Введите название заметки: ')
		file_content = input('Введите описание заметки:\n')
		output_text = ''
		m = 0
		string_length = 96

		while True:
			file_content =file_content +'\n' + input()
			if file_content[-3:]=='end': break

		length = len(file_content)-1

		for i in range(0,length):
			if file_content[i] == '\n':
				output_text+= '\n' + file_content[i-m:i+1].strip()
				m = -1
			elif m >= string_length - 1 or i == length:
				if file_content[i+1]==' ' or (not file_content[i].isalpha() and file_content[i+1].isalpha()):
					output_text += '\n' + file_content[i-m:i+1].strip()
					m = -1

			m=m+1
		note = Note(file_name, output_text.rstrip('en'))
		shelf.add_notes(note)

	elif command == 'show':
		shelf.load_notes()
		k=1
		for i in shelf.catalog:
			print("{0} ".format(k)+i)
			k=k+1

	elif command == 'help':
		print('\tnew - создать новую записку\n\tshow - посмотреть имеющиеся\n\topen <название> - посмотреть конкретную запись\n\topen all - вывести содержимое ВСЕХ записей\n\thelp - вызов списка команд\n\texit - выход')

	elif 'open' in command:
		filename = shelf.get_key(command)
		if filename != None:
			print('\n\t' + filename + shelf.catalog[filename])
	
	elif 'add' in command:
		filename = shelf.get_key(command)
		if filename != None:
			shelf.catalog[filename]+='\n' + input('Введите добавочный текст:\n')
			shelf.save_notes()

	elif command == 'exit':
		return

	elif 'rm' in command:
		try:
			target_key = shelf.get_key(command)
			del shelf.catalog[target_key]
			shelf.save_notes()
		except:
			print('Введи цифру правильно!!!')
	main_menu(shelf)

# Main
print(main_menu.__doc__)
shelf = Note_shelf('notes')
main_menu(shelf)



