# Python + Databricks Jobs — 3 sposoby uruchamiania kodu

Mini-projekt do wykładu. Jedno repozytorium na GitHub, trzy niezależne warianty uruchomienia **tej samej logiki**:

- **A — Python script:** `scripts/sales_job.py`
- **B — Notebook:** `notebooks/sales_job.ipynb`
- **C — Python wheel:** pakiet w `src/pw_databricks_demo/`, konfiguracja w `pyproject.toml`

Kod generuje w pamięci fikcyjne dane sprzedaży z 7 dni i wypisuje JSON. Nie korzysta ze Sparka, chmury, plików, baz, sieci ani zależności innych niż biblioteka standardowa Python.

## Struktura

```text
pw-databricks-jobs-demo/
├── scripts/
│   └── sales_job.py               # A. Python script
├── notebooks/
│   └── sales_job.ipynb            # B. Jupyter notebook
├── src/
│   └── pw_databricks_demo/
│       ├── __init__.py
│       └── job.py                 # C. Python wheel - logika i entry point
├── tests/
│   └── test_demo.py               # Testy (unittest, bez pytest)
├── pyproject.toml                 # Metadane wheel + entry point
├── .gitignore
└── README.md
```

## 1. Otwórz w PyCharm

1. Rozpakuj ZIP.
2. W PyCharm wybierz **Open** i wskaż folder `pw-databricks-jobs-demo`.
3. Skonfiguruj interpreter Python (zalecany Python 3.10+; projekt obsługuje 3.9+).
4. Aby sprawdzić A, uruchom `scripts/sales_job.py` lub w terminalu projektu:

```bash
python scripts/sales_job.py
```

**Spodziewany wynik każdego wariantu:**

```json
{
  "days": 7,
  "orders": 112,
  "revenue_pln": 2744,
  "best_day": 7
}
```

Notebook `.ipynb` otworzysz w PyCharm z obsługą notebooków lub bezpośrednio w Databricks. Uruchom jego komórkę z kodem.

## 2. Zbuduj wheel (C)

Z głównego katalogu projektu uruchom:

```bash
python -m pip wheel . --no-deps --wheel-dir dist
```

Paczka pojawi się w:

```text
dist/pw_databricks_demo-0.1.0-py3-none-any.whl
```

**Uwaga o zależnościach:** sama aplikacja ma `dependencies = []`, więc żaden wariant nie wymaga bibliotek zewnętrznych podczas uruchamiania. *Do zbudowania* wheel używany jest standardowy backend pakietowania `setuptools` i narzędzie `wheel`. `pip` może pobrać je do tymczasowego środowiska budowania; nie są zależnościami uruchomieniowymi projektu.

Aby wypróbować paczkę lokalnie, możesz ją zainstalować do własnego środowiska (nie jest to potrzebne do uruchomienia A ani B):

```bash
python -m pip install --no-deps dist/pw_databricks_demo-0.1.0-py3-none-any.whl
run_sales
```

## 3. Wypchnij repozytorium na GitHub

W katalogu projektu wykonaj (zastąp adres swoim repozytorium):

```bash
git init
git add .
git commit -m "Initial commit: Databricks Jobs demo"
git branch -M main
git remote add origin https://github.com/TWOJ_LOGIN/pw-databricks-jobs-demo.git
git push -u origin main
```

Repozytorium na GitHub powinno wcześniej istnieć (np. puste repo utworzone w interfejsie GitHub). Folder `dist/` jest ignorowany przez Git celowo: wheel jest **artefaktem budowania**, a nie kodem źródłowym.

## 4. Skonfiguruj Databricks Jobs

### A. Python script (bez budowania paczki)

1. Wejdź do **Jobs & Pipelines**, utwórz nowy Job.
2. Dodaj task typu **Python script**.
3. W polu **Source** wybierz **Git provider**, wskaż URL repo, provider GitHub i gałąź `main` (ew. skonfiguruj Git source w ustawieniach całego Job).
4. W polu **Path** wpisz dokładnie: `scripts/sales_job.py` (bez `/` na początku).
5. Wybierz dostępny compute i uruchom zadanie.

Do demonstracji można też najpierw sklonować GitHub jako **Git folder** w Workspace, a w tasku wybrać **Workspace** i wskazać plik z folderu. Dla zadań harmonogramowanych preferowany jest jednak `Git provider`.

### B. Notebook (bez budowania paczki)

1. Dodaj task typu **Notebook**.
2. Jako **Source** wybierz **Git provider**, użyj tego samego repo i gałęzi `main`.
3. Wskaż notebook `notebooks/sales_job.ipynb` (w niektórych widokach interfejsu ścieżka jest podawana bez końcówki `.ipynb`).
4. Wybierz compute, uruchom task. Databricks obsługuje notebooki `.ipynb` w Git folders i zadaniach Notebook.

### C. Python wheel (z artefaktu `.whl`)

1. W PyCharm wykonaj polecenie budowania wheel z punktu 2.
2. Prześlij plik `.whl` do Databricks Workspace Files albo do Unity Catalog Volume (według możliwości wybranego compute).
3. W Job dodaj task typu **Python wheel**.
4. Wpisz **Package name:** `pw_databricks_demo`.
5. Wpisz **Entry point:** `run_sales`.
6. W **Dependent libraries** (dla klasycznego compute) albo **Environment and Libraries → Add dependency** (dla serverless) dodaj przesłany plik `.whl`.
7. Uruchom task i sprawdź output.

**Istotne:** samo podłączenie repozytorium GitHub nie powoduje automatycznego zbudowania wheel w Databricks Jobs. Repo zawiera źródła do zbudowania paczki, ale zadanie `Python wheel` musi dostać gotowy artefakt `.whl` jako bibliotekę.

## 5. Testy (opcjonalnie)

Z głównego katalogu projektu:

```bash
python -m unittest discover -s tests -v
```

Testy sprawdzają, że skrypt, notebook i moduł zwracają dokładnie taki sam JSON, bez zewnętrznych pakietów.

## Co pokazać studentom?

| | A: Python script | B: Notebook | C: Python wheel |
|---|---|---|---|
| Format | `.py` | `.ipynb` | `.whl` |
| Bezpośredni kod z GitHub | Tak | Tak | Nie — potrzebny gotowy wheel |
| Możliwość edycji w Databricks | Tak | Tak | Źródła: tak; zbudowana paczka: nie |
| Typ Job task | Python script | Notebook | Python wheel |
| Typowe zastosowanie | Proste skrypty | Eksploracja, analizy, interaktywne prace | Kod pakietowany i wersjonowany |

Dokumentacja: [Python script task](https://docs.databricks.com/aws/en/jobs/tasks/python-script), [Notebook task](https://docs.databricks.com/aws/en/jobs/tasks/notebook), [Python wheel task](https://docs.databricks.com/aws/en/jobs/tasks/python-wheel), [Git with Jobs](https://docs.databricks.com/aws/en/jobs/git).
