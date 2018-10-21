#!/usr/bin/python3
from tkinter import *

class SelectOrder(Frame):

    screen=0
    
    def __init__(self,master):
        super(SelectOrder,self).__init__(master)
        self.grid()
        self.define_widgets()


    def define_widgets(self):

        temp=Label(self,text="Order Entry")
        temp.grid(row=0,column=1,columnspan=2,sticky=W)

        temp=Label(self,text="Order number :")
        temp.grid(row=2,column=0,sticky=E)

        self.order_number=StringVar()
        temp=Entry(self,textvariable=self.order_number)
        temp.grid(row=2,column=1,columnspan=3,sticky=W)

        temp=Button(self,text="Exit",command=self.leave)
        temp.grid(row=8,column=0,sticky=W)

        temp=Button(self,text="Next",command=self.btn_next)
        temp.grid(row=8,column=3,sticky=W)


    def leave(self):
        quit()

    def btn_next(self):
        SelectOrder.screen=1
        self.quit()

class CustomerAddress(Frame):

    screen=1
    
    def __init__(self,master):
        super(CustomerAddress,self).__init__(master)
        self.grid()
        self.define_widgets()


    def define_widgets(self):

        temp=Label(self,text="Order Entry")
        temp.grid(row=0,column=1,columnspan=2,sticky=W)

        temp=Label(self,text="Order number :")
        temp.grid(row=2,column=0,sticky=E)

        self.order_number=Label(self,text="How do i str(order_number)")
        self.order_number.grid(row=2,column=1,sticky=W)
        
        temp=Label(self,text="Address :")
        temp.grid(row=4,column=0,sticky=E)

        self.address1=StringVar()
        temp=Entry(self,textvariable=self.address1)
        temp.grid(row=4,column=1,columnspan=3,sticky=W)

        self.address2=StringVar()
        temp=Entry(self,textvariable=self.address2)
        temp.grid(row=5,column=1,columnspan=3,sticky=W)

        temp=Button(self,text="Exit",command=self.leave)
        temp.grid(row=8,column=0,sticky=W)

        temp=Button(self,text="Prev",command=self.btn_prev)
        temp.grid(row=8,column=2,sticky=W)

        temp=Button(self,text="Next",command=self.btn_next)
        temp.grid(row=8,column=3,sticky=W)


    def leave(self):
        quit()

    def btn_next(self):
        CustomerAddress.screen=2
        self.quit()

    def btn_prev(self):
        CustomerAddress.screen=0
        self.quit()

class OrderHeader(Frame):

    screen=2
    
    def __init__(self,master):
        super(OrderHeader,self).__init__(master)
        self.grid()
        self.define_widgets()


    def define_widgets(self):

        temp=Label(self,text="Order Header")
        temp.grid(row=0,column=1,columnspan=2,sticky=W)

        temp=Label(self,text="Order number :")
        temp.grid(row=2,column=0,sticky=E)

        self.order_number=Label(self,text="How do i str(order_number)")
        self.order_number.grid(row=2,column=1,sticky=W)
        
        temp=Label(self,text="Delviery :")
        temp.grid(row=4,column=0,sticky=E)

        self.delivery=StringVar()
        temp=Entry(self,textvariable=self.delivery)
        temp.grid(row=4,column=1,columnspan=3,sticky=W)

        temp=Label(self,text="Order Type :")
        temp.grid(row=5,column=0,sticky=E)

        self.order_type=StringVar()
        temp=Entry(self,textvariable=self.order_type)
        temp.grid(row=5,column=1,columnspan=3,sticky=W)

        temp=Button(self,text="Exit",command=self.leave)
        temp.grid(row=8,column=0,sticky=W)

        temp=Button(self,text="Prev",command=self.btn_prev)
        temp.grid(row=8,column=2,sticky=W)

        temp=Button(self,text="Done",command=self.btn_done)
        temp.grid(row=8,column=3,sticky=W)


    def leave(self):
        quit()

    def btn_done(self):
        OrderHeader.screen=-1
        self.quit()

    def btn_prev(self):
        OrderHeader.screen=1
        self.quit()

#
# main

root=Tk()
root.title("multi screen application")
root.geometry("600x300")

window=SelectOrder(root)
screen=window.screen

address1=None
address2=None
order_type=None
delivery=None

while True:
    root.mainloop()

    if screen==0:
        order_number=window.order_number.get()
    elif screen==1:
        address1=window.address1.get()
        address2=window.address2.get()
    elif screen==2:
        order_type=window.order_type.get()
        delivery=window.delivery.get()

    screen=window.screen

    if screen<0:
        print("write data")
        break
        
    #
    # this has to be in a try: as when you click X (window close) rather
    # than exit i get a double destruction problem 
    try:
        window.destroy()
    except TclError:
        quit()

    if screen==0:
        window=SelectOrder(root)
        window.order_number.set(order_number)
    elif screen==1:
        window=CustomerAddress(root)
        window.order_number["text"]=order_number
        if address1!=None:
            window.address1.set(address1)
        if address2!=None:
            window.address2.set(address2)    
    else:
        window=OrderHeader(root)
        window.order_number["text"]=order_number
        if order_type!=None:
            window.order_type.set(order_type)
        if delivery!=None:
            window.delivery.set(delivery)
