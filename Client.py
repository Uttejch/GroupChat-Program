from tkinter import *
import _thread
import socket
import win32gui
WindowTitle = 'JChat v0.1 - Client'
HOST = 'localhost'
PORT = 8011
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
class VerticalScrollBar(Frame):
    def __init__(self,parent,*args,**kw):
        Frame.__init__(self,parent,*args,**kw)
        vscrollbar=Scrollbar(self,orient=VERTICAL)
        vscrollbar.pack(fill=Y,side=RIGHT,expand=FALSE)
        self.canvas=canvas=Canvas(self,width=500,height=500,bd=0,bg="#fff799",highlightthickness=0,yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT,fill=BOTH,expand=TRUE)
        vscrollbar.config(command=canvas.yview)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        self.interior=interior=Frame(canvas,width=520,bg="#fff799")
        interior_id=canvas.create_window(0,0,window=interior,anchor=NW)
        def _configure_interior(event):
            size=(interior.winfo_reqwidth(),interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth()!=canvas.winfo_reqwidth():
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>',_configure_interior)
        def _configure_canvas(event):
            if(interior.winfo_reqwidth()!=canvas.winfo_reqwidth()):
                canvas.itemconfigure(interior_id,width=canvas.winfo_width())
        canvas.bind('<Configure>',_configure_canvas)
    def printsrecv(self,x):
        actionNo,msg=x.split('_')
        if actionNo=='1':
            label=Label(self.interior,text=msg,bg="WHITE",bd=1,fg="BLACK",wraplength=300,justify=LEFT,padx=0,pady=0)
            pad=Frame(self.interior,height=10,width=500,bg="#fff799")
            pad.pack()
            label.pack(anchor=E)
            label.config(highlightbackground="BLUE")
            label.config(highlightthickness=1)
            if(self.interior.winfo_reqheight()>440):
             size=(self.interior.winfo_reqwidth()-520,self.interior.winfo_reqheight()-440,self.interior.winfo_reqwidth(),self.interior.winfo_reqheight()+60)
             self.canvas.config(scrollregion="%s %s %s %s" % size)
        
    def prints(self):
     mtext=text.get("1.0",END)
     text.delete("1.0",END)
     label=Label(self.interior,text=mtext,bg="WHITE",bd=1,fg="BLACK",wraplength=300,justify=LEFT,padx=0,pady=0)
     pad=Frame(self.interior,height=10,width=500,bg="#fff799")
     pad.pack()
     label.pack(anchor=W)
     label.config(highlightbackground="BLUE")
     label.config(highlightthickness=1)
     action='1_'
     mtext=action+mtext
     #print(mtext)
     s.sendall(mtext.encode())
     if(self.interior.winfo_reqheight()>440):
         size=(self.interior.winfo_reqwidth()-520,self.interior.winfo_reqheight()-440,self.interior.winfo_reqwidth(),self.interior.winfo_reqheight()+60)
         self.canvas.config(scrollregion="%s %s %s %s" % size)
     return

root = Tk()
ment=StringVar()
frame=VerticalScrollBar(root)
root.geometry("500x600+300+300")
frame.pack()
global text
text = Text(root,width=45,height=5)
text.pack(side=LEFT)
button=Button(root,text="Send",bg="#fff799",fg="WHITE",command=frame.prints)
button.pack(side=LEFT)
def LoadConnectionInfo(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            ChatLog.insert(END, EntryText+'\n')
            frame.prints()
            ChatLog.delete("1.0",END)
def FlashMyWindow(title):
    ID = win32gui.FindWindow(None, title)
    win32gui.FlashWindow(ID,True)
def ReceiveData():
    try:
        s.connect((HOST, PORT))
        #LoadConnectionInfo(text, '[ Succesfully connected ]\n---------------------------------------------------------------')
    except:
        LoadConnectionInfo(text, '[ Unable to connect ]')
        return
    
    while 1:
        try:
            data = s.recv(1024).decode()
        except:
            LoadConnectionInfo(text, '\n [ Your partner has disconnected ] \n')
            break
        if data != '':
            frame.printsrecv(data)
            print(data)
            if root.focus_get() == None:
                FlashMyWindow(WindowTitle)
                
        else:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break

_thread.start_new_thread(ReceiveData,())
root.mainloop()
