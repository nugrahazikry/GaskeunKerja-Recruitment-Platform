"""Content for the 6 T5-fixture CVs (Area 5 QA T5-fixture).

Synthetic, fabricated candidates only — no real people. Deliberately fit-differentiated
against the real Web Developer JD competencies (HTML, CSS, JavaScript, Frontend Framework,
REST API, Git, Database, Backend Development, Responsive Design, Deployment, etc.) so T5
has real ground truth for a strong-vs-weak average-score comparison.
"""

STRONG_CVS = [
    (
        "FIXTURE-STRONG-1",
        """Ahmad Fixture Strong One
Web Developer

PENGALAMAN KERJA
Frontend Developer, PT Contoh Digital (2021 - Sekarang)
Membangun antarmuka web menggunakan React dan TypeScript, mengintegrasikan REST API,
menggunakan Git untuk kontrol versi, menerapkan desain responsif dengan CSS Flexbox dan
Grid, serta melakukan deployment ke cloud (AWS/Vercel) menggunakan CI/CD.

Backend Developer, PT Contoh Aplikasi (2019 - 2021)
Mengembangkan REST API dengan Node.js dan Express, merancang skema database PostgreSQL,
melakukan debugging dan optimasi performa query, bekerja dalam tim menggunakan metode Agile/Scrum.

KEAHLIAN
HTML, CSS, JavaScript, TypeScript, React, Node.js, Express, REST API, Git, PostgreSQL,
Responsive Design, Deployment, Cloud Deployment (AWS, Vercel), Agile/Scrum, Debugging,
Performance Optimization, Team Collaboration

PENDIDIKAN
S1 Teknik Informatika, Universitas Contoh (2019)
""",
    ),
    (
        "FIXTURE-STRONG-2",
        """Budi Fixture Strong Two
Full Stack Web Developer

PENGALAMAN KERJA
Full Stack Developer, PT Contoh Teknologi (2020 - Sekarang)
Mengembangkan aplikasi web full-stack menggunakan Vue.js di frontend dan Django REST
Framework di backend. Mendesain UI responsif dengan HTML/CSS, mengelola basis kode dengan
Git dan GitHub, melakukan deployment otomatis ke server cloud, serta berkolaborasi dalam
tim Scrum lintas fungsi.

Junior Web Developer, PT Contoh Solusi (2018 - 2020)
Membangun halaman web statis dan dinamis dengan JavaScript, mengintegrasikan REST API
pihak ketiga, menggunakan database MySQL untuk penyimpanan data.

KEAHLIAN
HTML, CSS, JavaScript, Vue.js, Django, REST API, Git, GitHub, MySQL, PostgreSQL,
Responsive Design, Cloud Deployment, Debugging, Team Collaboration, Agile/Scrum

PENDIDIKAN
S1 Sistem Informasi, Universitas Contoh Dua (2018)
""",
    ),
]

MID_CVS = [
    (
        "FIXTURE-MID-1",
        """Citra Fixture Mid One
Software Support Analyst

PENGALAMAN KERJA
IT Support Analyst, PT Contoh Layanan (2020 - Sekarang)
Menulis skrip otomasi sederhana menggunakan Python, melakukan query dasar pada database
MySQL untuk pelaporan, sedikit pengalaman dengan HTML untuk mengedit halaman intranet
perusahaan. Menggunakan Git untuk menyimpan skrip internal.

Data Entry Specialist, PT Contoh Administrasi (2018 - 2020)
Mengelola data pelanggan di spreadsheet dan database sederhana, tidak ada pengalaman
langsung dalam pengembangan aplikasi web.

KEAHLIAN
Python (dasar), HTML (dasar), MySQL (dasar), Git, Microsoft Office, Komunikasi Tim

PENDIDIKAN
S1 Manajemen Informatika, Universitas Contoh Tiga (2018)
""",
    ),
    (
        "FIXTURE-MID-2",
        """Dedi Fixture Mid Two
QA Tester

PENGALAMAN KERJA
Quality Assurance Tester, PT Contoh Perangkat Lunak (2019 - Sekarang)
Menguji aplikasi web secara manual dan menulis test case, memahami dasar-dasar HTML dan
CSS untuk memverifikasi tampilan, melaporkan bug melalui sistem tiket, menggunakan Git
untuk melacak perubahan pada dokumen pengujian. Belum pernah menulis kode backend atau
REST API secara langsung.

Technical Support, PT Contoh Bantuan (2017 - 2019)
Membantu pengguna dengan masalah perangkat lunak dasar.

KEAHLIAN
HTML (dasar), CSS (dasar), Manual Testing, Git, Dokumentasi Test Case, Komunikasi Tim

PENDIDIKAN
D3 Teknik Komputer, Politeknik Contoh (2017)
""",
    ),
]

WEAK_CVS = [
    (
        "FIXTURE-WEAK-1",
        """Eka Fixture Weak One
Staff Akuntansi

PENGALAMAN KERJA
Staff Akuntansi, PT Contoh Keuangan (2018 - Sekarang)
Mengelola pembukuan perusahaan, menyusun laporan keuangan bulanan, melakukan rekonsiliasi
bank, menggunakan Microsoft Excel dan software akuntansi standar. Tidak memiliki
pengalaman pemrograman atau pengembangan perangkat lunak.

Kasir, Toko Contoh Retail (2016 - 2018)
Melayani transaksi pelanggan, mengelola kas harian.

KEAHLIAN
Akuntansi, Microsoft Excel, Rekonsiliasi Bank, Pembukuan, Pelayanan Pelanggan

PENDIDIKAN
S1 Akuntansi, Universitas Contoh Empat (2016)
""",
    ),
    (
        "FIXTURE-WEAK-2",
        """Fajar Fixture Weak Two
Staff Administrasi Gudang

PENGALAMAN KERJA
Staff Administrasi Gudang, PT Contoh Logistik (2019 - Sekarang)
Mencatat keluar-masuk barang gudang, menyusun laporan stok bulanan menggunakan Microsoft
Excel, mengoordinasikan pengiriman dengan tim ekspedisi. Tidak memiliki latar belakang
teknologi informasi atau pengembangan web.

Staff Gudang, PT Contoh Distribusi (2017 - 2019)
Mengelola penyimpanan dan distribusi barang.

KEAHLIAN
Manajemen Gudang, Microsoft Excel, Logistik, Pengelolaan Stok, Koordinasi Tim

PENDIDIKAN
SMA Contoh Lima (2017)
""",
    ),
]

ALL_FIXTURE_CVS = [
    ("strong", *STRONG_CVS[0]),
    ("strong", *STRONG_CVS[1]),
    ("mid", *MID_CVS[0]),
    ("mid", *MID_CVS[1]),
    ("weak", *WEAK_CVS[0]),
    ("weak", *WEAK_CVS[1]),
]
