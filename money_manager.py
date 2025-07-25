# -*- coding: utf-8 -*-
"""
Created on Tue May 27 19:45:22 2025

This program should receive an amount of money 
as input and output a list of every amount given 
until the user prompts exiting the program. 
This list should have the amounts on the first column, 
followed by deposits followed by withdraws
Then this should output the Surplus.

@author: corte
"""
# =============================================================================
# import MM_Functions as fun
# =============================================================================
from tkinter import *
from tkinter import messagebox
import mysql.connector


def addExpense():
    # Read data provided by user
    Item = enterItem.get()
    Price = enterPrice.get()
    expense = Price
    income = 0
    Table = showTables.get(ACTIVE)   
    
    if(Item == "" or Price == ""):
        # If empty data provided by user
        messagebox.showwarning("Cannot Insert","All the fields are required")
    else: # Insert data in Finances table
        myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
        myCur = myDB.cursor()
        myCur.execute('insert into '+Table+' (Item,Expenses)  values("'+Item+'",'+expense+')')
        myDB.commit()
        
        # Clear out entries from fields
        
        resetFields()

        showData()
        computeLeftover()
        
        messagebox.showinfo("Add Status","Data Added to Table Succesfully")
        myDB.close()
                
def addIncome():
    # Read data provided by user
    Item = enterItem.get()
    Price = enterPrice.get()
    expense = 0
    income = Price
    Table = showTables.get(ACTIVE)
    
    if(Item == "" or Price == ""):
        # If empty data provided by user
        messagebox.showwarning("Cannot Insert","All the fields are required")
    else: # Insert data in Finances table
        myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
        myCur = myDB.cursor()
        
                                                
        myCur.execute('insert into '+Table+' (Item,Income) values("'+Item+'",'+income+')')
        myDB.commit()
        
        # Clear out entries from fields
        
        resetFields()

        showData()
        computeLeftover()
        
        messagebox.showinfo("Add Status","Data Added to Table Succesfully")
        myDB.close()

def updateData():
    # Read data provided by user
    Item = enterItem.get()
    Price = enterPrice.get()
    Table = showTables.get(ACTIVE)
    
    if(Item == "" or Price == "" or Table == ""):
        # If empty data provided by user
        messagebox.showwarning('Cannot Update','All fields are required')
    else:
        myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
        myCur = myDB.cursor()
        myCur.execute('select * from '+Table+'')
        
        data = myCur.fetchall()
        
        for row in data:
            if not row[1]:
                myCur.execute('update '+Table+' set Income='+Price+' where Item="'+Item+'"')
            elif not row[2]:
                myCur.execute('update '+Table+' set Expenses='+Price+' where Item="'+Item+'"')
                
        myDB.commit()
        
        resetFields()
        
        showData()
        computeLeftover()
        
        messagebox.showinfo('Update Status','Data Updated Succesfully')
        myDB.close()
        
    
def getData():
    
    Item = enterItem.get()
    Table = showTables.get(ACTIVE)
    
    if(Item == ""):
        messagebox.showwarning('Fetch Status','Please provide an Item to fetch its Price')
    else:
        myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
        myCur = myDB.cursor()
        myCur.execute('select * from '+Table+' where Item="'+Item+'"')
        data = myCur.fetchall()
        
        for row in data:
            if not row[1]:
                enterPrice.insert(0,row[2])
            elif not row[2]:
                enterPrice.insert(0,row[1])
            
        myDB.close()

def deleteData():
    
    Table = showTables.get(ACTIVE)
    
    if(enterItem.get() == ""):  # Read and check for empty data
        messagebox.showwarning('Cannot Delete','Please provide Item to delete data')
    else:   # Delete selected record from selected table
        myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
        myCur = myDB.cursor()
        myCur.execute('delete from '+Table+' where Item="'+enterItem.get()+'"')
        myDB.commit()
        
        # Clear out data from fields
        
        resetFields()
        
        showData()
        computeLeftover()
        
        messagebox.showinfo('Delete Status','Data Deleted Succesfully')
        myDB.close()

def resetFields():
    enterItem.delete(0,"end")
    enterPrice.delete(0,"end")
    enterTable.delete(0,"end")
    enterQuery.delete(0,"end")


def createTable():
    
    newTable = enterTable.get()
    
    myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
    myCur = myDB.cursor()
    myCur.execute('create table '+newTable+'(Item varchar(100) primary key, Expenses int, Income int)')
    myDB.commit()
        
    # Clear out fields
    
    resetFields()
    
    # Update display
    
    displayTables()
    showData()
    computeLeftover()
    
    messagebox.showinfo('Table Status','Table Created Succesfully')
    myDB.close()    

def deleteTable():
    
    Table = showTables.get(ACTIVE)
    
    myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
    myCur = myDB.cursor()
    myCur.execute('drop table '+Table+'')
    
    # Clear out fields
    
    resetFields()
    
    displayTables()
    
    messagebox.showinfo('Table Status','Table Deleted Succesfully')
    myDB.close() 
    
def displayTables():
    
    myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
    myCur = myDB.cursor()
    
    myCur.execute('show tables')
    tables = myCur.fetchall()
    showTables.delete(0,"end")
    
    for row in tables:
        addData = row[0]
        showTables.insert(showTables.size() + 1, addData)
        
    myDB.close()

def showSelectedTable():
    
    SelectedTable = showTables.get(ACTIVE)
    selectedTableLbl.config(text=f'Selected: {SelectedTable}')
    
    showData()
    computeLeftover()
    
