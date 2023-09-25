#Global JSON commands

#ENL Devices
device_id = "0xFE000006010220F85EFFFE3A6B3C0EF001"
device_class = "0x026B01"
battery_id = "0xFE00006C30303030313930354133434236"
battery_class = "0x027D01"
air_id = "0xFE000008DCFE23C3D62A00000000000000"
air_class = "0x013001"
air2_id = "0xFE00000B00000EF00180C7550100004CE0"
air2_class = "0x013001"
pcs_id = "0xFE00006C30303030313930354133434236"
pcs_class = "0x027901"
pv_id = "J220006476"
pv_class = "0x028801"
rb_id = "0x000000BF870E77FC6B3C3D9B695A7180"
rb_class = "0x028801"

statuses = []
# commands for status update
statuses.append("{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"act\":[\"0x80\",\"0xB0\",\"0xB2\",\"0xB3\",\"0xB6\",\"0xC0\",\"0xC1\",\"0xC3\",\"0xD1\",\"0xD3\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"act\":[\"0xE1\",\"0xE2\",\"0xE3\",\"0xEA\",\"0xE5\",\"0xE6\",\"0xEE\",\"0x85\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"act\":[\"0xAA\",\"0xAB\",\"0xCF\",\"0xD3\",\"0xD6\",\"0xD8\",\"0xDA\",\"0xDB\",\"0xDC\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"act\":[\"0xDD\",\"0xE2\",\"0xE4\",\"0xE5\",\"0xE7\",\"0xE8\",\"0xEB\",\"0xEC\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"act\":[\"0x80\",\"0x8F\",\"0xB0\",\"0xB3\",\"0xB4\",\"0xBA\",\"0xBB\",\"0xBE\",\"0xA0\",\"0xA3\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"act\":[\"0x84\",\"0x85\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"act\":[\"0x80\",\"0x8F\",\"0xB0\",\"0xB3\",\"0xBA\",\"0xBB\",\"0xBE\",\"0xA0\",\"0xA1\",\"0xA4\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"act\":[\"0x85\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + pcs_id + "\",\"cls\":\"" + pcs_class + "\",\"act\":[\"0x80\",\"0xA0\",\"0xB2\",\"0xB3\",\"0xB4\",\"0xC0\",\"0xC1\",\"0xC2\",\"0xC3\",\"0xD0\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + pcs_id + "\",\"cls\":\"" + pcs_class + "\",\"act\":[\"0xD1\",\"0xE0\",\"0xE1\",\"0xE3\",\"0xE5\",\"0xE8\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + pv_id + "\",\"cls\":\"" + pv_class + "\",\"act\":[\"0xE0\",\"0xE3\",\"0xE1\",\"0xE7\",\"0xE8\",\"0xEA\",\"0xEB\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + rb_id + "\",\"cls\":\"" + rb_class + "\",\"act\":[\"0xE1\",\"0xE7\",\"0xE8\",\"0xEA\",\"0xEB\"],\"cmd\":\"GET\"}")
statuses.append("{\"id\":\"" + rb_id + "\",\"cls\":\"" + rb_class + "\",\"act\":[\"0x80\",\"0xE0\",\"0xE3\"],\"cmd\":\"GET\"}")

# command sets for Eco-cute
b0_cmd1 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x41\"}]}"
b0_cmd2 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x42\"}]}"
b0_cmd3 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x43\"}]}"
b6_cmd1 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB6\":\"0x41\"}]}"
b6_cmd2 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB6\":\"0x42\"}]}"
b6_cmd3 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB6\":\"0x43\"}]}"
c0_cmd1 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xC0\":\"0x41\"}]}"
c0_cmd2 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xC0\":\"0x42\"}]}"
e3_cmd1 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xE3\":\"0x41\"}]}"
e3_cmd2 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xE3\":\"0x42\"}]}"
e5_cmd1 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xE5\":\"0x41\"}]}"
e5_cmd2 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xE5\":\"0x42\"}]}"
e6_cmd1 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xE6\":\"0x41\"}]}"
e6_cmd2 = "{\"id\":\"" + device_id + "\",\"cls\":\"" + device_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xE6\":\"0x42\"}]}"

def tmp_cmd(cls, tmp, tmp_epc, id):
    if cls == "0x026B01":
        return "{\"id\":\"" + id + "\",\"cls\":\"" + cls + "\",\"cmd\":\"SET\",\"act\":[{\"0x" + tmp_epc + "\":\"" + tmp + "\"}]}"
    elif cls == "0x027D01":
        tmp = tmp[2:]
        while len(tmp) < 8:
            tmp = "0" + tmp
        tmp = "0x" + tmp
        return "{\"id\":\"" + id + "\",\"cls\":\"" + cls + "\",\"cmd\":\"SET\",\"act\":[{\"0x" + tmp_epc + "\":\"" + tmp + "\"}]}"
    elif (cls == "0x013001"):
        return "{\"id\":\"" + id + "\",\"cls\":\"" + cls + "\",\"cmd\":\"SET\",\"act\":[{\"0x" + tmp_epc + "\":\"" + tmp + "\"}]}"
    elif (cls == "0x027901"):
        return "{\"id\":\"" + id + "\",\"cls\":\"" + cls + "\",\"cmd\":\"SET\",\"act\":[{\"0x" + tmp_epc + "\":\"" + tmp + "\"}]}"

