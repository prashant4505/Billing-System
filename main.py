from tkinter import*
import random
from tkinter import messagebox
import os

win=Tk()
win.geometry("1350x700+0+0")
win.title("Billing Software")
win.iconbitmap("icon\\rubik_cube_icon_182136.ico")

#========================= Cosmetics Price List ===========================
soap_price=10
fcream_price=20
fwash_price=10
hspray_price=25
hgell_price=15
bloshan_price=35

#========================= Grocery Price List ===========================
rice_price=30
foil_price=100
daal_price=100
wheat_price=18
sugar_price=38
tea_price=50

#========================= Cold Drink Price List ===========================
maza_price=40
cock_price=40
frooti_price=40
thumbsUp_price=40
limka_price=40
sprite_price=40

def exitapp():
    win.destroy()

def clear():
    #==========Clear Bill Area======================

    win.textarea.delete(1.0, END)

    #==========BILL NUMBER CLEAR====================

    global bill_num
    bill_num = random.randint(1000, 9999)

    #==========cosmetics field clear================
    m1_txt.delete(0,"end")
    c1_txt.delete(0, "end")
    bath_txt.delete(0,"end")
    fcream_txt.delete(0,"end")
    fwash_txt.delete(0,"end")
    hspray_txt.delete(0,"end")
    hgell_txt.delete(0,"end")
    bloshan_txt.delete(0,"end")

    #==========Grocery field clear===================
    m2_txt.delete(0,"end")
    c2_txt.delete(0,"end")
    rice_txt.delete(0,"end")
    foil_txt.delete(0,"end")
    daal_txt.delete(0,"end")
    wheat_txt.delete(0,"end")
    sugar_txt.delete(0,"end")
    tea_txt.delete(0,"end")

    #==========Cold Drink field clear=================
    m3_txt.delete(0,"end")
    c3_txt.delete(0,"end")
    maza_txt.delete(0,"end")
    cock_txt.delete(0,"end")
    frooti_txt.delete(0,"end")
    t_up_txt.delete(0,"end")
    limka_txt.delete(0,"end")
    sprite_txt.delete(0,"end")

    #===========Customer Detail Clear=================
    cname_txt.delete(0,"end")
    ccont_txt.delete(0,"end")
    cbill_txt.delete(0,"end")


#==================Cosmetics Function===================

def cosmetics():
    m1_txt.delete(0, "end")
    c1_txt.delete(0, "end")
    s1=soap_qty.get()
    s2=fcream_qty.get()
    s3=fwash_qty.get()
    s4=hspray_qty.get()
    s5=hgell_qty.get()
    s6=bloshan_qty.get()
    cosmetics_total=s1*soap_price+s2*fcream_price+s3*fwash_price+s4*hspray_price+s5*hgell_price+s6*bloshan_price
    m1_txt.insert(0,cosmetics_total)
    c1_txt.insert(0,(cosmetics_total*18)/100)

def grocery():
    m2_txt.delete(0, "end")
    c2_txt.delete(0, "end")
    g1=rice_qty.get()
    g2=foil_qty.get()
    g3=daal_qty.get()
    g4=wheat_qty.get()
    g5=sugar_qty.get()
    g6=tea_qty.get()
    grocery_total=g1*rice_price+g2*foil_price+g3*daal_price+g4*wheat_price+g5*sugar_price+g6*tea_price
    m2_txt.insert(0,grocery_total)
    c2_txt.insert(0,(grocery_total*18)/100)

def cold_drink():
    m3_txt.delete(0, "end")
    c3_txt.delete(0, "end")
    d1=maza_qty.get()
    d2=cock_qty.get()
    d3=frooti_qty.get()
    d4=thumbsUp_qty.get()
    d5=limka_qty.get()
    d6=sprite_qty.get()
    cold_drink_total=d1*maza_price+d2*cock_price+d3*frooti_price+d4*thumbsUp_price+d5*limka_price+d6*sprite_price
    m3_txt.insert(0,cold_drink_total)
    c3_txt.insert(0,(cold_drink_total*18)/100)

#============Bill Num=============
bill_num=random.randint(1000,9999)

def random_num():
    cbill_txt.delete(0,"end")
    cbill_txt.insert(0, bill_num)

