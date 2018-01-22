from tkinter import *
from tkinter import *
import _thread
import socket
import win32gui
import os
import ctypes
ctypes.windll.shell32.IsUserAnAdmin()
WindowTitle = 'JChat v0.1 - Client'
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = 'localhost'
PORT = 8011
conn=''
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
global clients
clients=[]
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
    def prints(self):
     mtext=text.get("1.0",END)
     mtext='1_'+mtext
     print(mtext)
     text.delete("1.0",END)
     label=Label(self.interior,text=mtext,bg="WHITE",bd=1,fg="BLACK",wraplength=300,justify=LEFT,padx=0,pady=0)
     pad=Frame(self.interior,height=10,width=500,bg="#fff799")
     pad.pack()
     label.pack(anchor=W)
     label.config(highlightbackground="BLUE")
     label.config(highlightthickness=1)
     for c in clients:
         c[0].sendall(mtext.encode('utf-8'))
     if(self.interior.winfo_reqheight()>440):
         size=(self.interior.winfo_reqwidth()-520,self.interior.winfo_reqheight()-440,self.interior.winfo_reqwidth(),self.interior.winfo_reqheight()+60)
         self.canvas.config(scrollregion="%s %s %s %s" % size)
    def printsrecv(self,x):
        label=Label(self.interior,text=x,bg="WHITE",bd=1,fg="BLACK",wraplength=300,justify=LEFT,padx=0,pady=0)
        pad=Frame(self.interior,height=10,width=500,bg="#fff799")
        pad.pack()
        label.pack(anchor=E)
        label.config(highlightbackground="BLUE")
        label.config(highlightthickness=1)
        if(self.interior.winfo_reqheight()>440):
         size=(self.interior.winfo_reqwidth()-520,self.interior.winfo_reqheight()-440,self.interior.winfo_reqwidth(),self.interior.winfo_reqheight()+60)
         self.canvas.config(scrollregion="%s %s %s %s" % size)
def LoadConnectionInfo(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            ChatLog.insert(END, EntryText+'\n')
            frame.prints()
            ChatLog.delete("1.0",END)
def GetConnected():
    global conn
    global addr
    while 1:
        conn, addr = s.accept()
        clients.append([conn,addr])
        LoadConnectionInfo(text, str(addr) + ' is Online')
        _thread.start_new_thread(dostuff,(conn,))
    s.close()
s.listen(5)
def dostuff(conn):
    while(1):
        try:
            data = conn.recv(1024).decode('utf-8')
            print(data)
        except:
            LoadConnectionInfo(text, '\n [ Your partner has disconnected ]\n [ Waiting for him to connect..] \n  ')
            GetConnected()
        if(data!=''):
            #print(data)
            actionNo,msg=data.split('_')
            print(actionNo)
            print(msg)
            if actionNo=='1':
                senddata(conn,msg)
                #frame.printsrecv(msg)
            if actionNo=='2':
                cli=[]
                for c in clients:
                    cli.append(str(c[1]))
                print(cli)
                msg1='*'.join(cli)
                msg1='2_'+msg1
                #LoadConnectionInfo(text, msg1)
                #print(msg1)
                conn.sendall(msg1.encode('utf-8'))
                
def senddata(conn,data):
    for c in clients:
        if(c[0]==conn):
            data1=str(c[1])+'\n'+data
            data1='1_'+data1
    for c in clients:
        if(c[0]==conn):
            continue
        else:
            c[0].sendall(data1.encode('utf-8'))
root = Tk()
ment=StringVar()
frame=VerticalScrollBar(root)
root.geometry("500x600+300+300")
frame.pack()
text = Text(root,width=45,height=5)
text.pack(side=LEFT)
button=Button(root,text="Send",bg="#fff799",fg="WHITE",height=1,command=frame.prints)
button.pack(side=LEFT)
for i in range(5):
        _thread.start_new_thread(GetConnected,())
root.mainloop()
