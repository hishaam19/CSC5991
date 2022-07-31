from tkinter import *
import sqlite3
import calendar
from datetime import datetime,date,timedelta
from tkinter import scrolledtext,messagebox,ttk
from tkcalendar import DateEntry
import psycopg2  
import psycopg2.extras

bl = "#8090ad"
bl1= "#8090ad"
wh = 'white'

now = datetime.now()

def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

class CalendarView:
    def __init__(self, parent,appointment):
        self.parent = parent
        self.appointment = appointment
        self.cal = calendar.TextCalendar(calendar.MONDAY)
        self.year = int(now.strftime('%Y'))
        self.month = int(now.strftime('%m'))
        self.wid = []
        
        self.setup(self.year, self.month)
    
    # Resets the buttons
    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            self.wid.remove(w)
    
    # Moves to previous month/year on calendar
    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        self.clear()
        self.setup(self.year, self.month)
    
    # Moves to next month/year on calendar
    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1
        
        self.clear()
        self.setup(self.year, self.month)
    
     
    def setup(self, y, m):
        left = Button(self.parent, text='<', command=self.go_prev,bg=bl1,font=("HELVETICA",20,'bold'),fg=wh)
        self.wid.append(left)
        left.grid(row=0, column=0)
        
        header = Label(self.parent,font=("HELVETICA",24,'bold'),fg=wh,bg=bl, text='{} {}'.format(calendar.month_abbr[m], str(y)))
        self.wid.append(header)
        header.grid(row=0, column=1, columnspan=5)
        
        right = Button(self.parent, text='>', command=self.go_next,bg=bl1,font=("HELVETICA",20,'bold'),fg=wh)
        self.wid.append(right)
        right.grid(row=0, column=6)
        
        days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        for num, name in enumerate(days):
            t = Label(self.parent, text=name[:3],bg=bl,font=("HELVETICA",15,'bold'),fg=wh)
            self.wid.append(t)
            t.grid(row=1, column=num,pady=(20,5))
            
        di = {}
        
        for w, week in enumerate(self.cal.monthdatescalendar(y, m), 2):
            for d, day in enumerate(week):
                btn = Button(self.parent, text=day.strftime('%d'), bg=bl1,width=16,height=4,fg=wh,
                   font=("ARIAL",10,'bold'),command=lambda day=day: self.selection(day.strftime('%d'),m,y))
                btn.grid(row=w, column=d, sticky='nsew')
                if day.month != m:
                    btn['bg'] = '#aaa'
                    btn['state'] = 'disabled'
                li = []
                for i in self.appointment:
                    if i[4] == day.strftime('%Y-%m-%d'):
                        if day.strftime('%Y-%m-%d') not in di:
                            di[day.strftime('%Y-%m-%d')] = i[1]
                        else:
                            get = di[day.strftime('%Y-%m-%d')]
                            if get not in li:
                                li.append(get)
                                li.append(i[1])
                            else:
                                li.append(i[1])
                            l2 = [x for x in li if type(x) == str]
                            di[day.strftime('%Y-%m-%d')] = l2
                        btn['bg'] = '#0d82b5'
                        if len(di[day.strftime('%Y-%m-%d')][0]) == 1:
                            btn['text'] = day.strftime('%d')+'\n'+di[day.strftime('%Y-%m-%d')]
                        else:
                            btn['text'] = day.strftime('%d')+'\n'+di[day.strftime('%Y-%m-%d')][0]+'\n+'+str(len(di[day.strftime('%Y-%m-%d')])-1)+' more'

                    self.wid.append(btn)
                    if day.month != m:
                        btn['bg'] = '#aaa'
                        btn['state'] = 'disabled'
    

    global conn, cursor
     
    conn=psycopg2.connect(dbname='Scheduling', user='okteto', host='10.152.137.106', password='okteto', port='5432')
    conn.autocommit=True
    cursor = conn.cursor() 
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments 
                   (app_id serial NOT NULL PRIMARY KEY, 
                   firstname  VARCHAR ( 50 ) NOT NULL, 
                   job  VARCHAR ( 50 ) NOT NULL, 
                   email  VARCHAR ( 50 ) NOT NULL, 
                   date DATE, 
                   start_time  VARCHAR ( 50 ) NOT NULL, 
                   end_time  VARCHAR ( 50 ) NOT NULL, 
                   company INTEGER);
                   ''')     
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
        (user_id serial NOT NULL PRIMARY KEY, 
        admin_name  VARCHAR ( 50 ) NOT NULL, 
        username  VARCHAR ( 50 ) NOT NULL, 
        password  VARCHAR ( 255 ) NOT NULL);
        ''')
    
