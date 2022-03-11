
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from nltk.corpus import stopwords
from ttkthemes import ThemedTk
import sqlite3
import json




#file path for the names
NAME_PATH = 'name.json'

#Connect to the database
conn = sqlite3.connect('relationship_notes.db')
cur = conn.cursor()

#Create the tables if not exists
sql = '''CREATE TABLE IF NOT EXISTS Positive_notes (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,  
    note TEXT,
    date TEXT
    );
    '''
cur.execute(sql)

sql2 = '''CREATE TABLE IF NOT EXISTS Negative_notes (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,     
    note TEXT,
    date TEXT
    );
    '''
cur.execute(sql2)
conn.commit()
conn.close()



class Notes:
    def __init__(self, root):
        root.title('Remote Relationship')
        root.iconbitmap('heart_icon.ico')
        root.columnconfigure(0, weight= 1)
        root.rowconfigure(0, weight=1)


        mainframe = ttk.Frame(root, padding='3 3 12 12')
        mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        name_frame = ttk.Frame(mainframe, borderwidth=5, relief='raised', width=300, height=200)
        name_frame.grid(column=0, row=0, sticky=(N, S, E, W))
        name_frame.columnconfigure(0, weight=1)
        # name_frame.rowconfigure(0, weight=1)

        notes_frame = ttk.Frame(mainframe, borderwidth=5, relief='raised', width=300, height=500 )
        notes_frame.grid(column=0, row=1, sticky=(N, S, E, W))
        notes_frame.columnconfigure(0, weight=1)
        notes_frame.rowconfigure(2, weight=1)

        delete_btn_frame = ttk.Frame(mainframe, borderwidth=5, relief='raised', width=300, height=500 )
        delete_btn_frame.grid(column=0, row=2, sticky=(N, S, E, W))
        delete_btn_frame.columnconfigure(0, weight=1)

        list_frame = ttk.Frame(mainframe, borderwidth=5, relief='raised', width=300, height=200)
        list_frame.grid(column=1, row=0, sticky=(N, S, E, W))
        list_frame.columnconfigure(1, weight=1)

        search_frame = ttk.Frame(mainframe, borderwidth=5, relief='raised', width=300, height=500 )
        search_frame.grid(column=1, row=1, sticky=(N, S, E, W), rowspan=2)
        search_frame.columnconfigure(0, weight=1)

        
        #Setting the relationship name
        self.name = StringVar()
        self.date = StringVar()
        n, dt = self.read_name(NAME_PATH)

        if len(n) > 0 and len(dt) > 0:
            self.name.set(n)
            self.date.set(dt)
        else:
            self.name.set('Please type your name and the name of your partner')

        self.app_name = ttk.Label(name_frame, text='Welcome to Remote Relationship', font=('Helvetica', 30))
        self.app_name.grid(column=0, row=0, padx=5, pady=5)

        self.name_label = ttk.Label(name_frame, textvariable=self.name, font=('Helvetica', 20))
        self.name_label.grid(column=0, row=1, padx=5, pady=5)

        self.date_label = ttk.Label(name_frame, textvariable=self.date)
        self.date_label.grid(column=0, row=2, padx=5, pady=5, sticky=(N, S, E, W))

        self.write_space = ttk.Entry(name_frame, width=20, font=('Helvetica', 11))
        self.write_space.grid(column=0, row=3, padx=5, pady=5, sticky=(E, W))
    
        self.name_button = ttk.Button(name_frame, text='Set relationship', width=20, command=self.set_name)
        self.name_button.grid(column=0, row=4, padx=5, pady=5)
        

        #Setting the notes
        self.save_title = ttk.Label(notes_frame, text='Save your notes', font=('Helvetica', 20) )
        self.save_title.grid(column=0, row=0, padx=5, pady=5, columnspan=3)

        self.note_name_label = ttk.Label(notes_frame, text='Name for this note', font=('Helvetica', 11))
        self.note_name_label.grid(column=0, row=1, padx=10, pady=10, sticky=W)

        self.note_name_space = ttk.Entry(notes_frame, width=40, font=('Helvetica', 11))
        self.note_name_space.grid(column=1, row=1, padx=10, pady=10, sticky=W)

        self.note_label = ttk.Label(notes_frame, text='Write your note', font=('Helvetica', 11))
        self.note_label.grid(column=0, row=2, padx=10, pady=10, sticky=W)

        self.note_space = Text(notes_frame, width=70, height=15, relief='sunken', font=('Helvetica', 11))
        self.note_space.grid(column=1, row=2, padx=10, pady=10, sticky=(W,N), columnspan=2)
        
        self.delete_text_btn = ttk.Button(notes_frame, text='Delete text', width=15, command=lambda: self.delete_text(self.note_space))
        self.delete_text_btn.grid(column=0, row=3, padx=10, pady=10)

        self.save_positive = ttk.Button(notes_frame, text='Save Positive note', width=20, command=self.save_p)
        self.save_positive.grid(column=1, row=3, padx=10, pady=10, sticky=W)

        self.save_negative = ttk.Button(notes_frame, text='Save Negative note', width=20, command=self.save_n)
        self.save_negative.grid(column=2, row=3, padx=10, pady=10, sticky=E)

        
        #Setting delete all notes and help
        self.help = ttk.Button(delete_btn_frame, text='Help!', width=15, command= self.show_help)
        self.help.grid(column=0, row=0, padx=5, pady=5, sticky=(W, E))

        self.delete_all = ttk.Button(delete_btn_frame, text='Delete all notes', width=20, command=lambda: self.delete_all_notes('all'))
        self.delete_all.grid(column=1, row=0, padx=5, pady=5, sticky=(W, E))

        self.delete_pos = ttk.Button(delete_btn_frame, text='Delete all positive notes', width=30, command=lambda: self.delete_all_notes('positive'))
        self.delete_pos.grid(column=2, row=0, padx=5, pady=5, sticky=(W, E))

        self.delete_neg = ttk.Button(delete_btn_frame, text='Delete all negative notes', width=30, command=lambda: self.delete_all_notes('negative'))
        self.delete_neg.grid(column=3, row=0, padx=5, pady=5, sticky=(W, E))


        #Setting list the notes and statistics button
        self.list_title = ttk.Label(list_frame, text='Check your notes', font=('Helvetica', 20))
        self.list_title.grid(column=0, row=0, padx=10, pady=5, columnspan=3)

        self.explanation_title = ttk.Label(list_frame, text='Here you can see the ID, name, content and date of your positive and negative notes.\n\t\t Also you can check the statistics of your relationship.', font=('Helvetica', 11))
        self.explanation_title.grid(column=0, row=1, padx=10, pady=15, columnspan=3)

        self.list_positive_btn = ttk.Button(list_frame, text='My positive notes', width=20, command=self.list_p)
        self.list_positive_btn.grid(column=1, row=2, padx=10, pady=23, sticky=(E, W))

        self.list_negative_btn = ttk.Button(list_frame, text='My negative notes', width=20, command=self.list_n)
        self.list_negative_btn.grid(column=0, row=2, padx=10, pady=23, sticky=(E, W))

        self.list_stats_btn = ttk.Button(list_frame, text='Statistics', width=20, command=self.get_stats)
        self.list_stats_btn.grid(column=2, row=2, padx=10, pady=23, sticky=(E, W))

        
        
        #Setting the search, edit and delete function
        self.search_title = ttk.Label(search_frame, text='Edit your notes', font=('Helvetica', 20) )
        self.search_title.grid(column=0, row=0, padx=5, pady=5, columnspan=4)

        self.type_title = ttk.Label(search_frame, text='Choose the note type:', font=('Helvetica', 11) )
        self.type_title.grid(column=0, row=1, padx=5, pady=5)

        self.type_note = ttk.Combobox(search_frame, values=('Positive', 'Negative'), state='readonly')
        self.type_note.grid(column=1, row=1, padx=5, pady=5, sticky=W)

        self.id_title = ttk.Label(search_frame, text='Type the ID of the note:', font=('Helvetica', 11) )
        self.id_title.grid(column=2, row=1, padx=5, pady=5)

        self.id_space = ttk.Entry(search_frame, width=10, font=('Helvetica', 11))
        self.id_space.grid(column=3, row=1, padx=5, pady=5, sticky=W)

        self.search_button = ttk.Button(search_frame, text='Search', width=20, command=self.search)
        self.search_button.grid(column=0, row=2, padx=20, pady=5, columnspan=4)

        self.search_name_label = ttk.Label(search_frame, text='Name for this note', font=('Helvetica', 11))
        self.search_name_label.grid(column=0, row=3, padx=5, pady=5, sticky=W, columnspan=2)

        self.search_name_space = ttk.Entry(search_frame, width=40, font=('Helvetica', 11))
        self.search_name_space.grid(column=1, row=3, padx=5, pady=5, sticky=W, columnspan=3)

        self.search_note_label = ttk.Label(search_frame, text='Edit your note', font=('Helvetica', 11))
        self.search_note_label.grid(column=0, row=4, padx=5, pady=5, sticky=W)

        self.search_note_space = Text(search_frame, width=70, height=15, relief='sunken', font=('Helvetica', 11))
        self.search_note_space.grid(column=1, row=4, padx=5, pady=5, sticky=(W,N), columnspan=3)

        self.search_delete_text_btn = ttk.Button(search_frame, text='Delete text', width=15, command=lambda: self.delete_text(self.search_note_space))
        self.search_delete_text_btn.grid(column=0, row=5, padx=5, pady=5)
        
        self.search_save_btn = ttk.Button(search_frame, text='Save changes', width=15, command= self.update)
        self.search_save_btn.grid(column=1, row=5, padx=5, pady=5, sticky=W)

        self.search_delete_note = ttk.Button(search_frame, text='Delete note', width=15, command= self.delete_note)
        self.search_delete_note.grid(column=3, row=5, padx=5, pady=5, sticky=E)


    def read_name(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)['info']
                name = data['name']
                dt = data['date']
        except FileNotFoundError:
            name = ''
            dt = ''

        return name, dt

    def write_name(self, file_path, name, dt):
        with open(file_path, 'w') as f:
            info = {'info': {'name': name, 'date': dt}}
            json.dump(info, f, indent= 2)

    def set_name(self):
        name = self.write_space.get()
        if len(name) < 1:
            return

        dt = str(date.today())
        self.name.set(name)
        self.date.set(dt)

        self.write_name(NAME_PATH, name, dt)
        self.write_space.delete(0, END)

    def delete_text(self, space):
        space.delete('1.0', 'end')


    def save_p(self):
        conn = sqlite3.connect('relationship_notes.db')
        cur = conn.cursor()

        note_name = self.note_name_space.get()
        note_content = self.note_space.get('1.0', 'end')
        dt = str(date.today())

        if len(note_name) < 1 or len(note_content) < 1:
            messagebox.showerror('Error...', 'The notes must have a name and at least 1 character as content.')
            conn.close()
            return

        sql = 'INSERT INTO Positive_notes (name, note, date) VALUES (?, ?, ?);'
        cur.execute(sql, (note_name, note_content, dt))
        conn.commit()
        cur.close()

        self.note_name_space.delete(0, END)
        self.note_space.delete('1.0', 'end')

        messagebox.showinfo('Saved', 'Your note was saved.')
        

    def save_n(self):
        conn = sqlite3.connect('relationship_notes.db')
        cur = conn.cursor()

        note_name = self.note_name_space.get()
        note_content = self.note_space.get('1.0', 'end')
        dt = str(date.today())

        if len(note_name) < 1 or len(note_content) < 1:
            messagebox.showerror('Error...', 'The notes must have a name and at least 1 character as content.')
            conn.close()
            return

        sql = 'INSERT INTO Negative_notes (name, note, date) VALUES (?, ?, ?);'
        cur.execute(sql, (note_name, note_content, dt))
        conn.commit()
        cur.close()

        self.note_name_space.delete(0, END)
        self.note_space.delete('1.0', 'end')

        messagebox.showinfo('Saved', 'Your note was saved.')

    def delete_all_notes(self, tp):
        conn = sqlite3.connect('relationship_notes.db')
        cur = conn.cursor()

        if tp == 'all':
            answer = messagebox.askokcancel('Attention...', 'Are you sure you want to delete all of your notes?')
            if answer:
                sql = 'DELETE FROM Positive_notes'
                cur.execute(sql)

                sql = 'DELETE FROM Negative_notes'
                cur.execute(sql)
            else:
                conn.close()
                return   
        
        elif tp == 'positive':
            answer = messagebox.askokcancel('Attention...', 'Are you sure you want to delete all of your positive notes?')
            if answer:
                sql = 'DELETE FROM Positive_notes'
                cur.execute(sql)
            else: 
                conn.close()
                return

        elif tp == 'negative':
            answer = messagebox.askokcancel('Attention...', 'Are you sure you want to delete all of your negative notes?')
            if answer:
                sql = 'DELETE FROM Negative_notes'
                cur.execute(sql)
            else:
                conn.close()
                return

        conn.commit()
        conn.close()



    def show_help(self):
        messagebox.showinfo('Help...', '''To set up your environment:\n\n 1. Type your name and the name of your partner, then click on SET RELATIONSHIP. \n\n 2. You just need to type the name for your note and the content in order to save your first note.\n\n 3. Finally, once you have your first note, you will be able to view, edit and delete your notes. You can also check the statistics base on your notes''')

    def list_p(self):
        conn = sqlite3.connect('relationship_notes.db')
        cur = conn.cursor()

        sql = 'SELECT * FROM Positive_notes;'
        cur.execute(sql)
        positive = cur.fetchall()
        if len(positive) < 1:
            messagebox.showerror('Error...', 'No notes available')
            conn.close()
            return

        list_window = ThemedTk(theme='adapta')
        list_window.geometry('900x300')
        list_window.title('My Positive Notes')
        list_window.iconbitmap('heart_icon.ico')
        list_window.columnconfigure(0, weight= 1)


        titleframe = ttk.Frame(list_window, relief='raised', padding='3 3 12 12', width=600, height=600)
        titleframe.pack(fill=BOTH, expand=YES, anchor=CENTER, side=TOP)
        
        canvas = Canvas(list_window)
        canvas.pack(fill=BOTH, expand=YES, side=LEFT)
        

        s_vertical = Scrollbar(list_window, orient=VERTICAL, relief='sunken')
        s_vertical.pack(side=RIGHT, fill=Y)
       
    
        s_vertical.config(command=canvas.yview)
        canvas.config(yscrollcommand=s_vertical.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox('all')))
        

        

        listframe = ttk.Frame(canvas, relief='raised', padding='3 3 12 12', width=500, height=500)
        canvas.create_window((0,0), window=listframe, anchor='nw')
        listframe.columnconfigure(0, weight=1)
        listframe.rowconfigure(0, weight=1)


        positive_title = ttk.Label(titleframe, text='Your notes', font=('Helvetica', 20))
        positive_title.pack(anchor=CENTER)

        id_title = ttk.Label(listframe, text='ID', font=('Helvetica', 15))
        id_title.grid(column=0, row=0, padx=10, pady=5)

        name_title = ttk.Label(listframe, text='Note name', font=('Helvetica', 15))
        name_title.grid(column=1, row=0, padx=10, pady=5)

        note_title = ttk.Label(listframe, text='Note', font=('Helvetica', 15))
        note_title.grid(column=2, row=0, padx=10, pady=5)

        date_title = ttk.Label(listframe, text='Date', font=('Helvetica', 15))
        date_title.grid(column=3, row=0, padx=10, pady=5)

        row = 1
        for item in positive:
            item_id = item[0]
            id_label = ttk.Label(listframe, text=item_id, font=('Helvetica', 11), wraplength=100)
            id_label.grid(column=0, row=row, padx=5, pady=5)
            item_name = item[1]
            name_label = ttk.Label(listframe, text=item_name, font=('Helvetica', 11), wraplength=100)
            name_label.grid(column=1, row=row, padx=5, pady=5)
            item_note = item[2]
            name_label = ttk.Label(listframe, text=item_note, font=('Helvetica', 11), wraplength=600)
            name_label.grid(column=2, row=row, padx=5, pady=5)
            item_date = item[3]
            date_label = ttk.Label(listframe, text=item_date, font=('Helvetica', 11), wraplength=100)
            date_label.grid(column=3, row=row, padx=5, pady=5)

            row += 1

        conn.commit()
        conn.close()
        
    def list_n(self):
        conn = sqlite3.connect('relationship_notes.db')
        cur = conn.cursor()

        sql = 'SELECT * FROM Negative_notes;'
        cur.execute(sql)
        negative = cur.fetchall()
        if len(negative) < 1:
            messagebox.showerror('Error...', 'No notes available')
            conn.close()
            return

        list_window = ThemedTk(theme='adapta')
        list_window.geometry('900x300')
        list_window.title('My Negative Notes')
        list_window.iconbitmap('heart_icon.ico')
        list_window.columnconfigure(0, weight= 1)


        titleframe = ttk.Frame(list_window, relief='raised', padding='3 3 12 12', width=600, height=600)
        titleframe.pack(fill=BOTH, expand=YES, anchor=CENTER, side=TOP)
        
        
        canvas = Canvas(list_window)
        canvas.pack(fill=BOTH, expand=YES, side=LEFT)
        

        s_vertical = Scrollbar(list_window, orient=VERTICAL, relief='sunken')
        s_vertical.pack(side=RIGHT, fill=Y)
       
        
        s_vertical.config(command=canvas.yview)
        canvas.config(yscrollcommand=s_vertical.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox('all')))
        

        listframe = ttk.Frame(canvas, relief='raised', padding='3 3 12 12', width=500, height=500)
        canvas.create_window((0,0), window=listframe, anchor='nw')
        listframe.columnconfigure(0, weight=1)
        listframe.rowconfigure(0, weight=1)


        negative_title = ttk.Label(titleframe, text='Your notes', font=('Helvetica', 20))
        negative_title.pack(anchor=CENTER)

        id_title = ttk.Label(listframe, text='ID', font=('Helvetica', 15))
        id_title.grid(column=0, row=0, padx=10, pady=5)

        name_title = ttk.Label(listframe, text='Note name', font=('Helvetica', 15))
        name_title.grid(column=1, row=0, padx=10, pady=5)

        note_title = ttk.Label(listframe, text='Note', font=('Helvetica', 15))
        note_title.grid(column=2, row=0, padx=10, pady=5)

        date_title = ttk.Label(listframe, text='Date', font=('Helvetica', 15))
        date_title.grid(column=3, row=0, padx=10, pady=5)

        row = 1
        for item in negative:
            item_id = item[0]
            id_label = ttk.Label(listframe, text=item_id, font=('Helvetica', 11), wraplength=100)
            id_label.grid(column=0, row=row, padx=5, pady=5)
            item_name = item[1]
            name_label = ttk.Label(listframe, text=item_name, font=('Helvetica', 11), wraplength=100)
            name_label.grid(column=1, row=row, padx=5, pady=5)
            item_note = item[2]
            name_label = ttk.Label(listframe, text=item_note, font=('Helvetica', 11), wraplength=600)
            name_label.grid(column=2, row=row, padx=5, pady=5)
            item_date = item[3]
            date_label = ttk.Label(listframe, text=item_date, font=('Helvetica', 11), wraplength=100)
            date_label.grid(column=3, row=row, padx=5, pady=5)

            row += 1

        conn.commit()
        conn.close()
        

    def get_stats(self):
        conn = sqlite3.connect('relationship_notes.db')
        cur = conn.cursor()

        #database queries
        sql = 'SELECT COUNT (*) FROM Positive_notes'
        cur.execute(sql)
        record_p = cur.fetchone()
        positive_c = record_p[0]

        sql = 'SELECT COUNT (*) FROM Negative_notes'
        cur.execute(sql)
        record_n = cur.fetchone()
        negative_c = record_n[0]

        sql = 'SELECT note FROM Positive_notes'
        cur.execute(sql)
        positive_db = cur.fetchall()
        
        sql = 'SELECT note FROM Negative_notes'
        cur.execute(sql)
        negative_db = cur.fetchall()

        all_notes = positive_db + negative_db
        print(all_notes)


        #stats operations
        #average
        total = positive_c + negative_c
        if total < 1:
            messagebox.showerror('Attention...', 'No statistics available')
            conn.close()
            return

        av = str(round((positive_c / total) * 100, 2)) +'%'

        #most common word
        words_count = {}
        for x in all_notes:
            string = x[0].lower().replace(',', '').replace('.', '')
           
            lst = [word for word in string.split() if word not in stopwords.words('spanish') and word not in stopwords.words('english')]
            for word in lst:
                words_count[word] = words_count.get(word, 0) + 1
        
        words_count = {k:v for k,v in sorted(words_count.items(), reverse=True, key= lambda item: item[1])}
    
        common_word = list(words_count.keys())[0]
        

        #interface
        stat_root = ThemedTk(theme='adapta')
        stat_root.title('Your Statistics')
        stat_root.iconbitmap('heart_icon.ico')
        stat_root.columnconfigure(0, weight= 1)
        stat_root.rowconfigure(0, weight=1)


        m_frame = ttk.Frame(stat_root, padding='3 3 12 12')
        m_frame.grid(column=0, row=0, sticky=(N, S, E, W))
        m_frame.columnconfigure(0, weight=1)
        m_frame.rowconfigure(0, weight=1)

        name_frame = ttk.Frame(m_frame, borderwidth=5, relief='raised', width=300, height=200)
        name_frame.grid(column=0, row=0, sticky=(N, S, E, W))
        name_frame.columnconfigure(0, weight=1)

        info_frame = ttk.Frame(m_frame, borderwidth=5, relief='raised', width=300, height=200)
        info_frame.grid(column=0, row=1, sticky=(N, S, E, W))
        info_frame.columnconfigure(0, weight=1)

        #title
        title = ttk.Label(name_frame, text='Statistics',  font=('Helvetica', 30))
        title.grid(column=0, row=0, padx=5, pady=5)

        #number of notes
        positive_number_label = ttk.Label(info_frame, text='Number of positive notes:', font=('Helvetica', 20))
        positive_number_label.grid(column=0, row=0, padx=5, pady=5)

        positive_number =  ttk.Label(info_frame, text=str(positive_c), font=('Helvetica', 20)) 
        positive_number.grid(column=1, row=0, padx=5, pady=5)

        negative_number_label = ttk.Label(info_frame, text='Number of negative notes:', font=('Helvetica', 20))
        negative_number_label.grid(column=0, row=1, padx=5, pady=5)

        negative_number =  ttk.Label(info_frame, text=str(negative_c), font=('Helvetica', 20)) 
        negative_number.grid(column=1, row=1, padx=5, pady=5)

        #average
        success_lb = ttk.Label(info_frame, text='Success of the relationship:',  font=('Helvetica', 20) )
        success_lb.grid(column=0, row=2, padx=5, pady=5)

        success = ttk.Label(info_frame, text=av,  font=('Helvetica', 20) )
        success.grid(column=1, row=2, padx=5, pady=5)
        
        #common word
        common_lb = ttk.Label(info_frame, text='Most used word:',  font=('Helvetica', 20) )
        common_lb.grid(column=0, row=3, padx=5, pady=5)

        common = ttk.Label(info_frame, text=common_word,  font=('Helvetica', 20) )
        common.grid(column=1, row=3, padx=5, pady=5)

        conn.commit()
        conn.close()
        


    def search(self):
        tp = self.type_note.get()
        note_id = self.id_space.get()
        if len(tp) < 1 or len(note_id) < 1:
            messagebox.showerror('Error...', 'Please choose the type of the note, and type the ID')
            return

        conn = sqlite3.connect('relationship_notes.db')
        cur = conn.cursor()

        if tp == 'Positive':
            sql = f'SELECT * FROM Positive_notes WHERE id = {note_id}'
            cur.execute(sql)
            record = cur.fetchall()
            
            if len(record) < 1:
                messagebox.showerror('Error...', 'There is no positive note with that ID')
                conn.close()
                return

            self.search_name_space.delete(0, END)
            self.search_note_space.delete('1.0', 'end')

            self.search_name_space.insert(0, record[0][1])
            self.search_note_space.insert('1.0', record[0][2])

        elif tp == 'Negative':
            sql = f'SELECT * FROM Negative_notes WHERE id = {note_id}'
            cur.execute(sql)
            record = cur.fetchall()
            
            if len(record) < 1:
                messagebox.showerror('Error...', 'There is no negative note with that ID')
                conn.close()
                return

            self.search_name_space.delete(0, END)
            self.search_note_space.delete('1.0', 'end')

            self.search_name_space.insert(0, record[0][1])
            self.search_note_space.insert('1.0', record[0][2])


        conn.commit()
        conn.close()


    def update(self):
        tp = self.type_note.get()
        note_id = self.id_space.get()
        if len(tp) < 1 or len(note_id) < 1:
            messagebox.showerror('Error...', 'Please choose the type of the note, and type the ID')
            return
        
        note_name = self.search_name_space.get()
        note_text = self.search_note_space.get('1.0', 'end')
        

        if len(note_name) < 1 or len(note_text) < 1:
            messagebox.showerror('Error...', 'The notes must have a name and at least 1 character as content.')
            return

        dt = str(date.today())


        answer = messagebox.askokcancel('Attention...', 'Are you sure you want to save the changes?')
        if not answer:
            return

        conn = sqlite3.connect('relationship_notes.db')
        cur = conn.cursor()

        
        if tp == 'Positive':
            sql = 'UPDATE Positive_notes SET name = ? , note = ? , date = ? WHERE id= ?'
            cur.execute(sql, (note_name, note_text, dt, note_id))

        elif tp == 'Negative':
            sql = 'UPDATE Negative_notes SET name = ?, note = ?, date = ? WHERE id= ?'
            cur.execute(sql, (note_name, note_text, dt, note_id))

        self.type_note.set('')
        self.id_space.delete(0, END)
        self.search_name_space.delete(0, END)
        self.search_note_space.delete('1.0', 'end')
        
        messagebox.showinfo('Success...', 'The changes for this note were succesfully saved.')

        conn.commit()
        conn.close()


    def delete_note(self):
        tp = self.type_note.get()
        note_id = self.id_space.get()
        if len(tp) < 1 or len(note_id) < 1:
            messagebox.showerror('Error...', 'Please choose the type of the note, and type the ID')
            return

        answer = messagebox.askokcancel('Attention...', 'Are you sure you want to delete this note?')
        if not answer:
            return

        conn = sqlite3.connect('relationship_notes.db')
        cur = conn.cursor()
  

        if tp == 'Positive':
            sql = f'DELETE FROM Positive_notes WHERE id = {note_id}'
            cur.execute(sql)

        elif tp == 'Negative':
            sql = f'DELETE FROM Negative_notes WHERE id = {note_id}'
            cur.execute(sql)

        self.type_note.set('')
        self.id_space.delete(0, END)
        self.search_name_space.delete(0, END)
        self.search_note_space.delete('1.0', 'end')
        
        messagebox.showinfo('Success...', 'The note was deleted.')

        conn.commit()
        conn.close()




root = ThemedTk(theme='adapta')
notes = Notes(root)
root.mainloop()