def showData():
    
    if(showTables.get(END) == ""):
        messagebox.showwarning('No Tables','There aren\'t any tables to show')
        pass
    else:
        Table = showTables.get(ACTIVE)
    
        myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
        myCur = myDB.cursor()
        
        myCur.execute('select * from '+Table+'')
        data = myCur.fetchall()
        
        showIncome.delete(0,"end")
        showExpenses.delete(0,"end")
        
        for row in data:
            if not row[1]:
                addData = row[0] + ' ' + str(row[2])
                showIncome.insert(showIncome.size()+1,addData)
            elif not row[2]:
                addData = row[0] + ' ' + str(row[1])
                showExpenses.insert(showExpenses.size()+1,addData)
        myDB.close()

def computeLeftover():
    
    Table = showTables.get(ACTIVE)
    
    myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
    myCur = myDB.cursor()
    myCur.execute('select * from '+Table+'')
    
    data = myCur.fetchall()
    
    totalIncome = []
    totalExpenses = []
    
    for row in data:
        if not row[1]:
            totalIncome.append(row[2])
        elif not row[2]:
            totalExpenses.append(row[1])
    
    leftoverTotal = sum(totalIncome) - sum(totalExpenses)
    
    leftoversLbl.config(text = f'Total Remaining: {leftoverTotal}')
    
    if enterQuery.get() == "":
        pass
    myDB.close()
    
    
def markPaid():
    
    Expense = showExpenses.get(ACTIVE)

    if not Expense:
        messagebox.showwarning('Mark Status','Please select an item to mark')
    else:
        showExpenses.config()
        

def executeQuery():
    
    query = enterQuery.get()
    Table = showTables.get(ACTIVE)
    
    if(query == ""):
        messagebox.showwarning('Search Status','Search Field is required')
    else:
        myDB = mysql.connector.connect(host='localhost',user='root',passwd='Cc.198422231',database='Finances')
        myCur = myDB.cursor()
        myCur.execute('select * from '+Table+' where Item like "%'+query+'%"')
        
        result = myCur.fetchall()
        showQuery.delete(0,"end")
        
        if result == []:
            messagebox.showwarning('Search Status','Not Found')
        else:
            for row in result:
                if not row[1]:
                    data = row[0] + ' ' + str(row[2])
                    showQuery.insert(showQuery.size()+1,data)
                elif not row[2]:
                    data = row[0] + ' ' + str(row[1])
                    showQuery.insert(showQuery.size()+1,data)
        
        
        resetFields()
        
        myDB.close()
        
# Create window
window = Tk()
window.geometry("700x500")
window.title("Money Manager")

# Create Labels
expenses = Label(window, text='Expenses', font=('Serif',12))
expenses.place(x=290,y=20)

income = Label(window, text='Income', font=('Serif',12))
income.place(x=440,y=20)

tables = Label(window, text='Tables', font=('Serif',12))
tables.place(x=590,y=20)

item = Label(window, text='Item', font=('Serif',12))
item.place(x=35,y=60)

price = Label(window, text='$', font=('Serif',12))
price.place(x=50,y=90)

leftoversLbl = Label(window, text = ' ')
leftoversLbl.place(x=20,y=480)

selectedTableLbl = Label(window, text = ' ')
selectedTableLbl.place(x=570,y=300)

# =============================================================================
# search = Label(window, text='Search', font=('Serif',12))
# search.place(x=40,y=410)
# =============================================================================

# Create Entries
enterItem = Entry(window)
enterItem.place(x=100,y=60)

enterPrice = Entry(window)
enterPrice.place(x=100,y=90)

enterQuery = Entry(window)
enterQuery.place(x=100,y=410)

enterTable = Entry(window)
enterTable.place(x=380,y=280)

# Create Buttons
addExpenseBtn = Button(window, text='Add Expense', font=('Sans',12),bg='white',command=addExpense)
addExpenseBtn.place(x=20,y=150)

addIncomeBtn = Button(window, text='Add Income', font=('Sans',12),bg='white',command=addIncome)
addIncomeBtn.place(x=140,y=150)

updateBtn = Button(window, text='Update', font=('Sans',12),bg='white',command=updateData)
updateBtn.place(x=20,y=190)

getBtn = Button(window, text='Fetch', font=('Sans',12),bg='white',command=getData)
getBtn.place(x=140,y=190)

deleteBtn = Button(window, text='Delete', font=('Sans',12),bg='white',command=deleteData)
deleteBtn.place(x=20,y=230)

resetBtn = Button(window, text='Reset', font=('Sans',12),bg='white',command=resetFields)
resetBtn.place(x=140,y=230)

createTableBtn = Button(window, text='Create New Table', font=('Sans',12),bg='white',command=createTable)
createTableBtn.place(x=370,y=240)

deleteTableBtn = Button(window, text='Delete Table', font=('Sans',12),bg='white',command=deleteTable)
deleteTableBtn.place(x=20,y=270)

queryBtn = Button(window,text='Search',font=('Serif',12),bg='white',command=executeQuery)
queryBtn.place(x=30,y=410)

selectTableBtn = Button(window, text = 'Select Table', font =('Sans',12),bg='white',command=showSelectedTable)
selectTableBtn.place(x=570,y=240)

markPaidBtn = Button(window,text='Mark\\Unmark Paid',font=('Serif',12),bg='green',command=markPaid)
markPaidBtn.place(x=20,y=310)

# Create Listboxes
showExpenses = Listbox(window)
showExpenses.place(x=260,y=60)

showIncome = Listbox(window)
showIncome.place(x=410,y=60)

showTables = Listbox(window)
showTables.place(x=560,y=60)

showQuery = Listbox(window)
showQuery.place(x=260,y=310)

displayTables()
showData()
computeLeftover()

window.mainloop()
