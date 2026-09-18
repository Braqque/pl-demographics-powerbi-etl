\# 📊 Poland Demographics Analysis (2013-2025)



Projekt analityczny End-to-End przedstawiający sytuację demograficzną w Polsce na poziomie województw.



!\[Dashboard View](dashboard/dashboard\_view.png)



\## 🔄 Opis Procesu

Projekt obejmuje pełen cykl przetwarzania danych, od źródła po końcową wizualizację biznesową:

1\. \*\*Ekstrakcja (Python):\*\* Automatyczne pobranie surowych wskaźników z API Głównego Urzędu Statystycznego (BDL) przy użyciu biblioteki `requests` i zapisanie ich do zoptymalizowanego formatu Parquet.

2\. \*\*Transformacja (Power Query):\*\* Oczyszczenie danych, zmiana struktury z formatu Long na Wide (Pivotowanie) oraz zastosowanie operacji oknowych (Self-Join na podstawie przesunięcia lat).

3\. \*\*Modelowanie i Wizualizacja (Power BI):\*\* Utworzenie warstwy semantycznej z wykorzystaniem języka DAX oraz budowa interaktywnego dashboardu ułatwiającego analizę przestrzenną (mapa kartogramu) i trendów czasowych.



\## 🛠️ Stack Technologiczny

\* \*\*Języki i narzędzia:\*\* Python, Power Query (M), DAX, Power BI Desktop

\* \*\*Biblioteki Python:\*\* `requests`, `pandas`, `fastparquet`, `logging`

\* \*\*Formaty zapisu:\*\* Parquet, CSV



\## ⚙️ Kluczowe Rozwiązanie Inżynieryjne

\*\*Imputacja migracji zagranicznych:\*\* API GUS nie udostępnia gotowego salda migracji zagranicznych zagregowanego bezpośrednio dla województw (potwierdza to eksploracyjny skrypt `bdl\_sonda\_migracje.py`). Brakujące wartości wyliczono w warstwie Power Query w oparciu o demograficzne równanie bilansu ludności. Zrekonstruowano je poprzez odjęcie przyrostu naturalnego i migracji wewnętrznych od całkowitej zmiany populacji rok do roku.



\## 🗂️ Struktura Repozytorium

\* `scripts/bdl\_etl\_demografia.py` – Główny skrypt ETL.

\* `scripts/bdl\_sonda\_migracje.py` – Skrypt walidujący dostępność zmiennych w API.

\* `data/` – Katalog docelowy na pliki z danymi.

\* `dashboard/` – Raport `.pbix` oraz zrzuty ekranu.

