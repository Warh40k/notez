#! /usr/bin/python
import os, argparse, mariadb, sys, pickle

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
        for i in shelf.catalog.keys():
            cur.execute(f'INSERT INTO noteshelf (note_id, note_name, note_content VALUES(null,"{i}","{shelf.content[i]}"')
    def load_notes(self):
        with open(os.path.join(self.path,self.name)+'.dat', 'rb') as file:
            pickle.load(file)

    def get_key(self,num):
        note_keys = list(self.catalog.keys())
        target_key = note_keys[int(num) - 1] if len(note_keys)>=int(num) - 1 else None
        return target_key
try:
    con = mariadb.connect(
        user = 'nikita',
        password = '428829',
        host = 'localhost',
        database = 'notes'
    )
    print(mariadb.apilevel)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")

cur = con.cursor()
shelf = Note_shelf('notes')
shelf.load_notes()

parser = argparse.ArgumentParser(description="NoteZ 1.0. Written by Nikita Zinkevich. Type '--help' to start.\nnew - создать новую записку\nshow - посмотреть имеющиеся\nopen <название> - посмотреть конкретную запись\nopen all - вывести содержимое ВСЕХ записей\nhelp - вызов списка команд\nexit - выход", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('option', metavar='OPTION', type=str)
parser.add_argument('number', metavar='NUM', type=int, nargs='?')
args=parser.parse_args()
command = args.option
file_path=shelf.path+'/.'

if args.number!=None:
    target_key = shelf.get_key(args.number)
    file_path += str(args.number)
else:
    file_path += str(len(shelf.catalog)-1)

if command == 'new':
    file_name = input('Введите название заметки: ')
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
    print('new - создать новую записку\nshow - посмотреть имеющиеся\nopen <название> - посмотреть конкретную запись\nopen all - вывести содержимое ВСЕХ записей\nhelp - вызов списка команд\nexit - выход')

elif 'show' in command:
    try:
        string = f'\n\t{target_key}\n\n{shelf.catalog[target_key]}'
        os.system(f'echo "{string}" | less')
    except:
        print('Error: not valid number')

elif 'edit' in command:
    try:
        os.system(f'echo "{shelf.catalog[target_key]}">{file_path}; nano {file_path}')
        with open(file_path,'r') as file:
            shelf.catalog[target_key] = ' '.join(file.readlines())
            shelf.save_notes()
        os.remove(file_path)
    except:
        print('Error: not valid number')
elif 'rm' in command:
    try:
        del shelf.catalog[target_key]
        shelf.save_notes()
    except:
        print('Error: not valid number')
