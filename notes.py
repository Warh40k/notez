import os, pickle, argparse

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

    def get_key(self,num):
        note_keys = list(self.catalog.keys())
        target_key = note_keys[int(num) - 1] if len(note_keys)>=int(num) - 1 else None
        return target_key

shelf = Note_shelf('notes')
shelf.load_notes()

parser = argparse.ArgumentParser(description="NoteZ 1.0. Written by Nikita Zinkevich. Type '--help' to start.\n\tnew - создать новую записку\n\tshow - посмотреть имеющиеся\n\topen <название> - посмотреть конкретную запись\n\topen all - вывести содержимое ВСЕХ записей\n\thelp - вызов списка команд\n\texit - выход", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('option', metavar='option', type=str)
parser.add_argument('number', metavar='num', type=int, nargs='?')
args=parser.parse_args()
command = args.option

target_key = shelf.get_key(args.number) if args.number!=None else None

if command == 'new':
    file_name = input('Введите название заметки: ')
    file_path = shelf.path + '/.' + file_name
    os.system('nano '+file_path)

    with open(file_path,'r') as file:
        shelf.add_notes(Note(file_name,' '.join(file.readlines())))
        os.remove(file_path)

elif command == 'list':
    shelf.load_notes()
    k=1
    for i in shelf.catalog:
        print("{0} ".format(k)+i)
        k=k+1
    print()

elif command == 'help':
    print('\tnew - создать новую записку\n\tshow - посмотреть имеющиеся\n\topen <название> - посмотреть конкретную запись\n\topen all - вывести содержимое ВСЕХ записей\n\thelp - вызов списка команд\n\texit - выход')

elif 'show' in command:
    try:
        print('\n\t' + shelf.catalog[target_key])
    except:
        print('Error: not valid number')

elif 'rm' in command:
    try:
        del shelf.catalog[target_key]
        shelf.save_notes()
    except:
        print('Error: not valid number')
