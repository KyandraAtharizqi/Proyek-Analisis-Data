# Proyek Analisis Data

## Link Deploy

```
https://dashboardpy-jqdfpzvkee7lsle2ybvtbv.streamlit.app/
````


Menggunakan Bike Sharing Dataset

https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset/data

Disini kita akan mencari tahu

**day.csv**
- Bagaimana performa tingkat penggunaan/jumlah pengguna E-Bike pada Tahun 2011 - 2012 berdasarkan bulan?
- Pada musim apa penggunaan E-Bike paling banyak?
- Bagaimana persen pembagian antara pengguna registered dan casual?
- Bagaimana korelasi/ hubungan antara jumlah user dengan beberapa variabel cuaca numerik seperti temperatur, kecepatan angin, dan kelembapan?

**hour.csv**
- Pada jam berapakah user banyak menggunakan sepeda?

**day.csv additional question**
- Bagaimana pengelompokkan hari-hari berdasarkan tingkat keramaiannya variabel cuaca numeriknya?


## Clone atau Download Repository
Clone
```
git clone https://github.com/KyandraAtharizqi/Proyek-Analisis-Data
```



## Setup environment
```
# Sesuaikan dengan direktori 
cd Proyek Analisis Data

python -m venv proyekanalisisdata
proyekanalisisdata\Scripts\activate

# Install library yang ada pada requirements.txt
pip install -r requirements.txt

# Atau bisa manual dengan cara ini
pip install numpy pandas matplotlib seaborn streamlit
```

## Run steamlit app
Gunakan pada  directory Proyek Analisis Data/dashboard /
```
streamlit run dashboard.py
```