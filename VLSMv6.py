from tkinter import *
from tkinter import messagebox
from math import log2,ceil
import pandas as pd
import ipaddress

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
    # Add new input fields for each company
    for i in range(n):
        Label(EntryFrame, text=i+1).grid(row=3+i,column=0)
        Hostn = Entry(EntryFrame)
        Hostn.grid(row=3+i,column=1)
        Hostn.insert(END,f"Company {i}")
        ListCompany.append(Hostn)
    CalcButton = Button(EntryFrame, text='Calculate', width=25, command=CalcSub)
    CalcButton.grid(row=3+n,column=2)

def CalcSub():
    n = int(NHosts.get())
    # Clear Output Frame
    for widget in OutFrame.winfo_children():
        widget.destroy()
    
    Data = getVLSMv6(n)
    Label(OutFrame, text='#').grid(row=0,column=0)
    for i in range(len(Data.columns)):
        Label(OutFrame, text=Data.columns[i]).grid(row=0,column=i+1)

    for i in range(n):
        Label(OutFrame, text=i+1).grid(row=1+i,column=0)
        for j in range(len(Data.columns)):
            Label(OutFrame, text=Data.iloc[i,j]).grid(row=1+i,column=1+j)
    return

def getVLSMv6(n):
    try:
        network = ipaddress.IPv6Network(NetIP.get())
    except:
        print("Invalid ipv6 address entered")
    print(network.prefixlen)
    print(network.exploded)
    subprefix = network.prefixlen+ceil(log2(n))
    print("Subnet Prefix: ", subprefix)
    if(subprefix>127):
        print("Cannot divide into subnets")
        return
    
    ColNames = ["Company","Total Addresses","Network Address","Slash","Subnet Mask","Broadcast","Wildcard"]
    SubnetDF = pd.DataFrame(columns = ColNames,index=range(n))

    ipAddress = network.network_address

    for i in range(n):
        SubnetDF["Company"][i] = ListCompany[i].get()
        SubnetDF["Total Addresses"][i] = 2**(128-subprefix)
        print("Total Addresses: ", 2**(128-subprefix))
        SubnetDF["Slash"][i] = subprefix

        subnet = ipaddress.IPv6Network(str(ipAddress)+f"/{SubnetDF.Slash[i]}", False)

        SubnetDF["Network Address"][i] = subnet.network_address
        print("Network Address: ", subnet.network_address) 

        SubnetDF["Subnet Mask"][i] = subnet.netmask
        print("Subnet Mask: ", subnet.netmask)

        SubnetDF["Broadcast"][i] = subnet.broadcast_address
        print("Broadcast Address: ", subnet.broadcast_address)

        SubnetDF["Wildcard"][i] = subnet.hostmask
        print("Wildcard Address: ", subnet.hostmask)

        ipAddress += SubnetDF["Total Addresses"][i]
        print()
    print(SubnetDF.head())
    return SubnetDF






# Quit program confirmation
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        mainWindow.destroy()
# GUI
mainWindow = Tk()
mainWindow.title('VLSM Calculator (ipv6)')

configFrame = Frame(mainWindow)
# Input Network IP and Number of Hosts
Label(configFrame, text='Network Address').grid(row=0,column=0)
NetIP = Entry(configFrame,state="normal")
NetIP.grid(row=0,column=1)
NetIP.insert(END,"2001:db8::/32")

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