# Pipeline Analitik Operasional DustiniaDelixia Groceria


## Tinjauan Umum

DustiniaDelixia Groceria (DDG) adalah marketplace e-commerce asal Indonesia yang sedang berkembang pesat, menghubungkan ribuan seller UMKM dengan jutaan pembeli di seluruh nusantara.

Seiring meningkatnya volume transaksi, tim Operasional menerima semakin banyak keluhan pelanggan terkait performa pengiriman, sementara tim Finance menuntut efisiensi biaya logistik yang lebih baik.

Untuk mendukung pengambilan keputusan berbasis data, proyek ini membangun **Pipeline Analitik Operasional End-to-End** yang mengubah data operasional mentah menjadi wawasan konkret melalui data warehouse dan dashboard Business Intelligence (BI).

---

## Permasalahan Bisnis

Head of Operations membutuhkan pemahaman yang lebih jelas mengenai performa pengiriman di seluruh platform untuk menjawab beberapa tantangan utama:

- Seberapa sering keterlambatan pengiriman terjadi secara aktual?

- Wilayah mana yang memiliki tingkat keterlambatan tertinggi?

- Tahap operasional mana (Seller atau Kurir) yang paling berkontribusi terhadap keterlambatan?

- Bagaimana keterlambatan mempengaruhi skor kepuasan pelanggan secara sistemik?

- Apakah terdapat inefisiensi biaya logistik di wilayah tertentu?

---

## Tujuan Analisis

Proyek ini bertujuan untuk:

1. Mengukur performa pengiriman secara menyeluruh menggunakan KPI utama.

2. Mengidentifikasi faktor operasional dan geografis yang menyebabkan keterlambatan.

3. Menganalisis dampak performa pengiriman terhadap kepuasan pelanggan (Review Score).

4. Mengevaluasi efisiensi biaya logistik berdasarkan jarak dan biaya pengiriman.

5. Memberikan rekomendasi tindakan konkret untuk perbaikan operasional.

---

## Dataset

Sumber Dataset:
Brazilian E-Commerce Public Dataset (yang diadaptasi untuk studi kasus DDG).

Dataset utama yang digunakan:

- orders: Data pesanan dan timestamp pengiriman.

- order\_items: Detail produk, seller, dan biaya ongkir.

- customers & sellers: Data lokasi (State & Geolocation).

- products: Dimensi dan berat produk.

- reviews: Skor kepuasan dan komentar pelanggan.

---

## Teknologi yang Digunakan

| Komponen | Teknologi | Alasan |
| --- | --- | --- |
| Orchestration | Apache Airflow | Mengatur jadwal dan alur pipeline secara otomatis. |
| Processing | Python, Pandas | Membersihkan data dan melakukan feature engineering berat. |
| Data Lake | Parquet | Penyimpanan data intermediat yang ringkas dan cepat. |
| Data Warehouse | ClickHouse | Database OLAP untuk kueri analitik volume besar dengan performa tinggi. |
| Dashboard | Metabase | Visualisasi data yang interaktif untuk audiens non-teknis. |
| Deployment | Docker | Memastikan lingkungan aplikasi konsisten di mana saja. |

---

## Arsitektur Data Pipeline

File CSV Mentah
↓
Ekstraksi Data (Airflow)
↓
Pembersihan & Transformasi Data
↓
Feature Engineering (Penghitungan Metrik)
↓
Parquet Data Lake
↓
ClickHouse Data Warehouse
↓
Dashboard Metabase

---

## Rekayasa Fitur (Feature Engineering)

Beberapa metrik operasional yang dihasilkan meliputi:

- **Performa Pengiriman:** actual\_delivery\_time, is\_late, days\_delayed.

- **Akar Masalah:** seller\_process\_days, carrier\_transit\_days.

- **Logistik:** distance\_km, cost\_per\_km (Haversine Formula).

- **Pengalaman Pelanggan:** review\_score, NLP Bigrams untuk ulasan negatif.

- **Segmentasi:** seller\_type (Besar vs UMKM), weight\_class (Berat Produk).

---

## Struktur Dashboard

### 1\. Ringkasan Eksekutif (KPI Utama)

Menampilkan gambaran besar performa operasional:

- **Total Orders:** 219,772 pesanan berhasil dianalisis.

- **Late Delivery Rate:** 7.9% dari total pesanan mengalami keterlambatan.

