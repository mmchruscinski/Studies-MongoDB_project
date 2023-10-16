import tkinter as tk
from pymongo import MongoClient

def ButtonSearch(st1, st2):
    st1_sel = st1.get()
    st2_sel = st2.get()
    print(st1_sel)
    print(st2_sel)