def Login(event=None):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if username.get() == "" or password.get() == "":
        lbl_text.config(text="Please fill all the fields!", fg="red")
    else:
                    
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username1.get(), password1.get()))
                    
        if cursor.fetchone() is not None:
            HomeWindow()
            username.set("")
            password.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password", fg="red")
            username.set("")
            password.set("")   
    cursor.close()
    conn.close()
    
def Register():
    def register_a():
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if name.get() == "" or username1.get() == "" or password1.get() == "":
            lbl_text2.config(text="Please fill all the fields!", fg="red")
        else:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username1.get(),))
            if cursor.fetchone() is not None:
                lbl_text2.config(text='Username Already Exists. Please Try a New Username',fg='red')
                username.set("")
            else:
                cursor.execute("INSERT INTO users (admin_name, username, password) VALUES(%s, %s, %s)",(name.get(),username1.get(),password1.get()))
                conn.commit()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username1.get(), password1.get()))
        cursor.close()
        conn.close()
        messagebox.showinfo('Successful!','You are successfully registered!')
        reg.destroy()
    
    def Back2():
        reg.destroy()
        root.deiconify()

    root.withdraw()
    reg = Toplevel()
    reg.title('Register')
    reg.config(bg=bl)
    reg.resizable(0,0)

    head = Label(reg,text='REGISTRATION',bg=bl, fg=wh, font=('HELVETICA',24,'bold'))
    head.grid(row=0,column=0,padx=10,pady=10,columnspan=2)

    n_lbl = Label(reg,text='Email',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
    n_lbl.grid(row=2,column=0,padx=10,pady=10)

    name = Entry(reg,width=20,font=("ARIAL",12))
    name.grid(row=2,column=1,pady=10,padx=(0,20))

    u_lbl = Label(reg,text='Username',bg=bl,fg=wh,font=("ARIAL",14,'bold'))
    u_lbl.grid(row=1,column=0,padx=10,pady=10)

    username1 = Entry(reg,width=20,font=("ARIAL",12))
    username1.grid(row=1,column=1,pady=10,padx=(0,20))

    pa_lbl = Label(reg,text='Password',bg=bl,fg=wh,font=("ARIAL",14,'bold'))
    pa_lbl.grid(row=3,column=0,padx=10,pady=10)

    password1 = Entry(reg,width=20,show='*',font=("ARIAL",12))
    password1.grid(row=3,column=1,pady=10,padx=(0,20))

    regist = Button(reg,text='Register',font=('HELVETICA',16,'bold'),width=12,fg=wh,bg=bl1,bd=4,relief=RAISED,command=register_a)
    regist.grid(row=4,column=0,columnspan=2,padx=10,pady=10)

    lbl_text2 = Label(reg,bg=bl,font=('arial',12,'bold'))
    lbl_text2.grid(row=7,column=0,columnspan=2,padx=10,pady=(5,20))

    lbl_text3 = Label(reg,bg=bl,font=('arial',12,'bold'),text='OR')
    lbl_text3.grid(row=5,column=0,columnspan=2,padx=10,pady=5)

    btn_reg = Button(reg, text="Login", font=('arial',14,'bold'), command=Back2,bg=bl1,fg=wh,width=12,bd=4,relief=RAISED)
    btn_reg.grid(pady=10, row=6,column=0, columnspan=2,padx=10)
 
def Back():
    Home.destroy()
    username.set("")
    password.set("")
    root.deiconify()

def HomeWindow():
   
    def add_app():
        def conf():
            try:
                start_time = datetime.strptime(start.get(), '%I:%M').time()
            except:
                start_time = datetime.strptime(start.get(), '%I').time()
            try:
                stop_time = datetime.strptime(end.get(), '%I:%M').time()
            except:
                stop_time = datetime.strptime(end.get(), '%I').time()
                
            datetime1 = datetime.combine(date.today(), start_time)
            datetime2 = datetime.combine(date.today(), stop_time)
            time_elapsed = datetime2 - datetime1

            seconds = time_elapsed.total_seconds()
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if int(hours) < 0:
                hours+=12
            start1 = start_time
            end1 = stop_time

            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT start_time,end_time,company from appointments WHERE date = %s",(cal.get_date(),))
            tim = cursor.fetchall()

            if int(hours) >= 2 and int(minutes) > 0:
                messagebox.showerror('Timing Error!','The maximum time of appointments can be 2 hours only!')               

            else:
                if len(tim) == 0:
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute("INSERT INTO appointments (firstname, job, email, date, start_time, end_time, company) VALUES(%s,%s,%s,%s,%s,%s,%s)",(f_name.get(),s_name.get(),email.get(),cal.get_date(),start.get(),end.get(),companys.get()))
                    conn.commit()
                    messagebox.showinfo('Successful!','Appointments is added successfully!')
                    f_name.delete(0,END)
                    s_name.delete(0,END)
                    email.delete(0,END)
                    start.delete(0,END)
                    end.delete(0,END)
                    root2.destroy()
                else:
                    ti = {}
                    li = []
                    for i in tim:
                        try:
                            first = datetime.strptime(str(i[0]), '%I:%M').time()
                        except:
                            first = datetime.strptime(str(i[0]), '%I').time()
                        try:
                            second = datetime.strptime(str(i[1]), '%I:%M').time()
                        except:
                            second = datetime.strptime(str(i[1]), '%I').time()

                        if (time_in_range(first, second, end1) == True or time_in_range(first, second, start1) == True):
                            if False not in ti:
                                ti[False] = i[2]
                            else:
                                get = ti[False]
                                if get not in li:
                                    li.append(get)
                                    li.append(i[2])
                                else:
                                    li.append(i[2])
                                ti[False] = li
                        else:
                            ti[True] = i[2]
                    if False in ti:
                        find = ti[False]
                        try:
                            if 1 in find and 2 in find:
                                messagebox.showerror('Sorry','There are already 2 appointments at this time.')

                            elif companys.get() in find:
                                messagebox.showerror('Not available','This company is not available. Try to find another schedule')
                            else:
                                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                                cursor.execute("INSERT INTO appointments (firstname, job, email, date, start_time, end_time, company) VALUES(%s,%s,%s,%s,%s,%s,%s)",(f_name.get(),s_name.get(),email.get(),cal.get_date(),start.get(),end.get(),companys.get()))
                                conn.commit()
                                messagebox.showinfo('Successful!','Appointments is added successfully!')
                                f_name.delete(0,END)
                                s_name.delete(0,END)
                                email.delete(0,END)
                                start.delete(0,END)
                                end.delete(0,END)
                                root2.destroy()
                        except:
                            if companys.get() == find:
                                messagebox.showerror('Not available','This company is not available. Try to find another schedule')
                            else:
                                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                                cursor.execute("INSERT INTO appointments (firstname, job, email, date, start_time, end_time, company) VALUES(%s,%s,%s,%s,%s,%s,%s)",(f_name.get(),s_name.get(),email.get(),cal.get_date(),start.get(),end.get(),companys.get()))
                                conn.commit()
                                messagebox.showinfo('Successful!','Appointments is added successfully!')
                                f_name.delete(0,END)
                                s_name.delete(0,END)
                                email.delete(0,END)
                                start.delete(0,END)
                                end.delete(0,END)
                                root2.destroy()
                    elif True in ti:
                        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                        cursor.execute("INSERT INTO appointments (firstname, job, email, date, start_time, end_time, company) VALUES(%s,%s,%s,%s,%s,%s,%s)",(f_name.get(),s_name.get(),email.get(),cal.get_date(),start.get(),end.get(),companys.get()))
                        conn.commit()
                        messagebox.showinfo('Successful!','Appointments is added successfully!')
                        f_name.delete(0,END)
                        s_name.delete(0,END)
                        email.delete(0,END)
                        start.delete(0,END)
                        end.delete(0,END)
                        root2.destroy()
                Home.destroy()
                HomeWindow()
               
        root2 = Toplevel()
        root2.config(bg=bl)
        root2.resizable(0,0)

        companys = IntVar()
        
        head = Label(root2,text="ADD APPOINTMENTS",font=("HELVETICA",23,'bold'),bg=bl,fg=wh)
        head.grid(row=0,column=0,padx=10,pady=10,columnspan=2)

        f_lbl = Label(root2,text='First Name',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        f_lbl.grid(row=1,column=0,padx=10,pady=10)

        f_name = Entry(root2,width=20,font=("HELVETICA",12))
        f_name.grid(row=1,column=1,pady=10,padx=(0,20))

        s_lbl = Label(root2,text='Job',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        s_lbl.grid(row=3,column=0,padx=10,pady=10)

        s_name = Entry(root2,width=20,font=("HELVETICA",12))
        s_name.grid(row=3,column=1,pady=10,padx=(0,20))

        p_lbl = Label(root2,text='Email',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        p_lbl.grid(row=2,column=0,padx=10,pady=10)

        email = Entry(root2,width=20,font=("HELVETICA",12))
        email.grid(row=2,column=1,pady=10,padx=(0,20))

        d_lbl = Label(root2,text='Select Date',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        d_lbl.grid(row=4,column=0,padx=10,pady=10)

        cal = DateEntry(root2, width=20,background=bl1,date_pattern='dd/mm/yyyy')
        cal.grid(row=4,column=1,pady=10,padx=(0,20))
        
        s_lbl = Label(root2,text='Start Time',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        s_lbl.grid(row=5,column=0,padx=10,pady=10)

        start = Entry(root2,width=20,font=("HELVETICA",12))
        start.grid(row=5,column=1,pady=10,padx=(0,20))

        e_lbl = Label(root2,text='End Time',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        e_lbl.grid(row=6,column=0,padx=10,pady=10)

        end = Entry(root2,width=20,font=("HELVETICA",12))
        end.grid(row=6,column=1,pady=10,padx=(0,20))

        b_lbl = Label(root2,text='Company',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
        b_lbl.grid(row=7,column=0,padx=10,pady=10)

        company1 = Radiobutton(root2,font=("HELVETICA",12),variable=companys,text='1',value=1,bg=bl,fg=wh,selectcolor=bl,activebackground=bl,activeforeground=wh, tristatevalue=0)
        company1.grid(row=7,column=1,pady=10,padx=(0,120))
        
        company2 = Radiobutton(root2,font=("HELVETICA",12),variable=companys,text='2',value=2,bg=bl,fg=wh,selectcolor=bl,activebackground=bl,activeforeground=wh, tristatevalue=0)
        company2.grid(row=7,column=1,pady=10,padx=(100,20))
        company1.select()

        confirm = Button(root2,text='Confirm',font=("HELVETICA",14,'bold'),width=13,bg=bl1,fg=wh,command=conf)
        confirm.grid(row=10,columnspan=2,pady=10,padx=10)
        
    def edit_app():
        edit = Toplevel()
        edit.title('Edit Appointments')
        edit.config(bg=bl)
        edit.resizable(0,0)
        h = edit.winfo_screenheight() 
        w = edit.winfo_screenwidth()
        edit.geometry("{}x{}".format(w-100, h-150))

        def selectItem(a):
            ask = messagebox.askquestion ('Confirmation','Are You sure you want to Edit this appointment?')
            if ask == 'yes':
                curItem = tree.focus()
                data = tree.item(curItem)['values']
                item = tree.item(curItem)
                new = Toplevel()
                new.resizable(0,0)
                new.title('Edit Appointments')
                new.config(bg=bl)

                def conf():
                    try:
                        start_time = datetime.strptime(start.get(), '%I:%M').time()
                    except:
                        start_time = datetime.strptime(start.get(), '%I').time()
                    try:
                        stop_time = datetime.strptime(end.get(), '%I:%M').time()
                    except:

                        stop_time = datetime.strptime(end.get(), '%I').time()
                        
                    datetime1 = datetime.combine(date.today(), start_time)
                    datetime2 = datetime.combine(date.today(), stop_time)
                    time_elapsed = datetime2 - datetime1

                    seconds = time_elapsed.total_seconds()
                    hours = seconds // 3600
                    minutes = (seconds % 3600) // 60
                    if int(hours) < 0:
                        hours+=12
                    start1 = start_time
                    end1 = stop_time

                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute("SELECT app_id,start_time,end_time from appointments WHERE date = %s",(cal.get_date(),))
                    tim = cursor.fetchall()

                    if int(hours) >= 2 and int(minutes) > 0:
                        messagebox.showerror('Timing Error!','The maximum time of appointments can be 2 hours only!')               

                    else:
                        for i in tim:
                            if int(idd.get()) == int(i[0]):
                                try:
                                    first = datetime.strptime(i[1], '%I:%M').time()
                                except:
                                    first = datetime.strptime(i[1], '%I').time()
                                try:
                                    second = datetime.strptime(i[2], '%I:%M').time()
                                except:
                                    second = datetime.strptime(i[2], '%I').time()

                                if first == start1 and second == end1:
                                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                                    cursor.execute("UPDATE appointments SET firstname = %s, job = %s, email = %s, date = %s, start_time = %s, end_time = %s WHERE app_id = %s",(f_name.get(),s_name.get(),email.get(),cal.get_date(),start.get(),end.get(),idd.get()))
                                    conn.commit()
                                    messagebox.showinfo('Successful!','Appointments is Edited successfully!')
                                    res = []
                                    res.append(int(idd.get()))
                                    res.append(f_name.get())
                                    res.append(s_name.get())
                                    res.append(int(email.get()))
                                    res.append(cal.get_date().strftime('%Y-%m-%d'))
                                    res.append(int(start.get()))
                                    res.append(int(end.get()))
                                    item['values']=res
                                    tree.insert('', str(curItem)[1:], values=(res), tags='T')
                                    tree.delete(curItem)
                                    new.withdraw()
                                    
                                elif time_in_range(first, second, end1) == True or time_in_range(first, second, start1) == True:
                                    messagebox.showerror('Timing Error!','There is already an appointments at this time.')

                                else:
                                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                                    cursor.execute("UPDATE appointments SET firstname = %s, job = %s, email = %s, date = %s, start_time = %s, end_time = %s WHERE app_id = %s",(f_name.get(),s_name.get(),email.get(),cal.get_date(),start.get(),end.get(),idd.get()))
                                    conn.commit()
                                    messagebox.showinfo('Successful!','Appointments is Edited successfully!')
                                    res = []
                                    res.append(int(idd.get()))
                                    res.append(f_name.get())
                                    res.append(s_name.get())
                                    res.append(int(email.get()))
                                    res.append(cal.get_date().strftime('%Y-%m-%d'))
                                    res.append(int(start.get()))
                                    res.append(int(end.get()))
                                    item['values']=res
                                    tree.insert('', str(curItem)[1:], values=(res), tags='T')
                                    tree.delete(curItem)
                                    new.withdraw()

                h = Label(new,text="EDIT APPOINTMENTS",font=("HELVETICA",20,'bold'),bg=bl,fg=wh)
                h.grid(row=0,column=0,columnspan=2,padx=10,pady=10)

                i_lbl = Label(new,text='Appointments ID',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                i_lbl.grid(row=1,column=0,padx=10,pady=10)

                idd = Entry(new,width=20,font=("HELVETICA",12))
                idd.grid(row=1,column=1,pady=10,padx=(0,20))

                f_lbl = Label(new,text='First Name',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                f_lbl.grid(row=2,column=0,padx=10,pady=10)

                f_name = Entry(new,width=20,font=("HELVETICA",12))
                f_name.grid(row=2,column=1,pady=10,padx=(0,20))

                s_lbl = Label(new,text='Job',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                s_lbl.grid(row=3,column=0,padx=10,pady=10)

                s_name = Entry(new,width=20,font=("HELVETICA",12))
                s_name.grid(row=3,column=1,pady=10,padx=(0,20))

                p_lbl = Label(new,text='Email Number',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                p_lbl.grid(row=4,column=0,padx=10,pady=10)

                email = Entry(new,width=20,font=("HELVETICA",12))
                email.grid(row=4,column=1,pady=10,padx=(0,20))

                d_lbl = Label(new,text='Select Date',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                d_lbl.grid(row=5,column=0,padx=10,pady=10)

                cal = DateEntry(new, width=20,background=bl1,date_pattern='dd/mm/yyyy')
                cal.grid(row=5,column=1,pady=10,padx=(0,20))
                
                s_lbl = Label(new,text='Start Time',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                s_lbl.grid(row=6,column=0,padx=10,pady=10)

                start = Entry(new,width=20,font=("HELVETICA",12))
                start.grid(row=6,column=1,pady=10,padx=(0,20))

                e_lbl = Label(new,text='End Time',bg=bl,fg=wh,font=("HELVETICA",14,'bold'))
                e_lbl.grid(row=7,column=0,padx=10,pady=10)

                end = Entry(new,width=20,font=("HELVETICA",12))
                end.grid(row=7,column=1,pady=10,padx=(0,20))

                idd.insert(END,data[0])
                idd.config(state='disabled')
                f_name.insert(END,data[1])
                s_name.insert(END,data[2])
                email.insert(END,data[3])
                cal.delete(0,END)
                cal.insert(END,data[4])
                start.insert(END,data[5])
                end.insert(END,data[6])

                confirm = Button(new,text='Confirm',font=("HELVETICA",14,'bold'),width=13,bg=bl1,fg=wh,command=conf)
                confirm.grid(row=10,columnspan=2,pady=10,padx=10)
        
        head = Label(edit,text="EDIT APPOINTMENTS",font=("HELVETICA",23,'bold'),bg=bl,fg=wh)
        head.pack(pady=30,padx=10)

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM appointments")
        names = [description[0] for description in cursor.description]
        apps = cursor.fetchall()

        style = ttk.Style(edit)
        style.theme_use("clam")
        style.configure('Treeview', rowheight=40)

        tree= ttk.Treeview(edit,show='headings', selectmode="browse")
        tree["columns"] = names
        tree["displaycolumns"] = names
        for head in names:
            tree.heading(head, text=head, anchor=CENTER)
            tree.column(head, anchor=CENTER, stretch=True)

        for row in apps:
            tree.insert('', END, values=tuple(row), tags='T')

        scrolltable1 = Scrollbar(edit, command=tree.yview, orient='vertical')
        scrolltable2 = Scrollbar(edit, command=tree.xview, orient='horizontal')
        tree.configure(yscrollcommand=scrolltable1.set,xscrollcommand=scrolltable2.set)
        scrolltable1.pack(side=RIGHT, fill=Y)
        scrolltable2.pack(side=BOTTOM,fill=X)
        tree.tag_configure('T', font='Arial 13')
        tree.pack(fill=BOTH,expand=YES)
        tree.bind('<ButtonRelease-1>', selectItem)
        
    
    def del_app():
        
        dele = Toplevel()
        dele.title('Delete Appointments')
        dele.config(bg=bl)
        dele.resizable(0,0)
        h = dele.winfo_screenheight() 
        w = dele.winfo_screenwidth()
        dele.geometry("{}x{}".format(w-100, h-150))

        def selectItem(a):
            ask = messagebox.askquestion ('Confirmation','Are You sure you want to delete this appointments?')
            if ask == 'yes':
                curItem = tree.focus()
                data =tree.item(curItem)['values'] 
                cursor.execute("DELETE FROM appointments WHERE app_id = %s",(data[0],))
                conn.commit()
                messagebox.showinfo("Deletion Successful",("The Appointments number "+str(data[0])+' has been deleted'))
            cursor.close()
            conn.close()
            curItem = tree.focus()
            tree.delete(curItem)
        
        head = Label(dele,text="DELETE APPOINTMENTS",font=("HELVETICA",23,'bold'),bg=bl,fg=wh)
        head.pack(pady=30,padx=10)

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM appointments")
        names = [description[0] for description in cursor.description]
        apps = cursor.fetchall()

        style = ttk.Style(dele)
        style.theme_use("clam")
        style.configure('Treeview', rowheight=40)

        tree= ttk.Treeview(dele,show='headings', selectmode="browse")
        tree["columns"] = names
        tree["displaycolumns"] = names
        for head in names:
            tree.heading(head, text=head, anchor=CENTER)
            tree.column(head, anchor=CENTER, stretch=True)

        for row in apps:
            tree.insert('', END, values=tuple(row), tags='T')

        scrolltable1 = Scrollbar(dele, command=tree.yview, orient='vertical')
        scrolltable2 = Scrollbar(dele, command=tree.xview, orient='horizontal')
        tree.configure(yscrollcommand=scrolltable1.set,xscrollcommand=scrolltable2.set)
        scrolltable1.pack(side=RIGHT, fill=Y)
        scrolltable2.pack(side=BOTTOM,fill=X)
        tree.tag_configure('T', font='Arial 13')
        tree.pack(fill=BOTH,expand=YES)
        tree.bind('<ButtonRelease-1>', selectItem)
        

    global Home
    root.withdraw()
    Home = Toplevel()
    Home.title("Interview Reservation System")
    Home.config(bg=bl)
    Home.state('zoomed')
    Home.resizable(0,0)
    head = Label(Home, text="Interview Reservation System", font=('HELVETICA', 24,'bold'),bg=bl,fg=wh)
    head.grid(row=0,column=0,padx=10,columnspan=7)

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT admin_name FROM users WHERE username = %s", (username.get(),))
    name = cursor.fetchone()
    
    lbl_home = Label(Home, text="WELCOME "+name[0].upper(), font=('HELVETICA', 20,'bold'),bg=bl,fg=wh)
    lbl_home.grid(row=1,column=0,padx=10,columnspan=7)

    year = int(now.strftime('%Y'))

    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()

    global calendarViewFrame
    calendarViewFrame = Frame(Home, borderwidth=5, bg=bl)
    calendarViewFrame.grid(row=2, column=0, columnspan=7,rowspan=6)
    viewCalendar = CalendarView(calendarViewFrame,appointments)

    add = Button(Home, text='ADD APPOINTMENTS', command=add_app,bg=bl1,fg=wh,width=20,height=2,font=("HELVETICA",15,'bold'))
    add.grid(row=4,column=8,pady=5,padx=(40,10))

    edit = Button(Home, text='EDIT APPOINTMENTS', command=edit_app,bg=bl1,fg=wh,width=20,height=2,font=("HELVETICA",15,'bold'))
    edit.grid(row=5,column=8,pady=5,padx=(40,10))

    delete = Button(Home, text='DELETE APPOINTMENTS', command=del_app,bg=bl1,fg=wh,width=20,height=2,font=("HELVETICA",15,'bold'))
    delete.grid(row=6,column=8,pady=5,padx=(40,10))  
    
    logout = Button(Home, text='LOGOUT', command=Back,bg=bl1,fg=wh,width=20,height=2,font=("HELVETICA",15,'bold'))
    logout.grid(row=7,column=8,pady=20,padx=(40,10))

    Home.mainloop()

root = Tk()
root.title("Login Page")
root.resizable(0, 0)
root.config(bg=bl)

username = StringVar()
password = StringVar()
 
lbl_title = Label(root, text = "LOG IN", font=('HELVETICA', 25,'bold'),bg=bl,fg=wh)
lbl_title.grid(row=0,column=0,padx=10,pady=10,columnspan=2)

lbl_username = Label(root, text = "Username:", font=('arial', 14),bg=bl,fg=wh)
lbl_username.grid(row=1,column=0, sticky="e",padx=(70,10),pady=(30,10))

username1 = Entry(root, textvariable=username, font=(14))
username1.grid(row=1, column=1,padx=(10,70),pady=(30,10))

lbl_password = Label(root, text = "Password:", font=('arial', 14),bg=bl,fg=wh)
lbl_password.grid(row=2,column=0, sticky="e",padx=(70,10),pady=10)

password1 = Entry(root, textvariable=password, show="*", font=(14))
password1.grid(row=2, column=1,padx=(10,70),pady=10)

btn_login = Button(root, text="Login", font=('arial',14,'bold'), command=Login,bg=bl1,fg=wh,width=12,bd=4,relief=RAISED)
btn_login.grid(pady=(30,10), row=3,column=0, columnspan=2,padx=10)
btn_login.bind('<Return>', Login)

lbl_text1 = Label(root,bg=bl,font=('arial',12,'bold'),text='OR')
lbl_text1.grid(row=4,column=0,columnspan=2,padx=10,pady=5)

btn_reg = Button(root, text="Register", font=('arial',14,'bold'), command=Register,bg=bl1,fg=wh,width=12,bd=4,relief=RAISED)
btn_reg.grid(pady=10, row=5,column=0, columnspan=2,padx=10)

lbl_text = Label(root,bg=bl,font=('arial',12,'bold'))
lbl_text.grid(row=6,column=0,columnspan=2,padx=10,pady=(5,20))

if __name__ == '__main__':
    root.mainloop()
