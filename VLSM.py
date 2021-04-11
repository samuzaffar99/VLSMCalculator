from tkinter import *
from tkinter import messagebox
from math import log2,ceil, modf
import pandas as pd
import numpy as np
    # ConnectButton.configure(text = "Connect", command=Connect)
    # sendButton.configure(state="disabled")
    # uname.configure(state="normal")

ListCompany=[]
def UpdateEntry():
    global NHosts
    n = int(NHosts.get())
    # Clear Entry Frame
    for widget in EntryFrame.winfo_children():
        widget.destroy()
    # Clear Output Frame
    for widget in OutFrame.winfo_children():
        widget.destroy()
    ListCompany.clear()
    # Column Headers
    Label(configFrame, text='#').grid(row=2,column=0)
    Label(configFrame, text='Company').grid(row=2,column=1)
    Label(configFrame, text='Hosts').grid(row=2,column=2)
    # Add new input fields for each company
    for i in range(n):
        Label(EntryFrame, text=i+1).grid(row=3+i,column=0)
        Hostn = Entry(EntryFrame)
        Hostn.grid(row=3+i,column=1)
        Hostn.insert(END,f"Company {i}")
        Hostsn = Entry(EntryFrame)
        Hostsn.grid(row=3+i,column=2)
        ListCompany.append((Hostn,Hostsn))
    CalcButton = Button(EntryFrame, text='Calculate', width=25, command=CalcSub)
    CalcButton.grid(row=3+n,column=2)

def CalcSub():
    n = int(NHosts.get())
    # Clear Output Frame
    for widget in OutFrame.winfo_children():
        widget.destroy()
    Data = getVLSM(n)
    # for i in range(len(Data.columns)):
    #     Label(OutFrame, text=Data.columns[i]).grid(row=0,column=i)
    # Column Headers
    # ColNames = Data.columns
    # ColNames = ["#","Company","Hosts Needed","Hosts Available","Unused Hosts","Network Address","Slash","Mask","Usable Range","Broadcast","Wildcard"]
    Label(OutFrame, text='#').grid(row=0,column=0)
    Label(OutFrame, text='Company').grid(row=0,column=1)
    Label(OutFrame, text='Hosts Needed').grid(row=0,column=2)
    Label(OutFrame, text='Hosts Available').grid(row=0,column=3)
    Label(OutFrame, text='Unused Hosts').grid(row=0,column=4)
    Label(OutFrame, text='Network Address').grid(row=0,column=5)
    Label(OutFrame, text='Slash').grid(row=0,column=6)
    Label(OutFrame, text='Mask').grid(row=0,column=7)
    Label(OutFrame, text='Usable Range').grid(row=0,column=8)
    Label(OutFrame, text='Broadcast').grid(row=0,column=9)
    Label(OutFrame, text='Wildcard').grid(row=0,column=10)
    # Hosts Needed
    # Hosts Available
    # Unused Hosts
    # Network Address
    # Slash
    # Mask
    # Usable Range
    # Broadcast
    # Wildcard
    # Add output fields for each company
    for i in range(n):
        Label(OutFrame, text=i+1).grid(row=1+i,column=0)
        for j in range(len(Data[i])):
            Label(OutFrame, text=Data[i][j]).grid(row=1+i,column=1+j)
    return