def total():
    cosmetics()
    grocery()
    cold_drink()
    random_num()

#=================Bill Area===========================
def welcome_bill():
    win.textarea.delete(1.0,END)
    win.textarea.insert(END,"\t Welcome Webcode Retail")
    win.textarea.insert(END, f"\n Bill Number : {bill_num}")
    win.textarea.insert(END, f"\n Customer Name : {cname.get()}")
    win.textarea.insert(END, f"\n Phone Number : {cnum.get()}")
    win.textarea.insert(END,"\n=======================================")
    win.textarea.insert(END, "\nProduct\t\t\tPrice")
    win.textarea.insert(END, "\n=======================================")
    win.textarea.insert(END, f"\n Cosmetics :\t\t\t{float(m1_txt.get())}")
    win.textarea.insert(END, f"\n Grocery :\t\t\t{float(m2_txt.get())}")
    win.textarea.insert(END, f"\n Cold Drink :\t\t\t{float(m3_txt.get())}")
    win.textarea.insert(END, f"\n Cosmetics Tax:\t\t\t{c1_txt.get()}")
    win.textarea.insert(END, f"\n Grocery Tax:\t\t\t{c2_txt.get()}")
    win.textarea.insert(END, f"\n Cold Drink Tax:\t\t\t{c3_txt.get()}")
    total_bill=float(m1_txt.get())+float(m2_txt.get())+float(m3_txt.get())+float(c1_txt.get())+float(c2_txt.get())+float(c3_txt.get())
    win.textarea.insert(END, "\n=======================================")
    win.textarea.insert(END, f"\nTotal\t\t\t{total_bill}")
    win.textarea.insert(END, "\n=======================================")
    win.textarea.insert(END, f"\n\t\t\tSignature")

    save_bill()

#==================== Save Bill ======================

def save_bill():
    op=messagebox.askyesno("Save Bill","Do You Want To Save The Bill ?")
    if op>0:
        bill_data=win.textarea.get(1.0,END)
        f1=open("bills/"+str(cbill_txt.get())+".txt","w")
        f1.write(bill_data)
        f1.close()
        messagebox.showinfo("Saved","Bill Saved Successfully")
    else:
        return

#================= Search Bill ==========================

def search_bill():
    win.textarea.delete(1.0, END)
    present="no"
    for i in os.listdir("bills/"):
        if i.split(".")[0]==cbill_txt.get():
            f1=open(f"bills/{i}","r")
            win.textarea.delete("1.0",END)
            for d in f1:
                win.textarea.insert(END, d)
            f1.close()
            present="yes"
    if present=="no" :
        messagebox.showinfo("Error"," Invalid Bill No. ")

#==================== Title ==========================

title=Label(win,text="Billing Software",bd=8,font=("times new roman",25,"bold"),relief=GROOVE,bg="red",fg="yellow",pady=2)
title.pack(fill=X)
#==================== Cutomer details ================
f1=LabelFrame(win,text="Customer Details",font=("times new roman",10,"bold"),fg="Gold",bg="red",bd=8,relief=GROOVE)
f1.place(x=0,y=60,relwidth=1)

#====Customer Name
cname_lbl=Label(f1,text="Customer Name : ",font=("times new roman",15,"bold"),fg="white",bg="red")
cname_lbl.grid(row=0,column=0,padx=20,pady=00)
cname=StringVar()
cname_txt=Entry(f1,text="",font=("times new roman",10,"bold"),textvariable=cname,fg="Blue",bd=7)
cname_txt.grid(row=0,column=1,padx=20,pady=00)

#====Customer Contact
ccont_lbl=Label(f1,text="Contact No : ",font=("times new roman",15,"bold"),fg="white",bg="red")
ccont_lbl.grid(row=0,column=2,padx=20,pady=00)
cnum=StringVar()
ccont_txt=Entry(f1,text="",font=("times new roman",10,"bold"),textvariable=cnum,fg="Blue",bd=7)
ccont_txt.grid(row=0,column=3,padx=20,pady=00)

