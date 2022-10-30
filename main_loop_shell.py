from get_ina219_0x40 import measure, camera_shoot


a = "Open"
while a!= "close":
    a = input("Ingrese el comando: ")
    list = ["aa","bb","cc","dd","get_v","TAKE_PIC","close"]
    if a in list:
        print("Comando recibido")
        if a =="get_v":
            add = input("Sensor a usar:")
            ad_list = ["0x40","0x41"]
            dic = {"0x40":0x40,"0x41":0x41}
            if add in ad_list:
                addres = dic[add]
                measure(2,0.2,add,"w",address=addres)
            else:
                print("Sensor no encontrado.")
                
        elif a =="TAKE_PIC":
            camera_shoot()
        
            
            
        elif a =="close":
            print("Cerrando")

    else:
        print("Comando erroneo")
    
        
