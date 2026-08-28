import subprocess

CAMINHO_CLI = r"arduino-cli\arduino-cli.exe"
FQBN_UNO = "arduino:avr:uno"


def compilar(caminho_sketch):
    resultado = subprocess.run(
        [CAMINHO_CLI, "compile", "--fqbn", FQBN_UNO, caminho_sketch],
        capture_output=True,
        text=True,
    )

    if resultado.returncode == 0:
        print("Compilação OK")
        print(resultado.stdout)
    else:
        print("Erro na compilação")
        print(resultado.stderr)

compilar("blink_test")