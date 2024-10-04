import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Membaca dataset

script_dir = os.path.dirname(os.path.realpath(__file__))
mainhour_df = pd.read_csv(f"{script_dir}/dashboardmainhour_df.csv")
mainday_df = pd.read_csv(f"{script_dir}/dashboardmainhour_df.csv")
# Sidebar untuk tab
st.set_page_config(layout="wide")  # Mengatur halaman agar lebar untuk ruang lebih
# Menambahkan header untuk dashboard
st.header("Dashboard Dataset Bike Sharing :sparkles:")

with st.sidebar:
    st.write("Navigasi Dashboard:")
    # Membuat tab di sidebar
    selected_tab = st.radio("Pilih tampilan", ["Overview", "Tampilan Data Harian"])


if selected_tab == "Overview":
    st.subheader("Jumlah pengguna per Bulan")
    # Menghitung jumlah pengguna total per bulan untuk 2011 dan 2012
    monthly_user_2011 = mainday_df[mainday_df['yr'] == 0].groupby('mnth')['cnt'].sum()
    monthly_user_2012 = mainday_df[mainday_df['yr'] == 1].groupby('mnth')['cnt'].sum()
    # Menggabungkan jumlah pengguna untuk kedua tahun
    monthly_user_combined = np.concatenate([monthly_user_2011.values, monthly_user_2012.values])
    # Membuat label untuk bulan (2011 dan 2012)
    months_labels = ['Jan 2011', 'Feb 2011', 'Mar 2011', 'Apr 2011', 'Mei 2011', 'Jun 2011',
                     'Jul 2011', 'Agu 2011', 'Sep 2011', 'Okt 2011', 'Nov 2011', 'Des 2011',
                     'Jan 2012', 'Feb 2012', 'Mar 2012', 'Apr 2012', 'Mei 2012', 'Jun 2012',
                     'Jul 2012', 'Agu 2012', 'Sep 2012', 'Okt 2012', 'Nov 2012', 'Des 2012']
    # Mengidentifikasi bulan dengan jumlah pengguna tertinggi dan terendah
    max_month_2011 = monthly_user_2011.idxmax() - 1  
    min_month_2011 = monthly_user_2011.idxmin() - 1
    max_month_2012 = monthly_user_2012.idxmax() + 11  
    min_month_2012 = monthly_user_2012.idxmin() + 11
    # Membuat diagram batang menggunakan Matplotlib
    plt.figure(figsize=(12, 6))
    bars = plt.bar(np.arange(24), monthly_user_combined, color='lightblue')
    # Sorot batang max dan min dengan warna merah dan biru
    bars[max_month_2011].set_color('red')
    bars[min_month_2011].set_color('blue')
    bars[max_month_2012].set_color('red')
    bars[min_month_2012].set_color('blue')
    # Menambahkan label teks di atas batang
    for i, bar in enumerate(bars):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), int(bar.get_height()), 
                 ha='center', va='bottom', fontsize=8)
    # Mengatur label sumbu x dengan rotasi untuk keterbacaan yang lebih baik
    plt.xticks(np.arange(24), labels=months_labels, rotation=45)
    # Mengatur label sumbu dan judul
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Pengguna')
    plt.title('Jumlah Pengguna per Bulan (2011 dan 2012)')
    # Menyesuaikan layout
    plt.tight_layout()
    # Menampilkan plot di Streamlit
    st.pyplot(plt)


    # Membuat dua kolom
    col1, col2 = st.columns(2)
    # Kolom kiri untuk jumlah pengguna berdasarkan kondisi cuaca
    with col1:
        st.write("### Jumlah Pengguna Berdasarkan Musim")
        user_counts_by_season = mainday_df.groupby('season')['cnt'].sum().sort_values(ascending=False)
        # Membuat diagram batang horizontal untuk weathersit
        plt.figure(figsize=(12, 6))
        bars = plt.barh(user_counts_by_season.index, user_counts_by_season.values, color='lightblue')
        # Mengubah warna batang dengan nilai tertinggi
        bars[0].set_color('red')
        # Menambahkan label teks di sebelah kanan setiap batang
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, int(bar.get_width()), 
                     va='center', ha='left', fontsize=8)
        # Menambahkan label dan judul
        plt.xlabel('Jumlah Pengguna')
        plt.ylabel('Kondisi Cuaca')
        plt.title('Jumlah Pengguna Berdasarkan Kondisi Cuaca')
        # Menampilkan plot pertama
        plt.tight_layout()
        st.pyplot(plt)

    # Kolom kanan untuk diagram lingkaran pengguna Casual vs Registered
    with col2:
        st.write("### Persentase Total Pengguna: Casual vs Registered")
        total_casual = mainday_df['casual'].sum()
        total_registered = mainday_df['registered'].sum()
        # Data untuk diagram lingkaran
        labels = ['Kasual', 'Terdaftar']
        sizes = [total_casual, total_registered]
        colors = ['lightblue', 'lightgreen']
        # Membuat diagram lingkaran
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('Persentase Total Pengguna: Kasual vs Terdaftar')
        plt.axis('equal')
        # Menampilkan plot kedua
        st.pyplot(plt)

