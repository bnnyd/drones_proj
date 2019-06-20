#!/usr/bin/env python3
from tkinter import *
from .general_common import States

class Screen():
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, height = 410, width = 150)
        self.states_rec = {}
        self.states_rec[States.IDLE] = self.canvas.create_rectangle(10, 10, 140, 50, fill="#C2B6BF")
        self.canvas.create_text((70, 30), text="IDLE")
        self.states_rec[States.STAND_BY] = self.canvas.create_rectangle(10, 60, 140, 100, fill="#C2B6BF")
        self.canvas.create_text((75, 80), text="STAND-BY")
        self.states_rec[States.MANUAL_CONTROL] = self.canvas.create_rectangle(10, 110, 140, 150, fill="#C2B6BF")
        self.canvas.create_text((75, 130), text="MANUAL-CONTROL")
        self.states_rec[States.RED_CIRCLE] = self.canvas.create_rectangle(10, 160, 140, 200, fill="#C2B6BF")
        self.canvas.create_text((75, 180), text="RED CIRCLE")
        self.states_rec[States.UP] = self.canvas.create_rectangle(10, 210, 140, 250, fill="#C2B6BF")
        self.canvas.create_text((70, 230), text="TAKE-OFF")
        self.states_rec[States.LINE] = self.canvas.create_rectangle(10, 260, 140, 300, fill="#C2B6BF")
        self.canvas.create_text((75, 280), text="LINE ANGLE")
        self.states_rec[States.STOP] = self.canvas.create_rectangle(10, 310, 140, 350, fill="#C2B6BF")
        self.canvas.create_text((70, 330), text="LANDING")
        self.states_rec[States.STOP] = self.canvas.create_rectangle(10, 360, 140, 400, fill="#C2B6BF")
        self.canvas.create_text((70, 380), text="STOP")

        self.canvas.pack()
        self.root.update()

    def update_state(self, state):
        for rec in self.states_rec:
            self.canvas.itemconfig(self.states_rec[rec], fill="#C2B6BF")
        try:
            self.canvas.itemconfig(self.states_rec[state], fill='#80FF00')
        except:
            pass
        self.root.update()
