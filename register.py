from tkinter import  *
from PIL import  ImageTk
from tkinter import messagebox
from tkinter import font
import mysql.connector
# import  re

def clear():
    first_name.delete(0, END)
    last_name.delete(0, END)
    user.delete(0, END)
    email.delete(0, END)
    code.delete(0, END)
    Rcode.delete(0, END)
    terms_check.set('Accepted')


def login_page():
    project_window.destroy()
    import wave_login

# def validate_email(email):
#     # Use a regex pattern to validate the email address
#     pattern = r'^\S+@\S+\.\S+$'
#     # If the string matches the regex, it is a valid email
#     if re.match(pattern, email):
#         return True
#     else:
#         return False
#
# def validate_password(code):
#     # Use the same regex pattern for password validation
#     pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
#     # If the string matches the regex, it is a valid password
#     if re.match(pattern, code):
#         return True
#     else:
#         return False

def database_connect():
    if first_name.get() == '' or last_name.get() == '' or user.get() == '' or code.get() == '' or email.get() == '' or Rcode.get()== '':
        messagebox.showerror('Error', 'All Entries Are Required')

    elif code.get() != Rcode.get():
        messagebox.showerror('Error','Password does not match')

    elif terms_check.get() != 'Accepted':
        messagebox.showerror('Error', 'Accept Terms and Condition')

    else:
        try:
            conn = mysql.connector.connect(host='localhost', user="root", password='')
            cursor = conn.cursor()
        except:
            messagebox.showerror('Error', 'Unable to Connect to Server')
            return

        try:
            Query= 'create database waveproject'
            cursor.execute(Query)
            Query= 'use waveproject'
            cursor.execute(Query)
            Query= 'CREATE TABLE IF NOT EXISTS logs (id int auto_increment primary key, Firstname TEXT, Lastname TEXT, Email TEXT, Username TEXT, Password varchar(20), Diary_entries TEXT, Date int)'
            cursor.execute(Query)

        except:
            cursor.execute('use waveproject')

        #     checking if user exists
        Query= "select * from logs where Username=%s and Email=%s"
        cursor.execute(Query, (user.get(), email.get()))

        old = cursor.fetchone()
        if old != None:
            messagebox.showerror('Error', 'User already exists')

        else:
            Query= 'insert into logs(Firstname, Lastname, Email, Username, Password) values (%s,%s,%s,%s,%s)'
            cursor.execute(Query,(first_name.get(), last_name.get(),email.get(), user.get(), code.get()))

            conn.commit()
            conn.close()
            messagebox.showinfo('Success', "Registration is Successful")
            clear()
            project_window.destroy()
            import wave_login


project_window = Tk()
project_window.title('Login')
project_window.geometry ('921x600+50+50')
project_window.resizable(False,False)

# Creating a font
Pfont = font.Font(family="Zedaya")

background_image= ImageTk.PhotoImage(file = 'background.jpg')
bgLabel= Label(project_window, image= background_image, bg= 'Azure2')
bgLabel.pack()

frame = Frame(project_window, width= 350, height= 500, bg= 'Azure2')
frame.place(x= 100, y = 70)

Heading= Label(frame,text= 'CREATE AN ACCOUNT', bg= 'Azure2',fg= 'chocolate1', font=(Pfont, 18, 'bold' ))
Heading.place(x= 35, y= 10)

# Create usernane entry
label= Label(frame,text= 'Firstname:', bg='Azure2', fg= 'chocolate1', font= (Pfont, 12, 'bold'))
label.place(x= 40, y=70)
first_name = Entry(frame, width=30, bg='white', border=2, fg='Black', font=('Zedaya', 11))
first_name.place(x= 43, y=90)

label= Label(frame,text= 'Lastname:', bg='Azure2', fg= 'chocolate1', font= (Pfont, 12, 'bold'))
label.place(x= 40,y=120)
last_name = Entry(frame, width=30, bg='white', border=2, fg='Black', font=('Zedaya', 11))
last_name.place(x= 43, y=140)

label= Label(frame,text= 'Email:', bg='Azure2', fg= 'chocolate1', font= (Pfont, 12, 'bold'))
label.place(x= 40, y=170)
email = Entry(frame, width=30, bg='white', border=2, fg='Black', font=('Zedaya', 11))
email.place(x= 43, y=190)

label= Label(frame,text= 'Username:', bg='Azure2', fg= 'chocolate1', font= (Pfont, 12, 'bold'))
label.place(x= 40, y=220)
user = Entry(frame, width=30, bg='white', border=2, fg='Black', font=('Zedaya', 11))
user.place(x= 43, y=240)

label= Label(frame,text= 'Password:', bg='Azure2', fg= 'chocolate1', font= (Pfont, 12, 'bold'))
label.place(x= 40, y=270)
code = Entry(frame, width=30, bg='white', border=2, fg='Black', font=('Zedaya', 11))
code.place(x= 43, y=290)

label= Label(frame,text= 'Confirm Password:', bg='Azure2', fg= 'chocolate1', font= (Pfont, 12, 'bold'))
label.place(x= 40, y=320)
Rcode = Entry(frame, width=30, bg='white', border=2, fg='Black', font=('Zedaya', 11))
Rcode.place(x= 43, y=340)

terms_check = StringVar(value= 'Not Accepted')
termsandconditions = Checkbutton(frame, text= 'I agree to the Terms & Conditions', font= (Pfont, 11), bg= 'Azure2', cursor= 'hand2',
                                 variable= terms_check,
                                 onvalue= 'Accepted',
                                 offvalue= 'Not Accepted')
termsandconditions.place(x=40, y= 370 )

Button(frame, width= 34, pady= 5 , text= 'Signup',cursor= 'hand2', bg = 'chocolate1', fg= 'white', border=0, command= database_connect ). place(x=40, y= 410)

alreadyaccount= Label(frame, text= 'Already created an account?', bg= 'Azure2', font= (Pfont, 9 ) )
alreadyaccount.place(x= 40, y= 450)

Login= Button(frame, text= 'Login',bd= 0, bg= 'Azure2', cursor= 'hand2', fg= 'chocolate1',  font=(Pfont,9, 'bold'), command= login_page)
Login.place(x= 205, y= 450)


project_window.mainloop()