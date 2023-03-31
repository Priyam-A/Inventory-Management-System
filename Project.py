
#Importing required modules
from tkinter import *
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

#Functions used by many other functions

def con():  #Connects to the mysql database
    mycon=mysql.connector.connect(host='localhost',user='root',passwd='Kolkata52',database='project')
    cursor=mycon.cursor()
    return(mycon,cursor)

def scrollFrame(s): #Creates a scrollable window titled s
    R=Tk()
    R.title(s)
    R.geometry=('1800x720')
    my_canvas = Canvas(R)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    y_scrollbar = Scrollbar(R,orient=VERTICAL,command=my_canvas.yview)
    y_scrollbar.pack(side=RIGHT,fill=Y)
    my_canvas.configure(yscrollcommand=y_scrollbar.set)
    my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(ALL))) 
    frame = Frame(my_canvas)
    my_canvas.create_window((0,0),window= frame, anchor="nw")
    return(frame,R)

def dispInfo(a,s):  #Creates a window cosisting of information about a product
    mycon,cursor=con()
    cursor.execute('SELECT items.Product_ID,Company,Type,Model_no,Cost,YOM,qty FROM items,stock \
                            WHERE items.Product_ID=stock.Product_ID and items.Product_ID={}'.format(a))
    t1=cursor.fetchone()
    r=Tk()
    r.title(s)
    Label(r,text='Product ID:').grid(row=1,column=0,padx=2,pady=2)
    Label(r,text='Company:').grid(row=2,column=0,padx=2,pady=2)
    Label(r,text='Type:').grid(row=3,column=0,padx=2,pady=2)
    Label(r,text='Model no.:').grid(row=4,column=0,padx=2,pady=2)
    Label(r,text='Cost:').grid(row=5,column=0,padx=2,pady=2)
    Label(r,text='Year of mfg:').grid(row=6,column=0,padx=2,pady=2)
    Label(r,text='Qty:').grid(row=7,column=0,padx=2,pady=2)
    for i in range(len(t1)):
        Label(r,text=str(t1[i])).grid(row=i+1,column=1,padx=2,pady=2)
    Button(r,text='Close',command=r.destroy).grid(row=i+2,column=0,padx=2,pady=2,columnspan=2)
    mycon.close()
    
def valid(p):   #Checks whether the given product_id p is in the product_id list or not
    mycon,cursor=con()
    cursor.execute('SELECT Product_ID FROM items;')
    q=cursor.fetchall()
    mycon.close()
    if (p,) in q:
        return True
    else:
        return False

#Adding Data
    
def addItem(t): #Connects to MySQL and adds the data in tuple t
    mycon,cursor=con()
    cursor.execute('SELECT MAX(Product_ID) FROM items')
    Product_ID=(cursor.fetchone())[0]+1
    qty=t[-1]
    t1=(Product_ID,t[0],t[1],t[2],t[3],t[4])
    cursor.execute("INSERT INTO items VALUES{};".format(t1))
    cursor.execute('INSERT INTO stock VALUES({},{})'.format(Product_ID,qty))
    mycon.commit()
    mycon.close()  
    return Product_ID

