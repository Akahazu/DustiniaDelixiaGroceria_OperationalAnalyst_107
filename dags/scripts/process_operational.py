import pandas as pd
from clickhouse_driver import Client
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np

def run_processing():
    df = pd.read_parquet('/opt/airflow/data_lake/operational/operational_data.parquet')
    client = Client(host='clickhouse-server', user='admin', password='rahasia')
    client.execute('CREATE DATABASE IF NOT EXISTS ddg_analytics')

    # Update Skema: Tambahkan distance, cost_per_km, dan koordinat
    client.execute("""
        CREATE TABLE IF NOT EXISTS ddg_analytics.fact_operational_performance (
            order_id String,
            seller_id String,
            customer_state String,
            seller_state String,
            actual_delivery_time Float64,
            is_late UInt8,
            days_delayed Float64,
            seller_process_days Float64,
            carrier_transit_days Float64,
            distance_km Float64,
            cost_per_km Float64,
            review_score Float32,
            seller_type String,
            weight_class String,
            cust_lat Float64,
            cust_lng Float64
        ) ENGINE = MergeTree()
        ORDER BY order_id
    """)

    client.execute("""
        CREATE TABLE IF NOT EXISTS ddg_analytics.top_negative_bigrams (
            phrase String, score Float64
        ) ENGINE = MergeTree() ORDER BY phrase
    """)

    # --- PROCESSING BIGRAMS ---
    df_neg = df[(df['is_late'] == True) & (df['review_score'] <= 2) & (df['review_comment_message'].notnull())].copy()
    if not df_neg.empty:
        def clean(t): return re.sub(r'[^\w\s]', '', str(t).lower())
        vectorizer = TfidfVectorizer(ngram_range=(2, 2), max_features=10)
        tfidf_matrix = vectorizer.fit_transform(df_neg['review_comment_message'].apply(clean))
        words = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.sum(axis=0).A1
        bigram_data = [tuple(x) for x in zip(words, scores.astype(float))]
        client.execute("TRUNCATE TABLE ddg_analytics.top_negative_bigrams")
        client.execute("INSERT INTO ddg_analytics.top_negative_bigrams VALUES", bigram_data)

    # --- INSERT MAIN DATA ---
    # Tambahkan kolom baru ke list insert
    cols_to_insert = [
        'order_id', 'seller_id', 'customer_state', 'seller_state',
        'actual_delivery_time', 'is_late', 'days_delayed',
        'seller_process_days', 'carrier_transit_days', 
        'distance_km', 'cost_per_km', # Kolom baru
        'review_score', 'seller_type', 'weight_class',
        'cust_lat', 'cust_lng' # Kolom koordinat
    ]
    
    final_df = df[cols_to_insert].replace({np.nan: 0})
    final_df['is_late'] = final_df['is_late'].astype(int)
    
    data_tuples = [tuple(x) for x in final_df.to_numpy()]
    
    client.execute("TRUNCATE TABLE ddg_analytics.fact_operational_performance")
    client.execute("INSERT INTO ddg_analytics.fact_operational_performance VALUES", data_tuples)
    print("Pipeline Berhasil ke ClickHouse dengan Koordinat Map!")

if __name__ == "__main__":
    run_processing()