import pandas as pd

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self, level=0, is_last=True, prefix=""):
        connector = "└── " if is_last else "├── "
        lines = []
        if level == 0:
            lines.append(self.name)
        else:
            lines.append(prefix + connector + str(self.name))
        if self.children:
            for i, child in enumerate(self.children):
                last = i == len(self.children) - 1
                child_prefix = prefix + ("    " if is_last else "│   ")
                lines.append(child.__repr__(level + 1, last, child_prefix))
        return "\n".join(lines)

# Baca data dari Excel
file_path = 'data_tiket_konser.xlsx'
data = pd.read_excel(file_path)

print("=== PEMESANAN TIKET KONSER ===")

# Pilih Jenis
jenis_list = sorted(data['Jenis'].unique())
for idx, jenis in enumerate(jenis_list, 1):
    print(f"{idx}. {jenis}")
jenis_idx = int(input("Pilih Jenis Tiket (angka): ")) - 1
jenis_pilihan = jenis_list[jenis_idx]

# Pilih Kategori
kategori_list = sorted(data[data['Jenis'] == jenis_pilihan]['Kategori'].unique())
for idx, kategori in enumerate(kategori_list, 1):
    print(f"{idx}. {kategori}")
kategori_idx = int(input("Pilih Kategori Tiket: ")) - 1
kategori_pilihan = kategori_list[kategori_idx]

# Pilih Day
day_list = sorted(data[(data['Jenis'] == jenis_pilihan) & (data['Kategori'] == kategori_pilihan)]['Day'].unique())
for idx, day in enumerate(day_list, 1):
    print(f"{idx}. Day {day}")
day_idx = int(input("Pilih Hari (Day): ")) - 1
day_pilihan = day_list[day_idx]

# Ambil baris data yang sesuai
row = data[(data['Jenis'] == jenis_pilihan) & 
           (data['Kategori'] == kategori_pilihan) & 
           (data['Day'] == day_pilihan)].iloc[0]

harga = row['Harga']
metode_list = [m.strip() for m in row['Metode Pembayaran'].split(',')]
for idx, metode in enumerate(metode_list, 1):
    print(f"{idx}. {metode}")
metode_idx = int(input("Pilih Metode Pembayaran: ")) - 1
metode_pilihan = metode_list[metode_idx]

if metode_pilihan == "e-wallet":
    ewallet_list = [e.strip() for e in row['e-wallet'].split(',')]
    for idx, ew in enumerate(ewallet_list, 1):
        print(f"{idx}. {ew}")
    ewallet_idx = int(input("Pilih Jenis e-wallet: ")) - 1
    metode_detail = ewallet_list[ewallet_idx]
elif metode_pilihan == "Transfer Bank":
    transfer_list = [t.strip() for t in row['Transfer Bank'].split(',')]
    for idx, tf in enumerate(transfer_list, 1):
        print(f"{idx}. {tf}")
    transfer_idx = int(input("Pilih Bank: ")) - 1
    metode_detail = transfer_list[transfer_idx]
else:
    metode_detail = "-"

# Ambil info virtual account dan no rekening
virtual_account = row['virtual account']
no_rekening = row['No.Rekening']

# Ringkasan Pemesanan
print("\n=== RINGKASAN PEMESANAN ===")
print(f"Jenis Tiket       : {jenis_pilihan}")
print(f"Kategori Tiket    : {kategori_pilihan}")
print(f"Hari              : Day {day_pilihan}")
print(f"Harga             : {harga}")
print(f"Metode Pembayaran : {metode_pilihan} ({metode_detail})")
if metode_pilihan == "e-wallet":
    print(f"Virtual Account   : {virtual_account}")
elif metode_pilihan == "Transfer Bank":
    print(f"No Rekening       : {no_rekening}")

# Tree ringkasan pemesanan user dengan garis terhubung
user_root = TreeNode("Pemesanan Tiket")
jenis_node = TreeNode(jenis_pilihan)
kategori_node = TreeNode(kategori_pilihan)
day_node = TreeNode(f"Day {day_pilihan}")
harga_node = TreeNode(f"Harga: {harga}")
metode_node = TreeNode(f"Metode: {metode_pilihan}")
metode_detail_node = TreeNode(f"Pilihan: {metode_detail}")

# Tambahan node virtual account / no rekening
if metode_pilihan == "e-wallet":
    info_node = TreeNode(f"Virtual Account: {virtual_account}")
elif metode_pilihan == "Transfer Bank":
    info_node = TreeNode(f"No Rekening: {no_rekening}")
else:
    info_node = None

user_root.add_child(jenis_node)
jenis_node.add_child(kategori_node)
kategori_node.add_child(day_node)
day_node.add_child(harga_node)
day_node.add_child(metode_node)
metode_node.add_child(metode_detail_node)
if info_node:
    metode_node.add_child(info_node)

print("\n=== TREE PEMESANAN USER ===")
print(user_root)