def add():  #Creates a GUI to obtain data to be added
    def addGUI():   #Gets data from the GUI(defined inside add() to use the LEGB rule)
        t=(rad1_var,rad2_var,e1_var,e2_var,e3_var,e4_var)
        d1={0:'%',1:'Hitachi', 2:'Daikin', 3:'BlueStar', 4:'Voltas'}
        d2={0:'%',1:'Window', 2:'Split', 3:'Concealed'}
        Company=d1[t[0].get()]
        Type=d2[t[1].get()]
        Model_no=t[2].get()
        Cost=int(t[3].get())
        YOM=int(t[4].get())
        qty=int(t[5].get())
        t1=(Company,Type,Model_no,Cost,YOM,qty)
        p=addItem(t1)
        s1='Item Added'
        dispInfo(p,s1)
        r2.destroy()
    r2=Tk()
    r2.title('Add Item')
    Label(r2,text='Company name:').grid(row=0,column=0,pady=2,padx=2)
    Label(r2,text='Type of ac:').grid(row=1,column=0,pady=2,padx=2)
    Label(r2,text='Model no.:').grid(row=2,column=0,pady=2,padx=2)
    Label(r2,text='Cost:').grid(row=3,column=0,pady=2,padx=2)
    Label(r2,text='Year of mfg:').grid(row=4,column=0,pady=2,padx=2)
    Label(r2,text='Qty:').grid(row=5,column=0,pady=2,padx=2)
    rad1_var=IntVar(r2)
    Radiobutton(r2,text='Hitachi',variable=rad1_var,value=1).grid(row=0,column=1,pady=2,padx=2)
    Radiobutton(r2,text='Daikin',variable=rad1_var,value=2).grid(row=0,column=2,pady=2,padx=2)
    Radiobutton(r2,text='BlueStar',variable=rad1_var,value=3).grid(row=0,column=3,pady=2,padx=2)
    Radiobutton(r2,text='Voltas',variable=rad1_var,value=4).grid(row=0,column=4,pady=2,padx=2)
    rad2_var=IntVar(r2)
    rad5=Radiobutton(r2,text='Window',variable=rad2_var,value=1).grid(row=1,column=1,pady=2,padx=2)
    rad6=Radiobutton(r2,text='Split',variable=rad2_var,value=2).grid(row=1,column=2,pady=2,padx=2)
    rad7=Radiobutton(r2,text='Concealed',variable=rad2_var,value=3).grid(row=1,column=3,pady=2,padx=2)
    e1_var=StringVar(r2)
    e2_var=StringVar(r2)
    e3_var=StringVar(r2)
    e4_var=StringVar(r2)
    e1=Entry(r2,textvariable=e1_var)
    e2=Entry(r2,textvariable=e2_var)
    e3=Entry(r2,textvariable=e3_var)
    e4=Entry(r2,textvariable=e4_var)
    e1.grid(row=2,column=1,pady=2,padx=2)
    e2.grid(row=3,column=1,pady=2,padx=2)
    e3.grid(row=4,column=1,pady=2,padx=2)
    e4.grid(row=5,column=1,pady=2,padx=2)
    b=Button(r2,text='Add Data',command=addGUI).grid(row=6,column=2,pady=2,padx=2)

#Searching For data
    
def search(t):  #Obtains data from MySQL on the basis of given tuple t
    mycon,cursor=con()
    d1={0:'Hitachi', 1:'Daikin', 2:'BlueStar', 3:'Voltas'}
    d2={0:'Window', 1:'Split', 2:'Concealed'}
    d3={0:'Product_ID', 1:'cost', 2:'qty'}
    a,b="(","("
    for c1 in t[0]:
        a+="'"+d1[c1]+"',"
    for c2 in t[1]:
        b+="'"+d2[c2]+"',"
    a=a[:-1]+')'
    b=b[:-1]+')'
    z="SELECT items.Product_id,Company,Type,Model_no,Cost,YOM,Qty \
        FROM items,stock \
        WHERE items.Product_ID=Stock.Product_ID AND\
        Items.Company IN {} AND type IN {} AND cost>{} AND cost<{} AND YOM={} AND qty>={} ORDER BY {}"
    cursor.execute(z.format(a,b,t[2],t[3],t[4],t[5],d3[t[6]]))
    p=cursor.fetchall()
    mycon.close()
    return p

