import serial
import time

# SCRIPT FEITO PARA EXTRAIR OS 4MB DE MEMORIA DO ROTEADOR ATRAVÉS DO COMANDO "MD" (MEMORY DISPLAY). ESSE PROCESSO É CONHECIDO COMO "DUMP".
# A CADA 0.1 SEGUNDO MANDA O COMANDO {MD <ADDR> 4} NO CONSOLE ATRAVÉS DA COMUNICAÇÃO SERIAL
# ESTE SCRIPT FOI ESSENCIAL PARA EXTRAIR OS DADOS SEM QUE HOUVESSE FALHAS NA COMUNICAÇÃO DEVIDO A TAXA DE COMUNICAÇÃO.
 
# CONFIGURAÇÕES
PORT = "/dev/ttyUSB0"
BAUDRATE = 115200
FLASH_BASE = 0x9f035590     # 0x9f000000 < esta é a flash base, porém como eu parei o script para ajustar o time.sleep decidi continuar de onde parei
FLASH_SIZE = 0x400000       # 4MB
WORD_SIZE = 16              # 4 bytes por palavra (vezes 4 palavras = 16bytes) 
WORDS_TOTAL = FLASH_SIZE // WORD_SIZE

LOG_FILE = "dump_word_by_word.log"

def open_serial():
    return serial.Serial(PORT, BAUDRATE, timeout=0.5)

def send_command(ser, cmd):
    ser.write((cmd + "\n").encode("utf-8"))
    ser.flush()

def read_line(ser):
    line = b""
    while True:
        char = ser.read(1)
        if not char:
            break
        line += char
        if char == b"\n":
            break
    return line.decode(errors="ignore").strip()

def main():
    ser = open_serial()
    print(f"Conectado em {PORT}")
    addr = FLASH_BASE

    with open(LOG_FILE, "a") as log:
        for i in range((addr - 0x9f000000) // WORD_SIZE, WORDS_TOTAL):
            print(f"Lendo o endereço: {hex(addr)}")
            cmd = f"md {hex(addr)} 4"
            send_command(ser, cmd)

            for _ in range(2): 
                line = read_line(ser)
                if line and line.startswith(hex(addr)[2:]):
                    log.write(line + "\n")
                    log.flush()
                    print(f"{i+1}/{WORDS_TOTAL}] {line}")
                    break
                time.sleep(0.1)

            addr += WORD_SIZE
            time.sleep(0.1)

    ser.close()
    print(f"Dump salvo em {LOG_FILE}")

if __name__ == "__main__":
    main()
