import ENL_win
from ENL_win import *
import ENL_win_globals
from ENL_win_globals import *
from tkinter import *
from tkinter import ttk
import threading
from binascii import hexlify
import mysql.connector
import time
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta

#########################################
#Setup Database setup for the first time#
#########################################
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Hugo1983522",
    database = "enl",
)
my_cursor = mydb.cursor()
#my_cursor.execute("DROP TABLE `enl`.`enl_data1`;")
my_cursor.execute("CREATE DATABASE IF NOT EXISTS enl")
my_cursor.execute("""CREATE TABLE IF NOT EXISTS enl_data1 (
                time DATETIME, 
                eco_heat_mode_B0 VARCHAR(255),
                eco_heat_status_B2 VARCHAR(255),
                eco_heat_temp_set_B3 INTEGER(10),
                eco_tank_mode_B6 VARCHAR(255),
                eco_heat_temp_C1 INTEGER(10),
                eco_supply_status_C3 VARCHAR(255),
                eco_supply_temp_set_D1 INTEGER(10),
                eco_bath_temp_set_D3 INTEGER(10),
                eco_water_remain_E1 INTEGER(10),
                eco_tank_capacity_E2 INTEGER(10),
                eco_bath_mode_E3 VARCHAR(255),
                eco_bath_status_EA VARCHAR(255),
                eco_cum_power_85 INTEGER(10),
                bat_status_CF VARCHAR(255),
                bat_instant_power_D3 INTEGER(10),
                bat_cum_dis_D6 INTEGER(10),
                bat_cum_chr_D8 INTEGER(10),
                bat_mode_DA VARCHAR(255),
                bat_remain_E2 INTEGER(10),
                bat_remain_E4 INTEGER(10),
                bat_health_E5 INTEGER(10),
                air1_status_80 VARCHAR(255),
                air1_mode_B0 VARCHAR(255),
                air1_temp_set_B3 INTEGER(10),
                air1_room_temp_BB INTEGER(10),
                air1_outdoor_temp_BE INTEGER(10),
                air1_instant_power_84 INTEGER(10),
                air1_cum_power_85 INTEGER(10),
                air2_status_80 VARCHAR(255),
                air2_mode_B0 VARCHAR(255),
                air2_temp_set_B3 INTEGER(10),
                air2_room_temp_BB INTEGER(10),
                air2_outdoor_temp_BE INTEGER(10),
                air2_cum_power_85 INTEGER(10),          
                pcs_instant_gen_E0 INTEGER(10),
                pcs_cum_gen_E1 INTEGER(10),
                pcs_cum_sold_E3 INTEGER(10),
                pv_instant_E7 FLOAT(8),
                pv_instant_E8 VARCHAR(255),
                pv_cum_import_EA FLOAT(8),
                pv_cum_export_EB FLOAT(8),
                pv_cum_import_E0 FLOAT(8),
                pv_cum_export_E3 FLOAT(8),
                rb_instant_E7 FLOAT(8),
                rb_instant_E8 VARCHAR(255),
                rb_cum_import_EA FLOAT(8),
                rb_cum_export_EB FLOAT(8),
                rb_cum_import_E0 FLOAT(8),
                rb_cum_export_E3 FLOAT(8),                      
                record_id INTEGER AUTO_INCREMENT PRIMARY key
                )
                """)
my_cursor.close()
mydb.close()

# List for updating the datebase
db_buff = {}

root = Tk()
root.title('ENL Control Panel')
root.geometry("1100x920")
frame_upper = LabelFrame(root, padx=5, pady=5, border=0)
frame_upper.pack(padx=10, pady=10, anchor=W)
frame_lower = LabelFrame(root, padx=5, pady=5, border=0)
frame_lower.pack(padx=10, pady=10, anchor=W)
tabControl = ttk.Notebook(frame_lower)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)
tab6 = ttk.Frame(tabControl)
tab7 = ttk.Frame(tabControl)

meterID = StringVar()
meterID.set("J220006476")

# Create lower part of the user interface
tabControl.add(tab1, text ='Eco-Cute')
tabControl.add(tab2, text ='Battery')
tabControl.add(tab3, text ='Air-Con1')
tabControl.add(tab4, text ='Air-Con2')
tabControl.add(tab5, text ='PCS')
tabControl.add(tab6, text ='PV')
tabControl.add(tab7, text ='Utility')
tabControl.grid(row=3, column=0, columnspan=7, pady=10, sticky=E+W+N+S)

# EPC list for eco-cute
# 0xB0
b0 = StringVar()
b0.set("N/A")
epc_b0 = ttk.Entry(tab1, textvariable = b0, width=20)
epc_b0.grid(row=0, column=1, padx=10, sticky=E)
B0_Button = ttk.Button(tab1, text="Auto", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.b0_cmd1.encode()).decode()))
B0_Button.grid(row=0, column=2, padx=10)
B0_Button2 = ttk.Button(tab1, text="Stopped", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.b0_cmd2.encode()).decode()))
B0_Button2.grid(row=0, column=3, padx=10)
B0_Button3 = ttk.Button(tab1, text="Non-Auto", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.b0_cmd3.encode()).decode()))
B0_Button3.grid(row=0, column=4, padx=10)
B0_Lable = ttk.Label(tab1, text="Automatic water heating setting - 0xB0")
B0_Lable.grid(column = 0, row = 0, padx = 10, pady = 10, sticky=W)
# 0xB2
global epc_b2
b2 = StringVar()
b2.set("N/A")
epc_b2 = ttk.Entry(tab1, textvariable = b2, width=20)
epc_b2.grid(row=1, column=1, padx=10, sticky=E)
B2_Lable = ttk.Label(tab1, text="Water heater status - 0xB2")
B2_Lable.grid(column = 0, row = 1, padx = 10, pady = 10, sticky=W)
global epc_b3
b3 = StringVar()
b3.set("N/A")
epc_b3 = ttk.Entry(tab1, textvariable = b3, width=20)
epc_b3.grid(row=2, column=1, padx=10, sticky=E)
B3_Button = ttk.Button(tab1, text="Set", command=lambda:set_temp("0x026B01", "B3"))
B3_Button.grid(row=2, column=2, padx=10)
B3_Lable = ttk.Label(tab1, text="Water heating temperature setting - 0xB3")
B3_Lable.grid(column = 0, row = 2, padx = 10, pady = 10, sticky=W)
global epc_b6
b6 = StringVar()
b6.set("N/A")
epc_b6 = ttk.Entry(tab1, textvariable = b6, width=20)
epc_b6.grid(row=3, column=1, padx=10, sticky=E)
B6_Button = ttk.Button(tab1, text="Standard", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.b6_cmd1.encode()).decode()))
B6_Button.grid(row=3, column=2, padx=10)
B6_Button2 = ttk.Button(tab1, text="Saving", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.b6_cmd2.encode()).decode()))
B6_Button2.grid(row=3, column=3, padx=10)
B6_Button3 = ttk.Button(tab1, text="Extra", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.b6_cmd3.encode()).decode()))
B6_Button3.grid(row=3, column=4, padx=10)
B6_Lable = ttk.Label(tab1, text="Tank operation mode setting - 0xB6")
B6_Lable.grid(column = 0, row = 3, padx = 10, pady = 10, sticky=W)
global epc_c0
c0 = StringVar()
c0.set("N/A")
epc_c0 = ttk.Entry(tab1, textvariable = c0, width=20)
epc_c0.grid(row=4, column=1, padx=10, sticky=E)
C0_Button = ttk.Button(tab1, text="Permit", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.c0_cmd1.encode()).decode()))
C0_Button.grid(row=4, column=2, padx=10)
C0_Button2 = ttk.Button(tab1, text="Not permit", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.c0_cmd2.encode()).decode()))
C0_Button2.grid(row=4, column=3, padx=10)
C0_Lable = ttk.Label(tab1, text="Daytime reheating permission setting - 0xC0")
C0_Lable.grid(column = 0, row = 4, padx = 10, pady = 10, sticky=W)
global epc_c1
c1 = StringVar()
c1.set("N/A")
epc_c1 = ttk.Entry(tab1, textvariable = c1, width=20)
epc_c1.grid(row=5, column=1, padx=10, sticky=E)
C1_Lable = ttk.Label(tab1, text="Measured temperature of water in water heater - 0xC1")
C1_Lable.grid(column = 0, row = 5, padx = 10, pady = 10, sticky=W)
global epc_c3
c3 = StringVar()
c3.set("N/A")
epc_c3 = ttk.Entry(tab1, textvariable = c3, width=20)
epc_c3.grid(row=6, column=1, padx=10, sticky=E)
C3_Lable = ttk.Label(tab1, text="Hot water supply status - 0xC3")
C3_Lable.grid(column = 0, row = 6, padx = 10, pady = 10, sticky=W)
global epc_d1
d1 = StringVar()
d1.set("N/A")
epc_d1 = ttk.Entry(tab1, textvariable = d1, width=20)
epc_d1.grid(row=7, column=1, padx=10, sticky=E)
D1_Button = ttk.Button(tab1, text="Set", command=lambda:set_temp("0x026B01", "D1"))
D1_Button.grid(row=7, column=2, padx=10)
D1_Lable = ttk.Label(tab1, text="Temperature of supplied water setting - 0xD1")
D1_Lable.grid(column = 0, row = 7, padx = 10, pady = 10, sticky=W)
global epc_d3
d3 = StringVar()
d3.set("N/A")
epc_d3 = ttk.Entry(tab1, textvariable = d3, width=20)
epc_d3.grid(row=8, column=1, padx=10, sticky=E)
D3_Button = ttk.Button(tab1, text="Set", command=lambda:set_temp("0x026B01", "D3"))
D3_Button.grid(row=8, column=2, padx=10)
D3_Lable = ttk.Label(tab1, text="Bath water temperature setting - 0xD3")
D3_Lable.grid(column = 0, row = 8, padx = 10, pady = 10, sticky=W)
global epc_e1
e1 = StringVar()
e1.set("N/A")
epc_e1 = ttk.Entry(tab1, textvariable = e1, width=20)
epc_e1.grid(row=9, column=1, padx=10, sticky=E)
E1_Lable = ttk.Label(tab1, text="Measured amount of water remaining in tank - 0xE1")
E1_Lable.grid(column = 0, row = 9, padx = 10, pady = 10, sticky=W)
global epc_e2
e2 = StringVar()
e2.set("N/A")
epc_e2 = ttk.Entry(tab1, textvariable = e2, width=20)
epc_e2.grid(row=10, column=1, padx=10, sticky=E)
E2_Lable = ttk.Label(tab1, text="Tank capacity - 0xE2")
E2_Lable.grid(column = 0, row = 10, padx = 10, pady = 10, sticky=W)
global epc_e3
e3 = StringVar()
e3.set("N/A")
epc_e3 = ttk.Entry(tab1, textvariable = e3, width=20)
epc_e3.grid(row=11, column=1, padx=10, sticky=E)
E3_Button = ttk.Button(tab1, text="ON", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.e3_cmd1.encode()).decode()))
E3_Button.grid(row=11, column=2, padx=10)
E3_Button = ttk.Button(tab1, text="OFF", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.e3_cmd2.encode()).decode()))
E3_Button.grid(row=11, column=3, padx=10)
E3_Lable = ttk.Label(tab1, text="Automatic bath water heating mode setting - 0xE3")
E3_Lable.grid(column = 0, row = 11, padx = 10, pady = 10, sticky=W)
global epc_ea
ea = StringVar()
ea.set("N/A")
epc_ea = ttk.Entry(tab1, textvariable = ea, width=20)
epc_ea.grid(row=12, column=1, padx=10, sticky=E)
EA_Lable = ttk.Label(tab1, text="Bath operation status monitor - 0xEA")
EA_Lable.grid(column = 0, row = 12, padx = 10, pady = 10, sticky=W)
global epc_e5
e5 = StringVar()
e5.set("N/A")
epc_e5 = ttk.Entry(tab1, textvariable = e5, width=20)
epc_e5.grid(row=13, column=1, padx=10, sticky=E)
E5_Button = ttk.Button(tab1, text="ON", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.e5_cmd1.encode()).decode()))
E5_Button.grid(row=13, column=2, padx=10)
E5_Button2 = ttk.Button(tab1, text="OFF", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.e5_cmd2.encode()).decode()))
E5_Button2.grid(row=13, column=3, padx=10)
E5_Lable = ttk.Label(tab1, text="Manual bath hot water addition function setting - 0xE5")
E5_Lable.grid(column = 0, row = 13, padx = 10, pady = 10, sticky=W)
global epc_e6
e6 = StringVar()
e6.set("N/A")
epc_e6 = ttk.Entry(tab1, textvariable = e6, width=20)
epc_e6.grid(row=14, column=1, padx=10, sticky=E)
E6_Button = ttk.Button(tab1, text="ON", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.e6_cmd1.encode()).decode()))
E6_Button.grid(row=14, column=2, padx=10)
E6_Button2 = ttk.Button(tab1, text="OFF", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.e6_cmd2.encode()).decode()))
E6_Button2.grid(row=14, column=3, padx=10)
E6_Lable = ttk.Label(tab1, text="Manual lukewarm water temperature lowering function setting - 0xE6")
E6_Lable.grid(column = 0, row = 14, padx = 10, pady = 10, sticky=W)
global epc_ee
ee = StringVar()
ee.set("N/A")
epc_ee = ttk.Entry(tab1, textvariable = ee, width=20)
epc_ee.grid(row=15, column=1, padx=10, sticky=E)
EE_Button = ttk.Button(tab1, text="Set", command=lambda:set_temp("0x026B01", "EE"))
EE_Button.grid(row=15, column=2, padx=10)
EE_Lable = ttk.Label(tab1, text="Bath water volume setting 3 - 0xEE")
EE_Lable.grid(column = 0, row = 15, padx = 10, pady = 10, sticky=W)
global epc_85
eco_85 = StringVar()
eco_85.set("N/A")
epc_85 = ttk.Entry(tab1, textvariable = eco_85, width=20)
epc_85.grid(row=16, column=1, padx=10, sticky=E)
eco_85_Lable = ttk.Label(tab1, text="Measured cumulative power consumption - 0x85")
eco_85_Lable.grid(column = 0, row = 16, padx = 10, pady = 10, sticky=W)