def getVLSM(n):
    NetAdd,Prefix = getNetwork()
    # ColNames = ["#","Company","Hosts Needed","Hosts Available","Unused Hosts","Network Address","Slash","Mask","Usable Range","Broadcast","Wildcard"]
    # SubnetDataF = pd.DataFrame(columns = ColNames)
    # for i in range(n):
    #     SubnetDataF["Company"][i] = ListCompany[i][0].get()
    #     SubnetDataF["Hosts Needed"][i] = int(ListCompany[i][1].get())
    #     HostBits = ceil(log2(SubnetDataF["Hosts Needed"][i]))
    #     SubnetDataF["Hosts Available"][i] = 2**HostBits
    #     SubnetDataF["WastedHosts"][i] = SubnetDataF["Hosts Available"][i]-SubnetDataF["Hosts Needed"][i]
    SubnetData = []
    getClass(NetAdd)
    if(not isValidIP(NetAdd)):
        return
    SubnetData = []
    NetData = [0]*4
    MaskData = [0]*4
    Octet = int(Prefix/8)
    for i in range(Octet):
        NetData[i]=NetAdd[i]
    print(NetData)
    for i in range(n):
        Company = ListCompany[i][0].get()
        NeededHosts = int(ListCompany[i][1].get())
        HostBits = ceil(log2(NeededHosts))
        UnavailCount = 2 # *(4-Octet)
        AvailHosts= 2**HostBits
        ValidHosts = AvailHosts - UnavailCount 
        WastedHosts = ValidHosts-NeededHosts
        IPStart = NetData[3]
        IPEnd = NetData[3]+AvailHosts-1
        Slash = 32-HostBits
        for j in range(Octet):
            MaskData[j]=255
        MaskData[Octet]=sum((2**x) for x in range(8-(Slash%8), 8))
        Mask = '.'.join(map(str,MaskData))
        Network = ".".join(map(str, NetData))
        AvailStart = IPStart+1
        AvailStartStr = '.'.join(map(str,NetData[:3]+[AvailStart]))
        AvailEnd = IPEnd-1
        AvailEndStr = '.'.join(map(str,NetData[:3]+[AvailEnd]))
        Range = AvailStartStr + " - " + AvailEndStr
        BroadCast = IPEnd
        BroadCastStr = '.'.join(map(str,NetData[:3]+[BroadCast]))
        WildCard = AvailHosts-1
        WildCardStr = '.'.join(map(str,[0]*Octet+[WildCard]))
        NetData[3] += AvailHosts
        if(NetData[3]>255):
            print("No more subnets can be made")
        SubnetData.append([Company,NeededHosts,ValidHosts,WastedHosts,Network,Slash,Mask,Range,BroadCastStr,WildCardStr])
    TotalHosts = sum(row[2] for row in SubnetData)
    print("Total Hosts Required: ",TotalHosts)
    print("Total Hosts Available: ",2**(32-Prefix))
    print(SubnetData)
    return SubnetData

def getNetwork():
    NetStr = NetIP.get()
    NetSplit= NetStr.split("/")
    print(NetSplit)
    if(len(NetSplit)!=2):
        print("Invalid Network Address")
        return
    IPStr = NetSplit[0].split(".")
    IP = list(map(int,IPStr))
    Prefix = int(NetSplit[1])
    print(IP,Prefix)
    return IP, Prefix

def getClass(IP):
    classdict = {0:'A',1:'B',2:'C',3:'D',4:'E'}
    classint = -1
    for val in IP:
        if val>0:
            classint+=1
    if(IP[0]>=0):
        classint = max(classint,0)
    elif(IP[0]>=128):
        classint = max(classint,1)
    elif(IP[0]>=192):
        classint = max(classint,2)
    elif(IP[0]>=224):
        classint = max(classint,3)
    elif(IP[0]>=240):
        classint = max(classint,4)
    print("IP Class = ", classdict.get(classint))
    return classint

def isValidIP(IP):
    try:
        if(len(IP) == 4):
            return True
        else:
            return False
    except:
        return

# Quit program confirmation
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        mainWindow.destroy()
# GUI
mainWindow = Tk()
mainWindow.title('VLSM Calculator')

configFrame = Frame(mainWindow)
# Input Network IP and Number of Hosts
Label(configFrame, text='Network Address').grid(row=0,column=0)
NetIP = Entry(configFrame,state="normal")
NetIP.grid(row=0,column=1)
NetIP.insert(END,"192.168.1.0/24")

Label(configFrame, text='Companies').grid(row=1,column=0)
NHosts = Spinbox(configFrame, from_=1, to = 10,state="normal")
NHosts.grid(row=1,column=1)
ChangeButton = Button(configFrame, text='Change', width=25, command=UpdateEntry)
ChangeButton.grid(row=1,column=2)

configFrame.grid(row=0)

# Company Entry Box
EntryFrame = Frame(mainWindow)
EntryFrame.grid(row=4)

# Output Box
OutFrame = Frame(mainWindow)
OutFrame.grid(row=5)

mainWindow.protocol("WM_DELETE_WINDOW", on_closing)
mainWindow.mainloop()