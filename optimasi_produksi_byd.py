import streamlit as st
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Optimasi Produksi PT BYD Indonesia", layout="centered")

st.title("🔧 Optimasi Produksi Mobil Listrik PT BYD Indonesia")
st.markdown("Simulasi Linear Programming untuk produksi **BYD Dolphin** dan **BYD Seal**.")

st.header("📥 Input Data Produksi")

col1, col2 = st.columns(2)
with col1:
    bahan_baku_total = st.number_input("Total Bahan Baku (unit)", value=150)
    waktu_total = st.number_input("Total Jam Kerja (jam)", value=200)

with col2:
    keuntungan_dolphin = st.number_input("Keuntungan per unit Dolphin", value=60000)
    keuntungan_seal = st.number_input("Keuntungan per unit Seal", value=100000)

st.subheader("🔧 Konsumsi Sumber Daya per Unit")
col3, col4 = st.columns(2)
with col3:
    bb_dolphin = st.number_input("Bahan Baku per unit Dolphin", value=3)
    wk_dolphin = st.number_input("Jam Kerja per unit Dolphin", value=4)

with col4:
    bb_seal = st.number_input("Bahan Baku per unit Seal", value=5)
    wk_seal = st.number_input("Jam Kerja per unit Seal", value=6)

if st.button("🔍 Hitung Optimasi"):
    c = [-keuntungan_dolphin, -keuntungan_seal]
    A = [
        [bb_dolphin, bb_seal],
        [wk_dolphin, wk_seal]
    ]
    b = [bahan_baku_total, waktu_total]
    bounds = [(0, None), (0, None)]

    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

    if result.success:
        x, y = result.x
        profit = -result.fun

        st.success("✅ Solusi Optimal Ditemukan!")
        st.write(f"Jumlah BYD Dolphin (x): **{x:.2f}** unit")
        st.write(f"Jumlah BYD Seal (y): **{y:.2f}** unit")
        st.write(f"Total Keuntungan Maksimal: **Rp {profit:,.0f}**")

        # Grafik wilayah feasible
        st.subheader("📊 Visualisasi Wilayah Feasible")

        x_vals = np.linspace(0, bahan_baku_total / bb_dolphin, 400)
        y1 = (bahan_baku_total - bb_dolphin * x_vals) / bb_seal
        y2 = (waktu_total - wk_dolphin * x_vals) / wk_seal
        y_min = np.minimum(y1, y2)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y1, label="Kendala Bahan Baku")
        ax.plot(x_vals, y2, label="Kendala Jam Kerja")
        ax.fill_between(x_vals, 0, y_min, where=(y_min >= 0), color='lightgray', alpha=0.6)

        ax.plot(x, y, 'ro', label="Solusi Optimal")
        ax.set_xlabel("Jumlah BYD Dolphin (x)")
        ax.set_ylabel("Jumlah BYD Seal (y)")
        ax.set_title("Wilayah Feasible & Titik Optimal")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        

    else:
        st.error("❌ Solusi tidak ditemukan. Periksa input atau batasan.")