elif selected_tab == "Tampilan Data Harian":
    st.subheader("Jumlah Pengguna Per Jam")
    st.write(":warning: Batang Data Berwarna Orange Berarti Hasil Interpolasi :warning:")
    # Membuat widget pemilih tanggal untuk memilih tanggal
    selected_date = st.date_input("Pilih tanggal", value=pd.to_datetime("2011-01-01"))
    # Mengonversi tanggal yang dipilih ke format string untuk mencocokkan kolom 'dteday' di dataset
    selected_date_str = selected_date.strftime('%Y-%m-%d')
    # Memfilter dataframe untuk tanggal yang dipilih
    filtered_data = mainhour_df[mainhour_df['dteday'] == selected_date_str]
    # Memeriksa apakah ada data untuk tanggal yang dipilih
    if not filtered_data.empty:
        st.write(f"Menampilkan data untuk: {selected_date_str}")
        # Plot jumlah pengguna per jam untuk hari itu
        plt.figure(figsize=(15, 8))  # Membuat figure lebih besar (ukuran 15x8)
        # Plot jumlah pengguna per jam
        bars = plt.bar(filtered_data['hr'], filtered_data['cnt'], color='lightblue')
        # Sorot batang di mana data diinterpolasi
        interpolated_hours = filtered_data[filtered_data['interpolated'] == True]['hr']
        for i, bar in enumerate(bars):
            if filtered_data.iloc[i]['interpolated']:
                bar.set_color('orange')  # Set batang data interpolasi menjadi oranye
        # Menambahkan label teks di atas batang
        for i, bar in enumerate(bars):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), int(bar.get_height()), 
                     ha='center', va='bottom', fontsize=8)
        # Mengatur label sumbu x dan menampilkan semua jam (0 hingga 23)
        plt.xticks(np.arange(24), labels=[str(i) for i in range(24)], rotation=0)
        # Mengatur label sumbu dan judul
        plt.xlabel('Jam dalam Sehari')
        plt.ylabel('Jumlah Pengguna')
        plt.title(f'Jumlah Pengguna per Jam pada {selected_date_str}', fontsize=16)
        # Menyesuaikan layout
        plt.tight_layout()
        # Menampilkan plot di Streamlit
        st.pyplot(plt)
    else:
        st.write("Tidak ada data yang tersedia untuk tanggal ini.")
    
    # Tampilkan data cuaca dan keramaian
    st.write("### Data Cuaca dan Keramaian")
    relevant_columns = ['season', 'weathersit', 'cnt', 'cnt_group', 'temp', 'temp_group', 'hum', 'hum_group', 'windspeed', 'windspeed_group']
    mainday_display = mainday_df[relevant_columns].head(1)

    # Displaying data in organized rows
    for index, row in mainday_display.iterrows():

        # First row: Musim dan Situasi Cuaca
        col1, col2 = st.columns(2)
        col1.metric(label="Musim", value=row['season'])

        # Second row: Situasi Cuaca
        col1 = st.columns(1)[0]  # Create one column to take the full width
        col1.metric(label="Situasi Cuaca", value=row['weathersit'])

        # Third row: Jumlah dan Tingkat Keramaian
        col1, col2 = st.columns(2)
        col1.metric(label="Jumlah User (cnt)", value=row['cnt'])
        col2.metric(label="Tingkat Keramaian", value=row['cnt_group'])

        # Fourth row: Temperatur and Tingkat Suhu
        col1, col2 = st.columns(2)
        col1.metric(label="Temperatur", value=row['temp'])
        col2.metric(label="Tingkat Suhu", value=row['temp_group'])

        # Fifth row: Kelembapan dan Tingkat Kelembapan
        col1, col2 = st.columns(2)
        col1.metric(label="Kelembapan", value=row['hum'])
        col2.metric(label="Tingkat Kelembapan", value=row['hum_group'])

        # Sixth row: Kecepatan Angin dan Tingkat Kecepatan
        col1, col2 = st.columns(2)
        col1.metric(label="Kecepatan Angin", value=row['windspeed'])
        col2.metric(label="Tingkat Kecepatan", value=row['windspeed_group'])
        st.markdown("---")

# Footer
st.caption("Copyright © Rafi Kyandra Atharizqi 2024")