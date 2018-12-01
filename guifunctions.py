#!/usr/bin/env python3

import product
from product import Product
import tkinter as tk
from tkinter import ttk, messagebox
import sqlsetup as sql

#######################################################
    
def makeLabelsAndButtons(self,inventory):
    myfont=("Courier New" , 12)
    for Product in inventory:
        label = "Item: "+Product.getName()+" | Price: $" + str("{:.2f}".format(Product.getPrice())) +" | Stock: " + str(Product.getStock())
        productLabel = ttk.Label(self, font=myfont, text=label).grid(column=0, row=Product.getInd(), sticky=tk.W)
        productLabel


        self.addbuttons = []
        self.revbuttons = []
        
    for i in range(0,sql.getInventorySize()):
        self.addbuttons.append(ttk.Button(self, text="Add To Cart", command= lambda i=i: pullStock(self,i)))
        self.addbuttons[i].grid(column=2, row=i, sticky=tk.W)
        
    for i in range(0,sql.getInventorySize()):
        self.revbuttons.append(ttk.Button(self, text="Take From Cart", command= lambda i=i: returnStock(self,i)))
        self.revbuttons[i].grid(column=3, row=i, sticky=tk.W)
        
        #returnToCartBtn = ttk.Button(self, text="Take From Cart", command= lambda: returnStock(self,returnToCartBtn.grid_info()['row']))
        #returnToCartBtn.grid(column=3, row=i, sticky=tk.W)
    ttk.Button(self, text="View Cart", command= lambda: checkOut(self)).grid(column = 4, row = 0, sticky=tk.W)

def checkOut(self):
        self.Cart = tk.Toplevel(self)
        self.Cart.title("Cart")
        self.Cart.geometry("600x600")
        self.Cart.iconbitmap("icons\cart.ico")
        myfont=("Courier New" , 12)
        cart = []
        emptycart = 0
        grandTotal = 0.00
        cartSize = sql.getInventorySize()
        
        for i in range(0, cartSize):
            cart.append(sql.createProduct(i,"cart"))
            
        for Product in cart:
            if Product.getStock() == 0:
                emptycart += 1
                continue
            else:
                label = ("Item: "+Product.getName()+
                         " | Price: $" + str("{:.2f}".format(Product.getPrice()))+" | Qty: "+
                         str(Product.getStock())+" | Sub-Total: $"+
                         str("{:.2f}".format(Product.getPrice() * Product.getStock())))
                productLabel = ttk.Label(self.Cart, font=myfont, text=label)
                grandTotal += (Product.getPrice() * Product.getStock())
                productLabel.grid(column=0, row=Product.getInd(), sticky=tk.E)

                tax = grandTotal * 0.06
                cartTotalLabel = ttk.Label(self.Cart, text = "Cart Total: $" + str("{:.2f}".format(grandTotal)), font=myfont)
                taxLabel = ttk.Label(self.Cart, text = "Tax: $" + str("{:.2f}".format(tax)), font=myfont)
                grandTotalLabel = ttk.Label(self.Cart, text = "Order Total: $" + str("{:.2f}".format(grandTotal + tax)), font=myfont)

                cartTotalLabel.grid(column=0, row=cartSize+2, sticky=tk.E)
                taxLabel.grid(column=0, row=cartSize+3, sticky=tk.E)
                grandTotalLabel.grid(column=0, row=cartSize+4, sticky=tk.E)

        if emptycart == cartSize:
            emptyLabel = ttk.Label(self.Cart, font='Helvetica', text="Your Cart is Empty")
            confirmButton = ttk.Button(self.Cart, state="disabled", text="Confirm Order")
            emptyLabel.grid(column = 1, row = 8, sticky=tk.W)
            confirmButton.grid(column = 0, row = 9, sticky=tk.W)
        else:
            confirmButton = ttk.Button(self.Cart, text="Confirm Order", command= lambda:confirmOrder(self, cart, grandTotal))
            confirmButton.grid(column = 0, row = cartSize+4, sticky=tk.W)
            

        for child in self.Cart.winfo_children():
            child.grid_configure(padx=5, pady=5)

def confirmOrder(self,cart, grandTotal):
        ordernum = sql.OrderInvoice(cart, grandTotal)
        self.Cart.destroy()
        messagebox.showinfo("Order Success!","Your order confirmation number is " + ordernum + " \n See project directory for text file.")

def pullStock(self,ind):
        inStock = sql.changeStock(ind)
        if inStock == False:
            messagebox.showinfo("Message",sql.getProductName(ind) + " is out of stock")
        else:
            messagebox.showinfo("Message",sql.getProductName(ind) + " was added to your cart")
        refreshGui(self)
            

def returnStock(self,ind):
    inStock = sql.returnStock(ind)
    if inStock == False:
        messagebox.showinfo("Message","No items to return")
    else:
        messagebox.showinfo("Message",sql.getProductName(ind) + " was removed from your cart")
    refreshGui(self)
        

def initGui(self,data_status):
    if data_status == False:
        messagebox.showerror("Error", "No working database in directory!")
        return 
    else:
        ##############
        inventory = []
        inventorySize = sql.getInventorySize()
        ##############
        
        for i in range(0, inventorySize):
            inventory.append(sql.createProduct(i,"inventory"))
        makeLabelsAndButtons(self,inventory)
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

def refreshGui(self):
        for widget in self.winfo_children():
            widget.destroy()
        ##############
        inventory = []
        inventorySize = sql.getInventorySize()
        ##############
        
        for i in range(0, inventorySize):
            inventory.append(sql.createProduct(i,"inventory"))
        makeLabelsAndButtons(self,inventory)
         
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
        

    
