#!/usr/bin/env python3
import sqlite3
import os.path
import random
import datetime


import product
from product import Product




def OrderInvoice(cart, grandTotal):
    tax = grandTotal * 0.06
    orderTotal = grandTotal + tax
    orderDate = datetime.datetime.now()
    orderNum = random.randint(100,100*100000)
    file = open("orders\order-confirmation_"+str(orderNum)+".txt","w")

    for Product in cart:
        if Product.getStock() > 0:
            file.write("Item: " + Product.getName() +" Price: $"+ str("{:.2f}".format(Product.getPrice()))
                       +" Qty: "+ str(Product.getStock()) + " Sub-Total: $" + str("{:.2f}".format(Product.getPrice() * Product.getStock())) + "\n")

    file.write('=' * 20)
    file.write("\nCart Total:"+ str("{:>10}".format("$" + str("{:.2f}".format(grandTotal)))))
    file.write("\nTaxes:" + str("{:>15}".format("+$" + str("{:.2f}".format(tax)))))
    file.write("\nOrder Total:" + str("{:>9}".format("$" + str("{:.2f}".format(orderTotal)))))
    file.write("\n")
    file.write('=' * 20)
    file.write("\nOrder Number: " + str(orderNum))
    file.write("\nOrder Date: " + orderDate.strftime('%m-%d-%y'))
    file.close()
    db = sqlite3.connect('database1.db')
    cn = db.cursor()
    cn.execute('update cart set productStock = 0 where productStock > 0')
    db.commit()
    cn.close()
    return str(orderNum)
    
    
    
def createInventory():
    if os.path.isdir('orders'):
        print()
    else:
        path = 'orders'
        os.mkdir(path)
    
    if not os.path.isfile('database1.db'):
        return False
    elif os.path.isfile('database1.db'):
        db = sqlite3.connect('database1.db')
        cn = db.cursor()
        try:
            cn.execute('create table inventory as select * from products')
        except sqlite3.OperationalError:
            db.commit()
            cn.close()
            return
        cn.execute('update inventory set productPrice = round(productPrice,2)')
        cn.execute('create table cart as select * from inventory')
        cn.execute('update cart set productStock = 0')
        db.commit()
        cn.close()
    
    
        
def getInventorySize():
    db = sqlite3.connect('database1.db')
    inventSize = db.execute('select count(*) from inventory')
    rowcount = inventSize.fetchall()[0][0]
    return rowcount

def createProduct(index,table):
        db = sqlite3.connect('database1.db')
        cn = db.cursor()
        cn.execute('select ind from '+table+' where ind=' +str(index))
        productInd = cn.fetchone()[0]
        cn.execute('select productName from '+table+' where ind=' +str(index))
        productName = cn.fetchone()[0]
        cn.execute('select productPrice from '+table+' where ind=' +str(index))
        productPrice = cn.fetchone()[0]
        cn.execute('select productStock from '+table+' where ind=' +str(index))
        productStock = cn.fetchone()[0]
        newProd = Product(productInd,productName,productPrice,productStock)
        cn.close()
        return newProd
    
def changeStock(ind):
    db = sqlite3.connect('database1.db')
    cn = db.cursor()
    cn.execute('select productStock from inventory where ind=' +str(ind))
    if cn.fetchone()[0] == 0:
        return False
    else:
        cn.execute('select productStock from inventory where ind=' +str(ind))
        newStock = cn.fetchone()[0] - 1
        cn.execute('update inventory set productStock=' + str(newStock) + ' where ind=' + str(ind))
        db.commit()
        cn.close()
        db = sqlite3.connect('database1.db')
        cn = db.cursor()
        cn.execute('select productStock from cart where ind=' +str(ind))
        newCartStock = cn.fetchone()[0] + 1
        cn.execute('update cart set productStock=' + str(newCartStock) + ' where ind=' + str(ind))
        db.commit()
        db.close()
        return True

def returnStock(ind):
    db = sqlite3.connect('database1.db')
    cn = db.cursor()
    cn.execute('select productStock from cart where ind=' +str(ind))
    if cn.fetchone()[0] == 0:
        return False
    else:
        cn.execute('select productStock from cart where ind=' +str(ind))
        newStock = cn.fetchone()[0] - 1
        cn.execute('update cart set productStock=' + str(newStock) + ' where ind=' + str(ind))
        db.commit()
        cn.close()
        db = sqlite3.connect('database1.db')
        cn = db.cursor()
        cn.execute('select productStock from inventory where ind=' +str(ind))
        newCartStock = cn.fetchone()[0] + 1
        cn.execute('update inventory set productStock=' + str(newCartStock) + ' where ind=' + str(ind))
        db.commit()
        db.close()
        return True

def getProductName(ind):
    db = sqlite3.connect('database1.db')
    cn = db.cursor()
    cn.execute('select productName from inventory where ind=' + str(ind))
    name = cn.fetchone()[0]
    return name


