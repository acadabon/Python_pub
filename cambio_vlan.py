from netmiko import ConnectHandler
import re
from getpass import getpass

# AGREGAR COLORES A LOS PRINTS##
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'
# RESETEA EL COLOR AL DEFAULT
RESET = '\033[0m'

IP = input ("Ingrese la ip del switch: ")
sw_username = input("Ingrese el usuario (Enter=acadabon): ")
if sw_username == "":
    sw_username = "acadabon"
    sw_password = getpass()        
vlan_actual = input ("Ingrese la vlan actual: ")
vlan_nueva = input ("Ingrese la vlan nueva: ")
# Datos de conexión al switch
cisco_switch = {
    'device_type': 'cisco_ios',
    'host': IP,      # IP del switch
    'username': sw_username,
    'password': sw_password,
    #'secret': 'tu_enable_secret',  # opcional, si se requiere enable
}

# Conectarse al switch
net_connect = ConnectHandler(**cisco_switch)
net_connect.enable()

# Obtener la configuración de interfaces
output = net_connect.send_command("show running-config | section interface")

# Buscar interfaces en acceso con la VLAN específica
interfaces = []
for section in output.split("interface "):
    if f"switchport access vlan {vlan_actual}" in section and "switchport mode access" in section:
        interface_name = section.splitlines()[0]
        interfaces.append(interface_name)

# Mostrar interfaces encontradas
print(GREEN +f"Interfaces encontradas en VLAN {vlan_actual}:\n {RED}{interfaces}" + RESET )

# Cambiar la VLAN de cada interfaz#
for intf in interfaces:
    config_commands = [
        f"interface {intf}",
        f"switchport access vlan {vlan_nueva}",
    ]
    print(GREEN+f"Cambiando {intf} a VLAN {vlan_nueva}")
    net_connect.send_config_set(config_commands)

# Guardar cambios
net_connect.save_config()

# Cerrar conexión
net_connect.disconnect()

print("¡Cambio de VLAN completado!"+RESET)
