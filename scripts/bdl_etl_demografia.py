import os
import time
import logging
import requests
import pandas as pd
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BDL_ETL")

class GusBdlETL:
    BASE_URL = "https://bdl.stat.gov.pl/api/v1/data/by-variable"
    
    BDL_CATALOG = {
        "Ludność ogółem": 72305,
        "Urodzenia żywe": 59868,
        "Zgony ogółem": 3231,
        "Migracje wewn. (Saldo)": 72198
    }

    def __init__(self, output_dir: str = "data_bdl"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_data(self, years: List[int]) -> pd.DataFrame:
        all_records = []
        
        for name, var_id in self.BDL_CATALOG.items():
            logger.info(f"Pobieranie wskaźnika: {name} (ID: {var_id})...")
            
            params = {
                "unit-level": 2, 
                "format": "json",
                "page-size": 100
            }
            
            url = f"{self.BASE_URL}/{var_id}"
            
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status() 
                
                data = response.json()
                
                for unit in data.get('results', []):
                    wojewodztwo = unit['name'].replace("WOJEWÓDZTWO ", "")
                    woj_id = unit['id']
                    
                    for val_data in unit.get('values', []):
                        rok = int(val_data['year'])
                        wartosc = val_data['val']
                        
                        if rok in years:
                            all_records.append({
                                "Wskaznik": name,
                                "Wojewodztwo": wojewodztwo,
                                "Wojewodztwo_ID": woj_id,
                                "Rok": rok,
                                "Wartosc": wartosc
                            })
                            
            except requests.exceptions.RequestException as e:
                logger.error(f"Błąd sieci/API dla wskaźnika {name}: {e}")
                continue
                
            time.sleep(0.5)

        return pd.DataFrame(all_records)

    def run(self, years: List[int]):
        start_time = time.time()
        logger.info(f"Rozpoczynam ekstrakcję dla lat: {min(years)} - {max(years)}")
        
        df = self.fetch_data(years)
        
        if df.empty:
            logger.warning("Brak danych! Proces przerwany.")
            return
            
        csv_path = os.path.join(self.output_dir, "bdl_demografia_master.csv")
        parquet_path = os.path.join(self.output_dir, "bdl_demografia_master.parquet")
        
        df.to_csv(csv_path, index=False, encoding="utf-8-sig", sep=";")
        df.to_parquet(parquet_path, index=False)
        
        elapsed_time = round(time.time() - start_time, 2)
        logger.info(f"=== ZAKOŃCZONO W {elapsed_time}s ===")
        logger.info(f"Pobrano {len(df)} rekordów.")
        logger.info(f"Ścieżka do pliku Parquet: {parquet_path}")

if __name__ == "__main__":
    LATA_ANALIZY = list(range(2012, 2026)) 
    
    etl = GusBdlETL()
    etl.run(years=LATA_ANALIZY)