def flow_cmd(cls, tmp, tmp_epc, id):
    if cls == "0x013001":
        return "{\"id\":\"" + id + "\",\"cls\":\"" + cls + "\",\"cmd\":\"SET\",\"act\":[{\"0x" + tmp_epc + "\":\"" + tmp + "\"}]}"
    else:
        return ""

# Command sets for battery
bat_da_cmd1 = "{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xDA\":\"0x41\"}]}"
bat_da_cmd2 = "{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xDA\":\"0x42\"}]}"
bat_da_cmd3 = "{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xDA\":\"0x43\"}]}"
bat_da_cmd4 = "{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xDA\":\"0x44\"}]}"
bat_da_cmd5 = "{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xDA\":\"0x45\"}]}"
bat_da_cmd6 = "{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xDA\":\"0x46\"}]}"
bat_da_cmd8 = "{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xDA\":\"0x48\"}]}"
bat_da_cmd9 = "{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xDA\":\"0x49\"}]}"
bat_da_cmd0 = "{\"id\":\"" + battery_id + "\",\"cls\":\"" + battery_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xDA\":\"0x40\"}]}"

# Command sets for air con
air_80_cmd1 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0x80\":\"0x30\"}]}"
air_80_cmd2 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0x80\":\"0x31\"}]}"
air_8f_cmd1 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0x8F\":\"0x41\"}]}"
air_8f_cmd2 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0x8F\":\"0x42\"}]}"
air_b0_cmd1 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x41\"}]}"
air_b0_cmd2 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x42\"}]}"
air_b0_cmd3 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x43\"}]}"
air_b0_cmd4 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x44\"}]}"
air_b0_cmd5 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x45\"}]}"
air_b0_cmd6 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x40\"}]}"
air_a0_cmd1 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA0\":\"0x41\"}]}"
air_a3_cmd1 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA3\":\"0x31\"}]}"
air_a3_cmd2 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA3\":\"0x41\"}]}"
air_a3_cmd3 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA3\":\"0x42\"}]}"
air_a3_cmd4 = "{\"id\":\"" + air_id + "\",\"cls\":\"" + air_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA3\":\"0x43\"}]}"

# Command sets for air con
air2_80_cmd1 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0x80\":\"0x30\"}]}"
air2_80_cmd2 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0x80\":\"0x31\"}]}"
air2_8f_cmd1 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0x8F\":\"0x41\"}]}"
air2_8f_cmd2 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0x8F\":\"0x42\"}]}"
air2_b0_cmd1 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x41\"}]}"
air2_b0_cmd2 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x42\"}]}"
air2_b0_cmd3 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x43\"}]}"
air2_b0_cmd4 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x44\"}]}"
air2_b0_cmd5 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x45\"}]}"
air2_b0_cmd6 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xB0\":\"0x40\"}]}"
air2_a0_cmd1 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA0\":\"0x41\"}]}"
air2_a1_cmd1 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA1\":\"0x41\"}]}"
air2_a1_cmd2 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA1\":\"0x42\"}]}"
air2_a1_cmd3 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA1\":\"0x43\"}]}"
air2_a1_cmd4 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA1\":\"0x44\"}]}"
air2_a4_cmd1 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA4\":\"0x41\"}]}"
air2_a4_cmd2 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA4\":\"0x42\"}]}"
air2_a4_cmd3 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA4\":\"0x43\"}]}"
air2_a4_cmd4 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA4\":\"0x44\"}]}"
air2_a4_cmd5 = "{\"id\":\"" + air2_id + "\",\"cls\":\"" + air2_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xA4\":\"0x45\"}]}"
pcs_80_cmd1 = "{\"id\":\"" + pcs_id + "\",\"cls\":\"" + pcs_class + "\",\"cmd\":\"SET\",\"act\":[{\"0x80\":\"0x30\"}]}"
pcs_80_cmd2 = "{\"id\":\"" + pcs_id + "\",\"cls\":\"" + pcs_class + "\",\"cmd\":\"SET\",\"act\":[{\"0x80\":\"0x31\"}]}"
pcs_c1_cmd1 = "{\"id\":\"" + pcs_id + "\",\"cls\":\"" + pcs_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xC1\":\"0x41\"}]}"
pcs_c1_cmd2 = "{\"id\":\"" + pcs_id + "\",\"cls\":\"" + pcs_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xC1\":\"0x42\"}]}"
pcs_c1_cmd3 = "{\"id\":\"" + pcs_id + "\",\"cls\":\"" + pcs_class + "\",\"cmd\":\"SET\",\"act\":[{\"0xC1\":\"0x43\"}]}"