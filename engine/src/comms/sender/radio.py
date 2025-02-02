import serial
   
def limitar_a_10_bits(numero):
    # Limitar el rango del número a 10 bits (incluyendo el bit de signo) (para V_x y V_y)
    return max(-512, min(511, numero))

def limitar_a_12_bits(numero):
    # Limitar el rango del número a 12 bits (incluyendo el bit de signo) (para V_th)
    return max(-2048, min(2047, numero))

def entero_a_binario(n, longitud):
    if n == 0:
        return '0' * longitud
    signo = '0' if n >= 0 else '1'
    n = abs(n)
    binario = ''
    while n > 0:
        binario = str(n % 2) + binario
        n //= 2
    return signo + (binario).zfill(longitud-1)

# Función para formar un trozo de 5 bytes con la estructura especificada
def formar_trozo(id_,dribb,kick, velocidad_x, velocidad_y, velocidad_th):
    #Se saturan los numeros a 10 bits (+511 -512) y 12 bits (+2047 -2048) respectivamente
    velocidad_x = limitar_a_10_bits(velocidad_x)
    velocidad_y = limitar_a_10_bits(velocidad_y)
    velocidad_th = limitar_a_12_bits(velocidad_th)

    a =  entero_a_binario(velocidad_x,10) 
    b = entero_a_binario(velocidad_y,10)
    c = entero_a_binario(velocidad_th,12)

    # Formar el trozo de 5 bytes
    trozo = bytearray([
        (((((id_<<3)+dribb)<<1)+kick)<<1),  # Primer byte: id | dribb | kick
        int(a[0] + (a[3:]),2),  # segundo byte: signo | LSB Vx
        int(b[0] + (b[3:]),2),  # Tercer byte: signo | LSB Vy
        int(c[0] + (c[5:]),2),  # Cuarto byte: signo | LSB Vth
        int((a[1:3]) + (b[1:3]) + (c[1:5]),2)  # Quinto byte: MSB Vx | MSB Vy |MSB Vth  int(velocidad_x >> 6) | ((velocidad_y >> 6) << 2) | ((velocidad_th >> 4) << 4)
    ])
    return trozo


class Radio():
    def __init__(self):
        self.int_to_byte = {
            0: 0b001,
            1: 0b010,
            2: 0b011,
            3: 0b100,
            4: 0b101,
            5: 0b110
        }
        self.puerto_serial = serial.Serial('/dev/ttyUSB0', 115200, bytesize=8, parity='N', stopbits=1, timeout=1) 

    def send_packets(self, robot_packets : list[list]):
        ids = [0,1,2,3,4,5]
        trozos = [0,0,0,0,0,0]
        for p in robot_packets:
            id = p[0]
            dribble_speed = p[1]
            kick_on = p[2]
            vx = p[3]
            vy = p[4]
            angular_velocity = p[5]
            
            packet = formar_trozo(self.int_to_byte[id], dribble_speed, kick_on, vx, vy , angular_velocity)
            trozos[id] = packet
            ids.remove(int(id))
        
        
        for id in ids:
            trozos[id] = formar_trozo(self.int_to_byte[id], 0,0,0,0,0)
        print(" ")
        print(trozos)
        buffer = bytearray(30)
        for i in range(6):
            if i == 0:
                print(trozos[i])
            buffer[i*5:i*5+5] = trozos[i]
        
        self.puerto_serial.write(buffer)

    def delete(self):
        self.puerto_serial.close()