def display(t):#Displays the data obtained by search()
    def select(t):#sets the value of the StringVar() object t as the one selected in display window
        t.set(str(p[v.get()][0]))
        r7.destroy()
    def notFound(): #destroys the current window and makes executes filsort()
        r7.destroy()
        filsort(t)
    p=search(q)
    del(q[:])
    if len(p)>0:
        r7=Tk()
        r7.title('Select item')
        Label(r7,text='Product id').grid(row = 0, column = 0, sticky = W, pady = 2,padx=2)
        Label(r7,text='Company').grid(row = 0, column = 1, sticky = W, pady = 2,padx=2)
        Label(r7,text='Type').grid(row = 0, column = 2, sticky = W, pady = 2,padx=2)
        Label(r7,text='Model no.').grid(row = 0, column = 3, sticky = W, pady = 2,padx=2)
        Label(r7,text='Cost').grid(row = 0, column = 4, sticky = W, pady = 2,padx=2)
        Label(r7,text='year of mfg').grid(row = 0, column = 5, sticky = W, pady = 2,padx=2)
        Label(r7,text='qty').grid(row = 0, column = 6, sticky = W, pady = 2,padx=2)
        Label(r7,text='Select').grid(row = 0, column = 7, sticky = W, pady = 2,padx=2)
        for i in range(len(p)):
            for j in range(7):
                Label(r7,text=p[i][j]).grid(row = i+2, column = j, sticky = W, pady = 2,padx=2)
            l=[]
            v=IntVar(r7)
            Radiobutton(r7,variable=v,value=i).grid(row = i+2, column = 7, sticky = W, pady = 2,padx=2)
        Button(r7,text='Get ID',width=25,command=lambda: select(t)).grid(row=i+5,column=6,sticky=E,pady=2,padx=2,columnspan=2)
    else:
        r7=Tk()
        r7.title('NO RESULTS FOUND!')
        del(q[:])
        Label(r7,text='No Results Found!!!').grid(row=1,column=2,sticky=N,pady=2,padx=2)
        Button(r7,text='Search Again?',command=lambda: filsort(t)).grid(row=3,column=0,sticky=N,pady=2,padx=2)
       
def filsort(t): #Gets the arguments to be passed on to search from the user
    def find(): #Gets the arguments to be passed on to search from the GUI
            q.append(Listbox1.curselection())
            q.append(Listbox2.curselection())
            q.append(int(e1_var.get()))
            q.append(int(e2_var.get()))
            q.append(int(e3_var.get()))
            q.append(int(e4_var.get()))
            q.append(v.get())
            r8.destroy()
            display(t)
    r8=Tk()
    r8.title('Filter by')
    Label1=Label(r8,text='Select Companies')
    Listbox1=Listbox(r8, selectmode=MULTIPLE,exportselection=0)
    Listbox1.insert(0,'Hitachi')
    Listbox1.insert(1,'Daikin')
    Listbox1.insert(2,'BlueStar')
    Listbox1.insert(3,'Voltas')
    Label2=Label(r8,text='Select Type')
    Listbox2=Listbox(r8, selectmode=MULTIPLE,exportselection=0)
    Listbox2.insert(0,'Window')
    Listbox2.insert(1,'Split')
    Listbox2.insert(2,'Concealed')
    Label3=Label(r8,text='minimum cost')
    Label4=Label(r8,text='maximum cost')
    Label5=Label(r8,text='Year of mfg')
    Label6=Label(r8,text='min qty')
    e1_var=StringVar(r8)
    e2_var=StringVar(r8)
    e3_var=StringVar(r8)
    e4_var=StringVar(r8)
    e1=Entry(r8,textvariable=e1_var)
    e2=Entry(r8,textvariable=e2_var)
    e3=Entry(r8,textvariable=e3_var)
    e4=Entry(r8,textvariable=e4_var)
    Label7=Label(r8,text='Sort by')
    v=IntVar(r8)
    rad1=Radiobutton(r8, text='Product ID', variable=v, value=0)
    rad2=Radiobutton(r8, text='cost', variable=v, value=1)
    rad3=Radiobutton(r8, text='qty', variable=v, value=2)
    
    Label1.grid(row = 0, column = 0, sticky = W, pady = 2,padx=2)
    Listbox1.grid(row = 1, column = 0,sticky = W, pady = 2,padx=2)
    Label2.grid(row = 0, column = 1, sticky = W, pady = 2,padx=2)
    Listbox2.grid(row = 1, column = 1, sticky = W, pady = 2,padx=2)
    Label3.grid(row = 2, column = 0, sticky = W, pady = 2,padx=2)
    e1.grid(row = 2, column = 1, sticky = W, pady = 2,padx=2)
    Label4.grid(row = 3, column = 0, sticky = W, pady = 2,padx=2)
    e2.grid(row = 3, column = 1, sticky = W, pady = 2,padx=2)
    Label5.grid(row = 4, column = 0, sticky = W, pady = 2,padx=2)
    e3.grid(row = 4, column = 1, sticky = W, pady = 2,padx=2)
    Label6.grid(row = 5, column = 0, sticky = W, pady = 2,padx=2)
    e4.grid(row = 5, column = 1, sticky = W, pady = 2,padx=2)
    Label7.grid(row = 6, column = 0, sticky = W, pady = 2,padx=2)
    rad1.grid(row = 7, column = 0, sticky = W, pady = 2,padx=2)
    rad2.grid(row = 7, column = 1, sticky = W, pady = 2,padx=2)
    rad3.grid(row = 7, column = 2, sticky = W, pady = 2,padx=2)
    global q
    b=Button(r8, text='Filter', width=25, command=find)
    b.grid(row = 12, column = 0, sticky = E , pady = 2,padx=2)