- **Avg Delivery Time:** Rata-rata pengiriman membutuhkan waktu 12.46 hari.

- **Avg Review Score:** Rata-rata kepuasan pelanggan berada di angka 4.05.

### 2\. Analisis Akar Masalah (Root Cause)

- **Komposisi Waktu:** Keterlambatan didominasi oleh waktu transit kurir (**25.3 hari**) dibandingkan proses internal seller (**5.48 hari**).

- **Kontribusi Masalah:** 14.9 ribu keterlambatan disebabkan oleh masalah di kurir, sementara hanya 2.4 ribu yang disebabkan oleh seller.

### 3\. Dampak Pelanggan (Customer Impact)

- **Korelasi Skor:** Pesanan yang tepat waktu memiliki skor **4.19**, sedangkan yang terlambat jatuh hingga **2.49**.

- **Analisis Kata Kunci (NLP):** Keluhan utama pelanggan terpusat pada frasa "Não recebi" (Belum terima) dan "Ainda não" (Masih belum).

### 4\. Analisis Efisiensi & Geografis

- **Inefisiensi Biaya:** Negara bagian **SP (Sao Paulo)** memiliki biaya per KM tertinggi (**0.28**).

- **Hotspot Wilayah:** Wilayah Utara (**RR, AM, AP**) memiliki durasi pengiriman terlama (>25 hari), sementara **MA** memiliki tingkat keterlambatan (Late Rate) tertinggi.

---

## Temuan Utama & Insight

Berdasarkan analisis dashboard, ditemukan beberapa pola krusial:

1. **Keterlambatan adalah Pembunuh Kepuasan:** Terdapat korelasi kuat (**\-0.31**) antara keterlambatan dan skor review. Setiap keterlambatan menurunkan kepuasan pelanggan sebesar ~40%.

2. **Kurir sebagai Bottleneck:** Variasi total waktu pengiriman sangat ditentukan oleh performa kurir (korelasi **0.92**). Seller relatif sudah efisien dalam memproses pesanan.

3. **Anomali Biaya SP:** Wilayah perkotaan seperti Sao Paulo memiliki biaya logistik per KM yang mahal meskipun jaraknya dekat, menunjukkan inefisiensi pada kontrak flat rate kurir jarak pendek.

4. **Masalah Seller Spesifik:** Melalui analisis Word Cloud, ditemukan satu entitas bermasalah yaitu **"Lojas Lannister"** yang sering disebut dalam ulasan negatif terkait pengiriman.

---

## Rekomendasi Tindakan

1. **Audit Mitra Logistik:** Perlu dilakukan evaluasi ulang terhadap mitra pengiriman (3PL) khusus untuk rute wilayah Utara (Amazonas & Roraima) karena performa transit yang sangat lambat.

2. **Program Pendampingan Seller Besar:** Melakukan investigasi operasional pada seller berskala besar seperti **Lojas Lannister** untuk mengurangi waktu pemrosesan gudang.

3. **Optimasi Kontrak Finance:** Menegosiasikan ulang struktur biaya pengiriman di wilayah Metropolitan (SP) agar lebih efisien berdasarkan rasio jarak tempuh.

4. **Sistem Peringatan Dini:** Mengimplementasikan notifikasi otomatis atau kompensasi proaktif bagi pelanggan yang pesanannya masuk kategori keterlambatan parah (>7 hari) untuk menjaga loyalitas.

---

## Struktur Repositori

Text

```
.
├── dags/
│   ├── pipeline.py         # Definisi DAG Airflow
│   └── scripts/            # Script Python untuk Processing & Fetching
│
├── dashboard/              # Screenshot & Query Metabase
│
├── notebook/
│   └── .ipynb           # Eksplorasi Data Awal, Pre Processing, serta Post-Analysis di Google Colab
│
├── data/                   # Dataset CSV Mentah, merupakan data hasil pre-processing
│
├── docker-compose.yml      # Konfigurasi Infrastruktur (Airflow, ClickHouse, Metabase)
├── requirements.txt        # Library Python yang dibutuhkan
└── README.md               # Dokumentasi Proyek
```

---

## Penulis
| Name           | NRP        |
| --- | --- |
| Muhammad Zahran Rizki Primanda            | 5025241107        |
**Final Project MCI – Analitik Operasional DustiniaDelixia Groceria**