# EPC list for Battery
# 0xAA
global battery_epc_aa
battery_aa = StringVar()
battery_aa.set("N/A")
epc_battery_aa = ttk.Entry(tab2, textvariable = battery_aa, width=20)
epc_battery_aa.grid(row=0, column=3, padx=10, sticky=E)
battery_AA_Button = ttk.Button(tab2, text="Set", command=lambda:set_temp("0x027D01", "AA"))
battery_AA_Button.grid(row=0, column=4, padx=10)
battery_AA_Lable = ttk.Label(tab2, text="AC charge amount setting value - 0xAA")
battery_AA_Lable.grid(column = 0, row = 0, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xAB
global battery_epc_ab
battery_ab = StringVar()
battery_ab.set("N/A")
battery_epc_ab = ttk.Entry(tab2, textvariable = battery_ab, width=20)
battery_epc_ab.grid(row=1, column=3, padx=10, sticky=E)
battery_AB_Button = ttk.Button(tab2, text="Set", command=lambda:set_temp("0x027D01", "AB"))
battery_AB_Button.grid(row=1, column=4, padx=10)
battery_AB_Lable = ttk.Label(tab2, text="AC discharge amount setting value - 0xAB")
battery_AB_Lable.grid(column = 0, row = 1, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xCF
global battery_epc_cf
battery_cf = StringVar()
battery_cf.set("N/A")
battery_epc_cf = ttk.Entry(tab2, textvariable = battery_cf, width=20)
battery_epc_cf.grid(row=2, column=3, padx=10, sticky=E)
battery_CF_Lable = ttk.Label(tab2, text="Working operation status - 0xCF")
battery_CF_Lable.grid(column = 0, row = 2, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xD3
global battery_epc_d3
battery_d3 = StringVar()
battery_d3.set("N/A")
battery_epc_d3 = ttk.Entry(tab2, textvariable = battery_d3, width=20)
battery_epc_d3.grid(row=3, column=3, padx=10, sticky=E)
battery_D3_Lable = ttk.Label(tab2, text="Measured instantaneous charging/discharging electric power - 0xD3")
battery_D3_Lable.grid(column = 0, row = 3, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xD6
global battery_epc_d6
battery_d6 = StringVar()
battery_d6.set("N/A")
battery_epc_d6 = ttk.Entry(tab2, textvariable = battery_d6, width=20)
battery_epc_d6.grid(row=4, column=3, padx=10, sticky=E)
battery_D6_Lable = ttk.Label(tab2, text="Measured cumulative discharging electric energy - 0xD6")
battery_D6_Lable.grid(column = 0, row = 4, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xD8
global battery_epc_d8
battery_d8 = StringVar()
battery_d8.set("N/A")
battery_epc_d8 = ttk.Entry(tab2, textvariable = battery_d8, width=20)
battery_epc_d8.grid(row=5, column=3, padx=10, sticky=E)
battery_D8_Lable = ttk.Label(tab2, text="Measured cumulative charging electric energy - 0xD8")
battery_D8_Lable.grid(column = 0, row = 5, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xDA
global battery_epc_da
battery_da = StringVar()
battery_da.set("N/A")
battery_epc_da = ttk.Entry(tab2, textvariable = battery_da, width=20)
battery_epc_da.grid(row=6, column=3, padx=10, sticky=E)
battery_DA_Button = ttk.Button(tab2, text="Rapid", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.bat_da_cmd1.encode()).decode()))
battery_DA_Button.grid(row=6, column=4, padx=10)
battery_DA_Button2 = ttk.Button(tab2, text="Charge", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.bat_da_cmd2.encode()).decode()))
battery_DA_Button2.grid(row=6, column=5, padx=10)
battery_DA_Button2 = ttk.Button(tab2, text="Discharge", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.bat_da_cmd3.encode()).decode()))
battery_DA_Button2.grid(row=6, column=6, padx=10)
battery_DA_Button2 = ttk.Button(tab2, text="Standby", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.bat_da_cmd4.encode()).decode()))
battery_DA_Button2.grid(row=7, column=4, padx=10)
battery_DA_Button2 = ttk.Button(tab2, text="Test", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.bat_da_cmd5.encode()).decode()))
battery_DA_Button2.grid(row=7, column=5, padx=10)
battery_DA_Button2 = ttk.Button(tab2, text="Auto", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.bat_da_cmd6.encode()).decode()))
battery_DA_Button2.grid(row=7, column=6, padx=10)
battery_DA_Button2 = ttk.Button(tab2, text="Restart", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.bat_da_cmd8.encode()).decode()))
battery_DA_Button2.grid(row=8, column=4, padx=10)
battery_DA_Button2 = ttk.Button(tab2, text="Recalculate", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.bat_da_cmd9.encode()).decode()))
battery_DA_Button2.grid(row=8, column=5, padx=10)
battery_DA_Button2 = ttk.Button(tab2, text="Other", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.bat_da_cmd0.encode()).decode()))
battery_DA_Button2.grid(row=8, column=6, padx=10)
battery_DA_Lable = ttk.Label(tab2, text="Operation mode setting - 0xDA")
battery_DA_Lable.grid(column = 0, row = 6, columnspan=3,  padx = 10, pady = 10, sticky=W)
# 0xDB
global battery_epc_db
battery_db = StringVar()
battery_db.set("N/A")
battery_epc_db = ttk.Entry(tab2, textvariable = battery_db, width=20)
battery_epc_db.grid(row=9, column=3, padx=10, sticky=E)
battery_DB_Lable = ttk.Label(tab2, text="System-interconnected type - 0xDB")
battery_DB_Lable.grid(column = 0, row = 9, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xDC
global battery_epc_dc
battery_dc = StringVar()
battery_dc.set("N/A")
battery_epc_dc = ttk.Entry(tab2, textvariable = battery_dc, width=20)
battery_epc_dc.grid(row=10, column=3, padx=10, sticky=E)
battery_DC_Lable = ttk.Label(tab2, text="Minimum/maximum charging electric power (Independent) - 0xDC")
battery_DC_Lable.grid(column = 0, row = 10, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xDD
global battery_epc_dd
battery_dd = StringVar()
battery_dd.set("N/A")
battery_epc_dd = ttk.Entry(tab2, textvariable = battery_dd, width=20)
battery_epc_dd.grid(row=11, column=3, padx=10, sticky=E)
battery_DD_Lable = ttk.Label(tab2, text="Minimum/maximum discharging electric power (Independent) - 0xDD")
battery_DD_Lable.grid(column = 0, row = 11, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE2
global battery_epc_e2
battery_e2 = StringVar()
battery_e2.set("N/A")
battery_epc_e2 = ttk.Entry(tab2, textvariable = battery_e2, width=20)
battery_epc_e2.grid(row=12, column=3, padx=10, sticky=E)
battery_E2_Lable = ttk.Label(tab2, text="Remaining stored electricity 1 - 0xE2")
battery_E2_Lable.grid(column = 0, row = 12, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE4
global battery_epc_e4
battery_e4 = StringVar()
battery_e4.set("N/A")
battery_epc_e4 = ttk.Entry(tab2, textvariable = battery_e4, width=20)
battery_epc_e4.grid(row=13, column=3, padx=10, sticky=E)
battery_E4_Lable = ttk.Label(tab2, text="Remaining stored electricity 3 - 0xE4")
battery_E4_Lable.grid(column = 0, row = 13, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE5
global battery_epc_e5
battery_e5 = StringVar()
battery_e5.set("N/A")
battery_epc_e5 = ttk.Entry(tab2, textvariable = battery_e5, width=20)
battery_epc_e5.grid(row=14, column=3, padx=10, sticky=E)
battery_E5_Lable = ttk.Label(tab2, text="Battery state of health - 0xE5")
battery_E5_Lable.grid(column = 0, row = 14, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE7
global battery_epc_e7
battery_e7 = StringVar()
battery_e7.set("N/A")
battery_epc_e7 = ttk.Entry(tab2, textvariable = battery_e7, width=20)
battery_epc_e7.grid(row=15, column=3, padx=10, sticky=E)
battery_E7_Button = ttk.Button(tab2, text="Set", command=lambda:set_temp("0x027D01", "E7"))
battery_E7_Button.grid(row=15, column=4, padx=10)
battery_E7_Lable = ttk.Label(tab2, text="Charging amount setting 1 - 0xE7")
battery_E7_Lable.grid(column = 0, row = 15, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE8
global battery_epc_e8
battery_e8 = StringVar()
battery_e8.set("N/A")
battery_epc_e8 = ttk.Entry(tab2, textvariable = battery_e8, width=20)
battery_epc_e8.grid(row=16, column=3, padx=10, sticky=E)
battery_E8_Button = ttk.Button(tab2, text="Set", command=lambda:set_temp("0x027D01", "E8"))
battery_E8_Button.grid(row=16, column=4, padx=10)
battery_E8_Lable = ttk.Label(tab2, text="Discharging amount setting 1 - 0xE8")
battery_E8_Lable.grid(column = 0, row = 16, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xEB
global battery_epc_eb
battery_eb = StringVar()
battery_eb.set("N/A")
battery_epc_eb = ttk.Entry(tab2, textvariable = battery_eb, width=20)
battery_epc_eb.grid(row=17, column=3, padx=10, sticky=E)
battery_EB_Button = ttk.Button(tab2, text="Set", command=lambda:set_temp("0x027D01", "EB"))
battery_EB_Button.grid(row=17, column=4, padx=10)
battery_EB_Lable = ttk.Label(tab2, text="Charging electric power setting - 0xEB")
battery_EB_Lable.grid(column = 0, row = 17, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xEC
global battery_epc_ec
battery_ec = StringVar()
battery_ec.set("N/A")
battery_epc_ec = ttk.Entry(tab2, textvariable = battery_ec, width=20)
battery_epc_ec.grid(row=18, column=3, padx=10, sticky=E)
battery_EC_Button = ttk.Button(tab2, text="Set", command=lambda:set_temp("0x027D01", "EC"))
battery_EC_Button.grid(row=18, column=4, padx=10)
battery_EC_Lable = ttk.Label(tab2, text="Discharging electric power setting - 0xEC")
battery_EC_Lable.grid(column = 0, row = 18, columnspan=3, padx = 10, pady = 10, sticky=W)

# EPC list for Air condition - 1
# 0x80
global air_epc_80
air_80 = StringVar()
air_80.set("N/A")
epc_air_80 = ttk.Entry(tab3, textvariable = air_80, width=20)
epc_air_80.grid(row=0, column=3, padx=10, sticky=E)
air_80_Button = ttk.Button(tab3, text="ON", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_80_cmd1.encode()).decode()))
air_80_Button.grid(row=0, column=4, padx=10)
air_80_Button = ttk.Button(tab3, text="OFF", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_80_cmd2.encode()).decode()))
air_80_Button.grid(row=0, column=5, padx=10)
air_80_Lable = ttk.Label(tab3, text="Operation status - 0x80")
air_80_Lable.grid(column = 0, row = 0, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0x8F
global air_epc_8f
air_8f = StringVar()
air_8f.set("N/A")
epc_air_8f = ttk.Entry(tab3, textvariable = air_8f, width=20)
epc_air_8f.grid(row=1, column=3, padx=10, sticky=E)
air_8F_Button = ttk.Button(tab3, text="Saving", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_8f_cmd1.encode()).decode()))
air_8F_Button.grid(row=1, column=4, padx=10)
air_8F_Button = ttk.Button(tab3, text="Normal", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_8f_cmd2.encode()).decode()))
air_8F_Button.grid(row=1, column=5, padx=10)
air_8F_Lable = ttk.Label(tab3, text="Power-saving operation setting - 0x8F")
air_8F_Lable.grid(column = 0, row = 1, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xB0
global air_epc_b0
air_b0 = StringVar()
air_b0.set("N/A")
epc_air_b0 = ttk.Entry(tab3, textvariable = air_b0, width=20)
epc_air_b0.grid(row=2, column=3, padx=10, sticky=E)
air_B0_Button = ttk.Button(tab3, text="Automatic", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_b0_cmd1.encode()).decode()))
air_B0_Button.grid(row=2, column=4, padx=10)
air_B0_Button = ttk.Button(tab3, text="Cooling", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_b0_cmd2.encode()).decode()))
air_B0_Button.grid(row=2, column=5, padx=10)
air_B0_Button = ttk.Button(tab3, text="Heating", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_b0_cmd3.encode()).decode()))
air_B0_Button.grid(row=2, column=6, padx=10)
air_B0_Button = ttk.Button(tab3, text="Dehumidify", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_b0_cmd4.encode()).decode()))
air_B0_Button.grid(row=3, column=4, padx=10)
air_B0_Button = ttk.Button(tab3, text="Air circulator", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_b0_cmd5.encode()).decode()))
air_B0_Button.grid(row=3, column=5, padx=10)
air_B0_Button = ttk.Button(tab3, text="Other", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_b0_cmd6.encode()).decode()))
air_B0_Button.grid(row=3, column=6, padx=10)
air_B0_Lable = ttk.Label(tab3, text="Operation mode setting - 0xB0")
air_B0_Lable.grid(column = 0, row = 2, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xB3
global air_epc_b3
air_b3 = StringVar()
air_b3.set("N/A")
air_epc_b3 = ttk.Entry(tab3, textvariable = air_b3, width=20)
air_epc_b3.grid(row=4, column=3, padx=10, sticky=E)
air_B3_Button = ttk.Button(tab3, text="Set", command=lambda:set_temp("0x013001", "B3", ENL_win_globals.air_id))
air_B3_Button.grid(row=4, column=4, padx=10)
air_B3_Lable = ttk.Label(tab3, text="Set temperature value - 0xB3")
air_B3_Lable.grid(column = 0, row = 4, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xB4
global air_epc_b4
air_b4 = StringVar()
air_b4.set("N/A")
air_epc_b4 = ttk.Entry(tab3, textvariable = air_b4, width=20)
air_epc_b4.grid(row=5, column=3, padx=10, sticky=E)
air_B4_Button = ttk.Button(tab3, text="Set", command=lambda:set_temp("0x013001", "B4", ENL_win_globals.air_id))
air_B4_Button.grid(row=5, column=4, padx=10)
air_B4_Lable = ttk.Label(tab3, text="Set relative humidity in dehumidifying mode - 0xB4")
air_B4_Lable.grid(column = 0, row = 5, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xBA
global air_epc_ba
air_ba = StringVar()
air_ba.set("N/A")
air_epc_ba = ttk.Entry(tab3, textvariable = air_ba, width=20)
air_epc_ba.grid(row=6, column=3, padx=10, sticky=E)
air_BA_Lable = ttk.Label(tab3, text="Measured value of room relative humidity - 0xBA")
air_BA_Lable.grid(column = 0, row = 6, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xBB
global air_epc_bb
air_bb = StringVar()
air_bb.set("N/A")
air_epc_bb = ttk.Entry(tab3, textvariable = air_bb, width=20)
air_epc_bb.grid(row=7, column=3, padx=10, sticky=E)
air_BB_Lable = ttk.Label(tab3, text="Measured value of room temperature - 0xBB")
air_BB_Lable.grid(column = 0, row = 7, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xBE
global air_epc_be
air_be = StringVar()
air_be.set("N/A")
air_epc_be = ttk.Entry(tab3, textvariable = air_be, width=20)
air_epc_be.grid(row=8, column=3, padx=10, sticky=E)
air_BE_Lable = ttk.Label(tab3, text="Measured outdoor air temperature - 0xBE")
air_BE_Lable.grid(column = 0, row = 8, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xA0
global air_epc_a0
air_a0 = StringVar()
air_a0.set("N/A")
epc_air_a0 = ttk.Entry(tab3, textvariable = air_a0, width=20)
epc_air_a0.grid(row=9, column=3, padx=10, sticky=E)
air_A0_Button = ttk.Button(tab3, text="Auto", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_a0_cmd1.encode()).decode()))
air_A0_Button.grid(row=9, column=4, padx=10)
air_A0_Button = ttk.Button(tab3, text="Set", command=lambda:set_flow("0x013001", "A0", ENL_win_globals.air_id))
air_A0_Button.grid(row=9, column=5, padx=10)
air_A0_Lable = ttk.Label(tab3, text="Air flow rate setting - 0xA0")
air_A0_Lable.grid(column = 0, row = 9, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xA3
global air_epc_a3
air_a3 = StringVar()
air_a3.set("N/A")
epc_air_a3 = ttk.Entry(tab3, textvariable = air_a3, width=20)
epc_air_a3.grid(row=10, column=3, padx=10, sticky=E)
air_A3_Button = ttk.Button(tab3, text="Not used", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_a3_cmd1.encode()).decode()))
air_A3_Button.grid(row=10, column=4, padx=10)
air_A3_Button = ttk.Button(tab3, text="Vertical", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_a3_cmd2.encode()).decode()))
air_A3_Button.grid(row=10, column=5, padx=10)
air_A3_Button = ttk.Button(tab3, text="Horizontal", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_a3_cmd3.encode()).decode()))
air_A3_Button.grid(row=10, column=6, padx=10)
air_A3_Button = ttk.Button(tab3, text="Both", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air_a3_cmd4.encode()).decode()))
air_A3_Button.grid(row=10, column=7, padx=10)
air_A3_Lable = ttk.Label(tab3, text="Automatic swing of air flow setting - 0xA3")
air_A3_Lable.grid(column = 0, row = 10, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0x84
global air_epc_84
air_84 = StringVar()
air_84.set("N/A")
air_epc_84 = ttk.Entry(tab3, textvariable = air_84, width=20)
air_epc_84.grid(row=11, column=3, padx=10, sticky=E)
air_84_Lable = ttk.Label(tab3, text="Measured instantaneous power consumption - 0x84")
air_84_Lable.grid(column = 0, row = 11, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0x85
global air_epc_85
air_85 = StringVar()
air_85.set("N/A")
air_epc_85 = ttk.Entry(tab3, textvariable = air_85, width=20)
air_epc_85.grid(row=12, column=3, padx=10, sticky=E)
air_85_Lable = ttk.Label(tab3, text="Measured cumulative power consumption - 0x85")
air_85_Lable.grid(column = 0, row = 12, columnspan=3, padx = 10, pady = 10, sticky=W)

# EPC list for Air condition - 2
# 0x80
global air2_epc_80
air2_80 = StringVar()
air2_80.set("N/A")
epc_air2_80 = ttk.Entry(tab4, textvariable = air2_80, width=20)
epc_air2_80.grid(row=0, column=3, padx=10, sticky=E)
air2_80_Button = ttk.Button(tab4, text="ON", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_80_cmd1.encode()).decode()))
air2_80_Button.grid(row=0, column=4, padx=10)
air2_80_Button = ttk.Button(tab4, text="OFF", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_80_cmd2.encode()).decode()))
air2_80_Button.grid(row=0, column=5, padx=10)
air2_80_Lable = ttk.Label(tab4, text="Operation status - 0x80")
air2_80_Lable.grid(column = 0, row = 0, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0x8F
global air2_epc_8f
air2_8f = StringVar()
air2_8f.set("N/A")
epc_air2_8f = ttk.Entry(tab4, textvariable = air2_8f, width=20)
epc_air2_8f.grid(row=1, column=3, padx=10, sticky=E)
air2_8F_Button = ttk.Button(tab4, text="Saving", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_8f_cmd1.encode()).decode()))
air2_8F_Button.grid(row=1, column=4, padx=10)
air2_8F_Button = ttk.Button(tab4, text="Normal", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_8f_cmd2.encode()).decode()))
air2_8F_Button.grid(row=1, column=5, padx=10)
air2_8F_Lable = ttk.Label(tab4, text="Power-saving operation setting - 0x8F")
air2_8F_Lable.grid(column = 0, row = 1, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xB0
global air2_epc_b0
air2_b0 = StringVar()
air2_b0.set("N/A")
epc_air2_b0 = ttk.Entry(tab4, textvariable = air2_b0, width=20)
epc_air2_b0.grid(row=2, column=3, padx=10, sticky=E)
air2_B0_Button = ttk.Button(tab4, text="Automatic", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_b0_cmd1.encode()).decode()))
air2_B0_Button.grid(row=2, column=4, padx=10)
air2_B0_Button = ttk.Button(tab4, text="Cooling", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_b0_cmd2.encode()).decode()))
air2_B0_Button.grid(row=2, column=5, padx=10)
air2_B0_Button = ttk.Button(tab4, text="Heating", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_b0_cmd3.encode()).decode()))
air2_B0_Button.grid(row=2, column=6, padx=10)
air2_B0_Button = ttk.Button(tab4, text="Dehumidify", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_b0_cmd4.encode()).decode()))
air2_B0_Button.grid(row=3, column=4, padx=10)
air2_B0_Button = ttk.Button(tab4, text="Air circulator", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_b0_cmd5.encode()).decode()))
air2_B0_Button.grid(row=3, column=5, padx=10)
air2_B0_Button = ttk.Button(tab4, text="Other", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_b0_cmd6.encode()).decode()))
air2_B0_Button.grid(row=3, column=6, padx=10)
air2_B0_Lable = ttk.Label(tab4, text="Operation mode setting - 0xB0")
air2_B0_Lable.grid(column = 0, row = 2, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xB3
global air2_epc_b3
air2_b3 = StringVar()
air2_b3.set("N/A")
air2_epc_b3 = ttk.Entry(tab4, textvariable = air2_b3, width=20)
air2_epc_b3.grid(row=4, column=3, padx=10, sticky=E)
air2_B3_Button = ttk.Button(tab4, text="Set", command=lambda:set_temp("0x013001", "B3", ENL_win_globals.air2_id))
air2_B3_Button.grid(row=4, column=4, padx=10)
air2_B3_Lable = ttk.Label(tab4, text="Set temperature value - 0xB3")
air2_B3_Lable.grid(column = 0, row = 4, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xBA
global air2_epc_ba
air2_ba = StringVar()
air2_ba.set("N/A")
air2_epc_ba = ttk.Entry(tab4, textvariable = air2_ba, width=20)
air2_epc_ba.grid(row=5, column=3, padx=10, sticky=E)
air2_BA_Lable = ttk.Label(tab4, text="Measured value of room relative humidity - 0xBA")
air2_BA_Lable.grid(column = 0, row = 5, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xBB
global air2_epc_bb
air2_bb = StringVar()
air2_bb.set("N/A")
air2_epc_bb = ttk.Entry(tab4, textvariable = air2_bb, width=20)
air2_epc_bb.grid(row=6, column=3, padx=10, sticky=E)
air2_BB_Lable = ttk.Label(tab4, text="Measured value of room temperature - 0xBB")
air2_BB_Lable.grid(column = 0, row = 6, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xBE
global air2_epc_be
air2_be = StringVar()
air2_be.set("N/A")
air2_epc_be = ttk.Entry(tab4, textvariable = air2_be, width=20)
air2_epc_be.grid(row=7, column=3, padx=10, sticky=E)
air2_BE_Lable = ttk.Label(tab4, text="Measured outdoor air temperature - 0xBE")
air2_BE_Lable.grid(column = 0, row = 7, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xA0
global air2_epc_a0
air2_a0 = StringVar()
air2_a0.set("N/A")
epc_air2_a0 = ttk.Entry(tab4, textvariable = air2_a0, width=20)
epc_air2_a0.grid(row=8, column=3, padx=10, sticky=E)
air2_A0_Button = ttk.Button(tab4, text="Auto", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_a0_cmd1.encode()).decode()))
air2_A0_Button.grid(row=8, column=4, padx=10)
air2_A0_Button = ttk.Button(tab4, text="Set", command=lambda:set_flow("0x013001", "A0", ENL_win_globals.air2_id))
air2_A0_Button.grid(row=8, column=5, padx=10)
air2_A0_Lable = ttk.Label(tab4, text="Air flow rate setting - 0xA0")
air2_A0_Lable.grid(column = 0, row = 8, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xA1
global air2_epc_a1
air2_a1 = StringVar()
air2_a1.set("N/A")
epc_air2_a1 = ttk.Entry(tab4, textvariable = air2_a1, width=20)
epc_air2_a1.grid(row=9, column=3, padx=10, sticky=E)
air2_A1_Button = ttk.Button(tab4, text="Automatic", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_a1_cmd1.encode()).decode()))
air2_A1_Button.grid(row=9, column=4, padx=10)
air2_A1_Button = ttk.Button(tab4, text="Non-automatic", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_a1_cmd2.encode()).decode()))
air2_A1_Button.grid(row=9, column=5, padx=10)
air2_A1_Button = ttk.Button(tab4, text="Vertical", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_a1_cmd3.encode()).decode()))
air2_A1_Button.grid(row=10, column=4, padx=10)
air2_A1_Button = ttk.Button(tab4, text="Horizontal", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_a1_cmd4.encode()).decode()))
air2_A1_Button.grid(row=10, column=5, padx=10)
air2_A1_Lable = ttk.Label(tab4, text="Automatic control of air flow direction setting - 0xA1")
air2_A1_Lable.grid(column = 0, row = 9, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xA4
global air2_epc_a4
air2_a4 = StringVar()
air2_a4.set("N/A")
epc_air2_a4 = ttk.Entry(tab4, textvariable = air2_a4, width=20)
epc_air2_a4.grid(row=11, column=3, padx=10, sticky=E)
air2_A4_Button = ttk.Button(tab4, text="Uppermost", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_a4_cmd1.encode()).decode()))
air2_A4_Button.grid(row=11, column=4, padx=10)
air2_A4_Button = ttk.Button(tab4, text="Lowermost", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_a4_cmd2.encode()).decode()))
air2_A4_Button.grid(row=11, column=5, padx=10)
air2_A4_Button = ttk.Button(tab4, text="Central", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_a4_cmd3.encode()).decode()))
air2_A4_Button.grid(row=11, column=6, padx=10)
air2_A4_Button = ttk.Button(tab4, text="Midpoint up", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_a4_cmd4.encode()).decode()))
air2_A4_Button.grid(row=12, column=4, padx=10)
air2_A4_Button = ttk.Button(tab4, text="Midpoint low", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.air2_a4_cmd5.encode()).decode()))
air2_A4_Button.grid(row=12, column=5, padx=10)
air2_A4_Lable = ttk.Label(tab4, text="Air flow direction (vertical) setting - 0xA4")
air2_A4_Lable.grid(column = 0, row = 11, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0x85
global air2_epc_85
air2_85 = StringVar()
air2_85.set("N/A")
air2_epc_85 = ttk.Entry(tab4, textvariable = air2_85, width=20)
air2_epc_85.grid(row=13, column=3, padx=10, sticky=E)
air2_85_Lable = ttk.Label(tab4, text="Measured cumulative power consumption - 0x85")
air2_85_Lable.grid(column = 0, row = 13, columnspan=3, padx = 10, pady = 10, sticky=W)

#PCS
# 0x80
global pcs_epc_80
pcs_80 = StringVar()
pcs_80.set("N/A")
epc_pcs_80 = ttk.Entry(tab5, textvariable = pcs_80, width=20)
epc_pcs_80.grid(row=0, column=3, padx=10, sticky=E)
# pcs_80_Button = ttk.Button(tab5, text="ON", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.pcs_80_cmd1.encode()).decode()))
# pcs_80_Button.grid(row=0, column=4, padx=10)
# pcs_80_Button = ttk.Button(tab5, text="OFF", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.pcs_80_cmd2.encode()).decode()))
# pcs_80_Button.grid(row=0, column=5, padx=10)
pcs_80_Lable = ttk.Label(tab5, text="Operation status - 0x80")
pcs_80_Lable.grid(column = 0, row = 0, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xA0
global pcs_epc_a0
pcs_a0 = StringVar()
pcs_a0.set("N/A")
pcs_epc_a0 = ttk.Entry(tab5, textvariable = pcs_a0, width=20)
pcs_epc_a0.grid(row=1, column=3, padx=10, sticky=E)
pcs_A0_Button = ttk.Button(tab5, text="Set", command=lambda:set_temp("0x027901", "A0", ENL_win_globals.pcs_id))
pcs_A0_Button.grid(row=1, column=4, padx=10)
pcs_A0_Lable = ttk.Label(tab5, text="Output power control setting 1 - 0xA0")
pcs_A0_Lable.grid(column = 0, row = 1, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xB2
global pcs_epc_b2
pcs_b2 = StringVar()
pcs_b2.set("N/A")
pcs_epc_b2 = ttk.Entry(tab5, textvariable = pcs_b2, width=20)
pcs_epc_b2.grid(row=2, column=3, padx=10, sticky=E)
pcs_B2_Lable = ttk.Label(tab5, text="Type of surplus electricity purchase - 0xB2")
pcs_B2_Lable.grid(column = 0, row = 2, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xB3
global pcs_epc_b3
pcs_b3 = StringVar()
pcs_b3.set("N/A")
pcs_epc_b3 = ttk.Entry(tab5, textvariable = pcs_b3, width=20)
pcs_epc_b3.grid(row=3, column=3, padx=10, sticky=E)
pcs_B3_Lable = ttk.Label(tab5, text="Output power change time setting value - 0xB3")
pcs_B3_Lable.grid(column = 0, row = 3, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xB4
global pcs_epc_b4
pcs_b4 = StringVar()
pcs_b4.set("N/A")
pcs_epc_b4 = ttk.Entry(tab5, textvariable = pcs_b4, width=20)
pcs_epc_b4.grid(row=4, column=3, padx=10, sticky=E)
pcs_B4_Lable = ttk.Label(tab5, text="Upper limit clip setting value - 0xB4")
pcs_B4_Lable.grid(column = 0, row = 4, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xC0
global pcs_epc_c0
pcs_c0 = StringVar()
pcs_c0.set("N/A")
pcs_epc_c0 = ttk.Entry(tab5, textvariable = pcs_c0, width=20)
pcs_epc_c0.grid(row=5, column=3, padx=10, sticky=E)
pcs_C0_Lable = ttk.Label(tab5, text="Operation power factor setting value - 0xC0")
pcs_C0_Lable.grid(column = 0, row = 5, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xC1
global pcs_epc_c1
pcs_c1 = StringVar()
pcs_c1.set("N/A")
pcs_epc_c1 = ttk.Entry(tab5, textvariable = pcs_c1, width=20)
pcs_epc_c1.grid(row=6, column=3, padx=10, sticky=E)
pcs_80_Button = ttk.Button(tab5, text="FIT", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.pcs_c1_cmd1.encode()).decode()))
pcs_80_Button.grid(row=6, column=4, padx=10)
pcs_80_Button = ttk.Button(tab5, text="Non-FIT", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.pcs_c1_cmd2.encode()).decode()))
pcs_80_Button.grid(row=6, column=5, padx=10)
pcs_80_Button = ttk.Button(tab5, text="No setting", command=lambda:ENL_win.publish_mqtt(hexlify(ENL_win_globals.pcs_c1_cmd3.encode()).decode()))
pcs_80_Button.grid(row=6, column=6, padx=10)
pcs_C1_Lable = ttk.Label(tab5, text="FIT contract type - 0xC1")
pcs_C1_Lable.grid(column = 0, row = 6, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xC2
global pcs_epc_c2
pcs_c2 = StringVar()
pcs_c2.set("N/A")
pcs_epc_c2 = ttk.Entry(tab5, textvariable = pcs_c2, width=20)
pcs_epc_c2.grid(row=7, column=3, padx=10, sticky=E)
pcs_C2_Lable = ttk.Label(tab5, text="Self-consumption type - 0xC2")
pcs_C2_Lable.grid(column = 0, row = 7, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xC3
global pcs_epc_c3
pcs_c3 = StringVar()
pcs_c3.set("N/A")
pcs_epc_c3 = ttk.Entry(tab5, textvariable = pcs_c3, width=20)
pcs_epc_c3.grid(row=8, column=3, padx=10, sticky=E)
pcs_C3_Lable = ttk.Label(tab5, text="Capacity approved by equipment - 0xC3")
pcs_C3_Lable.grid(column = 0, row = 8, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xD0
global pcs_epc_d0
pcs_d0 = StringVar()
pcs_d0.set("N/A")
pcs_epc_d0 = ttk.Entry(tab5, textvariable = pcs_d0, width=20)
pcs_epc_d0.grid(row=9, column=3, padx=10, sticky=E)
pcs_D0_Lable = ttk.Label(tab5, text="System-interconnected type - 0xD0")
pcs_D0_Lable.grid(column = 0, row = 9, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xD1
global pcs_epc_d1
pcs_d1 = StringVar()
pcs_d1.set("N/A")
pcs_epc_d1 = ttk.Entry(tab5, textvariable = pcs_d1, width=20)
pcs_epc_d1.grid(row=10, column=3, padx=10, sticky=E)
pcs_D1_Lable = ttk.Label(tab5, text="Output power restraint status - 0xD1")
pcs_D1_Lable.grid(column = 0, row = 10, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE0
global pcs_epc_e0
pcs_e0 = StringVar()
pcs_e0.set("N/A")
pcs_epc_e0 = ttk.Entry(tab5, textvariable = pcs_e0, width=20)
pcs_epc_e0.grid(row=11, column=3, padx=10, sticky=E)
pcs_E0_Lable = ttk.Label(tab5, text="Measured instantaneous amount of electricity generated - 0xE0")
pcs_E0_Lable.grid(column = 0, row = 11, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE1
global pcs_epc_e1
pcs_e1 = StringVar()
pcs_e1.set("N/A")
pcs_epc_e1 = ttk.Entry(tab5, textvariable = pcs_e1, width=20)
pcs_epc_e1.grid(row=12, column=3, padx=10, sticky=E)
pcs_E1_Lable = ttk.Label(tab5, text="Measured cumulative amount of electric energy generated - 0xE1")
pcs_E1_Lable.grid(column = 0, row = 12, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE3
global pcs_epc_e3
pcs_e3 = StringVar()
pcs_e3.set("N/A")
pcs_epc_e3 = ttk.Entry(tab5, textvariable = pcs_e3, width=20)
pcs_epc_e3.grid(row=13, column=3, padx=10, sticky=E)
pcs_E3_Lable = ttk.Label(tab5, text="Measured cumulative amount of electric energy sold - 0xE3")
pcs_E3_Lable.grid(column = 0, row = 13, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE5
global pcs_epc_e5
pcs_e5 = StringVar()
pcs_e5.set("N/A")
pcs_epc_e5 = ttk.Entry(tab5, textvariable = pcs_e5, width=20)
pcs_epc_e5.grid(row=14, column=3, padx=10, sticky=E)
pcs_E5_Button = ttk.Button(tab5, text="Set", command=lambda:set_temp("0x027901", "E5", ENL_win_globals.pcs_id))
pcs_E5_Button.grid(row=14, column=4, padx=10)
pcs_E5_Lable = ttk.Label(tab5, text="Power generation output limit setting 1 - 0xE5")
pcs_E5_Lable.grid(column = 0, row = 14, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE8
global pcs_epc_e8
pcs_e8 = StringVar()
pcs_e8.set("N/A")
pcs_epc_e8 = ttk.Entry(tab5, textvariable = pcs_e8, width=20)
pcs_epc_e8.grid(row=15, column=3, padx=10, sticky=E)
# pcs_E8_Button = ttk.Button(tab5, text="Set", command=lambda:set_temp("0x027901", "E8", ENL_win_globals.pcs_id))
# pcs_E8_Button.grid(row=15, column=4, padx=10)
pcs_E8_Lable = ttk.Label(tab5, text="Rated power generation output - 0xE8")
pcs_E8_Lable.grid(column = 0, row = 15, columnspan=3, padx = 10, pady = 10, sticky=W)

#PV
# 0xE1
global pv_epc_e1
pv_e1 = StringVar()
pv_e1.set("N/A")
epc_pv_e1 = ttk.Entry(tab6, textvariable = pv_e1, width=20)
epc_pv_e1.grid(row=0, column=3, padx=10, sticky=E)
pv_E1_Lable = ttk.Label(tab6, text="Unit for cumulative amounts of electric energy - 0xE1")
pv_E1_Lable.grid(column = 0, row = 0, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE7
global pv_epc_e7
pv_e7 = StringVar()
pv_e7.set("N/A")
epc_pv_e7 = ttk.Entry(tab6, textvariable = pv_e7, width=20)
epc_pv_e7.grid(row=1, column=3, padx=10, sticky=E)
pv_E7_Lable = ttk.Label(tab6, text="Measured instantaneous electric energy - 0xE7")
pv_E7_Lable.grid(column = 0, row = 1, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE8
global pv_epc_e8
pv_e8 = StringVar()
pv_e8.set("N/A")
epc_pv_e8 = ttk.Entry(tab6, textvariable = pv_e8, width=20)
epc_pv_e8.grid(row=2, column=3, padx=10, sticky=E)
pv_E8_Lable = ttk.Label(tab6, text="Measured instantaneous currents - 0xE8")
pv_E8_Lable.grid(column = 0, row = 2, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xEA
global pv_epc_ea
pv_ea = StringVar()
pv_ea.set("N/A")
epc_pv_ea = ttk.Entry(tab6, textvariable = pv_ea, width=20)
epc_pv_ea.grid(row=3, column=3, padx=10, sticky=E)
pv_EA_Lable = ttk.Label(tab6, text="Cumulative amounts of electric energy measured at fixed time (normal) - 0xEA")
pv_EA_Lable.grid(column = 0, row = 3, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xEB
global pv_epc_eb
pv_eb = StringVar()
pv_eb.set("N/A")
epc_pv_eb = ttk.Entry(tab6, textvariable = pv_eb, width=20)
epc_pv_eb.grid(row=4, column=3, padx=10, sticky=E)
pv_EB_Lable = ttk.Label(tab6, text="Cumulative amounts of electric energy measured at fixed time (reverse) - 0xEB")
pv_EB_Lable.grid(column = 0, row = 4, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE0
global pv_epc_e0
pv_e0 = StringVar()
pv_e0.set("N/A")
epc_pv_e0 = ttk.Entry(tab6, textvariable = pv_e0, width=20)
epc_pv_e0.grid(row=5, column=3, padx=10, sticky=E)
pv_E0_Lable = ttk.Label(tab6, text="Cumulative amounts of electric energy (normal) - 0xE0")
pv_E0_Lable.grid(column = 0, row = 5, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE3
global pv_epc_e3
pv_e3 = StringVar()
pv_e3.set("N/A")
epc_pv_e3 = ttk.Entry(tab6, textvariable = pv_e3, width=20)
epc_pv_e3.grid(row=6, column=3, padx=10, sticky=E)
pv_E3_Lable = ttk.Label(tab6, text="Cumulative amounts of electric energy (reverse) - 0xE3")
pv_E3_Lable.grid(column = 0, row = 6, columnspan=3, padx = 10, pady = 10, sticky=W)

#Utility
# 0xE1
global rb_epc_e1
rb_e1 = StringVar()
rb_e1.set("N/A")
epc_rb_e1 = ttk.Entry(tab7, textvariable = rb_e1, width=20)
epc_rb_e1.grid(row=0, column=3, padx=10, sticky=E)
rb_E1_Lable = ttk.Label(tab7, text="Unit for cumulative amounts of electric energy - 0xE1")
rb_E1_Lable.grid(column = 0, row = 0, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE7
global rb_epc_e7
rb_e7 = StringVar()
rb_e7.set("N/A")
epc_rb_e7 = ttk.Entry(tab7, textvariable = rb_e7, width=20)
epc_rb_e7.grid(row=1, column=3, padx=10, sticky=E)
rb_E7_Lable = ttk.Label(tab7, text="Measured instantaneous electric energy - 0xE7")
rb_E7_Lable.grid(column = 0, row = 1, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE8
global rb_epc_e8
rb_e8 = StringVar()
rb_e8.set("N/A")
epc_rb_e8 = ttk.Entry(tab7, textvariable = rb_e8, width=20)
epc_rb_e8.grid(row=2, column=3, padx=10, sticky=E)
rb_E8_Lable = ttk.Label(tab7, text="Measured instantaneous currents - 0xE8")
rb_E8_Lable.grid(column = 0, row = 2, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xEA
global rb_epc_ea
rb_ea = StringVar()
rb_ea.set("N/A")
epc_rb_ea = ttk.Entry(tab7, textvariable = rb_ea, width=20)
epc_rb_ea.grid(row=3, column=3, padx=10, sticky=E)
rb_EA_Lable = ttk.Label(tab7, text="Cumulative amounts of electric energy measured at fixed time (normal) - 0xEA")
rb_EA_Lable.grid(column = 0, row = 3, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xEB
global rb_epc_eb
rb_eb = StringVar()
rb_eb.set("N/A")
epc_rb_eb = ttk.Entry(tab7, textvariable = rb_eb, width=20)
epc_rb_eb.grid(row=4, column=3, padx=10, sticky=E)
rb_EB_Lable = ttk.Label(tab7, text="Cumulative amounts of electric energy measured at fixed time (reverse) - 0xEB")
rb_EB_Lable.grid(column = 0, row = 4, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE0
global rb_epc_e0
rb_e0 = StringVar()
rb_e0.set("N/A")
epc_rb_e0 = ttk.Entry(tab7, textvariable = rb_e0, width=20)
epc_rb_e0.grid(row=5, column=3, padx=10, sticky=E)
rb_E0_Lable = ttk.Label(tab7, text="Cumulative amounts of electric energy (normal) - 0xE0")
rb_E0_Lable.grid(column = 0, row = 5, columnspan=3, padx = 10, pady = 10, sticky=W)
# 0xE3
global rb_epc_e3
rb_e3 = StringVar()
rb_e3.set("N/A")
epc_rb_e3 = ttk.Entry(tab7, textvariable = rb_e3, width=20)
epc_rb_e3.grid(row=6, column=3, padx=10, sticky=E)
rb_E3_Lable = ttk.Label(tab7, text="Cumulative amounts of electric energy (reverse) - 0xE3")
rb_E3_Lable.grid(column = 0, row = 6, columnspan=3, padx = 10, pady = 10, sticky=W)

def set_temp(cls, epc, id):

    def set_tmp():
        ENL_win.publish_mqtt(hexlify(ENL_win_globals.tmp_cmd(cls, str(hex(int(settmp.get(), 10))), epc, id).encode()).decode())
        input_win.destroy()

    input_win = Toplevel()
    temp_Lable = Label(input_win, text="Input parameter")
    temp_Lable.pack(pady=10)
    settmp = ttk.Entry(input_win, width=20)
    settmp.pack(pady=10, padx=10)
    tmp_Button = ttk.Button(input_win, text="Set", command=set_tmp)
    tmp_Button.pack(pady=10)

def set_flow(cls, epc, id):

    def set_flw():
        ENL_win.publish_mqtt(hexlify(ENL_win_globals.flow_cmd(cls, str(hex(int(settmp.get(), 10)+ 48)), epc, id).encode()).decode())
        input_win.destroy()

    input_win = Toplevel()
    temp_Lable = Label(input_win, text="Input parameter")
    temp_Lable.pack(pady=10)
    settmp = ttk.Entry(input_win, width=20)
    settmp.pack(pady=10, padx=10)
    tmp_Button = ttk.Button(input_win, text="Set", command=set_flw)
    tmp_Button.pack(pady=10)

# handle negative hex value
def hex_to_decimal(hex_value, num_bits):
    try:
        # Convert hex to binary
        binary_value = bin(int(hex_value, 16))[2:].zfill(num_bits)
        # Check if it's a negative value in two's complement (MSB is 1)
        if binary_value[0] == '1':
            # Perform two's complement
            inverted_bits = ''.join('1' if bit == '0' else '0' for bit in binary_value)
            decimal_value = -(int(inverted_bits, 2) + 1)
        else:
            # Positive value, simply convert binary to decimal
            decimal_value = int(binary_value, 2)
        return decimal_value
    except:
        return 0

def status_update():
    global db_buff
    rec_copy = ENL_win.rec.copy()
    if ("time" in rec_copy):
        last_time.set(rec_copy["time"][0:19].replace("T", " "))
    if ("cls" in rec_copy):
        # Eco Cute
        if (rec_copy["cls"] == "0x026B01"):
            if rec_copy.get("properties", {}).get("0xB0", 0):
                if (rec_copy["properties"]["0xB0"] == "0x41"):
                    b0.set("Auto")
                    db_buff["eco_heat_mode_B0"] = "Auto"
                if (rec_copy["properties"]["0xB0"] == "0x42"):
                    b0.set("Stopped")
                    db_buff["eco_heat_mode_B0"] = "Stopped"
                if (rec_copy["properties"]["0xB0"] == "0x43"):
                    b0.set("Non-Auto")
                    db_buff["eco_heat_mode_B0"] = "Non-Auto"
            if rec_copy.get("properties", {}).get("0xB2", 0):
                if (rec_copy["properties"]["0xB2"] == "0x41"):
                    b2.set("Heating")
                    db_buff["eco_heat_status_B2"] = "Heating"
                if (rec_copy["properties"]["0xB2"] == "0x42"):
                    b2.set("Not heating")
                    db_buff["eco_heat_status_B2"] = "Not heating"
            if rec_copy.get("properties", {}).get("0xB3", 0):
                    b3.set(str(int(rec_copy["properties"]["0xB3"], 0)) + "C")
                    db_buff["eco_heat_temp_set_B3"] = int(rec_copy["properties"]["0xB3"], 0)
            if rec_copy.get("properties", {}).get("0xB6", 0):
                if (rec_copy["properties"]["0xB6"] == "0x41"):
                    b6.set("Standard")
                    db_buff["eco_tank_mode_B6"] = "Standard"
                if (rec_copy["properties"]["0xB6"] == "0x42"):
                    b6.set("Saving")
                    db_buff["eco_tank_mode_B6"] = "Saving"
                if (rec_copy["properties"]["0xB6"] == "0x43"):
                    b6.set("Extra")
                    db_buff["eco_tank_mode_B6"] = "Extra"
            if rec_copy.get("properties", {}).get("0xC0", 0):
                if (rec_copy["properties"]["0xC0"] == "0x41"):
                    c0.set("Permitted")
                if (rec_copy["properties"]["0xC0"] == "0x42"):
                    c0.set("Not permitted")
            if rec_copy.get("properties", {}).get("0xC1", 0):
                c1.set(str(int(rec_copy["properties"]["0xC1"], 0)) + "C")
                db_buff["eco_heat_temp_C1"] = int(rec_copy["properties"]["0xC1"], 0)
            if rec_copy.get("properties", {}).get("0xC3", 0):
                if (rec_copy["properties"]["0xC3"] == "0x41"):
                    c3.set("Yes")
                    db_buff["eco_supply_status_C3"] = "Yes"
                if (rec_copy["properties"]["0xC3"] == "0x42"):
                    c3.set("No")
                    db_buff["eco_supply_status_C3"] = "No"
            if rec_copy.get("properties", {}).get("0xD1", 0):
                d1.set(str(int(rec_copy["properties"]["0xD1"], 0)) + "C")
                db_buff["eco_supply_temp_set_D1"] = int(rec_copy["properties"]["0xD1"], 0)
            if rec_copy.get("properties", {}).get("0xD3", 0):
                d3.set(str(int(rec_copy["properties"]["0xD3"], 0)) + "C")
                db_buff["eco_bath_temp_set_D3"] = int(rec_copy["properties"]["0xD3"], 0)
            if rec_copy.get("properties", {}).get("0xE1", 0):
                e1.set(str(int(rec_copy["properties"]["0xE1"], 0)) + "L")
                db_buff["eco_water_remain_E1"] = int(rec_copy["properties"]["0xE1"], 0)
            if rec_copy.get("properties", {}).get("0xE2", 0):
                e2.set(str(int(rec_copy["properties"]["0xE2"], 0)) + "L")
                db_buff["eco_tank_capacity_E2"] = int(rec_copy["properties"]["0xE2"], 0)
            if rec_copy.get("properties", {}).get("0xE3", 0):
                if (rec_copy["properties"]["0xE3"] == "0x41"):
                    e3.set("On")
                    db_buff["eco_bath_mode_E3"] = "On"
                if (rec_copy["properties"]["0xE3"] == "0x42"):
                    e3.set("Off")
                    db_buff["eco_bath_mode_E3"] = "Off"
            if rec_copy.get("properties", {}).get("0xEA", 0):
                if (rec_copy["properties"]["0xEA"] == "0x41"):
                    ea.set("Filling hot water")
                    db_buff["eco_bath_status_EA"] = "Filling hot water"
                if (rec_copy["properties"]["0xEA"] == "0x42"):
                    ea.set("Stopped")
                    db_buff["eco_bath_status_EA"] = "Stopped"
                if (rec_copy["properties"]["0xEA"] == "0x43"):
                    ea.set("Keeping temperature")
                    db_buff["eco_bath_status_EA"] = "Keeping temperature"
            if rec_copy.get("properties", {}).get("0xE5", 0):
                if (rec_copy["properties"]["0xE5"] == "0x41"):
                    e5.set("On")
                if (rec_copy["properties"]["0xE5"] == "0x42"):
                    e5.set("Off")
            if rec_copy.get("properties", {}).get("0xE6", 0):
                if (rec_copy["properties"]["0xE6"] == "0x41"):
                    e6.set("On")
                if (rec_copy["properties"]["0xE6"] == "0x42"):
                    e6.set("Off")
            if rec_copy.get("properties", {}).get("0xEE", 0):
                ee.set(str(int(rec_copy["properties"]["0xEE"], 0)) + "L")
            if rec_copy.get("properties", {}).get("0x85", 0):
                eco_85.set(str(int(rec_copy["properties"]["0x85"], 0)) + "kW")
                db_buff["eco_cum_power_85"] = int(rec_copy["properties"]["0x85"], 0)
        # Battery
        if (rec_copy["cls"] == "0x027D01"):
            if rec_copy.get("properties", {}).get("0xAA", 0):
                battery_aa.set(str(int(rec_copy["properties"]["0xAA"], 0)) + "Wh")
            if rec_copy.get("properties", {}).get("0xAB", 0):
                battery_ab.set(str(int(rec_copy["properties"]["0xAB"], 0)) + "Wh")
            if rec_copy.get("properties", {}).get("0xCF", 0):
                if (rec_copy["properties"]["0xCF"] == "0x41"):
                    battery_cf.set("Rapid charging")
                    db_buff["bat_status_CF"] = "Rapid charging"
                if (rec_copy["properties"]["0xCF"] == "0x42"):
                    battery_cf.set("Charging")
                    db_buff["bat_status_CF"] = "Charging"
                if (rec_copy["properties"]["0xCF"] == "0x43"):
                    battery_cf.set("Discharging")
                    db_buff["bat_status_CF"] = "Discharging"
                if (rec_copy["properties"]["0xCF"] == "0x44"):
                    battery_cf.set("Standby")
                    db_buff["bat_status_CF"] = "Standby"
                if (rec_copy["properties"]["0xCF"] == "0x45"):
                    battery_cf.set("Test")
                    db_buff["bat_status_CF"] = "Test"
                if (rec_copy["properties"]["0xCF"] == "0x46"):
                    battery_cf.set("Automatic")
                    db_buff["bat_status_CF"] = "Automatic"
                if (rec_copy["properties"]["0xCF"] == "0x48"):
                    battery_cf.set("Restart")
                    db_buff["bat_status_CF"] = "Restart"
                if (rec_copy["properties"]["0xCF"] == "0x49"):
                    battery_cf.set("Effective capacity recalculation processing")
                    db_buff["bat_status_CF"] = "Effective capacity recalculation processing"
                if (rec_copy["properties"]["0xCF"] == "0x40"):
                    battery_cf.set("Other")
                    db_buff["bat_status_CF"] = "Other"
            if rec_copy.get("properties", {}).get("0xD3", 0):
                battery_d3.set(str(hex_to_decimal(rec_copy["properties"]["0xD3"], 32)) + "W")
                db_buff["bat_instant_power_D3"] = hex_to_decimal(rec_copy["properties"]["0xD3"], 32)
            if rec_copy.get("properties", {}).get("0xD6", 0):
                battery_d6.set(str(hex_to_decimal(rec_copy["properties"]["0xD6"], 32)) + "Wh")
                db_buff["bat_cum_dis_D6"] = hex_to_decimal(rec_copy["properties"]["0xD6"], 32)
            if rec_copy.get("properties", {}).get("0xD8", 0):
                battery_d8.set(str(hex_to_decimal(rec_copy["properties"]["0xD8"], 32)) + "Wh")
                db_buff["bat_cum_chr_D8"] = hex_to_decimal(rec_copy["properties"]["0xD8"], 32)
            if rec_copy.get("properties", {}).get("0xDA", 0):
                if (rec_copy["properties"]["0xDA"] == "0x41"):
                    battery_da.set("Rapid charging")
                    db_buff["bat_mode_DA"] = "Rapid charging"
                if (rec_copy["properties"]["0xDA"] == "0x42"):
                    battery_da.set("Charging")
                    db_buff["bat_mode_DA"] = "Charging"
                if (rec_copy["properties"]["0xDA"] == "0x43"):
                    battery_da.set("Discharging")
                    db_buff["bat_mode_DA"] = "Discharging"
                if (rec_copy["properties"]["0xDA"] == "0x44"):
                    battery_da.set("Standby")
                    db_buff["bat_mode_DA"] = "Standby"
                if (rec_copy["properties"]["0xDA"] == "0x45"):
                    battery_da.set("Test")
                    db_buff["bat_mode_DA"] = "Test"
                if (rec_copy["properties"]["0xDA"] == "0x46"):
                    battery_da.set("Automatic")
                    db_buff["bat_mode_DA"] = "Automatic"
                if (rec_copy["properties"]["0xDA"] == "0x48"):
                    battery_da.set("Restart")
                    db_buff["bat_mode_DA"] = "Restart"
                if (rec_copy["properties"]["0xDA"] == "0x49"):
                    battery_da.set("Effective capacity recalculation processing")
                    db_buff["bat_mode_DA"] = "Effective capacity recalculation processing"
                if (rec_copy["properties"]["0xDA"] == "0x40"):
                    battery_da.set("Other")
                    db_buff["bat_mode_DA"] = "Other"
            if rec_copy.get("properties", {}).get("0xDB", 0):
                if (rec_copy["properties"]["0xDB"] == "0x00"):
                    battery_db.set("Reverse power flow acceptable")
                if (rec_copy["properties"]["0xDB"] == "0x01"):
                    battery_db.set("Independent type")
                if (rec_copy["properties"]["0xDB"] == "0x02"):
                    battery_db.set("Reverse power flow not acceptable")
            if rec_copy.get("properties", {}).get("0xDC", 0):
                battery_dc.set(str(hex_to_decimal(rec_copy["properties"]["0xDC"], 32)) + "W")
            if rec_copy.get("properties", {}).get("0xDD", 0):
                battery_dd.set(str(hex_to_decimal(rec_copy["properties"]["0xDD"], 32)) + "W")
            if rec_copy.get("properties", {}).get("0xE2", 0):
                battery_e2.set(str(hex_to_decimal(rec_copy["properties"]["0xE2"], 32)) + "Wh")
                db_buff["bat_remain_E2"] = hex_to_decimal(rec_copy["properties"]["0xE2"], 32)
            if rec_copy.get("properties", {}).get("0xE4", 0):
                battery_e4.set(str(int(rec_copy["properties"]["0xE4"], 0)) + "%")
                db_buff["bat_remain_E4"] = int(rec_copy["properties"]["0xE4"], 0)
            if rec_copy.get("properties", {}).get("0xE5", 0):
                battery_e5.set(str(int(rec_copy["properties"]["0xE5"], 0)) + "%")
                db_buff["bat_health_E5"] = int(rec_copy["properties"]["0xE5"], 0)
            if rec_copy.get("properties", {}).get("0xE7", 0):
                battery_e7.set(str(hex_to_decimal(rec_copy["properties"]["0xE7"], 32)) + "Wh")
            if rec_copy.get("properties", {}).get("0xE8", 0):
                battery_e8.set(str(hex_to_decimal(rec_copy["properties"]["0xE8"], 32)) + "Wh")
            if rec_copy.get("properties", {}).get("0xEB", 0):
                battery_eb.set(str(hex_to_decimal(rec_copy["properties"]["0xEB"], 32)) + "Wh")
            if rec_copy.get("properties", {}).get("0xEC", 0):
                battery_ec.set(str(hex_to_decimal(rec_copy["properties"]["0xEC"], 32)) + "Wh")
        # Air Con 2
        if (rec_copy["cls"] == ENL_win_globals.air2_class) and (rec_copy["id"] == ENL_win_globals.air2_id):
            if rec_copy.get("properties", {}).get("0x80", 0):
                if (rec_copy["properties"]["0x80"] == "0x30"):
                    air2_80.set("ON")
                    db_buff["air2_status_80"] = "ON"
                if (rec_copy["properties"]["0x80"] == "0x31"):
                    air2_80.set("OFF")
                    db_buff["air2_status_80"] = "OFF"
            if rec_copy.get("properties", {}).get("0x8F", 0):
                if (rec_copy["properties"]["0x8F"] == "0x41"):
                    air2_8f.set("Power-saving")
                if (rec_copy["properties"]["0x8F"] == "0x42"):
                    air2_8f.set("Normal operation")
            if rec_copy.get("properties", {}).get("0xB0", 0):
                if (rec_copy["properties"]["0xB0"] == "0x41"):
                    air2_b0.set("Automatic")
                    db_buff["air2_mode_B0"] = "Automatic"
                if (rec_copy["properties"]["0xB0"] == "0x42"):
                    air2_b0.set("Cooling")
                    db_buff["air2_mode_B0"] = "Cooling"
                if (rec_copy["properties"]["0xB0"] == "0x43"):
                    air2_b0.set("Heating")
                    db_buff["air2_mode_B0"] = "Heating"
                if (rec_copy["properties"]["0xB0"] == "0x44"):
                    air2_b0.set("Dehumidification")
                    db_buff["air2_mode_B0"] = "Dehumidification"
                if (rec_copy["properties"]["0xB0"] == "0x45"):
                    air2_b0.set("Air circulator")   
                    db_buff["air2_mode_B0"] = "Air circulator"
                if (rec_copy["properties"]["0xB0"] == "0x40"):
                    air2_b0.set("Other")
                    db_buff["air2_mode_B0"] = "Other"
            if rec_copy.get("properties", {}).get("0xB3", 0):
                air2_b3.set(str(int(rec_copy["properties"]["0xB3"], 0)) + "C")
                db_buff["air2_temp_set_B3"] = int(rec_copy["properties"]["0xB3"], 0)
            if rec_copy.get("properties", {}).get("0xBA", 0):
                air2_ba.set(str(int(rec_copy["properties"]["0xBA"], 0)) + "C")
            if rec_copy.get("properties", {}).get("0xBB", 0):
                air2_bb.set(str(int(rec_copy["properties"]["0xBB"], 0)) + "C")
                db_buff["air2_room_temp_BB"] = int(rec_copy["properties"]["0xBB"], 0)
            if rec_copy.get("properties", {}).get("0xBE", 0):
                air2_be.set(str(int(rec_copy["properties"]["0xBE"], 0)) + "C")
                db_buff["air2_outdoor_temp_BE"] = int(rec_copy["properties"]["0xBE"], 0)
            if rec_copy.get("properties", {}).get("0xA0", 0):
                if (rec_copy["properties"]["0xA0"] == "0x41"):
                    air2_a0.set("Auto")
                else:
                    air2_a0.set(str(int(rec_copy["properties"]["0xA0"], 0)-48))
            if rec_copy.get("properties", {}).get("0xA1", 0):
                if (rec_copy["properties"]["0xA1"] == "0x41"):
                    air2_a1.set("Automatic")
                if (rec_copy["properties"]["0xA1"] == "0x42"):
                    air2_a1.set("Non-automatic")
                if (rec_copy["properties"]["0xA1"] == "0x43"):
                    air2_a1.set("Vertical")
                if (rec_copy["properties"]["0xA1"] == "0x44"):
                    air2_a1.set("Horizontal")
            if rec_copy.get("properties", {}).get("0xA4", 0):
                if (rec_copy["properties"]["0xA4"] == "0x41"):
                    air2_a4.set("Uppermost")
                if (rec_copy["properties"]["0xA4"] == "0x42"):
                    air2_a4.set("Lowermost")
                if (rec_copy["properties"]["0xA4"] == "0x43"):
                    air2_a4.set("Central")
                if (rec_copy["properties"]["0xA4"] == "0x44"):
                    air2_a4.set("Midpoint between uppermost and central")
                if (rec_copy["properties"]["0xA4"] == "0x45"):
                    air2_a4.set("Midpoint between lowermost and central")
            if rec_copy.get("properties", {}).get("0x85", 0):
                air2_85.set(str(int(rec_copy["properties"]["0x85"], 0)) + "Wh")
                db_buff["air2_cum_power_85"] = int(rec_copy["properties"]["0x85"], 0)
        # Air Con 1
        if ((rec_copy["cls"] == ENL_win_globals.air_class) and (rec_copy["id"] == ENL_win_globals.air_id)):
            if rec_copy.get("properties", {}).get("0x80", 0):
                if (rec_copy["properties"]["0x80"] == "0x30"):
                    air_80.set("ON")
                    db_buff["air1_status_80"] = "ON"
                if (rec_copy["properties"]["0x80"] == "0x31"):
                    air_80.set("OFF")
                    db_buff["air1_status_80"] = "OFF"
            if rec_copy.get("properties", {}).get("0x8F", 0):
                if (rec_copy["properties"]["0x8F"] == "0x41"):
                    air_8f.set("Power-saving")
                if (rec_copy["properties"]["0x8F"] == "0x42"):
                    air_8f.set("Normal operation")
            if rec_copy.get("properties", {}).get("0xB0", 0):
                if (rec_copy["properties"]["0xB0"] == "0x41"):
                    air_b0.set("Automatic")
                    db_buff["air1_mode_B0"] = "Automatic"
                if (rec_copy["properties"]["0xB0"] == "0x42"):
                    air_b0.set("Cooling")
                    db_buff["air1_mode_B0"] = "Cooling"
                if (rec_copy["properties"]["0xB0"] == "0x43"):
                    air_b0.set("Heating")
                    db_buff["air1_mode_B0"] = "Heating"
                if (rec_copy["properties"]["0xB0"] == "0x44"):
                    air_b0.set("Dehumidification")
                    db_buff["air1_mode_B0"] = "Dehumidification"
                if (rec_copy["properties"]["0xB0"] == "0x45"):
                    air_b0.set("Air circulator")    
                    db_buff["air1_mode_B0"] = "Air circulator"
                if (rec_copy["properties"]["0xB0"] == "0x40"):
                    air_b0.set("Other")
                    db_buff["air1_mode_B0"] = "Other"
            if rec_copy.get("properties", {}).get("0xB3", 0):
                air_b3.set(str(int(rec_copy["properties"]["0xB3"], 0)) + "C")
                db_buff["air1_temp_set_B3"] = int(rec_copy["properties"]["0xB3"], 0)
            if rec_copy.get("properties", {}).get("0xB4", 0):
                air_b4.set(str(int(rec_copy["properties"]["0xB4"], 0)) + "%")
            if rec_copy.get("properties", {}).get("0xBA", 0):
                air_ba.set(str(int(rec_copy["properties"]["0xBA"], 0)) + "%")
            if rec_copy.get("properties", {}).get("0xBB", 0):
                air_bb.set(str(int(rec_copy["properties"]["0xBB"], 0)) + "C")
                db_buff["air1_room_temp_BB"] = int(rec_copy["properties"]["0xBB"], 0)
            if rec_copy.get("properties", {}).get("0xBE", 0):
                air_be.set(str(int(rec_copy["properties"]["0xBE"], 0)) + "C")
                db_buff["air1_outdoor_temp_BE"] = int(rec_copy["properties"]["0xBE"], 0)
            if rec_copy.get("properties", {}).get("0xA0", 0):
                if (rec_copy["properties"]["0xA0"] == "0x41"):
                    air_a0.set("Auto")
                else:
                    air_a0.set(str(int(rec_copy["properties"]["0xA0"], 0)-48))
            if rec_copy.get("properties", {}).get("0xA3", 0):
                if (rec_copy["properties"]["0xA3"] == "0x31"):
                    air_a3.set("Not used")
                if (rec_copy["properties"]["0xA3"] == "0x41"):
                    air_a3.set("Vertical")
                if (rec_copy["properties"]["0xA3"] == "0x42"):
                    air_a3.set("Horizontal")
                if (rec_copy["properties"]["0xA3"] == "0x43"):
                    air_a3.set("Vertical and Horizontal")
            if rec_copy.get("properties", {}).get("0x84", 0):
                air_84.set(str(int(rec_copy["properties"]["0x84"], 0)) + "W")
                db_buff["air1_instant_power_84"] = int(rec_copy["properties"]["0x84"], 0)
            if rec_copy.get("properties", {}).get("0x85", 0):
                air_85.set(str(int(rec_copy["properties"]["0x85"], 0)) + "kWh")
                db_buff["air1_cum_power_85"] = int(rec_copy["properties"]["0x85"], 0)
        # PCS
        if ((rec_copy["cls"] == ENL_win_globals.pcs_class) and (rec_copy["id"] == ENL_win_globals.pcs_id)):
            if rec_copy.get("properties", {}).get("0x80", 0):
                if (rec_copy["properties"]["0x80"] == "0x30"):
                    pcs_80.set("ON")
                if (rec_copy["properties"]["0x80"] == "0x31"):
                    pcs_80.set("OFF")
            if rec_copy.get("properties", {}).get("0xA0", 0):
                pcs_a0.set(str(int(rec_copy["properties"]["0xA0"], 0)) + "%")
            if rec_copy.get("properties", {}).get("0xB2", 0):
                if (rec_copy["properties"]["0xB2"] == "0x41"):
                    pcs_b2.set("Valid")
                if (rec_copy["properties"]["0xB2"] == "0x42"):
                    pcs_b2.set("Invalid")
            if rec_copy.get("properties", {}).get("0xB3", 0):
                pcs_b3.set(str(int(rec_copy["properties"]["0xB3"], 0)) + "s")
            if rec_copy.get("properties", {}).get("0xB4", 0):
                pcs_b4.set(str(int(rec_copy["properties"]["0xB4"], 0)) + "W")
            if rec_copy.get("properties", {}).get("0xC0", 0):
                pcs_c0.set(str(int(rec_copy["properties"]["0xC0"], 0)) + "%")
            if rec_copy.get("properties", {}).get("0xC1", 0):
                if (rec_copy["properties"]["0xC1"] == "0x41"):
                    pcs_c1.set("FIT")
                if (rec_copy["properties"]["0xC1"] == "0x42"):
                    pcs_c1.set("Non-FIT")
                if (rec_copy["properties"]["0xC1"] == "0x43"):
                    pcs_c1.set("No setting")
            if rec_copy.get("properties", {}).get("0xC2", 0):
                if (rec_copy["properties"]["0xC2"] == "0x41"):
                    pcs_c2.set("With self-consumption")
                if (rec_copy["properties"]["0xC2"] == "0x42"):
                    pcs_c2.set("Without self-consumption")
                if (rec_copy["properties"]["0xC2"] == "0x43"):
                    pcs_c2.set("Unknown")
            if rec_copy.get("properties", {}).get("0xC3", 0):
                pcs_c3.set(str(int(rec_copy["properties"]["0xC3"], 0)) + "W")
            if rec_copy.get("properties", {}).get("0xD0", 0):
                if (rec_copy["properties"]["0xD0"] == "0x00"):
                    pcs_d0.set("Reverse power flow acceptable")
                if (rec_copy["properties"]["0xD0"] == "0x01"):
                    pcs_d0.set("Independent type")
                if (rec_copy["properties"]["0xD0"] == "0x02"):
                    pcs_d0.set("Reverse power flow not acceptable")
                if (rec_copy["properties"]["0xD0"] == "0x03"):
                    pcs_d0.set("Unknown")
            if rec_copy.get("properties", {}).get("0xD1", 0):
                if (rec_copy["properties"]["0xD1"] == "0x41"):
                    pcs_d1.set("Output power control")
                if (rec_copy["properties"]["0xD1"] == "0x42"):
                    pcs_d1.set("Except output power control")
                if (rec_copy["properties"]["0xD1"] == "0x43"):
                    pcs_d1.set("Reason for restraint is unknown")
                if (rec_copy["properties"]["0xD1"] == "0x44"):
                    pcs_d1.set("Not restraining")
                if (rec_copy["properties"]["0xD1"] == "0x45"):
                    pcs_d1.set("Unknown")
            if rec_copy.get("properties", {}).get("0xE0", 0):
                pcs_e0.set(str(int(rec_copy["properties"]["0xE0"], 0)) + "W")
                db_buff["pcs_instant_gen_E0"] = int(rec_copy["properties"]["0xE0"], 0)
            if rec_copy.get("properties", {}).get("0xE1", 0):
                pcs_e1.set(str(int(rec_copy["properties"]["0xE1"], 0)) + "kW")
                db_buff["pcs_cum_gen_E1"] = int(rec_copy["properties"]["0xE1"], 0)
            if rec_copy.get("properties", {}).get("0xE3", 0):
                pcs_e3.set(str(int(rec_copy["properties"]["0xE3"], 0)) + "kW")
                db_buff["pcs_cum_sold_E3"] = int(rec_copy["properties"]["0xE3"], 0)
            if rec_copy.get("properties", {}).get("0xE5", 0):
                pcs_e5.set(str(int(rec_copy["properties"]["0xE5"], 0)) + "%")
            if rec_copy.get("properties", {}).get("0xE8", 0):
                pcs_e8.set(str(int(rec_copy["properties"]["0xE8"], 0)) + "W")
        # PV
        if ((rec_copy["cls"] == pv_class) and (rec_copy["id"] == ENL_win_globals.pv_id)):
            if rec_copy.get("properties", {}).get("0xE1", 0):
                if (rec_copy["properties"]["0xE1"] == "0x00"):
                    pv_e1.set("1kWh")
                if (rec_copy["properties"]["0xE1"] == "0x01"):
                    pv_e1.set("0.1kWh")
                if (rec_copy["properties"]["0xE1"] == "0x02"):
                    pv_e1.set("0.01kWh")
                if (rec_copy["properties"]["0xE1"] == "0x03"):
                    pv_e1.set("0.001kWh")
                if (rec_copy["properties"]["0xE1"] == "0x04"):
                    pv_e1.set("0.0001kWh")
                if (rec_copy["properties"]["0xE1"] == "0x0A"):
                    pv_e1.set("10kWh")
                if (rec_copy["properties"]["0xE1"] == "0x0B"):
                    pv_e1.set("100kWh")
                if (rec_copy["properties"]["0xE1"] == "0x0C"):
                    pv_e1.set("1000kWh")
                if (rec_copy["properties"]["0xE1"] == "0x0D"):
                    pv_e1.set("10000kWh")
            if rec_copy.get("properties", {}).get("0xE7", 0):
                if (hex_to_decimal(rec_copy["properties"]["0xE7"], 32) < 16777215): #display less than FFFFFF to avoid bugs in E7
                    pv_e7.set(str(hex_to_decimal(rec_copy["properties"]["0xE7"], 32)/10) + "W")
                    db_buff["pv_instant_E7"] = (hex_to_decimal(rec_copy["properties"]["0xE7"], 32)/10)
                else:
                    pv_e7.set("0W")
                    db_buff["pv_instant_E7"] = 0
            if rec_copy.get("properties", {}).get("0xE8", 0):
                pv_e8.set(str(hex_to_decimal(rec_copy["properties"]["0xE8"][2:6], 16)/100) + "A" + " / " + str(hex_to_decimal(rec_copy["properties"]["0xE8"][6:10], 16)/100) + "A")
                db_buff["pv_instant_E8"] = str(hex_to_decimal(rec_copy["properties"]["0xE8"][2:6], 16)/100) + "A" + " / " + str(hex_to_decimal(rec_copy["properties"]["0xE8"][6:10], 16)/100) + "A"
            if rec_copy.get("properties", {}).get("0xEA", 0):
                pv_ea.set(str(int("0x" + rec_copy["properties"]["0xEA"][-8:], 0)/100) + "Wh")
                db_buff["pv_cum_import_EA"] = int("0x" + rec_copy["properties"]["0xEA"][-8:], 0)/100
            if rec_copy.get("properties", {}).get("0xEB", 0):
                pv_eb.set(str(int("0x" + rec_copy["properties"]["0xEB"][-8:], 0)/100) + "Wh")
                db_buff["pv_cum_export_EB"] = int("0x" + rec_copy["properties"]["0xEB"][-8:], 0)/100
            if rec_copy.get("properties", {}).get("0xE0", 0):
                pv_e0.set(str(int("0x" + rec_copy["properties"]["0xE0"][-8:], 0)/10) + "Wh")
                db_buff["pv_cum_import_E0"] = int("0x" + rec_copy["properties"]["0xE0"][-8:], 0)/10
            if rec_copy.get("properties", {}).get("0xE3", 0):
                pv_e3.set(str(int("0x" + rec_copy["properties"]["0xE3"][-8:], 0)/10) + "Wh")
                db_buff["pv_cum_export_E3"] = int("0x" + rec_copy["properties"]["0xE3"][-8:], 0)/10
        # Utility
        if ((rec_copy["cls"] == rb_class) and (rec_copy["id"] == ENL_win_globals.rb_id)):
            if rec_copy.get("properties", {}).get("0xE1", 0):
                if (rec_copy["properties"]["0xE1"] == "0x00"):
                    rb_e1.set("1kWh")
                if (rec_copy["properties"]["0xE1"] == "0x01"):
                    rb_e1.set("0.1kWh")
                if (rec_copy["properties"]["0xE1"] == "0x02"):
                    rb_e1.set("0.01kWh")
                if (rec_copy["properties"]["0xE1"] == "0x03"):
                    rb_e1.set("0.001kWh")
                if (rec_copy["properties"]["0xE1"] == "0x04"):
                    rb_e1.set("0.0001kWh")
                if (rec_copy["properties"]["0xE1"] == "0x0A"):
                    rb_e1.set("10kWh")
                if (rec_copy["properties"]["0xE1"] == "0x0B"):
                    rb_e1.set("100kWh")
                if (rec_copy["properties"]["0xE1"] == "0x0C"):
                    rb_e1.set("1000kWh")
                if (rec_copy["properties"]["0xE1"] == "0x0D"):
                    rb_e1.set("10000kWh")
            if rec_copy.get("properties", {}).get("0xE7", 0):
                rb_e7.set(str(hex_to_decimal(rec_copy["properties"]["0xE7"], 32)) + "W")
                db_buff["rb_instant_E7"] = (hex_to_decimal(rec_copy["properties"]["0xE7"], 32))
            if rec_copy.get("properties", {}).get("0xE8", 0):
                rb_e8.set(str(hex_to_decimal(rec_copy["properties"]["0xE8"][2:6], 16)/10) + "A" + " / " + str(hex_to_decimal(rec_copy["properties"]["0xE8"][6:10], 16)/10) + "A")
                db_buff["rb_instant_E8"] = str(hex_to_decimal(rec_copy["properties"]["0xE8"][2:6], 16)/100) + "A" + " / " + str(hex_to_decimal(rec_copy["properties"]["0xE8"][6:10], 16)/100) + "A"
            if rec_copy.get("properties", {}).get("0xEA", 0):
                rb_ea.set(str(int("0x" + rec_copy["properties"]["0xEA"][-8:], 0)/10) + "Wh")
                db_buff["rb_cum_import_EA"] = int("0x" + rec_copy["properties"]["0xEA"][-8:], 0)/10
            if rec_copy.get("properties", {}).get("0xEB", 0):
                rb_eb.set(str(int("0x" + rec_copy["properties"]["0xEB"][-8:], 0)/10) + "Wh")
                db_buff["rb_cum_export_EB"] = int("0x" + rec_copy["properties"]["0xEB"][-8:], 0)/10
            if rec_copy.get("properties", {}).get("0xE0", 0):
                rb_e0.set(str(int("0x" + rec_copy["properties"]["0xE0"][-8:], 0)/10) + "Wh")
                db_buff["rb_cum_import_E0"] = int("0x" + rec_copy["properties"]["0xE0"][-8:], 0)/10
            if rec_copy.get("properties", {}).get("0xE3", 0):
                rb_e3.set(str(int("0x" + rec_copy["properties"]["0xE3"][-8:], 0)/10) + "Wh")
                db_buff["rb_cum_export_E3"] = int("0x" + rec_copy["properties"]["0xE3"][-8:], 0)/10
    root.after(1000, status_update)

def update():
    global db_buff
    # Connect to datebase
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "Hugo1983522",
            database = "enl",
        )
    my_cursor = mydb.cursor()
    # Write response date to database
    if len(db_buff) > 0:
        db_buff["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        TABLE_name = "enl_data1"
        columns = ", ".join(db_buff.keys())
        values = ", ".join(["%s"] * len(db_buff))
        query = f"INSERT INTO {TABLE_name} ({columns}) VALUES ({values})"
        try:
            my_cursor.execute(query, tuple(db_buff.values()))
            mydb.commit()
        except (mydb.Error, mydb.Warning) as e:
            print(e)
        db_buff.clear()
    # Disconnect to datebase
    my_cursor.close()
    mydb.close()
    # Publish enguiry command to S2C
    for status in ENL_win_globals.statuses:
        ENL_win.publish_mqtt(hexlify(status.encode()).decode())
        time.sleep(2)
        
def auto_update():
    while (auto.get() == 1):
        update()
        time.sleep(int(interval.get()))

def connect():
    global meterID, interval
    meterID = meter_id.get()
    t1 = threading.Thread(target=connect_mqtt, args=(meterID,))
    t1.start()
    t2 = threading.Thread(target=auto_update)
    t2.start()
    status_update()

def export():
    query = "SELECT * FROM enl_data1"
    # Connect to datebase
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "Hugo1983522",
            database = "enl",
        )
    my_cursor = mydb.cursor()
    # Load database to dateframe
    try:
        df = pd.read_sql(query, con=mydb)
        df.to_csv('output.csv', index=False)
        my_cursor.execute(query, tuple(db_buff.values()))
        mydb.commit()
    except Exception as e:
        print(e)
    # Disconnect to datebase
    my_cursor.close()
    mydb.close()

def graph_plot():    
    global newdate, today
    def start_plot():
        global newdate
        graph = Toplevel()
        graph.title(y_axis.get())
        # Connect to datebase
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "Hugo1983522",
            database = "enl",
        )
        my_cursor = mydb.cursor()
        # Get data from database and plot graph
        query = 'SELECT * FROM enl_data1 WHERE time BETWEEN %s AND %s'
        query_params = (newdate.strftime('%Y-%m-%d'), (newdate + timedelta(days=1)).strftime('%Y-%m-%d'))
        df = pd.read_sql(query, con=mydb, params=query_params)
        fig, ax = plt.subplots(figsize=(8, 6))
        df.plot(ax=ax, x='time', y=y_axis.get(),  kind='line', title= newdate.strftime('%Y-%m-%d'))
        canvas = FigureCanvasTkAgg(fig, master=graph)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        # Disconnect to datebase
        my_cursor.close()
        mydb.close()

    plot_win = Toplevel()
    plot_win.title('Graph Panel')
    frame_plot = LabelFrame(plot_win, padx=5, pady=5, border=0)
    frame_plot.pack(padx=10, pady=10, anchor=W)
    frame_plot2 = LabelFrame(plot_win, padx=5, pady=5, border=0)
    frame_plot2.pack(padx=10, pady=10, anchor=W)
    items_Lable = Label(frame_plot, text="Plot Items:")
    items_Lable.grid(row=0, column=0, padx=10, pady=10, sticky=W)
    
    ecocute_Lable = Label(frame_plot, text="Eco-Cute:")
    ecocute_Lable.grid(row=0, column=1, padx=10, pady=10, sticky=W)
    y_axis = StringVar()
    y_axis.set('eco_heat_temp_C1')
    eco_c1_plot = Radiobutton(frame_plot, text='Heat Temp (C1)', variable=y_axis, value='eco_heat_temp_C1')
    eco_c1_plot.grid(row=0, column=2, padx=10, sticky=W)
    eco_e1_plot = Radiobutton(frame_plot, text='Water Remain (E1)', variable=y_axis, value='eco_water_remain_E1')
    eco_e1_plot.grid(row=0, column=3, padx=10, sticky=W)

    battery_Lable = Label(frame_plot, text="Battery:")
    battery_Lable.grid(row=1, column=1, padx=10, pady=10, sticky=W)
    batt_d3_plot = Radiobutton(frame_plot, text='Instant Power (D3)', variable=y_axis, value='bat_instant_power_D3')
    batt_d3_plot.grid(row=1, column=2, padx=10, sticky=W)
    batt_e2_plot = Radiobutton(frame_plot, text='Remain (E3)', variable=y_axis, value='bat_remain_E2')
    batt_e2_plot.grid(row=1, column=3, padx=10, sticky=W)
    batt_e4_plot = Radiobutton(frame_plot, text='Remain (E4)', variable=y_axis, value='bat_remain_E4')
    batt_e4_plot.grid(row=1, column=4, padx=10, sticky=W)
    
    ac1_Lable = Label(frame_plot, text="Air-Con1:")
    ac1_Lable.grid(row=2, column=1, padx=10, pady=10, sticky=W)
    ac1_bb_plot = Radiobutton(frame_plot, text='Room Temp (BB)', variable=y_axis, value='air1_room_temp_BB')
    ac1_bb_plot.grid(row=2, column=2, padx=10, sticky=W)
    ac1_be_plot = Radiobutton(frame_plot, text='Outdoor Temp (BE)', variable=y_axis, value='air1_outdoor_temp_BE')
    ac1_be_plot.grid(row=2, column=3, padx=10, sticky=W)
    ac1_84_plot = Radiobutton(frame_plot, text='Instant (84)', variable=y_axis, value='air1_instant_power_84')
    ac1_84_plot.grid(row=2, column=4, padx=10, sticky=W)

    ac2_Lable = Label(frame_plot, text="Air-Con2:")
    ac2_Lable.grid(row=3, column=1, padx=10, pady=10, sticky=W)
    ac2_bb_plot = Radiobutton(frame_plot, text='Room Temp (BB)', variable=y_axis, value='air2_room_temp_BB')
    ac2_bb_plot.grid(row=3, column=2, padx=10, sticky=W)
    ac2_be_plot = Radiobutton(frame_plot, text='Outdoor Temp (BE)', variable=y_axis, value='air2_outdoor_temp_BE')
    ac2_be_plot.grid(row=3, column=3, padx=10, sticky=W)

    pcs_Lable = Label(frame_plot, text="PCS:")
    pcs_Lable.grid(row=4, column=1, padx=10, pady=10, sticky=W)
    pcs_e0_plot = Radiobutton(frame_plot, text='Instant generated (E0)', variable=y_axis, value='pcs_instant_gen_E0')
    pcs_e0_plot.grid(row=4, column=2, padx=10, sticky=W)

    pv_Lable = Label(frame_plot, text="PV:")
    pv_Lable.grid(row=5, column=1, padx=10, pady=10, sticky=W)
    pv_e7_plot = Radiobutton(frame_plot, text='Instant Power (E7)', variable=y_axis, value='pv_instant_E7')
    pv_e7_plot.grid(row=5, column=2, padx=10, sticky=W)
    
    rb_Lable = Label(frame_plot, text="Utility:")
    rb_Lable.grid(row=6, column=1, padx=10, pady=10, sticky=W)
    rb_e7_plot = Radiobutton(frame_plot, text='Instant Power (E7)', variable=y_axis, value='rb_instant_E7')
    rb_e7_plot.grid(row=6, column=2, padx=10, sticky=W)

    date_Lable = Label(frame_plot2, text="Date:")
    date_Lable.grid(row=7, column=0, padx=10, pady=10, sticky=W)
    currentDate = StringVar()
    today = datetime.now()
    currentDate.set(today.strftime('%Y-%m-%d'))
    newdate = today
    date_range = Entry(frame_plot2, textvariable = currentDate, width=10)
    date_range.grid(row=7, column=1, padx=10, sticky=E)
    
    def down():
        global newdate
        newdate = (newdate - timedelta(days=1))
        currentDate.set(newdate.strftime('%Y-%m-%d'))
    def up():
        global newdate
        newdate = (newdate + timedelta(days=1))
        currentDate.set(newdate.strftime('%Y-%m-%d'))
    def reset_date():
        global newdate
        newdate = today
        currentDate.set(newdate.strftime('%Y-%m-%d'))

    downButton = Button(frame_plot2, text="Down", command=down)
    downButton.grid(row=7, column=2, padx=10)
    todayButton = Button(frame_plot2, text="Today", command=reset_date)
    todayButton.grid(row=7, column=3, padx=10)
    upButton = Button(frame_plot2, text="Up", command=up)
    upButton.grid(row=7, column=4, padx=10)
    plotButton = Button(frame_plot2, text="Plot", command=start_plot)
    plotButton.grid(row=7, column=5, padx=10)

#Create Main upper part of user interface
meterLabel = Label(frame_upper, text="Meter ID")
meterLabel.grid(row=0, column=0, padx=10, pady=15, sticky=W)
meter_id = Entry(frame_upper, textvariable = meterID, width=15)
meter_id.grid(row=0, column=1, padx=10, sticky=E)
connectButton = Button(frame_upper, text="Connect", command=connect)
connectButton.grid(row=0, column=2, padx=10)
exportButton = Button(frame_upper, text="Export Data", command=export)
exportButton.grid(row=0, column=3, padx=10)
graphButton = Button(frame_upper, text="Graph", command=graph_plot)
graphButton.grid(row=0, column=4, padx=10)
lastupdateLabel = Label(frame_upper, text="Last update time:")
lastupdateLabel.grid(row=0, column=5, padx=10, columnspan=2 ,pady=10, sticky=W)
last_time = StringVar()
lastupdate = Entry(frame_upper, textvariable = last_time, width=18)
lastupdate.grid(row=0, column=7, padx=10, sticky=E)

deviceLabel = Label(frame_upper, text="Device ID")
deviceLabel.grid(row=1, column=0, padx=10, sticky=W)
dev_id = Entry(frame_upper, width=15)
dev_id.grid(row=1, column=1, padx=10, sticky=E)
refreshButton = Button(frame_upper, text="Update", command=update)
refreshButton.grid(row=1, column=2, padx=10)

interval = StringVar()
interval.set(300)
auto = IntVar()
auto.set(1)
autoUpdate = Checkbutton(frame_upper, text='Auto Update', variable=auto, onvalue=1, offvalue=0)
autoUpdate.grid(row=1, column=3, padx=10, sticky=W)
autoLabel1 = Label(frame_upper, text="Interval:")
autoLabel1.grid(row=1, column=4, padx=5, sticky=E)
auto_interval = Entry(frame_upper, textvariable = interval, width=7)
auto_interval.grid(row=1, column=5, padx=0, sticky=E)
autoLabel2 = Label(frame_upper, text="sec")
autoLabel2.grid(row=1, column=6, padx=0, sticky=W)

mainloop()