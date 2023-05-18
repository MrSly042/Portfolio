import tkinter as tk
from math import ceil
from tkinter import messagebox
from tkinter.ttk import Button as ttk_but

import pymysql as query
from PIL import Image, ImageTk

from dotenv import load_dotenv
import os

load_dotenv('local.env')

hostname: str = os.getenv('DB_HOST')
username: str = os.getenv('DB_USER')
password: str = os.getenv('DB_PASS')
database: str = os.getenv('DB_NAME')

class Hybrid(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        #get & set root icon
        icon = ImageTk.PhotoImage(file="CHEBBY ENERGY.png")
        
        self.title("Hybrid section")
        self.iconphoto(False, icon)
        self.wm_state('zoomed')
        
        # Create the welcome window
        self.create_welcome_window()
        
        # Create the other widgets
        self.create_widgets()
            
    def bring_children(self):
        for widget in self.winfo_children():
            widget.grid()
    
    def show_tooltip(self, event, a):
        global tooltip
        widget = event.widget
        if widget.cget("state") == "disabled":
            return
        
        if a == 1:
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)  # Hide window decorations
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")  # Position tooltip window
            tooltip_label = tk.Label(tooltip, text=" Enter date in format: 'yyyy-mm-dd' ", bg='cyan', fg='brown')
            tooltip_label.pack()
            tooltip.after(3000, tooltip.destroy)  # Hide tooltip after 3 seconds
    
        if a == 0:
            tooltip.destroy()
    
    def create_welcome_window(self):
        welcome = tk.Toplevel()
        welcome.overrideredirect(True)
        
        #get screen height and width
        sc_height = self.winfo_screenheight()
        sc_width = self.winfo_screenwidth()
        
        welcome.geometry("1000x550+{}+{}".format(((sc_width-1000)//2), ((sc_height-550)//2)))
        welcome.wm_attributes("-alpha", 0.3)
        
        img = Image.open("mod.png")
        wpercent = (200/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        welcome_img = img.resize((1000,550), Image.LANCZOS)
        
        self.welcome_img = ImageTk.PhotoImage(welcome_img)

        #func to implement optical intruigs with opacity
        def banner():
            x = 0.4
            
            def call(x):
                welcome.wm_attributes("-alpha", x)

            while True:
                welcome.after(200, call(x))
                x += 0.1
                
                if x >= 0.9:
                    welcome.after(1500, welcome.destroy)
                    
                    for var in (welcome, sc_height, sc_width, img, wpercent, hsize, welcome_img, self.welcome_img):
                        del var
                        
                    break
                
        welcome.after(200, banner)
        show_well = tk.Label(welcome, image=self.welcome_img)
        show_well.grid(row=0, column=0)
        
    def create_widgets(self):
        
        icon = ImageTk.PhotoImage(file="CHEBBY ENERGY.png")
        self.user = tk.PhotoImage(file='user.png')
                
        name, pass_w, confirm = tk.StringVar(), tk.StringVar(), tk.StringVar()
        serial, equip, quant = tk.IntVar(), tk.StringVar(), tk.IntVar()
        power, dec_var, runtime = tk.IntVar(), tk.StringVar(), tk.IntVar()
        date, capan, bat_vol = tk.StringVar(), tk.IntVar(), tk.IntVar()
        amp_hrs, back_var, isv_vare = tk.IntVar(), tk.IntVar(), tk.IntVar()
                
        liste = [serial, quant, power, dec_var, runtime, capan, bat_vol, amp_hrs, isv_vare]
        for var in liste:
            var.set('')
        
        #declare mysql statements
        keep = """INSERT INTO login 
                    VALUES (default, %s, %s)
                """
                    
        check_pass = """ SELECT user_id FROM login
                        where user_name = %s AND user_pass = %s 
                    """
        
        check_present = """ SELECT user_id, user_name FROM login
                        where user_name = %s
                    """
                    
        show_proj = """ SELECT serial_no, project_name, date_of_audit, date_completed  From projects
                        where project_id = %s
                    """
        
        add_proj = """ INSERT into projects
                       Values (%s, %s, %s, %s, %s)
                   """
        
        get_last_serial = """ SELECT serial_no from projects 
                              where project_id = %s
                          """
                        
        create_sum_tab = """ CREATE TABLE {table_name} (
                                serial_no INT,
                                equipment VARCHAR(100) DEFAULT NULL,
                                quantity INT DEFAULT 0,
                                power INT DEFAULT 0,
                                total_power INT DEFAULT 0,
                                run_time INT DEFAULT 0,
                                power_hour INT DEFAULT 0
                            ) """
        
        open_proj = """ SELECT * from {table_name}                    
                    """
                    
        add_row = """ INSERT INTO {table_name}
                      VALUES (%s, %s, %s, %s, %s, %s, %s)
                  """
                  
        row_serial = """ SELECT serial_no from {table_name}
                         UNION all
                         select max(serial_no) from {table_name}
                     """
        
        del_repl = """  DELETE FROM {table_name} 
                   """
        upd_date_comp = """ UPDATE projects SET date_completed = %s
                            where project_id = %s and serial_no = %s
                        """
                                
        del_proj = """ DELETE FROM projects WHERE serial_no = %s and project_id = %s
                  """
        
        upd_row = """ REPLACE INTO {table_name} VALUES (%s, %s, %s, %s, %s, %s, %s)
                  """
        
        del_sum = """ DROP TABLE {table_name}
                   """
                   
        del_row = """ DELETE FROM {table_name} where serial_no = %s
                  """
        
        #save user data & count for limit
        global count
        count = 0
        
        def reset(window):
            self.attributes("-disabled", False)
            self.focus_force()
            forms = [name, pass_w, confirm, serial, equip, quant, power, runtime, var, date]
            for item in forms:
                item.set('')
            window.destroy()
         
        def recover():
            messagebox.showinfo("COMING SOON!!!", 'This feature is not yet available.\nTry again soon!!')
         
        def save_data():
            if count == 3:
                messagebox.showwarning('Creation Limit reached', 'You have reached your limit on user creation for this session!!!')            
            else:
                
                new_user = tk.Toplevel()
                new_user.title("Create User")
                new_user.iconphoto(False, icon)
                new_user.resizable(0, 0)
                new_user.protocol("WM_DELETE_WINDOW", lambda: reset(new_user))
                new_user.geometry('500x300')
                                
                self.attributes("-disabled", True)
                
                create_user_label = tk.Label(new_user, text="Username: ", font=('Times New Roman', 15, ) )
                create_pass_label = tk.Label(new_user, text="Password: ", font=('Times New Roman', 15, ), )
                create_confirm_label = tk.Label(new_user, text="Confirm Password: ", font=('Times New Roman', 15, ) )
                
                create_user_ent = tk.Entry(new_user, textvariable=name, fg='brown', font=('Times New Roman', 15, ) )
                create_user_ent.focus_force()
                create_pass_ent = tk.Entry(new_user, textvariable=pass_w, show='*', font=('Times New Roman', 15, ) )
                create_conf_ent = tk.Entry(new_user, textvariable=confirm, show='*', font=('Times New Roman', 15, ) )
                
                create_user_label.grid(row=0, column=0, sticky='w', pady=(10, 0) )
                create_pass_label.grid(row=1, column=0, sticky='w', pady=(20, 0) )
                create_confirm_label.grid(row=2, column=0, sticky='w', pady=(20, 0) )
                
                create_user_ent.grid(row=0, column = 1, pady=(10, 0) )
                create_pass_ent.grid(row=1, column=1, pady=(20, 0))
                create_conf_ent.grid(row=2, column=1, pady=(20, 0))
                
                submit_cred_btn = ttk_but(new_user, text="Submit", command= lambda:submit_cred_create(new_user))
                submit_cred_btn.grid(row=3, column=2)
                
        def submit_cred_create(new_user):
                       
            #specify that count is global once more
            global count 
            
            name_val = name.get()
            pass_val = pass_w.get()#hash or encrypt first before saving
            conf_val = confirm.get()
            
            if conf_val != pass_val:
                messagebox.showerror('Try Again', "Passwords don't match")

            elif len(name_val) < 3 or all(char == ' ' for char in name_val):
                messagebox.showerror('Invalid Name', "User name must be at least 3 \ncharacters long and must contain characters!!")
            
            else:                           
                with query.connect(
                host = hostname,
                user = username,
                password = password,
                database = database
            
                ) as db:
                    
                    char = (name_val, pass_val)
                
                    curs = db.cursor()
                    
                    curs.execute(check_present, char[0])
                    
                    exist = curs.fetchall()
                    
                    if not exist:
                        curs.execute(keep, char)
                        db.commit()
                        curs.close()
                        
                        messagebox.showinfo("Completed!", 'Credentials have been stored successfully!!!')
                        login_proj(new_user, name_val, pass_val)
                        
                    else:
                        messagebox.showwarning("Existing Username!", 'Username already exists\nPlease select another username!')
                        curs.close()

                    reset(new_user)
                    count += 1

        def sign_in():
            
            login_wind = tk.Toplevel()
            login_wind.title("Sign In")
            login_wind.iconphoto(False, icon)
            
            login_wind.geometry('500x300')
            login_wind.resizable(0, 0)
            login_wind.protocol("WM_DELETE_WINDOW", lambda: reset(login_wind))
            
            self.attributes("-disabled", True)
            
            login_user_label = tk.Label(login_wind, text="Username: ", font=('Times New Roman', 15, ))
            login_pass_label = tk.Label(login_wind, text="Password: ", font=('Times New Roman', 15, ))
            
            login_user_ent = tk.Entry(login_wind, textvariable=name, fg='brown', font=('Times New Roman', 15, ))
            login_user_ent.focus_force()
            login_pass_ent = tk.Entry(login_wind, textvariable=pass_w, show='*', font=('Times New Roman', 15, ) )
            
            login_user_label.grid(row=0, column=0, pady=(10, 50))
            login_pass_label.grid(row=1, column=0)
            
            login_user_ent.grid(row=0, column = 1, pady=(10, 50))
            login_pass_ent.grid(row=1, column=1)
            
            submit_login_btn = ttk_but(login_wind, text="Submit", command = lambda win=login_wind: login_proj(win, name.get(), pass_w.get() ) )
            submit_login_btn.grid(row=3, column=2, pady=(40, 0) )
                
        def login_proj(login_wind, name_val, pass_val):
            
            if login_wind.winfo_exists():
                reset(login_wind)
            
            destroy_children()
            with query.connect(
                host = hostname,
                user = username,
                password = password,
                database = database
            
                ) as db:

                    values = (name_val, pass_val)
                    curs = db.cursor()
                    curs.execute(check_pass, values)
                    
                    get_output = curs.fetchall()
                    
                    if not get_output:
                        messagebox.showwarning("INCORRECT CREDENTIALS", "Username or Password is incorrect!")
                    else:
                        
                        ident = (get_output[0][0])
                        
                        curs.execute(show_proj, ident)
                        projects = curs.fetchall()
                        curs.close()
                        
                        new = [var for var in projects]
                        oth = [var for tup in projects for var in tup]
                        headers = ['S/N', 'Project Name', 'Date of Audit', 'Date of Completion']
                        
                        clear_children()
                        
                        frame_pro = tk.Frame(self, )
                        frame_pro.pack(side='left', fill='both', expand=True)
                        
                        canv_pro = tk.Canvas(frame_pro, )
                        canv_pro.pack(side='top', fill='both', expand=True)
                        
                        #scrollabars
                        proj_scroll_horiz = tk.Scrollbar(frame_pro, orient='horizontal', command=canv_pro.xview)
                        proj_scroll_horiz.pack(side='bottom', fill='x')
                                                
                        proj_scroll_vert = tk.Scrollbar(self, orient='vertical', command=canv_pro.yview)
                        proj_scroll_vert.pack(side='right', fill='y')
                        
                        #configure scrollbars for canvas
                        canv_pro.config(xscrollcommand=proj_scroll_horiz.set,
                                         yscrollcommand=proj_scroll_vert.set,
                                        )
                        proj_frame = tk.Frame(canv_pro, )
                        canv_pro.create_window((0,0), window = proj_frame, anchor = 'nw')
                        
                        def upd_scroll_proj(event):
                            if canv_pro.winfo_exists():
                                canv_pro.configure(scrollregion=canv_pro.bbox('all'))
                        
                        proj_frame.bind("<Configure>", upd_scroll_proj)
                    
                        for i, var in enumerate(headers):
                            label = tk.Label(proj_frame, text = var, font=('Times New Roman', 18, 'bold') )
                            label.grid(row = 0, column = i, ipadx=50, pady= (0, 20), )
                            
                        i, j, h = 1, 0, 0
                        for count, var in enumerate(oth):
                            
                            if count % 4 == 0 and count > 0:
                                nom = oth[1+(4*h)]
                                open_button = ttk_but(proj_frame, text = 'OPEN', command = lambda user=ident, 
                                                      ind=i , nom=nom, user_n = name_val, pass_n = pass_val: 
                                                      open_project(user, ind, nom, user_n, pass_n) )
                                
                                open_button.grid(row = i, column = j, pady = (0, 20), )
                                
                                del_proj_btn = ttk_but(proj_frame, text = 'DELETE',
                                                   command = lambda wind = frame_pro, 
                                                   user = name_val, pass_n = pass_val, 
                                                   ser = i, pro = user: del_proj_func(wind, user, pass_n, ser, pro) )
                                
                                i += 1
                                j = 0
                                h += 1
                                
                            label = tk.Label(proj_frame, text = var, font=('Times New Roman', 18, 'bold') )                            
                            label.grid(row = i, column = j, pady = (0, 25), )
                            j += 1
                        
                        if oth:
                            nom = oth[1+(4*h)]
                            open_button = ttk_but(proj_frame, text = 'OPEN', command = lambda user=ident, ind=i, nom=nom, 
                                                  user_n = name_val, pass_n = pass_val: open_project(user, ind, nom, user_n, pass_n) )
                            
                            open_button.grid(row = i, column = j, pady = (0, 20), )
                            
                            del_proj_btn = ttk_but(proj_frame, text = 'DELETE',
                                                   command = lambda wind = frame_pro, 
                                                   user = name_val, pass_n = pass_val, 
                                                   ser = i, pro = ident: del_proj_func(wind, user, pass_n, ser, pro) )
                            
                            del_proj_btn.grid(row = i, column = j+1, pady = (0, 20), padx = (45, 0) )
                    
                        create_new_proj_btn = ttk_but(proj_frame, text = 'NEW', command = lambda ident=ident: create_new_proj(ident, name_val, pass_val) )
                        create_new_proj_btn.grid(row = i+1, column=j, padx = (150, 0), pady = (40, 0))

                        sign_out_btn = ttk_but(proj_frame, text = 'SIGN OUT', command = lambda: (destroy_children(), self.bring_children()) )
                        sign_out_btn.grid(row = i+1, column = j+1, padx=(50, 0), pady = (40, 0))
                        
        def create_new_proj(ident, nom, passe):
            
            create_proj_wind = tk.Toplevel()
            create_proj_wind.wm_resizable(0,0)
            create_proj_wind.title("New Project")
            
            create_proj_wind.geometry('500x300')
            create_proj_wind.iconphoto(False, icon)
            create_proj_wind.protocol("WM_DELETE_WINDOW", lambda: reset(create_proj_wind))
            self.attributes('-disabled', True)
            
            create_proj_name_label = tk.Label(create_proj_wind, text='Project Name:', font=('Times New Roman', 15, ))
            create_proj_audit_label = tk.Label(create_proj_wind, text='Date of Audit:', font=('Times New Roman', 15, ))
            create_proj_complete_lab = tk.Label(create_proj_wind, text='Date Completed(optional): ', font=('Times New Roman', 15, ))
            create_proj_name_ent = tk.Entry(create_proj_wind, textvariable=name, font=('Times New Roman', 15, ))
            
            create_proj_audit_ent = tk.Entry(create_proj_wind, textvariable=pass_w, font=('Times New Roman', 15, ))
            create_proj_complete_ent = tk.Entry(create_proj_wind, textvariable=confirm, font=('Times New Roman', 15, ))
            
            create_proj_audit_ent.bind("<Enter>", lambda event: self.show_tooltip(event, 1))
            create_proj_audit_ent.bind("<Leave>", lambda event: self.show_tooltip(event, 0))
            
            create_proj_complete_ent.bind("<Enter>", lambda event: self.show_tooltip(event, 1))
            create_proj_complete_ent.bind("<Leave>", lambda event: self.show_tooltip(event, 0))
            create_new_proj_sub = ttk_but(create_proj_wind, text = 'SUBMIT', command = lambda ident=ident: submit_new_proj(ident, nom, passe,create_proj_wind))

            create_proj_name_label.grid(row = 0, column = 0, sticky='w', pady=(10, 0))
            create_proj_audit_label.grid(row = 1, column = 0, sticky='w', pady=(20, 0))
            create_proj_complete_lab.grid(row = 2, column = 0, sticky='w', pady=(20, 0))
            
            create_proj_name_ent.grid(row = 0, column = 1, pady=(10, 0))
            create_proj_audit_ent.grid(row = 1, column = 1, pady=(20, 0))
            create_proj_complete_ent.grid(row = 2, column = 1, pady=(20, 0))
            create_new_proj_sub.grid(row = 3, column = 1, pady=(30, 0))
           
        def submit_new_proj(ident, nom, passe, window):
            try:
                proj_name = name.get()
                proj_aud = pass_w.get()
                proj_comple = confirm.get()
                
                if not proj_comple:
                    proj_comple = None
                
                if len(proj_name) > 15:
                    proj_name = proj_name[:12] + '\n' + proj_name[12:]
                
                try:
                    with query.connect(
                        host = hostname,
                        user = username,
                        password = password,
                        database = database
                    
                        ) as db:

                            val = (ident)
                            curs = db.cursor()
                            curs.execute(get_last_serial, val)
                            
                            last = curs.fetchall()
                            
                            if not last:
                                new_val = 1
                            
                            else:
                                new_val = int(last[-1][0]) + 1
                                
                            val = (proj_name, proj_aud, proj_comple, ident, new_val)
                            
                            curs.execute(add_proj, val)
                            db.commit()
                            
                            concat = 'sum_{0}_{1}'.format(ident, new_val)
                            table = create_sum_tab.format(table_name = concat)
                            
                            curs.execute(table)
                            db.commit()
                            
                            curs.close()
                            messagebox.showinfo('Done', 'A New Project has been created!')
                            login_proj(window, nom, passe)
                    
                except query.Error as r:
                    messagebox.showerror('Error', 'The following error was encountered while saving details:\n{}'.format(r))
                    reset(window)
            
            except Exception as r:
                messagebox.showerror('Too many characters', '{}'.format(r))
                reset(window)
            
        def del_proj_func(wind, user, pass_n, ser_no, pro_id):
            try:

                val = (ser_no, pro_id)
                nom = 'sum_{}_{}'.format(pro_id, ser_no)
                del_sum_new = del_sum.format(table_name = nom)
                
                with query.connect(
                host = hostname,
                user = username,
                password = password,
                database = database
                ) as db:
                    
                    curs = db.cursor()
                    curs.execute(del_proj, val)
                    db.commit()
                    
                    curs.execute(del_sum_new)
                    db.commit()
                    curs.close()
                
                login_proj(wind, user, pass_n)
                
            except query.Error as e:
                messagebox.showerror('The following error occurred: \n' '{}'.format(e) )
        
        def del_row_func(pro, ser_tab, ser_item, proj_name, user_n, pass_n):
            try:
                
                nom = 'sum_{}_{}'.format(pro, ser_tab)
                del_row_new = del_row.format(table_name = nom)
                
                with query.connect(
                    host = hostname,
                    user = username,
                    password = password,
                    database = database
                ) as db:
                    
                    curs = db.cursor()
                    curs.execute(del_row_new, ser_item)
                    db.commit()
                    
                    curs.close()
                
                open_project(pro, ser_tab, proj_name, user_n, pass_n)
            
            except query.Error as f:
                messagebox.showerror('The following error occurred: \n' '{}'.format(f) )
            
            
        def show_pres_row(cont_frame, row, col, var, state = 0 ):
            if state == 0:
                entry_var = tk.IntVar()
                entry_var.set(var)
            
            else:
                entry_var = tk.StringVar()
                entry_var.set(var)
            
            key = f'pos_{row}_{col}'
            entry_dict[key] = entry_var
            
            entry = tk.Entry(cont_frame, textvariable = entry_var, font=('comic sans ms', 10, 'bold'))
            entry.grid(row = row, column = col, pady = (0, 10), )
            
        def add_new_row(user, ind, nom, user_n, pass_n ):

            try:
                runtime_g = 13
                quant_g, power_g = 0, 0
                
                equip_g = ''
                                                        
                total_pow = power_g * quant_g
                pow_hr = total_pow * runtime_g
                    
                try:
                    with query.connect(
                        host = hostname,
                        user = username,
                        password = password,
                        database = database
                    
                        ) as db:
                            curs = db.cursor() 
                                    
                            tab = 'sum_{0}_{1}'.format(user, ind)
                            restrict_ser = row_serial.format(table_name = tab)
                            curs.execute(restrict_ser)
                            
                            get_out = curs.fetchall()
                            new = [var for cont in get_out for var in cont]
                            
                            if new[-1] is not None: serial_g = new[-1] + 1
                            else: serial_g = 1
                            
                            
                            val = (serial_g, equip_g, quant_g, power_g, total_pow, runtime_g, pow_hr) #runtime_g for standard
                            adj_add = add_row.format(table_name = tab)
                            curs.execute(adj_add, val)

                            db.commit()                    
                            curs.close()
                            
                            open_project(user, ind, nom, user_n, pass_n)
            
                except ValueError as v:
                    messagebox.showerror('Error', 'The following error was encountered while saving details:\n{}'.format(v))
                            
                except query.Error as r:
                    messagebox.showerror('Error', 'The following error was encountered while saving details:\n{}'.format(r))
            
            except Exception as e:
                messagebox.showerror('Error', 'The following error occurred:\n{}'.format(e))
            
        def sub_new_row(user, ind, nom, user_n, pass_n):
            
            try:
                entries_list = [var.get() for var in entry_dict.values()]
                size = len(entries_list)
                new_tup = []
                ite = 7
                for i in range(0, size, 7):
                    new_tup.append( list(entries_list[i:ite]) )
                    ite += 7

                for i, var in enumerate(new_tup):
                    new_tup[i][4] = new_tup[i][3] * new_tup[i][2]
                    new_tup[i][6] = new_tup[i][5] * new_tup[i][4]
                                
                upd_row_new = upd_row.format(table_name = f'sum_{user}_{ind}')
                del_repl_new = del_repl.format(table_name = f'sum_{user}_{ind}')
                
                try:
                    with query.connect(
                        host = hostname,
                        user = username,
                        password = password,
                        database = database
                    
                        ) as db:
                            curs = db.cursor()
                            
                            curs.execute(del_repl_new)
                            db.commit()                            
                            curs.executemany(upd_row_new, new_tup)
                            
                            db.commit()                    
                            curs.close()
                            
                            open_project(user, ind, nom, user_n, pass_n)
                    
                except ValueError as v:
                    messagebox.showerror('Error', f'The following error was encountered while saving details:\n{v}')
                            
                except query.Error as r:
                    messagebox.showerror('Error', f'The following error was encountered while saving details:\n{r}')
            
            except tk.TclError as t:
                messagebox.showerror('Error', f'The following value is invalid in its position { str(t).split()[-1] }')
            
            except Exception as e:
                messagebox.showerror('Error', f'The following error occurred:\n{e}')
        
        def calib(sumey, a,b,c,d,e,f,g):
            try:
                if isv_vare.get() % 12 != 0 or isv_vare.get() < 12:
                    raise Exception('Invalid Value fo ISV')
                
                Ans = ceil(sumey/capan.get()) + 4
                Inv_cap = (sumey*1.2)/0.8
                TWA = Ans * capan.get()
                no_batt = (back_var.get() * sumey) / (bat_vol.get() * amp_hrs.get() * 0.8)
                                                    
                a.config(text=('No. of panels   =   {}'.format(Ans) ) )
                b.config(text=('Inverter Capacity(KW)   =   {}'.format( round(Inv_cap/1000, 3) ) ) )
                c.config(text=('Inverter Capacity(KVA)   =   {}'.format( round( (Inv_cap/0.8 )/1000, 3)) ) )
                d.config(text=('Total Wattage of Array(W)   =   {}'.format( round(TWA, 3) ) ) )
                e.config(text=('Total Load that works overnight   =   {}'.format(sumey) ) )
                f.config(text=('No. of Batteries   =   {}'.format(round(no_batt, 3)) ) )
                g.config(text=('Charge Controller Output(amps)   =   {}'.format( round(TWA/no_batt + 20, 3) ) ) ) 
            
            except tk.TclError:
                messagebox.showerror("Error", 'Invalid values were passed as input!!')
            
            except Exception as g:
                messagebox.showerror('Error', f'{g}')
            
        def open_project(user, ind, proj_name, user_n, pass_n):
            destroy_children()
                        
            try:
                with query.connect(
                    host = hostname,
                    user = username,
                    password = password,
                    database = database
                
                    ) as db:
                        curs = db.cursor()
                        
                        table = 'sum_{0}_{1}'.format(user, ind)
                        val = open_proj.format(table_name = table)
                        curs.execute(val)
                        
                        shown = curs.fetchall()
                        results = [var for tup in shown for var in tup]
                        
                        headings = ['Serial No.', 'Equipment', 'Quantity', 'Power', 'Total Power', 'Run Time', 'Power Hour']
                        list_of_tp = []
                        list_of_ph = []
                        
                        show_res = tk.Frame(self, )
                        show_res.pack(side='left', fill='both', expand=True)
                        
                        show_canv = tk.Canvas(show_res)
                        show_canv.pack(side='top', fill='both', expand=True)
                        
                        #scrollabars
                        show_scroll_horiz = tk.Scrollbar(show_res, orient='horizontal', command=show_canv.xview)
                        show_scroll_horiz.pack(side='bottom', fill='x')
                                                
                        show_scroll_vert = tk.Scrollbar(self, orient='vertical', command=show_canv.yview)
                        show_scroll_vert.pack(side='right', fill='y')
                        #configure scrollbars for canvas
                        show_canv.config(xscrollcommand=show_scroll_horiz.set,
                                         yscrollcommand=show_scroll_vert.set,
                                        )
                        
                        cont_frame = tk.Frame(show_canv, )
                        show_canv.create_window((0,0), window = cont_frame, anchor = 'nw')
                        
                        def change_show(event):
                            if show_canv.winfo_exists():
                                show_canv.configure(scrollregion=show_canv.bbox('all'))
                        
                        cont_frame.bind("<Configure>", change_show)

                        tk.Label(cont_frame, text = proj_name, font=('Times New Roman', 20, 'bold'), fg='gray').grid(row = 0, column = 0, columnspan = 4, padx=(50,0) ,sticky='e')
                        
                        for i, var in enumerate(headings):
                            label = tk.Label(cont_frame, text = var, font=('comic sans ms', 15, 'bold'))
                            label.grid(row = 1, column = i, ipadx=45, pady= (0, 10), )
                            
                        i, j, ite = 2, 0, 0
                        
                        for count, var in enumerate(results):
                            if count % 7 == 0 and count > 0:
                                save_button = ttk_but(cont_frame, text = 'SAVE', command = lambda user=user, ind=ind, nom=proj_name, 
                                                      ser=results[0+(7*(i-2))], user_n = user_n, 
                                                      pas = pass_n: sub_new_row( user, ind, nom, user_n, pas) )
                                
                                save_button.grid(row = i, column = j, pady = (0, 20), )
                                
                                del_work_btn = ttk_but(cont_frame, text = 'DELETE', command = lambda pro = user, 
                                                       ser_item = results[0+(7*(i-2))], ser_tab = ind, pro_name = proj_name, 
                                                       use_name = user_n, pass_name = pass_n: del_row_func(pro, ser_tab, ser_item,
                                                                                                           pro_name, use_name, pass_name) )
                                
                                del_work_btn.grid(row = i, column = j+1, pady = (0, 20), padx = (25, 20) )
                                                                      
                                list_of_tp.append(results[4+(7*(i-2))])
                                list_of_ph.append(results[6+(7*(i-2))])
                                i += 1
                                j = 0
                            
                            if j == 1:
                                show_pres_row(cont_frame, i, j, var, 1)
                                j += 1
                                continue
                            
                            if j == 4:
                                label = tk.Label(cont_frame, text = var, font=('comic sans ms', 10, 'bold'))
                                label.grid(row = i, column = j, pady = (0, 10), )
                                
                                key = f'pos_{i}_{j}'
                                entry_var = tk.IntVar()
                                entry_var.set(var)
                                
                                entry_dict[key] = entry_var
                                j += 1
                                continue
                            
                            elif j == 5:
                                label = tk.Label(cont_frame, text = var, font=('comic sans ms', 10, 'bold'))
                                label.grid(row = i, column = j, pady = (0, 10), )
                                                                
                                key = f'pos_{i}_{j}'
                                entry_var = tk.IntVar()
                                entry_var.set(var)
                                
                                entry_dict[key] = entry_var
                                j += 1
                                continue
                                
                            elif j == 6:
                                label = tk.Label(cont_frame, text = var, font=('comic sans ms', 10, 'bold'))
                                label.grid(row = i, column = j, pady = (0, 10), )
                                j += 1
                                                                
                                key = f'pos_{i}_{j}'
                                entry_var = tk.IntVar()
                                entry_var.set(var)
                                
                                entry_dict[key] = entry_var
                                j += 1
                                continue
                                
                            show_pres_row(cont_frame, i, j, var )
                            j += 1
                        
                        if results:
                            list_of_tp.append(results[4+(7*(i-2))])
                            list_of_ph.append(results[6+(7*(i-2))])
                            
                            sum_tp = sum(list_of_tp)
                            sum_ph = sum(list_of_ph)
                            
                            save_button = ttk_but(cont_frame, text = 'SAVE', command = lambda user=user, ind = ind, 
                                                  nom=proj_name, ser=results[0+(7*(i-2))], user_n = user_n, pas = pass_n: 
                                                  sub_new_row( user, ind, nom, user_n, pas) )
                            
                            save_button.grid(row = i, column = j, pady = (0, 20), )
                            
                            del_work_btn = ttk_but(cont_frame, text = 'DELETE', command = lambda pro = user, ser_item = results[0+(7*(i-2))], ser_tab = ind,
                                                   pro_name = proj_name, use_name = user_n, pass_name = pass_n: del_row_func(pro, ser_tab, 
                                                   ser_item, pro_name, use_name, pass_name) )
                            
                            del_work_btn.grid(row = i, column = j+1, pady = (0, 20), padx = (25, 20) )
                            
                            tk.Label(cont_frame, text='Total Load Required:', font=('Times New Roman', 25, 'bold')).grid(row = i+1, column=0, columnspan=4, sticky='e')
                            tk.Label(cont_frame, text=(sum_tp), font=('Times New Roman', 25, 'bold') ).grid(row = i+1, column = 4, )
                            tk.Label(cont_frame, text=(sum_ph), font=('Times New Roman', 25, 'bold') ).grid(row = i+1, column = 6, sticky='e', padx=(0, 80) )

                        else: 
                            sum_tp = 0
                            sum_ph = 0
                        
                        back_var.set(13)
                        
                        add_row_btn = ttk_but(cont_frame, text = 'ADD ROW', command = lambda user=user, 
                                              ind=ind, nom=proj_name, user_n = user_n, 
                                              pas = pass_n: add_new_row(user, ind, nom, user_n, pas) )
                        
                        add_row_btn.grid(row = i+1, column=j, pady = (40, 0))
                        
                        cap_lab = tk.Label(cont_frame, text="Capacity of Panels:  ", fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        cap_lab.grid(row=i+2, column=0, pady=(50, 0), sticky='e')
                        
                        cap_ent = tk.Entry(cont_frame, textvariable=capan, font=('Times New Roman', 16, 'bold'))
                        cap_ent.grid(row=i+2, column = 1, pady=(50, 0), sticky='w', ipadx=6)
                                                
                        no_pan_lab = tk.Label(cont_frame, text='No. of panels   =   0', fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        no_pan_lab.grid(row=i+2, column=3, columnspan=2, pady=(50, 0), sticky='w')
                        
                        cco_lab = tk.Label(cont_frame, text='Charge Controller Output (amps)   =   0', fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        cco_lab.grid(row=i+2, column=5, columnspan=4, pady=(50, 0), sticky='w')
                        
                        inc_wat_lab = tk.Label(cont_frame, text='Inverter Capacity(KW)   =   0', fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        inc_wat_lab.grid(row=i+3, column=0, columnspan=2, pady=(50, 0), sticky='w')
                        
                        inc_kva_lab = tk.Label(cont_frame, text='Inverter Capacity(KVA)   =   0', fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        inc_kva_lab.grid(row=i+3, column=3, columnspan=2, pady=(50, 0), sticky='w')
                        
                        tot_wat_lab = tk.Label(cont_frame, text='Total Wattage of Array(TWA)   =   0', fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        tot_wat_lab.grid(row=i+3, column=5, columnspan=2, pady=(50, 0), sticky='e')
                                                
                        bat_vol_lab = tk.Label(cont_frame, text='Battery Voltage:', fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        bat_vol_lab.grid(row=i+4, column=0, columnspan=1, pady=(50, 0), sticky='w')
                        
                        bat_vol_ent = tk.Entry(cont_frame, textvariable=bat_vol, font=('Times New Roman', 16, 'bold'))
                        bat_vol_ent.grid(row=i+4, column = 0, columnspan=2, pady=(50, 0), sticky='e', ipadx=6)
                        
                        tot_load_lab = tk.Label(cont_frame, text='Total Load that works overnight   =   0', fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        tot_load_lab.grid(row=i+4, column=3, columnspan=2, pady=(50, 0), sticky='w')
                        
                        calc_lab = tk.Label(cont_frame, text=('Backup Time   =   {}'.format(back_var.get())), fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        calc_lab.grid(row=i+4, column=6, columnspan=2, pady=(50, 0), sticky='w')
                        
                        amp_hr_lab = tk.Label(cont_frame, text='Amp Hours:', fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        amp_hr_lab.grid(row=i+5, column=0, columnspan=1, pady=(50, 0), sticky='w')
                        
                        amp_hr_ent = tk.Entry(cont_frame, textvariable=amp_hrs, font=('Times New Roman', 16, 'bold'))
                        amp_hr_ent.grid(row=i+5, column = 1, pady=(50, 0), sticky='w', ipadx=6)
                        
                        no_bat_lab = tk.Label(cont_frame, text='No. of Batteries   =   0', fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        no_bat_lab.grid(row=i+5, column=3, columnspan=2, pady=(50, 0), sticky='w')
                                                
                        isv_lab = tk.Label(cont_frame, text='ISV (watts): ', fg = 'brown', font=('Times New Roman', 18, 'bold') )
                        isv_lab.grid(row=i+5, column=4, columnspan=2, pady=(50, 0), sticky='e')
                        
                        isv_ent = tk.Entry(cont_frame, textvariable=isv_vare, font=('Times New Roman', 16, 'bold'))
                        isv_ent.grid(row=i+5, column = 6, pady=(50, 0), sticky='w', )
                                                
                        recal_btn = tk.Button(cont_frame, text='Re-calibrate', font=('Times New Roman', 16, 'bold'), command=lambda a=no_pan_lab, 
                                              b=inc_wat_lab, c=inc_kva_lab, d=tot_wat_lab, sumey=sum_tp,
                                              e=tot_load_lab, f=no_bat_lab, g=cco_lab: calib(sumey, a, b, c, d, e, f, g))
                        
                        recal_btn.grid(row=i+6, column=0, columnspan=3, pady=(50, 70), )
                        
                        #creating menu bar
                        menu_bar = tk.Menu(self)
                        
                        #add file tab to menu bar
                        file_tab = tk.Menu(menu_bar, tearoff = 0)
                        menu_bar.add_cascade(label = 'File', menu = file_tab)
                        
                        file_tab.add_command(label ='Close Project', command = lambda log_wind = show_res, user = user_n, pas = pass_n : login_proj(log_wind, user, pas) )
                        file_tab.add_command(label ='Import From Excel File', command = recover)
                        file_tab.add_command(label ='Export To Excel File', command = recover)
                        file_tab.add_command(label ='Sign Out', command = lambda: (destroy_children(), self.bring_children()) )
                        file_tab.add_separator()
                        file_tab.add_command(label ='Exit', command = self.destroy)
                        
                        #add other tabs
                        edit_tab = tk.Menu(menu_bar, tearoff = 0)
                        menu_bar.add_cascade(label = 'Edit', menu = edit_tab)
                        
                        edit_tab.add_command(label ='Add Row', command = lambda user=user, ind=ind, nom=proj_name, user_n = user_n, 
                                             pas = pass_n: add_new_row(user, ind, nom, user_n, pas ) )
                        
                        edit_tab.add_command(label ='Re-calibrate', command = lambda a=no_pan_lab, 
                                                        b=inc_wat_lab, c=inc_kva_lab, d=tot_wat_lab, sumey=sum_tp,
                                                        e=tot_load_lab, f=no_bat_lab, g=cco_lab: calib(sumey, a, b, c, d, e, f, g) )
                        
                        edit_tab.add_command(label ='', command = None)
                        edit_tab.add_separator()
                        
                        help_tab = tk.Menu(menu_bar, tearoff = 0) 
                        menu_bar.add_cascade(label ='Help', menu = help_tab)
                        
                        help_tab.add_command(label ='Help', command = recover)
                        help_tab.add_command(label ='More Apps From Kryptech', command = recover)
                        help_tab.add_separator()
                        help_tab.add_command(label ='About Hybrid', command = recover)
                        
                        #display menu
                        self.config(menu = menu_bar)
                        
            except query.Error as r:
                messagebox.showerror('Error', 'The following error was encountered while getting details:\n{}'.format(r))
        
        #set focus to follow mouse
        self.tk_focusFollowsMouse()
        
        #login screen details
        sign_in_btn = ttk_but(self, text="Sign In", command=sign_in)
        sign_in_btn.grid(row = 0, column=0, padx=50, pady=50)
        
        create_user_btn = ttk_but(self, text="Create User", command=save_data)
        create_user_btn.grid(row=0, column=1, padx=50, pady=50)
        
        recover_pass_btn = ttk_but(self, text="Recover Password", command=recover)
        recover_pass_btn.grid(row=0, column=2, padx=50, pady=50) 
        
        entry_dict = {}    
        
        def clear_children():
            for widget in self.winfo_children():
                if widget in obj:
                    widget.grid_remove()
                    
        def destroy_children():
            for widget in self.winfo_children():
                if  widget not in obj:
                    widget.destroy()
        obj = self.winfo_children()
        
if __name__ == '__main__':
    app = Hybrid()
    app.mainloop()
