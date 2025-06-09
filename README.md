#  ØkonomiApp – Personligt Budgetværktøj

Denne applikation er et Python-baseret værktøj, der hjælper privatpersoner med at få overblik over deres økonomi gennem registrering af indtægter og udgifter, analyse af forbrugsmønstre og visualisering af data. Projektet er udviklet med fokus på brugervenlighed, databehandling og fremtidig udvidelsesmulighed.

##  Funktionalitet

- Tilføj og gem transaktioner (indtægter og udgifter)
- Filtrér og analyser data pr. måned
- Vis forbrugsmønstre pr. kategori
- Visualisér:
  - Udgifter pr. kategori
  - Udgifter og indtægter pr. måned
  - Sammenligning mellem indtægter og udgifter

##  Teknologier brugt

- **Python 3**
- **Pandas** – til databehandling og analyse
- **Matplotlib** – til visualisering
- **Tkinter / terminal** (afhængigt af din implementering) – til brugergrænseflade


##  Projektstruktur

├── Components/
│ ├── data_manager.py
│ ├── pandas.py
│ └── plots.py
├── main.py
├── transactions.json
└── README.md

##  Sådan kommer du i gang

 **Klon projektet**  
   ```bash
   git clone https://github.com/din-bruger/okonomiapp.git
   cd okonomiapp
pip install pandas matplotlib
python gui.py
