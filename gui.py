from tkinter import *

def thing():
   #messagebox.showinfo( None,"Hello Poojan")
   print("start")
   import main as m
   m.start()
   print("end")

root=Tk()
root.title('Jarvis')

root.geometry("1020x507")

bg = PhotoImage(file = "vc.png")
label1 = Label( root, image = bg,bg='coral')
label1.place(x = 0, y =0 )

mybutton=Button(root,text="ACTIVATE JARVIS" , borderwidth = 0,bg='yellow',bd=6, width=14,height=2,command=thing)

mybutton.place(x=449,y=377)

mainloop()



