import csv
import requests

BASE = "http://localhost:58000/api/v1"

# 1) Pedir el ticket con el usuario del controlador
resp = requests.post(BASE + "/ticket", json={"username": "cisco", "password": "class"})
ticket = resp.json()["response"]["serviceTicket"]
headers = {"X-Auth-Token": ticket}

# 2) Consultar los equipos y los hosts que ve el controlador
equipos = requests.get(BASE + "/network-device", headers=headers).json()["response"]
hosts = requests.get(BASE + "/host", headers=headers).json()["response"]

# 3) Guardar todo en un archivo CSV
with open("inventario.csv", "w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.writer(archivo, delimiter=";")
    escritor.writerow(["Tipo", "Nombre", "Modelo", "IP", "MAC", "Estado / Interfaz"])
    for e in equipos:
        escritor.writerow(["Equipo", e.get("hostname", "(sin hostname)"), e.get("platformId", ""),
                           e.get("managementIpAddress", ""), e.get("macAddress", ""),
                           e.get("collectionStatus", "")])
    for h in hosts:
        escritor.writerow(["Host", h.get("hostName", ""), "", h.get("hostIp", ""),
                           h.get("hostMac", ""), h.get("connectedInterfaceName", "")])

print("Equipos:", len(equipos), "- Hosts:", len(hosts))
print("Archivo generado: inventario.csv")