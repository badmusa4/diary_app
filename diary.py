from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import datetime
import mysql.connector
from tkinter import ttk

# Initializing database connection
conn = mysql.connector.connect(host="localhost", user="root", password='', database="waveproject")
cursor = conn.cursor()
cursor.execute('use waveproject')

# Create a table for diary entries (if it doesn't exist)
cursor.execute('CREATE TABLE IF NOT EXISTS Diary (id INT AUTO_INCREMENT PRIMARY KEY, Topic VARCHAR(100), created_at TIMESTAMP NOT NULL, story TEXT NOT NULL)')

def add_entry():
    entry_content = entry_story_text.get("1.0", END)
    entry_date = datetime.datetime.now()
    entry_topic = entry_topic_entry.get()  # Get the topic from the entry widget

    # Insert the entry into the database
    cursor.execute('INSERT INTO Diary (Topic, created_at, story) VALUES (%s, %s, %s)', (entry_topic, entry_date, entry_content))
    conn.commit()
    messagebox.showinfo("Success", "Entry added successfully!")

def display_entries():
    # Clear existing table rows
    for row in entry_table.get_children():
        entry_table.delete(row)

    # Retrieve entries from the database
    cursor.execute("SELECT id, Topic, created_at FROM Diary")  # Select id, topic, and date from the Diary table
    entries = cursor.fetchall()

    # Display entries in the table
    for entry in entries:
        entry_table.insert('', 'end', values=(entry[0], entry[1], entry[2].strftime('%Y-%m-%d %H:%M:%S')))  # Convert date to string format

def open_management_window():
    management_window = Toplevel(diary)
    management_window.title("Diary Management")

    # Set default width and height for the window
    management_window.geometry("400x300")

    update_button = Button(management_window, text="Update Entry", command=update_entry)
    update_button.pack()

    Label(management_window, text="Entry ID to Delete:").pack()
    global entry_id_to_delete
    entry_id_to_delete = Entry(management_window)
    entry_id_to_delete.pack()

    delete_entry_button = Button(management_window, text="Delete Entry", command=delete_entry)
    delete_entry_button.pack()

def show_story_popup(item):
    selected_item_id = entry_table.item(item, "values")[0]  # Get the ID of the selected item
    cursor.execute("SELECT story FROM Diary WHERE id = %s", (selected_item_id,))
    story_content = cursor.fetchone()[0]

    story_popup = Toplevel(diary)
    story_popup.title("Story Details")
    story_popup.geometry("800x600")

    story_label = Label(story_popup, text="Story:")
    story_label.pack()

    story_text = Text(story_popup, height=30, width=100)
    story_text.insert(END, story_content)
    story_text.pack()

# Update entry
def update_entry():
    update_user_win = Toplevel(diary)
    update_user_win.title("Update Entry")
    update_user_win.geometry("800x600")

    Label(update_user_win, text="Entry ID:").pack()
    entry_id_entry = Entry(update_user_win)
    entry_id_entry.pack()

    fetch_button = Button(update_user_win, text="Fetch", command=lambda: fetch_entry_content(entry_id_entry.get(), updated_content_entry))
    fetch_button.pack()

    Label(update_user_win, text="Updated Content:").pack()
    updated_content_entry = Text(update_user_win, height=25, width=90)
    updated_content_entry.pack()


    update_button = Button(update_user_win, text="Update", command=lambda: update_entry_in_db(entry_id_entry.get(), updated_content_entry.get("1.0", END)))
    update_button.pack()


def fetch_entry_content(entry_id, updated_content_entry):
    try:
        # Fetch the current content of the specified entry
        cursor.execute("SELECT story FROM Diary WHERE id = %s", (entry_id,))
        current_content = cursor.fetchone()[0]

        # Populate the "Updated Content" field with the fetched content
        updated_content_entry.delete("1.0", END)  # Clear any existing content
        updated_content_entry.insert(END, current_content)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", "Failed to fetch entry. Please try again.")

#  update_entry_in_db
def update_entry_in_db(entry_id, updated_content):
    try:
        # Update the content of the specified entry with the new content
        cursor.execute("UPDATE Diary SET story = %s WHERE id = %s", (updated_content, entry_id))
        conn.commit()
        messagebox.showinfo("Success", "Entry updated successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", "Failed to update entry. Please try again.")

#  delete_entry
def delete_entry():
    entry_id = entry_id_to_delete.get()
    try:
        # Delete the specified entry
        cursor.execute("DELETE FROM Diary WHERE id = %s", (entry_id,))
        conn.commit()
        messagebox.showinfo("Success", "Entry deleted successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", "Failed to delete entry. Please try again.")

def exit_program():
    conn.close()
    cursor.close()
    exit()

# Create a tkinter window
diary = Tk()
diary.title('Diary App')
diary.geometry('921x600+50+50')
diary.resizable(False, False)

bg = Image.open('diary_bg.jpg')
bg = bg.resize((921, 600), Image.LANCZOS)
bg = ImageTk.PhotoImage(bg)
bglabel = Label(diary, image=bg)
bglabel.place(relwidth=1, relheight=1)

# Create widgets for your diary interface
entry_topic_label = Label(diary, text='Topic:')
entry_topic_label.place(x=50, y=50)
entry_topic_entry = Entry(diary, width=60)
entry_topic_entry.place(x=100, y=50)

entry_story_label = Label(diary, text='Story:')
entry_story_label.place(x=50, y=100)
entry_story_text = Text(diary, height=10, width=80)
entry_story_text.place(x=100, y=120)

add_button = Button(diary, width=20, text='Add Entry', command=add_entry, pady=5, bg='Azure3', cursor='hand2', bd=2)
add_button.place(x=100, y=300)

entry_table = ttk.Treeview(diary, columns=('ID', 'Topic', 'Date'), show='headings', height=10)
entry_table.heading('ID', text='ID')
entry_table.heading('Topic', text='Topic')
entry_table.heading('Date', text='Date')
entry_table.place(x=100, y=350)

display_button = Button(diary, text='Display Entries', command=display_entries, width=20, bg='Azure3', cursor='hand2', bd=3)
display_button.place(x=720, y=350)

manage_button = Button(diary, text="Manage Entries", command=open_management_window)
manage_button.place(x=720, y=400)


# Bind the treeview to show the story popup on item selection
entry_table.bind("<Double-1>", lambda event: show_story_popup(entry_table.selection()[0]))


diary.mainloop()
