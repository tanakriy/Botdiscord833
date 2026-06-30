import os
import subprocess
import time
import re
import ipaddress
import socket

# ==============================================
# 🛠️ ตรวจสอบเครื่องมือ
# ==============================================
def install_tools():
    print("=" * 60)
    print("📥 ตรวจสอบและติดตั้งเครื่องมือ...")
    print("=" * 60)
    try:
        subprocess.run(["pkg", "update", "-y"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["pkg", "install", "-y", "python", "nmap", "net-tools", "iproute2"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["pip", "install", "--upgrade", "speedtest-cli"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ ติดตั้งเสร็จสิ้น!")
        time.sleep(1)
    except Exception as e:
        print(f"❌ ผิดพลาด: {e}")
        time.sleep(2)

# ==============================================
# 📡 ดึงช่วง IP เครือข่าย/ฮอตสปอต
# ==============================================
def get_network_range():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return str(ipaddress.ip_network(f"{local_ip}/24", strict=False))
    except:
        return "192.168.43.0/24"

# ==============================================
# 🔍 สแกนอุปกรณ์ (ใช้ nmap แทน arp-scan)
# ==============================================
def scan_network():
    print("\n" + "=" * 60)
    print("📡 สแกนอุปกรณ์ที่เชื่อมต่อ")
    print("=" * 60)
    subnet = get_network_range()
    print(f"🌐 สแกนช่วง: {subnet}")
    print("-" * 60)
    print(f"{'IP Address':<18} {'MAC Address':<20} {'สถานะ'}")
    print("-" * 60)
    try:
        result = subprocess.check_output(["nmap", "-sn", "-PR", "-T4", subnet], text=True, stderr=subprocess.DEVNULL, timeout=30)
        ip = mac = None
        for line in result.splitlines():
            if "Nmap scan report for" in line:
                ip = re.search(r'\d+\.\d+\.\d+\.\d+', line).group()
            elif "MAC Address:" in line:
                mac = re.search(r'([0-9A-Fa-f:]{17})', line).group()
                print(f"{ip:<18} {mac:<20} 🟢 ออนไลน์")
    except Exception as e:
        print(f"⚠️ สแกนผิดพลาด: {e}")
    input("\nกด Enter เพื่อกลับเมนู...")

# ==============================================
# ⚡ ทดสอบความเร็วเน็ต
# ==============================================
def check_speed():
    print("\n" + "=" * 60)
    print("⚡ ทดสอบความเร็วอินเทอร์เน็ต")
    print("=" * 60)
    try:
        subprocess.run(["speedtest-cli"], check=True)
    except:
        print("❌ ไม่สามารถเรียกใช้ speedtest ได้")
    input("\nกด Enter เพื่อกลับเมนู...")

# ==============================================
# 📋 เมนูหลัก
# ==============================================
def main_menu():
    while True:
        os.system("clear")
        print("=" * 60)
        print("🛠️ ชุดเครื่องมือตรวจสอบเครือข่าย")
        print("=" * 60)
        print("1. ติดตั้ง/อัปเดตเครื่องมือ")
        print("2. สแกนอุปกรณ์ในเครือข่าย/ฮอตสปอต")
        print("3. ทดสอบความเร็วเน็ต")
        print("4. ออกจากโปรแกรม")
        print("-" * 60)
        choice = input("👉 เลือกเมนู: ")

        if choice == "1":
            install_tools()
        elif choice == "2":
            scan_network()
        elif choice == "3":
            check_speed()
        elif choice == "4":
            print("👋 จบการทำงาน")
            break
        else:
            print("❌ เลือกไม่ถูกต้อง")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
