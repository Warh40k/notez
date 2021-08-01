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

    def add_notes(self, note):
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
    NoteZ 1.0. Written by Nikita Zinkevich. Type 'help' to start.
    """
    shelf.load_notes()

    if len(argv)!=1:
        command = ' '.join(argv[1:])
    else:
        command = input('>>> ').strip()

    if command == 'new':
        file_name = input('Введите название заметки: ')
        file_path = shelf.path + '/.' + file_name
        os.system('nano '+file_path)

        with open(file_path,'r') as file:
            shelf.add_notes(Note(file_name,' '.join(file.readlines())))
            os.remove(file_path)

    elif command == 'show':
        shelf.load_notes()
        k=1
        for i in shelf.catalog:
            print("{0} ".format(k)+i)
            k=k+1
        print()

    elif command == 'help':
        print('\tnew - создать новую записку\n\tshow - посмотреть имеющиеся\n\topen <название> - посмотреть конкретную запись\n\topen all - вывести содержимое ВСЕХ записей\n\thelp - вызов списка команд\n\texit - выход')

    elif 'open' in command:
        try:
            filename = shelf.get_key(command)
        except:
            print('Введи цифру правильно!!!')

        if filename != None:
            print('\n\t' + shelf.catalog[filename])

    elif command == 'exit':
        return

    elif 'rm' in command:
        try:
            target_key = shelf.get_key(command)
            del shelf.catalog[target_key]
            shelf.save_notes()
        except:
            print('Введи цифру правильно!!!')
    if len(argv)==1:
        main_menu(shelf)
# Main
shelf = Note_shelf('notes')
main_menu(shelf)
