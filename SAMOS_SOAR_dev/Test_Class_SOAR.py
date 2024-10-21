from soar_tcs import SoarTCS
TCS = SoarTCS(host='139.229.15.2',port=40050)
print(TCS.is_connected(),'\n')
print(TCS.way())

target={"offset_ra":0.00, "offset_dec":0.00}
print("offset returned:",TCS.offset(target),'\n')

#print(TCS.focus(0,'relative'),'\n')
print(TCS.clm("OUT"))

#print(TCS.guider("PARK"))

#print(TCS.whitespot(0,False))

#print(TCS.get_lamp_number('Cu-He-Ar'),'\n')

print(TCS.lamp(1,"OFF",0),'\n')

lamps = {'lamp_0':0, 'lamp_1':0}
print(TCS.lamps_turn_on(lamps),'\n')

a=TCS.infoa()
print(a)
# Extracting all dictionary values
# Using values()
res = list(a.values()) 
# printing result
print("The list of values is : " +  str(res))
print(a['LAMP_1'])

print(TCS.rotator("TRACK_OFF"))

#print(TCS.ipa(0))

#print(TCS.instrument("SAMI"))

print(TCS.rotator("TRACK_OFF"))

target = {"ra": 0.00, "dec":0.00, "epoch":2000.0}
#print(TCS.target_move(target))

print(TCS.get_mount_position())

print(TCS.ADC(""))

