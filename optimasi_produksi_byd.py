# Optimasi Produksi Mobil Listrik PT BYD Indonesia
# Menggunakan Linear Programming (scipy.optimize.linprog)

from scipy.optimize import linprog

# Fungsi objektif: Maksimalkan Z = 60000x + 100000y
# Karena linprog meminimalkan, kita ubah jadi: -Z = -60000x - 100000y
c = [-60000, -100000]

# Kendala:
# 3x + 5y <= 150 (bahan baku)
# 4x + 6y <= 200 (jam kerja)
A = [
    [3, 5],
    [4, 6]
]
b = [150, 200]

# Batas variabel x >= 0, y >= 0
x_bounds = (0, None)
y_bounds = (0, None)

# Menjalankan linprog
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

# Menampilkan hasil
if result.success:
    x, y = result.x
    profit = -result.fun
    print(f"Jumlah BYD Dolphin (x): {x:.2f} unit")
    print(f"Jumlah BYD Seal (y): {y:.2f} unit")
    print(f"Total Keuntungan Maksimal: Rp {profit:,.0f}")
else:
    print("Solusi tidak ditemukan.")