#Removing Data
    
def remove(): #Obtains the product_id to be deleted through a GUI
    def removeItem():#Deletes the data from the database
        Product_ID=int(v1.get())
        if valid(Product_ID):
            dispInfo(Product_ID,'Deleted Data')
            cursor.execute('DELETE FROM items WHERE Product_ID={}'.format(Product_ID))
            Label(r4,text='item deleted').grid(row=3,column=0,padx=2,pady=2,columnspan=2)
        else:
            Label(r4,text='Invalid Product_ID').grid(row=3,column=0,padx=2,pady=2,columnspan=2)
        r4.after(3000,r4.destroy)
        mycon.commit()
        mycon.close()
    mycon,cursor=con()
    cursor.execute('SELECT Product_ID FROM items')
    prodList=cursor.fetchall()
    r4=Tk()
    r4.title('Remove Product')
    Label(r4,text='Product ID:').grid(row=0,column=0,padx=2,pady=2)
    v1=StringVar(r4)
    Entry(r4,textvariable=v1).grid(row=0,column=1,padx=2,pady=2)
    Button(r4,text='Submit',command=removeItem).grid(row=2,column=0,padx=2,pady=2)
    Button(r4,text='Fetch Data',command=lambda: filsort(v1)).grid(row=2,column=1,padx=2,pady=2)

#Updating Prices
    
def updateprice():  #Obtains the product_id and new price to be deleted through a GUI 
    def update():   #Updates the price and displays both old and updated data   
        mycon,cursor=con()
        Product_ID=int(v1.get())
        Cost=int(v2.get())
        if Cost>0 and valid(Product_ID):
            dispInfo(Product_ID,'Old Data')
            cursor.execute('UPDATE items SET Cost={} WHERE Product_ID={}'.format(Cost,Product_ID))
            mycon.commit()
            mycon.close()
            s2='Item Updated'
            dispInfo(Product_ID,s2)
            r5.destroy()
        else:
            Label(r5,text='INVALID SELECTION').grid(row=3,column=0,padx=2,pady=2,columnspan=2)
    r5=Tk()
    r5.title('Update price')
    Label(r5,text='Product ID: ').grid(row=0,column=0,padx=2,pady=2)
    v1=StringVar(r5)
    e1=Entry(r5,textvariable=v1).grid(row=0,column=1,padx=2,pady=2)
    Label(r5,text='New Cost: ').grid(row=1,column=0,padx=2,pady=2)
    v2=StringVar(r5)
    e2=Entry(r5,textvariable=v2).grid(row=1,column=1,padx=2,pady=2)
    Button(r5,text='Submit',command=update).grid(row=2,column=0,padx=2,pady=2)
    Button(r5,text='Fetch Data',command=lambda: filsort(v1)).grid(row=2,column=1,padx=2,pady=2)

