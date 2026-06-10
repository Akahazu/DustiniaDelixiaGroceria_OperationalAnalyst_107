import pandas as pd
import os
import numpy as np
from math import radians, cos, sin, asin, sqrt

# Fungsi Haversine untuk hitung jarak nyata
def calculate_distance(row):
    try:
        # Mengambil koordinat dari CSV
        lon1, lat1, lon2, lat2 = map(radians, [row['seller_lng'], row['seller_lat'], row['cust_lng'], row['cust_lat']])
        # Formula Haversine
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius bumi KM
        return c * r
    except:
        return 0.0

def fetch_and_clean():
    # Menggunakan path v2 yang sudah ada koordinatnya
    input_path = '/opt/airflow/data/master_operational_data.csv' 
    output_dir = '/opt/airflow/data_lake/operational/'
    output_path = os.path.join(output_dir, 'operational_data.parquet')

    os.makedirs(output_dir, exist_ok=True)

    print(f"Membaca data dari {input_path}...")
    df = pd.read_csv(input_path)

    # Konversi datetime
    time_cols = ['order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date']
    for col in time_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Feature Engineering Waktu
    df['actual_delivery_time'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.total_seconds() / 86400
    df['is_late'] = (df['order_delivered_customer_date'] > df['order_estimated_delivery_date'])
    df['days_delayed'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.total_seconds() / 86400
    df['days_delayed'] = df['days_delayed'].clip(lower=0)
    df['seller_process_days'] = (df['order_delivered_carrier_date'] - df['order_approved_at']).dt.total_seconds() / 86400
    df['carrier_transit_days'] = (df['order_delivered_customer_date'] - df['order_delivered_carrier_date']).dt.total_seconds() / 86400

    # SEKARANG MENGGUNAKAN JARAK ASLI (Bukan Dummy)
    print("Menghitung jarak pengiriman nyata...")
    df['distance_km'] = df.apply(calculate_distance, axis=1)

    # Cost per KM
    df['cost_per_km'] = np.where(df['distance_km'] > 0, df['freight_value'] / df['distance_km'], 0)

    # Weight Class
    def classify_weight(w):
        if pd.isna(w): return 'UNKNOWN'
        return 'LIGHT' if w < 500 else ('MEDIUM' if w < 2000 else 'HEAVY')
    
    df['weight_class'] = df['product_weight_g'].apply(classify_weight)

    # Bersihkan NaN numerik & koordinat
    numeric_cols = ['actual_delivery_time','days_delayed','seller_process_days','carrier_transit_days','distance_km','cost_per_km', 'cust_lat', 'cust_lng']
    df[numeric_cols] = df[numeric_cols].fillna(0)

    df.to_parquet(output_path, index=False)
    print(f"Data berhasil dipindah ke Data Lake: {output_path}")

if __name__ == "__main__":
    fetch_and_clean()