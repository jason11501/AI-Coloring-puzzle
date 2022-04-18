from tkinter import*
from tkinter import ttk
import tkinter.messagebox
class ConnectorDB:
    def __init__(self,root):
        self.root = root
        titlespace = " "
        self.root.title(102* titlespace + "Coloring Puzzle")
        self.root.geometry("1280x800+300+0")
        self.root.resizable(width = False, height = False)

        MainFrame = Frame(self.root, bd=10,width=700,height=1000,relief=RIDGE,bg='cadet blue')
        MainFrame.grid()

        TitleFrame=Frame(MainFrame,bd=7,width=770,height=100,relief=RIDGE)
        TitleFrame.grid(row=0,column=0)
        TopFrame3=Frame(MainFrame,bd=5,width=770,height=500,relief=RIDGE)
        TopFrame3.grid(row=1,column=0)

        LeftFrame=Frame(TopFrame3,bd=5,width=770,height=400,padx=2,bg='cadet blue',relief=RIDGE)
        LeftFrame.pack(side=LEFT)
        LeftFrame1=Frame(LeftFrame,bd=5,width=600,height=180,padx=2,pady=4,relief=RIDGE)
        LeftFrame1.pack(side=TOP,padx=0,pady=0)

        RightFrame1=Frame(TopFrame3,bd=5,width=100,height=400,padx=2,bg='cadet blue',relief=RIDGE)
        RightFrame1.pack(side=RIGHT)
        RightFrame1a=Frame(RightFrame1,bd=5,width=90,height=300,padx=2,pady=2,relief=RIDGE)
        RightFrame1a.pack(side=TOP)

        id=StringVar()
        time=StringVar()
        nameteam1=StringVar()
        nameteam2=StringVar()
        score=StringVar()
        goal=StringVar()
        redcard=StringVar()
        yellowcard=StringVar()

        def DisplayData():
            mydb = pymysql.connect(host="127.0.0.1",username="root",password="alpine",database ="livescore")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT FROM livescore")
            myresult = mycursor.fetchall()
            if len(myresult)!=0:
                self.livescore_records.delete(*self.livescore_records.get_children())
                for row in result:
                    self.livescore_records.insert('',END,values=row)
            mydb.commit()
            mydb.close()
        def search():
            peli.make_boxes()
            peli.make_numbers()
            peli.solve_step_1()
            peli.solve_step_2()
            res=""
            for i in range(h):
                for j in range(w):
                    res+=str(peli.boxes[i][j].value)
                res+='\n'
            tkinter.messagebox.showinfo(peli.check_table(),res)

        self.lbltitle=Label(TitleFrame, font=('arial',40,'bold'),text="Coloring Puzzle",bd=7)
        self.lbltitle.grid(row=0,column=0,padx=132)

        self.lblid=Label(LeftFrame1, font=('arial',12,'bold'),text="Path",bd=7)
        self.lblid.grid(row=1,column=0,sticky=W,padx=5)
        self.entid=Entry(LeftFrame1, font=('arial',12,'bold'),bd=5,width=44,justify='left',textvariable=id)
        self.entid.grid(row=1,column=1,sticky=W,padx=5)
        
        self.lblnameteam1=Label(LeftFrame1, font=('arial',12,'bold'),text="Step",bd=7)
        self.lblnameteam1.grid(row=2,column=0,sticky=W,padx=5)
        
        self.lblnameteam2=Label(LeftFrame1, font=('arial',12,'bold'),text="Heuristic",bd=7)
        self.lblnameteam2.grid(row=3,column=0,sticky=W,padx=5)
#         self.lblStep=Label(LeftFrame1, font=('arial',12,'bold'),text="Step",bd=7)
#         self.lblStep.grid(row=1,column=0,sticky=W,padx=5)
        
#         self.lblHeuristic=Label(LeftFrame1, font=('arial',12,'bold'),text="Heuristic",bd=7)
#         self.lblHeuristic.grid(row=1,column=0,sticky=W,padx=5)
        
#         self.lblid=Label(LeftFrame1, font=('arial',12,'bold'),text="Path",bd=7)

        scroll_x=Scrollbar(LeftFrame,orient=HORIZONTAL)
        self.livescore_records=ttk.Treeview(LeftFrame,height=14,columns=("Puzzle"),xscrollcommand=scroll_x.set)
        
#         self.livescore_records.heading("id", text="Puzzle")

        self.livescore_records['show']='headings'

#         self.livescore_records.column("id", width=70)

        self.livescore_records.pack(fill=BOTH,expand=1)
#         self.livescore_records.bind("<ButtonRelease-1>",livescoreInfo)

        self.btnSearch=Button(RightFrame1a, font=('arial',16,'bold'),text="Play",bd=4,pady=1,padx=24,width=8,height=2,command=search).grid(row=0,column=0,padx=1)

root = Tk()
application =ConnectorDB(root)
root.mainloop()