#Updating Quantity
    
def updateqty():    #Obtains the product_id and new qty to be deleted through a GUI 
    def updateStock(v2,a,p):  #Updates the qty 
        mycon,cursor=con()
        cursor.execute('SELECT Qty FROM stock WHERE Product_ID={}'.format(p))
        qty=cursor.fetchone()[0]
        if a==1:
            add=int(v2.get())
        elif a==2:
            add=-int(v2.get())
        if (qty+add)>=0:
            dispInfo(p,'Old data')
            cursor.execute('UPDATE stock SET Qty=Qty+{} WHERE Product_ID={}'.format(add,p))
            mycon.commit()
            mycon.close()
            s='Qty Updated'
            dispInfo(p,s)
            r6.destroy()
        else:
            Label(r6,text='INVALID QTY').grid(row=3,column=0,padx=2,pady=2)
            mycon.close()
    def addred(a):  #Creates an entry on the basis of addition/reduction of qty
        p=int(v1.get())
        if valid(p):
            b.destroy()
            b1.destroy()
            b2.destroy()
            if a==1:
                Label(r6,text='Add qty').grid(row=1,column=0,padx=2,pady=2)
                v2=StringVar(r6)
                Entry(r6,textvariable=v2).grid(row=1,column=1,padx=2,pady=2)
                b3=Button(r6,text='Add',command=lambda: updateStock(v2,1,p)).grid(row=2,column=0,padx=2,pady=2,columnspan=2)
            elif a==2:
                Label(r6,text='Reduce qty').grid(row=1,column=0,padx=2,pady=2)
                v2=StringVar(r6)
                Entry(r6,textvariable=v2).grid(row=1,column=1,padx=2,pady=2)
                b4=Button(r6,text='Reduce',command=lambda: updateStock(v2,2,p)).grid(row=2,column=0,padx=2,pady=2,columnspan=2)
        else:
            Label(r6,text='INVALID PROD_ID').grid(row=3,column=0,padx=2,pady=2)
    r6=Tk()
    r6.title('Update qty')
    Label(r6,text='Product ID: ').grid(row=0,column=0,padx=2,pady=2)
    v1=StringVar(r6)
    e1=Entry(r6,textvariable=v1).grid(row=0,column=1,padx=2,pady=2)
    b=Button(r6,text='Fetch Data',command=lambda: filsort(v1))
    b1=Button(r6,text='Add',command=lambda: addred(1))
    b2=Button(r6,text='Reduce',command=lambda: addred(2))
    b.grid(row=1,column=0,padx=2,pady=2)
    b1.grid(row=2,column=0,padx=2,pady=2)
    b2.grid(row=2,column=1,padx=2,pady=2)

#Plotting Graph
    
def getData():  #Gets the data from MySQL
    mycon,cursor=con()
    cursor.execute('CREATE VIEW abcd AS\
                    SELECT company, type, qty, cost, qty*cost AS stockvalue\
                    FROM items,stock\
                    WHERE items.Product_ID=stock.Product_ID')
    mycon.commit()
    t=('Window','Split','Concealed')
    l1,l2,l3,l4,l5,l6=[],[],[],[],[],[]
    s=10
    for i in t:
        cursor.execute('SELECT company,AVG(qty),AVG(cost),AVG(stockValue),SUM(qty)\
                        FROM abcd\
                        WHERE type="{}"\
                        GROUP BY company;'.format(i))
        p=cursor.fetchall()
        for j in p:
            l1.append((j[0]+'\n'+i))
            l2.append(round(j[1],0))
            l3.append(round(j[2],2))
            l4.append(round(j[3],2))
            l5.append(j[4])
            l6.append(s)
            s+=25
    cursor.execute('DROP VIEW abcd')
    mycon.close()
    return l1,l2,l3,l4,l5,l6

