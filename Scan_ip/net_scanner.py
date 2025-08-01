"""
net_scanner.py
Scanner une plage d'adresses IP entre deux adresses données par l'utilisateur.
Les résultats sont affichés et enregistrés sur le Bureau.
"""

import csv
import ipaddress
import platform
import subprocess
import os
from datetime import datetime

def ping(ip):
    """Vérifie si une IP répond au ping."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        subprocess.check_output(["ping", param, "1", str(ip)], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def ip_range(start_ip, end_ip):
    """Génère toutes les adresses IP entre start_ip et end_ip incluses."""
    start = int(ipaddress.IPv4Address(start_ip))
    end = int(ipaddress.IPv4Address(end_ip))
    return [str(ipaddress.IPv4Address(ip)) for ip in range(start, end+1)]

def scan_custom_range(start_ip, end_ip):
    """Scanne toutes les IP entre deux adresses."""
    ips = ip_range(start_ip, end_ip)
    results = []
    for ip in ips:
        active = ping(ip)
        results.append((ip, 'Active' if active else 'Inactive'))
    return results

def save_results(results):
    """Sauvegarde les résultats sur le Bureau avec un nom de fichier horodaté."""
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scan_{date_str}.csv"
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_path = os.path.join(desktop_path, filename)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['IP', 'Status'])
        for row in results:
            writer.writerow(row)

    print(f"\n✅ Fichier enregistré sur le Bureau : {output_path}")

def main():
    """Programme principal"""
    print("=== Scanner IP personnalisé ===")
    start_ip = input("Entrez la première IP (ex: 192.168.1.10) : ")
    end_ip = input("Entrez la dernière IP (ex: 192.168.1.254) : ")

    print(f"\n🔍 Scan des IP de {start_ip} à {end_ip}...\n")
    results = scan_custom_range(start_ip, end_ip)

    for ip, status in results:
        print(f"{ip} - {status}")

    save_results(results)

if __name__ == '__main__':
    main()
