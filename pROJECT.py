import tkinter as tk
import mysql.connector as m
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def conn_db():
    try:
        return m.connect(host='localhost',user='root',passwd='kitarp007@',database='fusion_gym_2'
        )
    except m.Error as e:
        messagebox.showerror("Database Connection Error",e)
        exit()

# Initialize database connection
db = conn_db()
cur = db.cursor()

def exec_qry(qry, params=()):
    try:
        cur.execute(qry, params)
        db.commit()
    except m.Error as e:
        messagebox.showerror("Database Error",e)

def chk_id(id_val):
    qry = "select count(*) from members where id=%s"
    cur.execute(qry, (id_val,))
    return cur.fetchone()[0] > 0

def add_mem():
    def get_new_id():
        cur.execute("select max(id) from members")
        data = cur.fetchone()
        return (int(data[0]) or 0) + 1

    def save_mem():
        p = ent_ph.get()
        if len(p) != 10 or not p.isdigit():
            messagebox.showerror("Input Error", "Phone number must be exactly 10 digits")
            return
        
        try:
            qry = """insert into members 
                     (id, name, phone_no, address, membership, trainer_id, enrolling_date, subscription, amount_due, amount_paid, status)
                     values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            member_id = get_new_id()  # Automatically generate the new ID
            exec_qry(qry, (
                member_id, ent_nm.get(), int(p), ent_addr.get(),
                ent_mem.get(), int(ent_tid.get()), ent_ed.get(),
                ent_sub.get(), int(ent_amt.get()), int(ent_amtp.get()), ent_st.get()
            ))
            messagebox.showinfo("Success", f"Member added successfully with ID {member_id}")
            add_win.destroy()
        except m.Error as e:
            messagebox.showerror("Database Error:",e)

    add_win = tk.Toplevel()
    add_win.title("Add Member")
    add_win.configure(bg="AliceBlue")

    lbls = [
        "Name:", "Phone:", "Address:", "Membership\n(Bronze/Gold/Platinum):",
        "Trainer ID:", "Enrolling Date(YYYY/MM/DD):", "Subscription:", "Amount due:", "Amount Paid:", "Status:"
    ]
    ents = [tk.Entry(add_win) for _ in lbls]

    for i, (l, e) in enumerate(zip(lbls, ents)):
        tk.Label(add_win, text=l, bg="AliceBlue", fg='black', font=('Arial', 12)).grid(row=i, column=0, padx=10, pady=5)
        e.grid(row=i, column=1, padx=10, pady=5)

    ent_nm, ent_ph, ent_addr, ent_mem, ent_tid, ent_ed, ent_sub, ent_amt, ent_amtp, ent_st = ents
    tk.Button(add_win, text="Save Member", command=save_mem, bg="ForestGreen", fg="black",
              font=('Arial', 12, 'bold'), padx=20, pady=10, relief=tk.RAISED).grid(row=len(lbls), columnspan=2, pady=10)


#Function for Updation of records.
def upd_rec():
    def save_upd():
        id_upd = ent_id.get()
        if not chk_id(id_upd):
            messagebox.showerror("Error", "ID does not exist")
            return
        
        c = ent_col.get()
        if not c:
            messagebox.showerror("Input Error", "Column name cannot be empty")
            return
        
        try:
            qry = f"update members set {c}=%s where id=%s"
            exec_qry(qry, (ent_val.get(), id_upd))
            messagebox.showinfo("Success", "Record updated successfully")
            upd_win.destroy()
        except m.Error as e:
            messagebox.showerror("Database Error:",e)

    upd_win = tk.Toplevel()
    upd_win.title("Update Record")
    upd_win.configure(bg="AliceBlue")

    tk.Label(upd_win, text="ID to Update:", bg="AliceBlue",fg='black', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
    ent_id = tk.Entry(upd_win)
    ent_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(upd_win, text="Column to Update:", bg="AliceBlue",fg='black', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
    ent_col = tk.Entry(upd_win)
    ent_col.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(upd_win, text="New Value:", bg="AliceBlue",fg='black', font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5)
    ent_val = tk.Entry(upd_win)
    ent_val.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(upd_win, text="Save Update", command=save_upd, bg="ForestGreen", fg="black",
              font=('Arial', 12, 'bold'), padx=20, pady=10, relief=tk.RAISED).grid(row=3, columnspan=2, pady=10)

#Function for deletion of records.
def del_rec():
    def conf_del():
        id_del = ent_id.get()
        if not chk_id(id_del):
            messagebox.showerror("Error", "ID does not exist")
            return
        
        try:
            qry = "delete from members where id=%s"
            exec_qry(qry, (id_del,))
            messagebox.showinfo("Success", "Record deleted successfully")
            del_win.destroy()
        except m.Error as e:
            messagebox.showerror("Database Error:",e)

    del_win = tk.Toplevel()
    del_win.title("Delete Record")
    del_win.configure(bg="AliceBlue")

    tk.Label(del_win, text="ID to Delete:", bg="AliceBlue",fg='black', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
    ent_id = tk.Entry(del_win)
    ent_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(del_win, text="Delete", command=conf_del, bg="Red", fg="black",
              font=('Arial', 12, 'bold'), padx=20, pady=10, relief=tk.RAISED).grid(row=1, columnspan=2, pady=10)

#Function for adding trainers.
def add_trn():
    def get_new_tid():
        cur.execute("select max(id) from trainers")
        data = cur.fetchone()
        if data[0]==None:
            return 100 + 1
        else:
            return (int(data[0])) + 1

    def save_trn():
        p = ent_phn.get()
        if len(p) != 10 or not p.isdigit():
            messagebox.showerror("Input Error", "Phone number must be exactly 10 digits")
            return
        
        try:
            qry = "insert into trainers (id, name, phone_no, experience) values (%s, %s, %s, %s)"
            trainer_id = get_new_tid()
            exec_qry(qry, (trainer_id, ent_nm.get(), int(p), int(ent_exp.get())))
            messagebox.showinfo("Success", "Trainer added successfully")
            trn_win.destroy()
        except m.Error as e:
            messagebox.showerror("Database Error:",e)

    trn_win = tk.Toplevel()
    trn_win.title("Add Trainer")
    trn_win.configure(bg="AliceBlue")

    tk.Label(trn_win, text="Trainer Name:", bg="AliceBlue", fg='black', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
    ent_nm = tk.Entry(trn_win)
    ent_nm.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(trn_win, text="Phone no.:", bg="AliceBlue", fg='black', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
    ent_phn = tk.Entry(trn_win)
    ent_phn.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(trn_win, text="Experience (Years):", bg="AliceBlue", fg='black', font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5)
    ent_exp = tk.Entry(trn_win)
    ent_exp.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(trn_win, text="Save Trainer", command=save_trn, bg="ForestGreen", fg="black",
              font=('Arial', 12, 'bold'), padx=20, pady=10, relief=tk.RAISED).grid(row=4, columnspan=2, pady=10)

#Function for bill generation.
def bill_generate():
    def generate_bill():
        mem_id = ent_id.get().strip()
        
        if not mem_id:
            messagebox.showerror("Error", "Member ID cannot be empty")
            return
        
        # Query to get member details based on ID
        qry = "select name, membership, subscription, enrolling_date, amount_paid from members where id=%s"
        try:
            cur.execute(qry, (mem_id,))
            member = cur.fetchone()
        except Exception as e:
            messagebox.showerror("Database Error:",e)
            return
        
        if not member:
            messagebox.showerror("Error", "Member ID not found")
            return
        
        name, membership, subscription, enrolling_date, amount_paid = member
        rates = {
            'Bronze': 4500,
            'Gold': 8000,
            'Platinum': 15000
        }
        
        if membership not in rates:
            messagebox.showerror("Error", "Invalid membership type")
            return
        
        bill_amount = rates[membership]
        months = {
            'Yearly': 12,
            'Half-Yearly': 6,
            'Quarterly': 4
        }
        
        total_amount = bill_amount * months[subscription]

        amount_pending = total_amount - amount_paid

        # Create a new window to display the bill
        bill_win = tk.Toplevel()
        bill_win.title("Generate Bill")
        bill_win.geometry("350x310")
        bill_win.configure(bg="AliceBlue")
        
        tk.Label(bill_win, text="Member Bill", font=('Arial', 16, 'bold'), bg="AliceBlue", fg="DarkGreen").pack(pady=10)
        tk.Label(bill_win, text=f"Name: {name}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(bill_win, text=f"Membership: {membership}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(bill_win, text=f"Subscription : {subscription}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(bill_win, text=f"Date: {enrolling_date}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(bill_win, text=f"Amount Due: Rs {bill_amount} Monthly", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(bill_win, text=f"Total Amount for Subscription: Rs {total_amount}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(bill_win, text=f"Amount Paid: Rs {amount_paid}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(bill_win, text=f"Amount pending: Rs {amount_pending}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)

    # Create the main window for bill generation
    bill_win = tk.Toplevel()
    bill_win.title("Bill Generation")
    bill_win.configure(bg="AliceBlue")

    tk.Label(bill_win, text="Enter Member ID:", bg="AliceBlue", fg="black", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
    ent_id = tk.Entry(bill_win)
    ent_id.grid(row=0, column=1, padx=10, pady=5, sticky='w')

    tk.Button(bill_win, text="Generate Bill", command=generate_bill, bg="ForestGreen", fg="black",
              font=('Arial', 12, 'bold'), padx=20, pady=10, relief=tk.RAISED).grid(row=1, columnspan=2, pady=10)


#Function for stats.
def show_stats():
    try:
        # Query for membership types and their counts
        qry_membership = "select membership, count(*) from members group by membership"
        cur.execute(qry_membership)
        membership_data = cur.fetchall()

        if not membership_data:
            messagebox.showinfo("No Data", "No membership data available.")
            return
        
        memberships = [row[0] for row in membership_data]
        membership_counts = [row[1] for row in membership_data]

        # Query for active and inactive members
        qry_status = "select status, count(*) from members group by status"
        cur.execute(qry_status)
        status_data = cur.fetchall()

        statuses = [row[0] for row in status_data]
        status_counts = [row[1] for row in status_data]

        # Query for number of members per year
        qry_years = "select year(enrolling_date) as year, count(*) from members group by year(enrolling_date)"
        cur.execute(qry_years)
        year_data = cur.fetchall()

        years = [row[0] for row in year_data]
        year_counts = [row[1] for row in year_data]

        # Create a new window for stats
        stats_win = tk.Toplevel()
        stats_win.title("Membership Statistics")
        stats_win.geometry("800x600")
        stats_win.configure(bg="AliceBlue")

        tk.Label(stats_win, text="Graphs of Various Fields", font=('Arial', 20, 'bold'), bg='AliceBlue', fg="DarkGreen").pack(pady=10)
        
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        
        # Plot for different memberships
        axs[0, 0].pie(membership_counts, labels=memberships, autopct='%1.1f%%', startangle=90)
        axs[0, 0].axis('equal')
        axs[0, 0].set_title('Membership Distribution')
        
        # Plot for active/inactive members
        axs[0, 1].bar(statuses, status_counts, color=['blue', 'yellow'])
        axs[0, 1].set_title('Active/Inactive Members')
        axs[0, 1].set_xlabel('Status')
        axs[0, 1].set_ylabel('Number of Members')
        
        # Plot for number of members per year
        axs[1, 0].bar(years, year_counts, color='pink')
        axs[1, 0].set_title('Members by Year')
        axs[1, 0].set_xlabel('Year')
        axs[1, 0].set_ylabel('Number of Members')
        
        # Hide the fourth subplot
        axs[1, 1].axis('off')
        
        canvas = FigureCanvasTkAgg(fig, master=stats_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    except m.Error as e:
        messagebox.showerror("Database Error",e)

#Function of gym information.
def show_info():
    info_win = tk.Toplevel()
    info_win.title("Gym Information")
    info_win.geometry('500x550')
    info_win.configure(bg="AliceBlue")

    hist_txt = (
        "Fusion Gym was established in 2020 with the goal of providing the best fitness experience in the region. "
        "Our gym have a size 70000 sq.ft.Started by a group of fitness enthusiasts, the gym offers state-of-the-art equipment and personalized training "
        "programs. Our mission is to help you achieve your fitness goals in a motivating and supportive environment."
    )

    fac_txt = (
        "Facilities:\n"
        "- Modern cardio and strength training equipment\n"
        "- Group fitness classes including yoga, pilates, and spinning\n"
        "- Personal training and nutrition guidance\n"
        "- Locker rooms with showers\n"
        "- Sauna and relaxation area"
    )

    mem_txt = (
        "Membership Types:\n"
        "1. Bronze: Basic access to gym facilities during off-peak hour.Membership price for bronze is Rs-4500 per month\n"
        "2. Gold: Full access to gym facilities, group classes, and a monthly personal training session. Rs-8000 per month\n"
        "3. Platinum: All Gold benefits plus unlimited personal training, priority booking, and access to premium facilities. Rs-15000 per month"
    )

    tk.Label(info_win, text="History of Fusion Gym", font=('Arial', 16, 'bold'), bg="AliceBlue", fg="DarkGreen").pack(pady=10)
    tk.Label(info_win, text=hist_txt, wraplength=400, justify=tk.LEFT, bg="AliceBlue",fg='black', font=('Arial', 14)).pack(pady=10)
    tk.Label(info_win, text="Facilities", font=('Arial', 16, 'bold'), bg="AliceBlue", fg="DarkGreen").pack(pady=10)
    tk.Label(info_win, text=fac_txt, wraplength=400, justify=tk.LEFT, bg="AliceBlue",fg='black', font=('Arial', 14)).pack(pady=10)
    tk.Label(info_win, text="Memberships", font=('Arial', 16, 'bold'), bg="AliceBlue", fg="DarkGreen").pack(pady=10)
    tk.Label(info_win, text=mem_txt, wraplength=400, justify=tk.LEFT, bg="AliceBlue",fg='black', font=('Arial', 14)).pack(pady=10)


#Function of Member's Details.
def id_card():
    def generate_id_card():
        mem_id = ent_id.get()
        
        qry = "select name, membership, phone_no, address, subscription, amount_due from members where id=%s"
        cur.execute(qry, (mem_id,))
        member = cur.fetchone()
        
        if not member:
            messagebox.showerror("Error", "Member ID not found")
            return
        
        name, membership, phone_no, address, subscription, amount_due = member

        if subscription == 'Quarterly':
            amount_due *= 4
        elif subscription == 'Half-Yearly':
            amount_due *= 6
        elif subscription == 'Yearly':
            amount_due *= 12
        
        id_card_win = tk.Toplevel()
        id_card_win.title("ID Card")
        id_card_win.geometry("300x300")
        id_card_win.configure(bg="AliceBlue")
        
        tk.Label(id_card_win, text="ID Card", font=('Arial', 20, 'bold'), bg="AliceBlue", fg="DarkGreen").pack(pady=10)
        tk.Label(id_card_win, text=f"Name: {name}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(id_card_win, text=f"Membership: {membership}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(id_card_win, text=f"Phone no.: {phone_no}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(id_card_win, text=f"Address: {address}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(id_card_win, text=f"Subscription: {subscription}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(id_card_win, text=f"Amount Due: {amount_due}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)

    id_card_win = tk.Toplevel()
    id_card_win.title("Generate ID Card")
    id_card_win.geometry("350x110")
    id_card_win.configure(bg="AliceBlue")

    tk.Label(id_card_win, text="Enter Member ID:", bg="AliceBlue", fg="black", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=5)
    ent_id = tk.Entry(id_card_win)
    ent_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(id_card_win, text="Generate ID Card", command=generate_id_card, bg="ForestGreen", fg="black",
              font=('Arial', 14, 'bold'), padx=20, pady=10, relief=tk.RAISED).grid(row=1, columnspan=2, pady=10)


#Function of Trainer's Deatils.
def trainers_card():
    def generate_trainer_card():
        trainer_id = ent_id.get()
        
        qry = "select id, name, experience, phone_no from trainers where id=%s"
        cur.execute(qry, (trainer_id,))
        trainer = cur.fetchone()
        
        if not trainer:
            messagebox.showerror("Error", "Trainer ID not found")
            return
        
        id, name, experience, phone_no = trainer
        
        trn_card_win = tk.Toplevel()
        trn_card_win.title("Trainer Card")
        trn_card_win.geometry("300x200")
        trn_card_win.configure(bg="AliceBlue")
        
        tk.Label(trn_card_win, text="Trainer Card", font=('Arial', 16, 'bold'), bg="AliceBlue", fg="DarkGreen").pack(pady=10)
        tk.Label(trn_card_win, text=f"Id: {id}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(trn_card_win, text=f"Name: {name}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(trn_card_win, text=f"Phone no.: {phone_no}", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
        tk.Label(trn_card_win, text=f"Experience: {experience} years", bg="AliceBlue", fg="black", font=('Arial', 14)).pack(pady=5)
    
    trn_card_win = tk.Toplevel()
    trn_card_win.title("Generate Trainer Card")
    trn_card_win.geometry("350x110")
    trn_card_win.configure(bg="AliceBlue")

    tk.Label(trn_card_win, text="Enter Trainer ID:", bg="AliceBlue", fg="black", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
    ent_id = tk.Entry(trn_card_win)
    ent_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(trn_card_win, text="Generate Trainer Card", command=generate_trainer_card, bg="ForestGreen", fg="black",
              font=('Arial', 12, 'bold'), padx=20, pady=10, relief=tk.RAISED).grid(row=1, columnspan=2, pady=10)
    

# Main application window
root = tk.Tk()
root.geometry('600x420')
root.title('Fusion Gym Management')
root.configure(bg="LightGray")

tk.Label(root, text="Fusion Gym", font=('Arial', 25, 'bold'), bg="LightGray", fg="DarkGreen").pack(pady=10)

btn_frame = tk.Frame(root, bg="LightGray")
btn_frame.pack(pady=10)
btns = {
    "Add Members": add_mem,
    "Update Records": upd_rec,
    "Delete Records": del_rec,
    "Add Trainers": add_trn,
    "Show Statistics": show_stats,
    "Gym Info": show_info,
    "Bill Generate": bill_generate,
    "ID Card": id_card,
    "Trainer Card": trainers_card
}

for i, (t, c) in enumerate(btns.items()):
    tk.Button(btn_frame, text=t, font=('Arial', 16, 'bold'), command=c, bg="ForestGreen", fg="black",
              padx=20, pady=10, relief=tk.RAISED).grid(row=i//2, column=i%2, padx=10, pady=10)

root.mainloop()
