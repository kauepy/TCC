import ipython_pygments_lexers 
codigo = """led = Led(13)

while True:
    led.on()
    wait(1000)
    led.off()
    wait(1000)
"""

for token in tokenizar_arquivo(codigo):
    print(token)