#====Customer Bill No
cbill_lbl=Label(f1,text="Bill No : ",font=("times new roman",15,"bold"),fg="white",bg="red")
cbill_lbl.grid(row=0,column=4,padx=20,pady=00)
cbill_num=StringVar()
cbill_txt=Entry(f1,text="",font=("times new roman",10,"bold"),textvariable=cbill_num,fg="Blue",bd=7)
cbill_txt.grid(row=0,column=5,padx=20,pady=00)

#Search Button
search_btn=Button(f1,text="Search",command=search_bill,font=("times new roman",12,"bold"),fg="Blue",bd=5,bg="Yellow")
search_btn.grid(row=0,column=7,padx=20,pady=00)

#=================Cosmetics Frame=====================

f2=LabelFrame(win,text="Cosmetics",relief=GROOVE,font=("times new roman",10,"bold"),fg="Gold",bg="red",bd=8)
f2.place(x=0,y=130,height=380,width=325)

bath_lbl=Label(f2,text="Bath Soap",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
bath_lbl.grid(row=0,column=0,padx=10,pady=10,sticky="w")
soap_qty=IntVar()
bath_txt=Entry(f2,font=("Times New Roman",12,"bold"),textvariable=soap_qty,fg="Blue",bd=5,justify=RIGHT)
bath_txt.grid(row=0,column=1,padx=10,pady=0,sticky="w")

fcream_lbl=Label(f2,text="Face Cream",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
fcream_lbl.grid(row=1,column=0,padx=10,pady=10,sticky="w")
fcream_qty=IntVar()
fcream_txt=Entry(f2,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=fcream_qty,justify=RIGHT)
fcream_txt.grid(row=1,column=1,padx=10,pady=0,sticky="w")

fwash_lbl=Label(f2,text="Face Wash",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
fwash_lbl.grid(row=2,column=0,padx=10,pady=10,sticky="w")
fwash_qty=IntVar()
fwash_txt=Entry(f2,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=fwash_qty,justify=RIGHT)
fwash_txt.grid(row=2,column=1,padx=10,pady=0,sticky="w")

hspray_lbl=Label(f2,text="Hair Spray",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
hspray_lbl.grid(row=3,column=0,padx=10,pady=10,sticky="w")
hspray_qty=IntVar()
hspray_txt=Entry(f2,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=hspray_qty,justify=RIGHT)
hspray_txt.grid(row=3,column=1,padx=10,pady=0,sticky="w")

hgell_lbl=Label(f2,text="Hair Gell",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
hgell_lbl.grid(row=4,column=0,padx=10,pady=10,sticky="w")
hgell_qty=IntVar()
hgell_txt=Entry(f2,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=hgell_qty,justify=RIGHT)
hgell_txt.grid(row=4,column=1,padx=10,pady=0,sticky="w")

bloshan_lbl=Label(f2,text="Body Loshan",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
bloshan_lbl.grid(row=5,column=0,padx=10,pady=10,sticky="w")
bloshan_qty=IntVar()
bloshan_txt=Entry(f2,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=bloshan_qty,justify=RIGHT)
bloshan_txt.grid(row=5,column=1,padx=10,pady=0,sticky="w")


#=================Grocery=====================

f3=LabelFrame(win,text="Grocery",relief=GROOVE,font=("times new roman",10,"bold"),fg="Gold",bg="red",bd=8)
f3.place(x=330,y=130,height=380,width=325)

rice_lbl=Label(f3,text="Rice",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
rice_lbl.grid(row=0,column=0,padx=10,pady=10,sticky="w")
rice_qty=IntVar()
rice_txt=Entry(f3,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=rice_qty,justify=RIGHT)
rice_txt.grid(row=0,column=1,padx=10,pady=0,sticky="w")

foil_lbl=Label(f3,text="Food Oil",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
foil_lbl.grid(row=1,column=0,padx=10,pady=10,sticky="w")
foil_qty=IntVar()
foil_txt=Entry(f3,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=foil_qty,justify=RIGHT)
foil_txt.grid(row=1,column=1,padx=10,pady=0,sticky="w")

daal_lbl=Label(f3,text="Daal",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
daal_lbl.grid(row=2,column=0,padx=10,pady=10,sticky="w")
daal_qty=IntVar()
daal_txt=Entry(f3,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=daal_qty,justify=RIGHT)
daal_txt.grid(row=2,column=1,padx=10,pady=0,sticky="w")

wheat_lbl=Label(f3,text="Wheat",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
wheat_lbl.grid(row=3,column=0,padx=10,pady=10,sticky="w")
wheat_qty=IntVar()
wheat_txt=Entry(f3,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=wheat_qty,justify=RIGHT)
wheat_txt.grid(row=3,column=1,padx=10,pady=0,sticky="w")

sugar_lbl=Label(f3,text="Sugar",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
sugar_lbl.grid(row=4,column=0,padx=10,pady=10,sticky="w")
sugar_qty=IntVar()
sugar_txt=Entry(f3,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=sugar_qty,justify=RIGHT)
sugar_txt.grid(row=4,column=1,padx=10,pady=0,sticky="w")

tea_lbl=Label(f3,text="Tea",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
tea_lbl.grid(row=5,column=0,padx=10,pady=10,sticky="w")
tea_qty=IntVar()
tea_txt=Entry(f3,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=tea_qty,justify=RIGHT)
tea_txt.grid(row=5,column=1,padx=10,pady=0,sticky="w")

#=================Cold Drink=====================

f4=LabelFrame(win,text="Cold Drink",relief=GROOVE,font=("times new roman",10,"bold"),fg="Gold",bg="red",bd=8)
f4.place(x=660,y=130,height=380,width=325)

maza_lbl=Label(f4,text="Maza",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
maza_lbl.grid(row=0,column=0,padx=10,pady=10,sticky="w")
maza_qty=IntVar()
maza_txt=Entry(f4,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=maza_qty,justify=RIGHT)
maza_txt.grid(row=0,column=1,padx=10,pady=0,sticky="w")

cock_lbl=Label(f4,text="Cock",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
cock_lbl.grid(row=1,column=0,padx=10,pady=10,sticky="w")
cock_qty=IntVar()
cock_txt=Entry(f4,font=("Times New Roman",12,"bold"),textvariable=cock_qty,fg="Blue",bd=5,justify=RIGHT)
cock_txt.grid(row=1,column=1,padx=10,pady=0,sticky="w")

frooti_lbl=Label(f4,text="Frooti",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
frooti_lbl.grid(row=2,column=0,padx=10,pady=10,sticky="w")
frooti_qty=IntVar()
frooti_txt=Entry(f4,font=("Times New Roman",12,"bold"),textvariable=frooti_qty,fg="Blue",bd=5,justify=RIGHT)
frooti_txt.grid(row=2,column=1,padx=10,pady=0,sticky="w")

t_up_lbl=Label(f4,text="Thumbs Up",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
t_up_lbl.grid(row=3,column=0,padx=10,pady=10,sticky="w")
thumbsUp_qty=IntVar()
t_up_txt=Entry(f4,font=("Times New Roman",12,"bold"),textvariable=thumbsUp_qty,fg="Blue",bd=5,justify=RIGHT)
t_up_txt.grid(row=3,column=1,padx=10,pady=0,sticky="w")

limka_lbl=Label(f4,text="Limka",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
limka_lbl.grid(row=4,column=0,padx=10,pady=10,sticky="w")
limka_qty=IntVar()
limka_txt=Entry(f4,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=limka_qty,justify=RIGHT)
limka_txt.grid(row=4,column=1,padx=10,pady=0,sticky="w")

sprite_lbl=Label(f4,text="Sprite",font=("Times New Roman",12,"bold"),bg="red",fg="lightgreen")
sprite_lbl.grid(row=5,column=0,padx=10,pady=10,sticky="w")
sprite_qty=IntVar()
sprite_txt=Entry(f4,font=("Times New Roman",12,"bold"),fg="Blue",bd=5,textvariable=sprite_qty,justify=RIGHT)
sprite_txt.grid(row=5,column=1,padx=10,pady=0,sticky="w")

#=================Bill Frame Area=====================

f5=Frame(win,bd=10,relief=GROOVE)
f5.place(x=990,y=130,height=380,width=360)

bill_title=Label(f5,text="Bill Area",font=("Times New Roman",15,"bold"),bd=7,relief=GROOVE).pack(fill=X)
s_bar=Scrollbar(f5,orient=VERTICAL)
win.textarea=Text(f5,yscrollcommand=s_bar.set)
s_bar.pack(side=RIGHT,fill=Y)
s_bar.config(command=win.textarea.yview)
win.textarea.pack(fill=BOTH)

#============Button Frame============

f6=LabelFrame(win,text="Bill Menu",relief=GROOVE,font=("times new roman",10,"bold"),fg="Gold",bg="red",bd=8)
f6.place(x=0,y=518,height=175,relwidth=1)

m1=Label(f6,text="Total Cosmetic Price",font=("times new ronam",12,"bold"),bg="red",fg="white")
m1.grid(row=0,column=0,padx=20,pady=5,sticky="w")
m1_txt=Entry(f6,width=18,font=("times new roman",12,"bold"),bd=7,relief=SUNKEN,justify=RIGHT)
m1_txt.grid(row=0,column=1,padx=10,pady=5)

m2=Label(f6,text="Total Grocery Price",font=("times new ronam",12,"bold"),bg="red",fg="white")
m2.grid(row=1,column=0,padx=20,pady=5,sticky="w")
m2_txt=Entry(f6,width=18,font=("times new roman",12,"bold"),bd=7,relief=SUNKEN,justify=RIGHT)
m2_txt.grid(row=1,column=1,padx=10,pady=5)

m3=Label(f6,text="Total Cold Drink Price",font=("times new ronam",12,"bold"),bg="red",fg="white")
m3.grid(row=2,column=0,padx=20,pady=5,sticky="w")
m3_txt=Entry(f6,width=18,font=("times new roman",12,"bold"),bd=7,relief=SUNKEN,justify=RIGHT)
m3_txt.grid(row=2,column=1,padx=10,pady=5)


c1=Label(f6,text="Cosmetic Tax",font=("times new ronam",12,"bold"),bg="red",fg="white")
c1.grid(row=0,column=2,padx=20,pady=5,sticky="w")
c1_txt=Entry(f6,width=18,font=("times new roman",12,"bold"),bd=7,relief=SUNKEN,justify=RIGHT)
c1_txt.grid(row=0,column=3,padx=10,pady=5)

c2=Label(f6,text="Grocery Tax",font=("times new ronam",12,"bold"),bg="red",fg="white")
c2.grid(row=1,column=2,padx=20,pady=5,sticky="w")
c2_txt=Entry(f6,width=18,font=("times new roman",12,"bold"),bd=7,relief=SUNKEN,justify=RIGHT)
c2_txt.grid(row=1,column=3,padx=10,pady=5)

c3=Label(f6,text="Cold Drink Tax",font=("times new ronam",12,"bold"),bg="red",fg="white")
c3.grid(row=2,column=2,padx=20,pady=5,sticky="w")
c3_txt=Entry(f6,width=18,font=("times new roman",12,"bold"),bd=7,relief=SUNKEN,justify=RIGHT)
c3_txt.grid(row=2,column=3,padx=10,pady=5)

#=================Button Frame==============

btn_f=Frame(f6,relief=GROOVE,bg="red",bd=8)
btn_f.place(x=740,width=585,height=130)

total_btn=Button(btn_f,text="Total",font=("times new roman",12,"bold"),command=total,bg="cadetblue",fg="Blue",pady=15,width=11,bd=5)
total_btn.grid(row=0,column=0,padx=10,pady=20)

gbill_btn=Button(btn_f,command=welcome_bill,text="Genrate Bill",font=("times new roman",12,"bold"),bg="cadetblue",fg="Blue",pady=15,width=11,bd=5)
gbill_btn.grid(row=0,column=1,padx=15,pady=20)

clear_btn=Button(btn_f,text="Clear",font=("times new roman",12,"bold"),bg="cadetblue",command=clear,fg="Blue",pady=15,width=11,bd=5)
clear_btn.grid(row=0,column=2,padx=15,pady=20)

exit_btn=Button(btn_f,text="Exit",font=("times new roman",12,"bold"),bg="cadetblue",fg="Blue",pady=15,width=11,bd=5,command=exitapp)
exit_btn.grid(row=0,column=3,padx=15,pady=20)



win.mainloop()