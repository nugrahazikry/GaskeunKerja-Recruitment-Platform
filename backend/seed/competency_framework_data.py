"""Competency framework + resource library content for the Data Analyst demo role (Area 3 T6/T7).

Ten competencies, each with a level description (used by the report to describe proficiency)
and lightweight relations to related competencies (feeds Area 2 T7's matching graph boost).
Three curated resources per competency (feeds the deterministic development report).
"""

JOB_ROLE = "Data Analyst"

# key -> (competency_name, level_description, related_keys)
COMPETENCIES = {
    "sql": (
        "SQL",
        "1=belum bisa menulis query dasar; 3=bisa JOIN, GROUP BY, dan subquery sederhana; "
        "5=mahir window functions, query tuning, dan desain skema.",
        ["data_cleaning", "dashboarding"],
    ),
    "excel": (
        "Excel/Spreadsheet",
        "1=hanya bisa input data manual; 3=mahir pivot table, VLOOKUP/XLOOKUP, dan formula bersyarat; "
        "5=mampu membangun model data kompleks dengan Power Query/Power Pivot.",
        ["data_visualization", "data_cleaning"],
    ),
    "data_visualization": (
        "Data Visualization",
        "1=hanya bisa membuat grafik dasar; 3=mampu memilih jenis visualisasi yang tepat untuk audiens; "
        "5=mahir membangun dashboard interaktif dengan storytelling data yang jelas.",
        ["dashboarding", "business_communication"],
    ),
    "statistics": (
        "Statistik",
        "1=paham statistik deskriptif dasar; 3=mampu melakukan uji hipotesis dan interpretasi korelasi; "
        "5=mahir regresi, analisis prediktif, dan menjelaskan signifikansi statistik ke non-teknis.",
        ["python_r", "data_cleaning"],
    ),
    "python_r": (
        "Python/R",
        "1=belum bisa menulis skrip analisis dasar; 3=mampu menggunakan pandas/dplyr untuk manipulasi data; "
        "5=mahir membangun pipeline analisis end-to-end dan otomatisasi laporan.",
        ["statistics", "data_cleaning"],
    ),
    "data_cleaning": (
        "Data Cleaning",
        "1=sering melewatkan data kotor/duplikat; 3=konsisten menangani missing values dan outlier; "
        "5=mahir merancang proses validasi data otomatis untuk pipeline berskala besar.",
        ["sql", "python_r"],
    ),
    "dashboarding": (
        "Dashboarding",
        "1=hanya bisa menyusun tabel statis; 3=mampu membangun dashboard dasar di Tableau/Power BI/Looker; "
        "5=mahir merancang dashboard real-time dengan drill-down dan filter interaktif.",
        ["data_visualization", "sql"],
    ),
    "business_communication": (
        "Komunikasi Bisnis",
        "1=kesulitan menjelaskan temuan data ke non-teknis; 3=mampu menyusun ringkasan insight yang jelas; "
        "5=mahir mempresentasikan rekomendasi berbasis data ke level manajemen dengan storytelling kuat.",
        ["data_visualization"],
    ),
    "domain_knowledge": (
        "Pemahaman Domain Bisnis",
        "1=belum memahami konteks industri/perusahaan; 3=paham metrik bisnis utama dan KPI relevan; "
        "5=mahir mengaitkan analisis data langsung ke keputusan strategis bisnis.",
        ["business_communication", "statistics"],
    ),
    "critical_thinking": (
        "Berpikir Kritis & Problem Solving",
        "1=hanya mengikuti instruksi analisis tanpa validasi; 3=mampu memvalidasi asumsi dan mencari akar masalah; "
        "5=mahir merumuskan pertanyaan analisis yang tepat dari masalah bisnis ambigu.",
        ["statistics", "domain_knowledge"],
    ),
}

