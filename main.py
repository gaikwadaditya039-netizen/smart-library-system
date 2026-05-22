# Smart Library System (premium UI)
import customtkinter as ctk
import json, os
from tkinter import messagebox
from datetime import datetime, timedelta

FILE = 'books.json'
if not os.path.exists(FILE):
    with open(FILE, 'w') as f:
        json.dump([], f)

def load_books():
    with open(FILE, 'r') as f:
        return json.load(f)

def save_books(data):
    with open(FILE, 'w') as f:
        json.dump(data, f, indent=4)

def refresh():
    textbox.delete('1.0', 'end')
    books = load_books()
    for i, b in enumerate(books, 1):
        status = 'Issued' if b['issued'] else 'Available'
        textbox.insert('end', f"{i}. {b['title']} | {b['author']} | {status} | {b.get('issue_date','-')} | {b.get('return_date','-')}\n")

def add_book():
    books = load_books()
    books.append({'title': title_entry.get(), 'author': author_entry.get(), 'issued': False, 'issue_date': '', 'return_date': ''})
    save_books(books)
    refresh()

def issue_book():
    books = load_books()
    for b in books:
        if b['title'].lower() == title_entry.get().lower():
            b['issued'] = True
            b['issue_date'] = datetime.now().strftime('%d-%m-%Y')
            b['return_date'] = (datetime.now()+timedelta(days=7)).strftime('%d-%m-%Y')
    save_books(books)
    refresh()

def return_book():
    books = load_books()
    for b in books:
        if b['title'].lower() == title_entry.get().lower():
            b['issued'] = False
            b['issue_date'] = ''
            b['return_date'] = ''
    save_books(books)
    refresh()

def search_book():
    keyword = title_entry.get().lower()
    textbox.delete('1.0', 'end')
    for b in load_books():
        if keyword in b['title'].lower():
            textbox.insert('end', f"{b['title']} by {b['author']}\n")

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')
app = ctk.CTk()
app.geometry('950x600')
app.title('Smart Library System')

ctk.CTkLabel(app, text='📚 Smart Library System', font=('Helvetica', 30, 'bold'), text_color='#4FC3F7').pack(pady=15)
ctk.CTkLabel(app, text=f"Date: {datetime.now().strftime('%d-%m-%Y')}", font=('Arial', 16)).pack()

title_entry = ctk.CTkEntry(app, placeholder_text='Book Title', width=350)
title_entry.pack(pady=8)
author_entry = ctk.CTkEntry(app, placeholder_text='Author Name', width=350)
author_entry.pack(pady=8)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text='Add', command=add_book, width=120).grid(row=0, column=0, padx=5)
ctk.CTkButton(button_frame, text='Issue', command=issue_book, width=120).grid(row=0, column=1, padx=5)
ctk.CTkButton(button_frame, text='Return', command=return_book, width=120).grid(row=0, column=2, padx=5)
ctk.CTkButton(button_frame, text='Search', command=search_book, width=120).grid(row=0, column=3, padx=5)
ctk.CTkButton(button_frame, text='View', command=refresh, width=120).grid(row=0, column=4, padx=5)

textbox = ctk.CTkTextbox(app, width=850, height=300, font=('Consolas', 14))
textbox.pack(pady=20)

refresh()
app.mainloop()

