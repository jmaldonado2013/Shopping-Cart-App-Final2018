#!/usr/bin/env python3

class Product:
    def __init__(self,ind,name,price,stock):
        self.ind = ind
        self.name = name
        self.price = price
        self.stock = stock

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getStock(self):
        return self.stock

    def getInd(self):
        return self.ind
