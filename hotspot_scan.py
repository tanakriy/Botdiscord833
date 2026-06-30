import os
import subprocess
import time
import re

# ==============================================
# 🛠️ ส่วนติดตั้งเครื่องมืออัตโนมัติ
# ==============================================
def install_tools():
    print("=" * 60)
    print("📥 กำลังตรวจสอบและติดตั้งเครื่องมือที่จำเป็น...")
    print("=" * 60)
    tools = [
        "python", "nmap", "net-tools", "iproute2", "arp-scan",
        "wireless-tools", "speedtest-cli", "tcpdump", "curl", "git"
    ]
    try:
        subprocess.run(["pkg", "update", "-y"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["pkg", "upgrade", "-y"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for tool in tools:
            print(f"🔧 ติดตั้ง: {tool}")
            subprocess.run(["pkg", "install", "-y", tool], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["pip", "install", "--upgrade", "pip", "speedtest-cli"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ ติดตั้งเครื่องมือทั้งหมดเสร็จสิ้น!")
        time.sleep(1)
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดตอนติดตั้ง: {e}")
        time.sleep(2)

# ==============================================
# 📶 สแกนอุปกรณ์ในเครือข่าย
# ==============================================
def scan_network():
    print("\n" + "=" * 60)
    print("📡 สแกนอุปกรณ์ที่เชื่อมต่อในเครือข่าย")
    print("=" * 60)
    try:
        result = subprocess.check_output(["arp-scan", "-l"], text=True, stderr=subprocess.DEVNULL)
        print(f"{'IP Address':<18} {'MAC Address':<20} {'ผู้ผลิต/รายละเอียด'}")
        print("-" * 60)
        lines = result.splitlines()
        for line in lines:
            if re.match(r'\d+\.\d+\.\d+\.\d+', line):
                parts = line.split()
                if len(parts) >= 3:
                    ip = parts[0]
                    mac = parts[1].upper()
                    vendor = " ".join(parts[2:])
                    print(f"{ip:<18} {mac:<20} {vendor}")
    except:
        print("⚠️ arp-scan ไม่ทำงาน ใช้ nmap แทน...")
        subnet = "192.168.43.0/24"
        result = subprocess.check_output(["nmap", "-sn", "-T4", subnet], text=True, stderr=subprocess.DEVNULL)
        ip = mac = None
        print(f"{'IP Address':<18} {'MAC Address':<20} {'สถานะ'}")
        print("-" * 60)
        for line in result.splitlines():
            if "Nmap scan report for" in line:
                ip = re.search(r'(\d+\.\d+\.\d+\.\d+)', line).group(1)
            elif "MAC Address:" in line:
                mac = re.search(r'([0-9A-Fa-f:]{17})', line).group(0)
                print(f"{ip:<18} {mac:<20} 🟢 ออนไลน์")
    input("\nกด Enter เพื่อกลับเมนู...")

# ==============================================
# 📊 ตรวจสอบความเร็วอินเทอร์เน็ต
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
# 📻 วิเคราะห์สัญญาณ Wi‑Fi
# ==============================================
def analyze_wifi():
    print("\n" + "=" * 60)
    print("📶 วิเคราะห์สัญญาณ Wi‑Fi")
    print("=" * 60)
    try:
        subprocess.run(["iwlist", "wlan0", "scan"], check=True)
    except:
        print("⚠️ ไม่สามารถสแกนคลื่นได้ในโหมดปกติ (ต้องใช้สิทธิ์พิเศษหรืออุปกรณ์รองรับ)")
        print("💡 แสดงข้อมูลเครือข่ายปัจจุบันแทน:")
        subprocess.run(["ip", "addr", "show", "wlan0"])
    input("\nกด Enter เพื่อกลับเมนู...")

# ==============================================
# 🛡️ เมนูหลัก
# ==============================================
def main_menu():
    while True:
        os.system("clear")
        print("=" * 60)
        print("📦 ชุดเครื่องมือตรวจสอบเครือข่าย & สัญญาณ")
        print("=" * 60)
        print("1. ติดตั้งเครื่องมือทั้งหมดอัตโนมัติ")
        print("2. สแกนอุปกรณ์ในเครือข่าย / ฮอตสปอต")
        print("3. ทดสอบความเร็วอินเทอร์เน็ต")
        print("4. วิเคราะห์สัญญาณ Wi‑Fi")
        print("5. ออกจากโปรแกรม")
        print("-" * 60)
        choice = input("👉 เลือกเมนูที่ต้องการ: ")

        if choice == "1":
            install_tools()
        elif choice == "2":
            scan_network()
        elif choice == "3":
            check_speed()
        elif choice == "4":
            analyze_wifi()
        elif choice == "5":
            print("👋 จบการทำงาน...")
            break
        else:
            print("❌ เลือกไม่ถูกต้อง ลองใหม่")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
