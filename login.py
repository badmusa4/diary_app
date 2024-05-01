from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import font
import mysql.connector


# login functionality


def forget_code():
    def change_password():
        if user.get() == '' or newcode.get() == '' or Rcode.get() == '':
            messagebox.showerror('Error', 'All Fields Are Required', parent=window)

        elif newcode.get() != Rcode.get():
            messagebox.showerror('Error', 'Passwords does not match', parent=window)

        else:
            conn = mysql.connector.connect(host='localhost', user="root", password='', database='waveproject')
            cursor = conn.cursor()

            query = "select * from logs where Username=%s"
            cursor.execute(query, (user.get(),))

            old = cursor.fetchone()
            if old != 'None':
                # messagebox.showerror('Error', 'Incorrect Username', parent= window)
                query = "update logs SET Password = %s where Username=%s"
                cursor.execute(query, (newcode.get(), user.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Password Reset Successful, Please Login with New Password!",
                                    parent=window)

                window.destroy()
            else:
                messagebox.showerror('Error', 'Incorrect Username', parent=window)

    window = Toplevel()
    window.title('Change Password')
    window.geometry('850x550+50+50')
    window.resizable(False, False)

    bg_image = ImageTk.PhotoImage(file='background.jpg')
    bgLabel = Label(window, image=bg_image)
    bgLabel.pack()

    win_frame = Frame(window, width=260, height=400, bg='azure2')
    win_frame.place(x=100, y=70)

    win_head = Label(win_frame, text='RESET PASSWORD', bg='azure2', fg='dark slate grey', font=(Pfont, 18, 'bold'))
    win_head.place(x=15, y=20)

    label = Label(win_frame, text='Username', bg='azure2', fg='dark slate grey', font=(Pfont, 12, 'bold'))
    label.place(x=20, y=78)
    user = Entry(win_frame, width=25, fg='dark slate grey', border=0, bg='white', font=(Pfont, 11, 'bold'))
    user.place(x=20, y=100)

    Frame(win_frame, width=205, height=2, bg='dark slate grey').place(x=20, y=120)

    label = Label(win_frame, text='New Password', bg='azure2', fg='dark slate grey', font=(Pfont, 12, 'bold'))
    label.place(x=20, y=125)
    newcode = Entry(win_frame, width=25, fg='dark slate grey', border=0, bg='white', font=(Pfont, 11, 'bold'))
    newcode.place(x=20, y=150)

    Frame(win_frame, width=205, height=2, bg='dark slate grey').place(x=20, y=170)

    label = Label(win_frame, text='Confirm Password', bg='azure2', fg='dark slate grey', font=(Pfont, 12, 'bold'))
    label.place(x=20, y=175)
    Rcode = Entry(win_frame, width=25, fg='dark slate grey', border=0, bg='white', font=(Pfont, 11, 'bold'))
    Rcode.place(x=20, y=200)

    Frame(win_frame, width=205, height=2, bg='dark slate grey').place(x=20, y=220)

    Button(win_frame, width=28, pady=5, text='Submit', cursor='hand2', bg='dark slate grey', fg='white', border=0,
           command=change_password).place(x=20, y=250)

    window.mainloop()


def login_user():
    if User.get() == '' or code.get() == '':
        messagebox.showerror('Error', 'All Entries Are Required')

    else:
        try:
            conn = mysql.connector.connect(host='localhost', user="root", password='')
            cursor = conn.cursor()
        except:
            messagebox.showerror('Error', 'Unable to Connect to Server')
            return

        query = 'USE waveproject'
        cursor.execute(query)
        query = 'select * from logs where Username=%s and Password=%s'
        cursor.execute(query, (User.get(), code.get()))
        invalid = cursor.fetchone()
        if invalid == 'None':
            messagebox.showerror('Error', 'Invalid login details')
        else:
            messagebox.showinfo('Welcome', 'Login Successful')

            root.destroy()
            import diary


def signup_page():
    root.destroy()
    import wave_signin


def hide():
    openeye.config(file='closed lock.png')
    code.config(show='*')
    eye_button.config(command=show)


def show():
    openeye.config(file='openlock.png')
    code.config(show='')
    eye_button.config(command=hide)


def on_entry_focus_in(event):
    # Handle focus in (entry widget gains focus)
    if event.widget == User:
        if User.get() == 'Username':
            User.delete(0, END)
    elif event.widget == code:
        if code.get() == 'Password':
            code.delete(0, END)


def on_exit_focus_out(event):
    # Handle focus out (entry widget loses focus)
    if event.widget == User:
        if not User.get():
            User.insert(0, 'Username')
    elif event.widget == code:
        if not code.get():
            code.insert(0, 'Password')


root = Tk()
root.title('Login')
root.geometry('921x600+50+50')
root.resizable(False, False)

# Creating a font
Pfont = font.Font(family="Microsoft Yahei UI Light")

background_image = Image.open('background.jpg')
background_photo = ImageTk.PhotoImage(background_image)
background_label = Label(root, image=background_photo)
background_label.pack()

# create logo
image_path = 'python.png'
icon_image = Image.open(image_path)
image = ImageTk.PhotoImage(icon_image)
root.iconphoto(True, image)

frame = Frame(root, width=250, height=400, bg='Azure3')
frame.place(x=100, y=70)

Heading = Label(frame, text='USER LOGIN', bg='Azure3', fg='deepskyblue4', font=("Microsoft Yahei UI Light", 18, 'bold'))
Heading.place(x=50, y=20)

User = Entry(frame, width=25, fg='deepskyblue4', border=0, bg='white', font=(Pfont, 11, 'bold'))
User.place(x=20, y=100)
User.insert(0, 'Username')
# Bind focus events to Entry widgets
User.bind("<FocusIn>", on_entry_focus_in)
User.bind("<FocusOut>", on_exit_focus_out)

Frame(frame, width=205, height=2, bg='deepskyblue4').place(x=20, y=120)

code = Entry(frame, width=25, fg='deepskyblue4', border=0, bg='white', font=(Pfont, 11, 'bold'))
code.place(x=20, y=150)
code.insert(0, 'Password')
# Bind focus events to Entry widgets
code.bind("<FocusIn>", on_entry_focus_in)
code.bind("<FocusOut>", on_exit_focus_out)

Frame(frame, width=205, height=2, bg='deepskyblue4').place(x=20, y=170)

openeye = PhotoImage(file='openlock.png')
eye_button = Button(frame, image=openeye, bd=0, bg='white', cursor='hand2', command=hide)
eye_button.place(x=200, y=150)

forgot = Button(frame, text='Forgot Password?', bd=0, bg='Azure3', fg='deepskyblue4',
                cursor='hand2', font=(Pfont, 9, 'bold'), command=forget_code)
forgot.place(x=115, y=187)

# creating signin button
Button(frame, width=28, pady=5, text='Login', cursor='hand2', bg='deepskyblue4', fg='white', border=0,
       command=login_user).place(x=20, y=220)

account = Label(frame, text="Don't have an account?", fg='black', bg='Azure3', font=(Pfont, 9, 'bold'))
account.place(x=25, y=255)

sign_up = Button(frame, width=6, text='Sign Up', border=0, bg='Azure3', cursor='hand2', fg='deepskyblue4',
                 font=(Pfont, 9, 'bold'), command=signup_page)
sign_up.place(x=165, y=255)

root.mainloop()