def bargraph(root,title,list1,list2,list3,color_list,xlabel,ylabel):    #Creates a bar graph 
    fig = Figure(figsize = (12, 6),dpi = 100)
    plot1 = fig.add_subplot(111)
    plot1.bar(list3, list2, tick_label = list1,width = 15, color = color_list)
    canvas = FigureCanvasTkAgg(fig,master = root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas,root)
    toolbar.update()
    canvas.get_tk_widget().pack()
    plot1.set_xlabel(xlabel)
    plot1.set_ylabel(ylabel)
    plot1.set_title(title)

def piegraph(root,title,list1,list2,color_list):    #Creates a Pie graph
    fig = Figure(figsize = (12, 6),dpi = 100)
    plot1 = fig.add_subplot(111)
    plot1.pie(list2,labels=list1,radius=1.2, colors=color_list,autopct = '%1.1f%%')
    canvas = FigureCanvasTkAgg(fig,master = root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas,root)
    toolbar.update()
    canvas.get_tk_widget().pack()
    plot1.set_title(title+'\n\n')

def plotData():     #Creates a window for Graphs to be embedded
    f,r8=scrollFrame('Graphs plotted')
    l1,l2,l3,l4,l5,l6=getData()
    colours=['r','y','g','b','c','m','pink','orange','yellow','lime','indigo','purple']
    bargraph(f,'Product Type vs Mean qty',l1,l2,l6,colours,'Product Type','mean qty')
    bargraph(f,'Product Type vs Mean Price',l1,l3,l6,colours,'Product Type','mean Price')
    bargraph(f,'Product Type vs Mean StockPrice',l1,l4,l6,colours,'Product Type','mean price of available stock' )
    piegraph(f,'Product Type: Share in qty',l1,l5,colours)

#Creating The Homepage
    
def homePage(): #Holds Buttons for execution of functions when called
    def quitProg(): #Closes the application
        rmain.destroy()
        r=Tk()
        r.title('Thank You')
        Label(r,text='Thank You for using this application').pack()
        r.after(3000,r.destroy)
    rmain=Tk()
    rmain.title('Home Page')
    l1=Label(rmain,text='Alpha AC Shop',font=('Baskerville Old Face',25))
    b1=Button(rmain,text='Add Product',font=('Californian FB',20),width=18,command=add)
    b2=Button(rmain,text='Remove Product',font=('Californian FB',20),width=18,command=remove)
    b3=Button(rmain,text='Update Price',font=('Californian FB',20),width=18,command=updateprice)
    b4=Button(rmain,text='Update Qty',font=('Californian FB',20),width=18,command=updateqty)
    b5=Button(rmain,text='Plot Data',font=('Californian FB',20),width=18,command=plotData)
    b6=Button(rmain,text='Quit',font=('Californian FB',20),width=18,command=quitProg)
    l1.grid(row=1,column=2,pady=2,padx=2)
    b1.grid(row=3,column=1,pady=2,padx=2)
    b2.grid(row=3,column=2,pady=2,padx=2)
    b3.grid(row=3,column=3,pady=2,padx=2)
    b4.grid(row=4,column=1,pady=2,padx=2)
    b5.grid(row=4,column=2,pady=2,padx=2)
    b6.grid(row=4,column=3,pady=2,padx=2)
    rmain.mainloop()

#Main Code Starts Here
    
q=[]    #Used by filsort() to pass data to search()
homePage()  #All other functions can be called from here

#Code ends