# competency_key -> [(title, duration, milestone_description, url), ...]
RESOURCES = {
    "sql": [
        ("SQL for Data Analysis (Mode Analytics)", "6 jam", "Mampu menulis JOIN dan agregasi multi-tabel", None),
        ("Advanced SQL: Window Functions", "3 jam", "Mampu menggunakan ROW_NUMBER, RANK, dan LAG/LEAD", None),
        ("Query Performance Tuning Basics", "2 jam", "Memahami cara membaca query execution plan", None),
    ],
    "excel": [
        ("Excel Pivot Tables Masterclass", "3 jam", "Mampu membangun pivot table multi-dimensi", None),
        ("Power Query untuk Analis Data", "4 jam", "Mampu menggabungkan dan membersihkan data dari banyak sumber", None),
        ("Formula Excel Tingkat Lanjut", "2 jam", "Mahir XLOOKUP, INDEX-MATCH, dan formula array", None),
    ],
    "data_visualization": [
        ("Storytelling with Data", "5 jam", "Mampu memilih visualisasi yang sesuai konteks audiens", None),
        ("Prinsip Desain Dashboard yang Efektif", "3 jam", "Memahami hierarki visual dan penggunaan warna", None),
        ("Data Visualization dengan Python (matplotlib/seaborn)", "4 jam", "Mampu membuat visualisasi custom dari data mentah", None),
    ],
    "statistics": [
        ("Statistik Dasar untuk Analis Data", "6 jam", "Memahami mean, median, variansi, dan distribusi", None),
        ("Uji Hipotesis Praktis", "4 jam", "Mampu melakukan t-test dan interpretasi p-value", None),
        ("Pengantar Regresi Linear", "5 jam", "Mampu membangun dan menginterpretasi model regresi sederhana", None),
    ],
    "python_r": [
        ("Python untuk Analisis Data (Pandas)", "8 jam", "Mampu memanipulasi dataframe untuk analisis harian", None),
        ("Automating Reports with Python", "4 jam", "Mampu membangun skrip laporan otomatis terjadwal", None),
        ("R untuk Data Analyst", "6 jam", "Mampu melakukan analisis data dasar dengan dplyr/tidyr", None),
    ],
    "data_cleaning": [
        ("Data Cleaning Fundamentals", "4 jam", "Mampu menangani missing values dan duplikasi data", None),
        ("Outlier Detection Techniques", "3 jam", "Mampu mengidentifikasi dan menangani outlier secara tepat", None),
        ("Data Validation Pipelines", "5 jam", "Mampu merancang aturan validasi data otomatis", None),
    ],
    "dashboarding": [
        ("Tableau untuk Pemula", "6 jam", "Mampu membangun dashboard dasar dengan filter interaktif", None),
        ("Power BI Dashboard Design", "6 jam", "Mampu membangun dashboard multi-halaman dengan drill-down", None),
        ("Looker Studio Praktis", "3 jam", "Mampu menghubungkan sumber data dan membangun laporan real-time", None),
    ],
    "business_communication": [
        ("Menyampaikan Insight Data ke Non-Teknis", "3 jam", "Mampu menyusun ringkasan eksekutif dari analisis data", None),
        ("Presentasi Data yang Efektif", "4 jam", "Mampu membangun narasi presentasi berbasis data", None),
        ("Menulis Laporan Analisis yang Jelas", "2 jam", "Mampu menyusun laporan terstruktur dan actionable", None),
    ],
    "domain_knowledge": [
        ("Memahami KPI Bisnis Umum", "3 jam", "Mampu mengaitkan metrik data dengan tujuan bisnis", None),
        ("Business Analytics Fundamentals", "5 jam", "Memahami bagaimana data mendukung keputusan strategis", None),
        ("Studi Kasus Analisis Bisnis Industri", "4 jam", "Mampu menganalisis studi kasus bisnis nyata", None),
    ],
    "critical_thinking": [
        ("Problem Solving untuk Data Analyst", "4 jam", "Mampu merumuskan pertanyaan analisis dari masalah ambigu", None),
        ("Validating Data Assumptions", "3 jam", "Mampu memverifikasi asumsi sebelum menganalisis data", None),
        ("Root Cause Analysis Techniques", "3 jam", "Mampu menelusuri akar masalah dari anomali data", None),
    ],
}
