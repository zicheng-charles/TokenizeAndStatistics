import os
from re import I
from tkinter  import *
import tkinter.filedialog
from tkinter.font import Font
from data import Data
import tkinter.messagebox
from threading import Thread
from write import *

if __name__=="__main__":

    """
    读取选定文件下的所有文件
    """
    def readAllFiles(file_dir): 
        print("Read file and obtaining data in...... \n")  
        allData=[]
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                dataPath=root+'\\'+file
                text=[]
                f=open(dataPath,encoding="utf-8")
                text=text+f.readlines()
                allData.append(Data(text,file,dataPath))
        print("Successfully acquired data.\n")
        return allData

    unFinshedData=[]
    finishedData=[]
    """
    创建父窗口，设置大小为1000*700，并禁止缩放
    """
    top=Tk()
    top.geometry("1000x700")
    top.resizable(False,False)

    """
    使用框架将标签，输入框，按钮等组件包含在一起
    """
    filePathFrame=Frame(top,width=800,height=100)
    filePathFrame.pack_propagate(0)
    filePathFrame.pack(padx=1,pady=10)
    filePathLabel=Label(filePathFrame,text="文 件 夹 路 径")
    filePathLabel.pack(side=LEFT,padx=20)
    filePathInput=Entry(filePathFrame,width=60)
    filePathInput.pack(side=LEFT,padx=30)

    """
    选择文件夹按钮的回调函数，该函数通过创建文件对话框获取文件夹路径，并把值赋给输入框
    """
    def selectDirectory():
        file_name = tkinter.filedialog.askdirectory()
        filePathInput.delete(0,"end")
        filePathInput.insert(0,file_name)

    tkinter.Button(filePathFrame, text='选择文件夹', command=selectDirectory).pack(side=LEFT,padx=20)

    """
    确定按钮的回调函数，获取文件夹下所有的text文件并展示到Listbox组件中
    """
    def show():
        theLB.clipboard_clear()
        global unFinshedData
        unFinshedData=readAllFiles(filePathInput.get())
        theLB.delete(0, "end")
        for item in unFinshedData:
            theLB.insert("end", item.getDataName())

    tkinter.Button(filePathFrame, text='确定', command=show).pack(side=LEFT,padx=20)


    listFrame=Frame(top)
    listFrame.pack(side=LEFT,padx=20)

    """
    该组件用于展示文件夹下的所有text文件，可以多选
    """
    theLB = Listbox(listFrame,width=30,height=15,selectmode=EXTENDED)
    theLB.grid(row=0,column=0)

    finishLB = Listbox(listFrame,width=30,height=15,selectmode=EXTENDED)
    finishLB.grid(row=1,column=0,pady=10)

    processingButtonFrame=Frame(top)
    processingButtonFrame.pack(side=LEFT,padx=20)

    sb = Scrollbar(top)
    sb.pack(side="right", fill="y")

    def clear():
        global unFinshedData
        global finishedData
        unFinshedData=[]
        finishedData=[]
        finishLB.delete(0, "end")
        result.delete(1.0, "end")
        theLB.delete(0, "end")
        filePathInput.delete(0,"end")

    tkinter.Button(processingButtonFrame, text='       刷 新       ', command=clear).grid(row=0,column=0,pady=20)

    def processing():
        global unFinshedData
        global finishedData
        items=theLB.curselection()
        if len(items) ==0 :
            if len(unFinshedData)==0:
                tkinter.messagebox.showinfo('提示','该目录下未找到text文件')
            else:
                tkinter.messagebox.showinfo('提示','未选中')
        else:
            temp=[]
            for index in range(len(unFinshedData)):
                if index in items:
                    unFinshedData[index].processing()
                    finishedData.append(unFinshedData[index])
                else :
                    temp.append(unFinshedData[index])
            unFinshedData=temp
            theLB.delete(0, "end")
            for item in unFinshedData:
                theLB.insert("end", item.getDataName())
            finishLB.delete(0, "end")
            for item in finishedData:
                finishLB.insert("end", item.getDataName())

            tkinter.messagebox.showinfo('提示','文本处理完成')    

    tkinter.Button(processingButtonFrame, text='       处 理       ', command=processing).grid(row=1,column=0,pady=20)

    def showTokenizeResult():
        if len(finishLB.curselection()) ==0 and len(finishedData)==0:
            tkinter.messagebox.showinfo('提示','暂无处理结果') 
        elif len(finishLB.curselection()) ==0:
            tkinter.messagebox.showinfo('提示','未选中')
        else:  
            result.delete(1.0, "end")
            for item in finishLB.curselection():
                result.insert("insert",finishedData[item].getTokenizeString())

    tkinter.Button(processingButtonFrame, text='   查 看 分 词   ', command=showTokenizeResult).grid(row=2,column=0,pady=20)

    def showStaticsResult():
        if len(finishLB.curselection()) ==0 and len(finishedData)==0:
            tkinter.messagebox.showinfo('提示','暂无处理结果') 
        elif len(finishLB.curselection()) ==0:
            tkinter.messagebox.showinfo('提示','未选中')
        else:  
            result.delete(1.0, "end")
            allcounts={}
            for item in finishLB.curselection():
                counts=finishedData[item].getStatics()
                for word in counts:
                    if word in allcounts.keys():
                        allcounts[word]+=counts[word]
                    else :
                        allcounts[word]=counts[word]

            wordstr=""
            for word in allcounts:
                wordstr+=word+": "+str(allcounts[word])+"\n"
            result.insert("insert",wordstr)

    tkinter.Button(processingButtonFrame, text='   查 看 统 计   ', command=showStaticsResult).grid(row=3,column=0,pady=20)

    def exportTokenize():
        print(1)
        if len(finishLB.curselection()) ==0 and len(finishedData)==0:
            tkinter.messagebox.showinfo('提示','暂无处理结果') 
        elif len(finishLB.curselection()) ==0:
            tkinter.messagebox.showinfo('提示','未选中')
        else:  
            for item in finishLB.curselection():
                writeText(finishedData[item].getTokenizeString(),filePathInput.get()+"/"+"Tokenize_"+finishedData[item].getDataName())


    tkinter.Button(processingButtonFrame, text='   导 出 分 词   ', command=exportTokenize).grid(row=4,column=0,pady=20)

    def exportStatics():
        if len(finishLB.curselection()) ==0 and len(finishedData)==0:
            tkinter.messagebox.showinfo('提示','暂无处理结果') 
        elif len(finishLB.curselection()) ==0:
            tkinter.messagebox.showinfo('提示','未选中')
        else:  
            allcounts={}
            for item in finishLB.curselection():
                counts=finishedData[item].getStatics()
                for word in counts:
                    if word in allcounts.keys():
                        allcounts[word]+=counts[word]
                    else :
                        allcounts[word]=counts[word]
            writeCSV(allcounts,None,filePathInput.get()+"/"+"Statics")
    tkinter.Button(processingButtonFrame, text='   导 出 统 计   ', command=exportStatics).grid(row=5,column=0,pady=20)

    def exportAll():
        exportTokenize()
        exportStatics()

    tkinter.Button(processingButtonFrame, text='   全 部 导 出   ', command=exportAll).grid(row=6,column=0,pady=20)
    result=Text(top,height=35,yscrollcommand=sb.set,font=Font(size=12))
    sb.config(command=result.yview)
    result.pack(side=LEFT)

    top.mainloop()