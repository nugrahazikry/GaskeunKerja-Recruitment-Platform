## Slide 1

### Executive Summary (max 150 kata)

Jelaskan versi terbaru dari solusi Anda, termasuk problem utama, pendekatan solusi, dan dampak utama yang ditargetkan.

| Aspek | Penjelasan |
| --- | --- |
| Masalah Utama | Indonesia menghadapi tantangan ketenagakerjaan sistemik yang ditandai oleh naiknya jumlah pengangguran hingga 7,36 juta jiwa dan tingginya kesenjangan kompetensi antara kebutuhan industri dan kemampuan jobseeker. Banyak jobseeker melamar secara acak karena tidak memahami kecocokan kompetensinya terhadap lowongan yang tersedia, sementara employer kesulitan menemukan kandidat yang cocok. |
| Pendekatan Solusi | GaskeunKerja hadir sebagai platform pengembangan karir berbasis AI yang mengintegrasikan agregasi lowongan terkini, skill-based job matching, analisis skill gap, dan personalized learning roadmap dalam satu ekosistem. Sistem menganalisis CV dan kebutuhan kompetensi dari berbagai lowongan untuk menghasilkan rekomendasi pekerjaan yang lebih akurat, mengidentifikasi kesenjangan keterampilan secara transparan, serta memberikan jalur pembelajaran terpersonalisasi untuk meningkatkan kesiapan kerja bagi setiap jobseeker. |
| Dampak Utama | GaskeunKerja menargetkan peningkatan kualitas pencocokan kerja, percepatan penyerapan tenaga kerja, pengurangan skill mismatch, serta peningkatan daya saing tenaga kerja Indonesia secara berkelanjutan. Solusi ini mendukung tema hackathon dengan mendorong penyerapan tenaga kerja digital dan berkontribusi langsung dalam meningkatkan kualitas SDM secara berkelanjutan. |

---

## Slide 2

### Problem Statement

Sesuai dengan penulisan Problem Statement yang sesuai.

| Problem Statement |
| --- |
| Digitalisasi Penciptaan Lapangan Kerja |

---

## Slide 3

### Primary Sub-Problem Statement

Sesuai dengan penulisan Sub-Problem Statement yang sesuai, boleh lebih dari 1.

| No | Sub-Problem Statement |
| --- | --- |
| 1 | Platform Job Matching Berbasis Kecerdasan Artifisial |
| 2 | Skill Gap Advisor |
| 3 | Personalized Training |

---

## Slide 4

### Problem Validation (Max 180 kata)

Apa masalah inti yang Anda selesaikan saat ini? Jelaskan akar masalahnya.

Indonesia menghadapi tantangan struktural dalam ketenagakerjaan yang saling berkaitan:

| No | Masalah | Penjelasan |
| --- | --- | --- |
| 1 | Mismatch Kompetensi | Jobseeker melamar secara acak tanpa memahami kesesuaian skill mereka terhadap kebutuhan industri. Pengangguran Indonesia terus naik dari 7,28 juta (Feb 2025) menjadi 7,36 juta (Nov 2025) (BPS, 2025), meski lapangan kerja tersedia. |
| 2 | Inefisiensi Rekrutmen | Pencocokan kandidat masih bergantung pada keyword matching yang tidak menangkap konteks kompetensi secara menyeluruh. 46% perusahaan kesulitan menemukan kandidat sesuai kebutuhan, dan 50% menilai keterampilan teknis pelamar masih di level pemula (ManpowerGroup Talent Shortage Survey, 2024). |
| 3 | Minimnya Transparansi Skill Gap | Jobseeker tidak mengetahui skill spesifik yang menjadi kekurangan mereka terhadap suatu lowongan. Tanpa feedback konkret, proses pengembangan kompetensi menjadi tidak terarah. |
| 4 | Disconnect Pembelajaran dan Kebutuhan Industri | Program upskilling jarang dikaitkan langsung dengan kebutuhan skill aktual dari lowongan (WEF Future of Jobs Report, 2023), sehingga upaya belajar tidak meningkatkan employability secara signifikan. |

Keempat masalah ini saling berkaitan dan membentuk siklus mismatch sistemik yang menghambat penyerapan tenaga kerja nasional.

---

## Slide 5

### Problem–Solution Mapping (Max 180 kata)

Jelaskan secara eksplisit hubungan antara problem → mekanisme solusi → outcome.

| No | Problem | Mekanisme | Outcome |
| --- | --- | --- | --- |
| 1 | Mismatch Kompetensi: Jobseeker melamar secara acak tanpa memahami kesesuaian skill mereka, mengakibatkan conversion rate rendah. | Deepseek V4 Flash mem-parsing CV dan menghasilkan matching score per lowongan menggunakan Knowledge Graph Embeddings. | Lamaran lebih terarah, conversion rate meningkat hingga 2–3x. |
| 2 | Keyword Matching Terbatas: Platform konvensional gagal menangkap konteks kompetensi kandidat secara menyeluruh. | KGE dan GNN menghitung kedekatan relasional antara vektor kompetensi kandidat dan kebutuhan lowongan. | Rekomendasi lowongan lebih akurat dengan target matching accuracy ≥85%. |
| 3 | Minimnya Transparansi Skill Gap: Jobseeker tidak mengetahui skill spesifik yang perlu diperbaiki sehingga pengembangan diri tidak terarah. | Deepseek V4 Pro menganalisis gap kompetensi dan menyusun personalized learning roadmap berbasis kebutuhan pasar. | Panduan pengembangan terukur dengan target skill completion rate ≥30% dalam 12 bulan. |
| 4 | Inefisiensi Rekrutmen: Volume lamaran tidak relevan memaksa tim HR melakukan screening manual yang membuang waktu. | Agregasi lowongan harian dan feedback loop pembaruan CV menghasilkan shortlist kandidat otomatis. | Waktu rekrutmen berkurang 30–40% dan kualitas kandidat di tahap interview meningkat. |

---

## Slide 6

### Ecosystem Alignment (Max 150 kata)

Bagaimana solusi Anda berinteraksi dengan stakeholder dan regulasi?

Berikut adalah solusi kami dalam rangka alignment dengan stakeholder & regulasi:

| Aspek | Penjelasan |
| --- | --- |
| Interaksi dengan Stakeholder | GaskeunKerja berinteraksi dengan tiga kelompok stakeholder utama. Jobseeker sebagai pengguna inti yang mendapatkan rekomendasi lowongan, analisis skill gap, dan learning roadmap secara personal. Employer dan rekruter yang mendapat manfaat dari shortlist kandidat yang lebih relevan dan terfilter berdasarkan kompetensi nyata. Platform pembelajaran dan job portal sebagai mitra yang memperkuat ekosistem dengan menyediakan data lowongan dan konten pelatihan secara berkelanjutan. |
| Kepatuhan Regulasi | GaskeunKerja dirancang sesuai dengan Undang-Undang Perlindungan Data Pribadi (UU PDP) Indonesia. Seluruh data pengguna dienkripsi saat transit maupun saat disimpan, akses dokumen CV dibatasi berbasis kebijakan IAM, dan autentikasi sesi menggunakan JWT token dengan masa berlaku terbatas. Pengguna memiliki kendali penuh atas data pribadi mereka sesuai prinsip persetujuan yang diatur dalam regulasi. |

---

## Slide 7

### Solution Approach & Mechanism (Max 250 kata)

Jelaskan bagaimana solusi bekerja secara end-to-end.

**Fase Input (Pengumpulan & Ekstraksi Data)**

| Langkah | Deskripsi |
| --- | --- |
| Unggah & Simpan CV | User mengunggah CV melalui aplikasi. File secara aman disimpan di Google Cloud Storage (GCS). |
| Parsing CV | Model Deepseek V4 Flash mem-parsing CV untuk mengekstrak kompetensi, pengalaman, dan kualifikasi ke dalam BigQuery secara otomatis. Pengguna memvalidasi preferensi dan hasil parsing AI. |
| Agregasi Lowongan Harian | Pipeline agregasi mengoleksi lowongan terbaru harian dari berbagai job portal (LinkedIn, Glassdoor, dll) yang kualifikasinya akan diringkas oleh AI dan disimpan ke BigQuery. |

**Fase Proses (Pencocokan ML & Analisis Mendalam)**

| Langkah | Deskripsi |
| --- | --- |
| Proses Embedding (Transformasi Data) | Data profil kandidat dan data kriteria lowongan pekerjaan diubah menjadi vektor data menggunakan model embedding AI yang disimpan di Qdrant Vector Database. |
| Pencocokan ML | Sistem menggunakan Knowledge Graph Embeddings untuk memetakan kompetensi pengguna dan lowongan dari vektor data yang sudah tersimpan di Qdrant. Semantic search digunakan untuk menghitung matching skor kecocokan multidimensi dengan membandingkan vektor profil user dengan vektor ribuan lowongan untuk mendapatkan hasil lowongan pekerjaan yang paling relevan untuk user. |
| Deteksi Skill Gap & Perencanaan Roadmap | Menggunakan Deepseek V4 Pro, AI bertindak sebagai reviewer untuk menganalisis kesenjangan skill yang user miliki dan menyusun personal learning path secara dinamis. |

**Fase Output (Rekomendasi & Peningkatan)**

| Langkah | Deskripsi |
| --- | --- |
| Rekomendasi Terarah | Sistem menyajikan rekomendasi lowongan pekerjaan dengan tingkat kecocokan tertinggi di dashboard pengguna. |
| Aksi Peningkatan Skill | User mendapatkan insight langsung terkait keahlian yang harus dipelajari beserta akses ke simulasi interview. |
| Perbaikan Berulang | Saat jobseeker meningkatkan skill dan memperbarui CV, siklus pencocokan AI akan mengulang prosesnya untuk memberikan rekomendasi yang lebih baik (iteratif). |

---

## Slide 8

### Impact Scale & Targets (Max 230 kata)

Apa dampak utama solusi Anda? Jelaskan skala dampaknya.

GaskeunKerja menargetkan dampak terukur bagi tiga segmen utama dalam tiga fase waktu:

| Segmen | Jangka Waktu | Target |
| --- | --- | --- |
| Jobseeker | 0–6 bulan | 500–1.000 pengguna aktif dari pilot di 3–5 kampus dan komunitas jobseeker digital, dengan matching score rata-rata di atas 70% dan CV parsing accuracy ≥85%. |
| Jobseeker | 6–24 bulan | 10.000–50.000 pengguna aktif, dengan ≥40% pengguna melaporkan penurunan waktu pencarian kerja, serta skill completion rate ≥30% pada learning roadmap yang direkomendasikan. |
| Jobseeker | 2–5 tahun | 500.000+ pengguna terdaftar dengan job placement rate ≥25% dari total pengguna aktif yang menggunakan fitur matching secara konsisten. |
| Employer | 6–24 bulan | 50–200 perusahaan mitra aktif dengan penurunan waktu rekrutmen rata-rata sebesar 30–40% dan peningkatan interview-to-hire rate sebesar 20% dibanding proses konvensional. |
| Industri | 2–5 tahun | Kontribusi terhadap penurunan skill mismatch sebesar 10–15% pada segmen fresh graduate dan early-career di sektor digital. Tersedianya skill gap dashboard nasional yang mencakup data dari ≥10 sektor industri sebagai referensi kebijakan upskilling pemerintah. |

Seluruh dampak diukur melalui: matching accuracy, placement rate, time-to-hire reduction, skill completion rate, dan mismatch reduction rate secara periodik.

---

## Slide 9

### Impact Measurement (Max 270 kata)

Bagaimana Anda mengukur keberhasilan solusi secara kuantitatif?

Keberhasilan GaskeunKerja diukur melalui indikator kuantitatif yang mencerminkan dampak terhadap jobseeker, employer, dan ekosistem ketenagakerjaan.

| Segmen | Metrik Pengukuran |
| --- | --- |
| Jobseeker | Metrik utama adalah jumlah pengguna aktif, jumlah profil skill yang berhasil dianalisis, dan persentase pengguna yang mendapatkan rekomendasi lowongan dengan matching score tinggi. Keberhasilan awal diukur dari peningkatan conversion rate dari rekomendasi ke lamaran, waktu rata-rata jobseeker menemukan lowongan relevan, serta jumlah skill gap report dan personalized learning roadmap yang dihasilkan. Selain itu, platform mengukur persentase pengguna yang menyelesaikan rekomendasi pelatihan dan peningkatan skill score setelah mengikuti learning path. |
| Employer | Keberhasilan diukur dari jumlah perusahaan yang menggunakan platform, jumlah lowongan yang diproses, akurasi shortlist kandidat, dan rasio kandidat yang lolos ke tahap interview. Metrik penting lainnya adalah penurunan waktu rekrutmen, penurunan biaya screening kandidat, serta peningkatan interview-to-hire rate dibandingkan proses rekrutmen konvensional. |
| Industri | Dampak diukur melalui jumlah jobseeker yang berhasil terserap kerja, persentase penurunan skill mismatch berdasarkan gap antara skill kandidat dan kebutuhan lowongan, serta distribusi penyerapan tenaga kerja per sektor dan wilayah. Dalam 6 bulan pertama, target utama adalah mempercepat proses pencarian kerja dan meningkatkan relevansi lamaran. Dalam 6-24 bulan, targetnya adalah peningkatan skill completion rate dan kenaikan penempatan kerja. Dalam 2-5 tahun, keberhasilan diukur dari kontribusi terhadap penurunan mismatch tenaga kerja secara regional dan nasional, serta pertumbuhan platform sebagai infrastruktur digital ketenagakerjaan berbasis skill. |

Total dampak utama diukur melalui: matching accuracy, skill improvement rate, placement rate, recruitment efficiency, dan mismatch reduction rate.

---

## Slide 10

### System & Public Value Proposition (Max 200 kata)

Bagaimana solusi memberikan nilai terhadap sistem yang lebih luas?

GaskeunKerja tidak hanya memberikan nilai kepada pengguna individu, tetapi berkontribusi langsung pada ekosistem ketenagakerjaan nasional yang lebih sehat dan efisien.

| No | Aspek | Penjelasan |
| --- | --- | --- |
| 1 | Bagi Ekosistem Ketenagakerjaan | Platform ini menjadi jembatan antara tenaga kerja yang tersedia dan kebutuhan rekrutmen industri secara real-time. Dengan mengumpulkan dan menganalisis data dari berbagai job portal, GaskeunKerja menghadirkan gambaran skill gap yang sebelumnya tidak tersedia secara terstruktur, baik di tingkat individu maupun nasional. |
| 2 | Bagi Kebijakan Publik | Data skill gap yang terkumpul dapat menjadi acuan bagi pemerintah dan lembaga pelatihan dalam merancang program upskilling yang tepat sasaran, sejalan dengan roadmap pengembangan SDM digital Indonesia. |
| 3 | Bagi Stabilitas Sosial-Ekonomi | Mempercepat penyerapan tenaga kerja secara akurat berarti mengurangi beban sosial dan fiskal akibat pengangguran struktural, khususnya bagi lulusan baru yang paling rentan terdampak mismatch kompetensi. |
| 4 | Kontribusi Sistemik | GaskeunKerja berpotensi menjadi infrastruktur digital ketenagakerjaan berbasis skill yang terhubung langsung dengan berbagai job portal sebagai sumber data lowongan, sekaligus terintegrasi dengan platform pembelajaran online untuk menyediakan rekomendasi pelatihan yang dapat langsung diakses jobseeker. Dengan ekosistem yang saling terhubung ini, GaskeunKerja mendorong peningkatan kompetensi tenaga kerja Indonesia secara berkelanjutan dan terukur. |

---

## Slide 11

### Solution Originality (Max 300 kata)

Apa yang benar-benar baru dari solusi Anda dibandingkan yang sudah ada?

GaskeunKerja menghadirkan beberapa diferensiasi utama yang tidak ditemukan pada platform rekrutmen konvensional:

| Fitur GaskeunKerja | Penjelasan | Metode Konvensional |
| --- | --- | --- |
| Agregator Lowongan pekerjaan paling terkini | Mengumpulkan dan memperbarui lowongan dari berbagai platform secara otomatis sehingga kandidat memperoleh akses ke peluang kerja terbaru dalam satu tempat. | Lowongan terbatas pada ekosistem platform masing-masing dan sering kali tidak terintegrasi lintas sumber. |
| ML Updated Job Matching | Sistem rekomendasi ML yang menghitung skor kesesuaian multidimensi konteks antara profil CV kandidat dengan kebutuhan skill paling kini lowongan. | Matching berbasis kata kunci sederhana tanpa memahami konteks kompetensi lowongan dan pengalaman kandidat. |
| Real-Time Skill Gap Analysis | Analisis kesenjangan kompetensi yang transparan dan selalu relevan, karena bersumber langsung dari lowongan terbaru dari lintas platform. | Tidak menyediakan analisis detail mengenai alasan ketidaksesuaian kandidat terhadap suatu lowongan. |
| Perbaikan CV berdasarkan format ATS | Evaluasi dan rekomendasi otomatis untuk meningkatkan kompatibilitas CV terhadap sistem ATS. | Hanya menyediakan unggah CV tanpa evaluasi kualitas maupun optimasi ATS. |
| Personalized Learning Roadmap | Setiap skill gap diterjemahkan menjadi jalur pengembangan diri yang terstruktur, lengkap dengan rekomendasi konten belajar paling terkini. | Tidak menyediakan panduan pembelajaran yang dipersonalisasi berdasarkan kebutuhan pasar kerja. |
| Simulasi interview | Simulasi wawancara berbasis AI sebagai sarana peningkatan kompetensi komunikasi, teknis, dan kesiapan menghadapi proses seleksi kerja. | Tidak menyediakan sarana latihan wawancara yang interaktif dan berbasis umpan balik. |

Platform rekrutmen saat ini mayoritas beroperasi sebagai etalase satu arah yang berpusat pada rekruter bukan kepada jobseeker. Kelemahan utamanya:

| No | Kelemahan Platform Konvensional |
| --- | --- |
| 1 | Evaluasi CV menjadi tidak transparan & objektif bagi pelamar. |
| 2 | Tidak ada panduan pengembangan skill untuk kandidat. |
| 3 | Matching masih berbasis keyword, bukan pemahaman konteks skill. |

Sebagai solusi, kami menghadirkan ekosistem karir interaktif yang secara proaktif memberdayakan pencari kerja. Melalui analisis AI yang mendalam, sistem kami mengurutkan lowongan yang sesuai, membedah skill gap secara objektif dan mengarahkan talenta pada personalized learning path untuk menutup kesenjangan skill yang dibutuhkan.

---

## Slide 12

### Technological / Method Innovation (Max 240 kata)

Apa pendekatan teknis/metodologi unik yang digunakan?

| No | Komponen Teknologi | Penjelasan |
| --- | --- | --- |
| 1 | Arsitektur Dual-LLM Berdasarkan Tingkat Kompleksitas | Sistem menerapkan metodologi workload splitting menggunakan dua model AI yang berbeda dalam Kubernetes Cluster. Deepseek V4 Flash dioptimalkan secara spesifik untuk tugas inferensi ringan berkecepatan tinggi seperti parsing CV dan ekstraksi kompetensi dasar. Sementara itu, Deepseek V4 Pro didelegasikan khusus untuk advanced reasoning seperti analisis skill gap kompleks dan penyusunan personalized learning roadmap. |
| 2 | Sistem Rekomendasi Berbasis KGE & GNN | Menggantikan pencocokan keyword matching dengan Knowledge Graph Embeddings (KGE) berbasis Graph Neural Networks (GNN). Metodologi ini memetakan hubungan entitas kompetensi ke dalam ruang vektor multidimensi, memungkinkan perhitungan matching score berdasarkan kedekatan relasional dan hierarki semantik yang akurat. |
| 3 | Arsitektur Data Hybrid | Memisahkan penyimpanan berdasarkan karakteristik data diantaranya BigQuery untuk data tabular terstruktur, Google Cloud Storage untuk dokumen CV tak terstruktur, dan Qdrant Vector Database untuk mengakomodasi semantic search berbasis embedding vektor. |
| 4 | Pipeline Data Otomatis & Real-time | Mengintegrasikan penarikan data lowongan kerja yang ditarik secara harian menggunakan SERP API dan mekanisme web scraping untuk menjamin kualitas data lowongan di dalam database internal. |
| 5 | Arsitektur Aplikasi Asinkron | Memanfaatkan FastAPI yang asinkron untuk mengorkestrasi seluruh pipeline AI dan data secara cepat, dibalut dengan frontend React.js untuk antarmuka yang responsif, serta dikontainerisasi penuh menggunakan Docker demi skalabilitas sistem. |
| 6 | Infrastruktur terintegrasi Cloud | Seluruh komponen tersebut diorkestrasi dalam klaster Kubernetes yang memanfaatkan Horizontal Pod Autoscaling (HPA) untuk skalabilitas otomatis sesuai jumlah user. Infrastruktur ini mencakup Load Balancer untuk manajemen trafik HTTPS/TLS, Secret Manager untuk keamanan kredensial, serta sistem monitoring dan logging untuk pengamatan berkala. |

---

## Slide 13

### Creativity in Implementation (Max 250 kata)

Jelaskan kreativitas dalam distribusi, monetisasi, atau user engagement.

GaskeunKerja menghadirkan pendekatan kreatif dalam distribusi, monetisasi, dan keterlibatan pengguna yang membedakannya dari platform rekrutmen konvensional.

| Aspek | Penjelasan |
| --- | --- |
| Distribusi | GaskeunKerja masuk melalui komunitas yang sudah ada seperti grup jobseeker di LinkedIn, Telegram, dan Discord tanpa bergantung pada iklan berbayar di awal. Strategi ini memanfaatkan kepercayaan antar sesama pencari kerja sebagai saluran distribusi organik yang efektif dan rendah biaya. |
| User Engagement | Platform dirancang agar jobseeker terus kembali secara alami. Setiap kali lowongan baru masuk yang cocok dengan profil mereka, notifikasi dikirim secara personal. Skill gap report yang dihasilkan bersifat dinamis dan berubah seiring perkembangan kebutuhan industri, sehingga jobseeker selalu punya alasan untuk memantau perkembangan kompetensi mereka. Simulasi interview berbasis AI juga mendorong pengguna untuk terus berlatih dan mengukur kesiapan mereka sebelum melamar. |
| Monetisasi | Model freemium menjadi fondasi utama, fitur dasar seperti rekomendasi lowongan dan skill gap analysis tersedia gratis untuk menjangkau sebanyak mungkin jobseeker. Pendapatan dihasilkan dari fitur premium jobseeker seperti akses simulasi interview tak terbatas dan laporan skill gap yang lebih mendalam, serta referral fee dari platform pembelajaran online ketika pengguna mengakses konten pelatihan berbayar melalui rekomendasi GaskeunKerja. |

---

## Slide 14

### System Architecture (Max 250 kata)

Jelaskan desain arsitektur solusi Anda secara sistemik.

| Komponen | Penjelasan |
| --- | --- |
| Web application frontend (React.JS) | UI responsif bagi user untuk mengelola profil, menganalisa skill gap berdasarkan CV, melacak rekomendasi lowongan secara real-time dan mengakses learning path. |
| Rest API Gateway Backend (FastAPI, Docker) | Komponen utama untuk mengorkestrasi alur data dan pipeline AI. Gateway ini bertindak sebagai orkestrator asinkron untuk rate limiting, validasi request, dan routing ke microservices. |
| Data Scraping & Aggregation pipeline (Serp API, Official Job Portal APIs) | Melakukan agregasi data lowongan terbaru dari berbagai platform setiap harinya. |
| Lightweight LLM inference (Deepseek V4 Flash) | Melakukan tugas inferensi ringan seperti parsing CV, ekstraksi kompetensi user (skill, pengalaman, kualifikasi), dan pembuatan ringkasan persyaratan lowongan. |
| Advanced reasoning LLM inference (Deepseek V4 Pro) | Menangani analisis kompleks seperti melakukan skill gap analysis, menyusun roadmap pembelajaran yang personal bagi user. |
| ML Recommendation (Knowledge Graph Embeddings) | Memetakan dan menghitung matching score secara kontekstual dari hubungan hierarki antara kompetensi user dengan kebutuhan lowongan menggunakan vektor multidimensi. |
| Vector Database (Qdrant) | Menyimpan data vektor hasil proses embedding untuk proses semantic search yang mendukung proses rekomendasi ML. |
| Tabular Database (BigQuery) | Menyimpan data tabular termasuk hasil skill gap analysis, riwayat rekomendasi, dan learning path pengguna. |
| Object Storage (GCS) | Menyimpan CV asli yang diunggah user dengan pengamanan ketat di Cloud. |
| Data Encryption (TLS, AES-256, JWT Token) | Sistem dirancang sesuai kepatuhan UU PDP Indonesia, menerapkan enkripsi in-transit (TLS 1.3), at-rest (AES-256), dan autentikasi JWT terpusat dengan masa berlaku terbatas. |
| Infrastructure & Scalability (Kubernetes) | Infrastruktur GKE diperkuat dengan Load Balancer, Cloud Armor (WAF), dan Secret Manager untuk resiliensi keamanan level enterprise dan scaling otomatis ketika user meningkat. |

---

## Slide 15

### Data & Feasibility (Max 200 kata)

Data apa yang digunakan? Dari mana sumbernya?

| Jenis Data | Penjelasan |
| --- | --- |
| Data CV Kandidat | Dokumen CV mentah format PDF atau Word yang diunggah secara langsung oleh user. CV asli akan disimpan dengan aman di Google Cloud Storage (GCS) dengan enkripsi at-rest. |
| Data Profil User Terstruktur | Merupakan data terformat hasil ekstraksi otomatis oleh Deepseek V4 Flash dari CV mentah. Data ini menggabungkan riwayat pengalaman, kompetensi teknis, kualifikasi, serta preferensi profesi dan lokasi kerja yang diinput langsung oleh pengguna. Seluruh data terstruktur ini disimpan secara tabular di Google BigQuery. |
| Data Lowongan Pekerjaan | Berasal dari berbagai platform karier (seperti LinkedIn, Glassdoor, dll.) yang ditarik secara harian menggunakan SERP API dan mekanisme web scraping. Data agregasi lowongan ini diproses melalui pipeline normalisasi sebelum diintegrasikan ke dalam sistem penargetan. |
| Data Vektor & Semantik | Berupa representasi embedding semantik dari kompetensi user dan lowongan yang memetakan hubungan kompetensi secara kontekstual. Dihasilkan dari transformasi data terstruktur (profil user dan lowongan) oleh embedding model yang kemudian disimpan di Qdrant Vector Database untuk keperluan semantic search. |
| Data Analitik & Output Sistem | Hasil rekomendasi pekerjaan, analisis skill gap, dan personalisasi learning path. Dihasilkan oleh DeepSeek LLM dan sistem rekomendasi Knowledge Graph, yang selanjutnya disimpan dalam bentuk tabular di BigQuery proses analitik. |

---

## Slide 16

### Security & Compliance (Max 200 kata)

Bagaimana solusi Anda menangani keamanan data dan kepatuhan?

Sistem mengadopsi prinsip Security by Design untuk melindungi data pengguna dan mematuhi UU PDP No. 27/2022 Indonesia melalui strategi berikut:

| Aspek Keamanan | Penjelasan |
| --- | --- |
| Enkripsi Data Komprehensif | Data saat transit (in-transit) dilindungi protokol TLS 1.3 antara Frontend dan Backend. Data tersimpan (at-rest) di Google Cloud Storage (GCS) dan BigQuery menggunakan standar enkripsi AES-256. |
| Kontrol Akses Ketat & IAM | Akses dokumen CV di GCS dibatasi menggunakan Cloud IAM Policy yang ketat dan mekanisme Signed URL dengan masa kadaluarsa singkat, memastikan hanya pengguna berwenang yang dapat mengakses. |
| Autentikasi & Otorisasi | Menggunakan JWT Token dengan masa berlaku terbatas (exp. limited) untuk manajemen sesi aman, dikombinasikan dengan sistem kontrol akses berbasis peran (RBAC). |
| Perlindungan Perimeter & Infrastruktur | Mengimplementasikan Google Cloud Armor sebagai Web Application Firewall (WAF) untuk mitigasi serangan siber (DDoS, OWASP Top 10) serta Secret Manager untuk mengisolasi kunci enkripsi dan kredensial API. |
| Kepatuhan & Tata Kelola Data | Menerapkan prinsip Data Minimization (hanya memproses data relevan untuk analisis kompetensi), menyediakan Audit Log menyeluruh untuk pelacakan aktivitas data, serta menjamin hak subjek data sesuai regulasi PDP nasional. |

---

## Slide 17

### Implementation Readiness (MVP) (Max 300 kata)

Apa scope MVP Anda dan target pembangunannya?

Target MVP: Menghasilkan platform karier berbasis AI yang mampu menghubungkan profil kompetensi pengguna dengan kebutuhan industri secara kontekstual. MVP diharapkan mampu menyediakan rekomendasi lowongan yang relevan, mengidentifikasi skill gap utama, serta menyusun roadmap pembelajaran yang dapat ditindaklanjuti pengguna. Hasil uji coba akan digunakan untuk memvalidasi kelayakan teknis, akurasi rekomendasi, dan potensi dampak terhadap peningkatan employability sebelum pengembangan menuju skala yang lebih luas. Target pembangunan produk ini dibagi atas 3 fase:

**Fase 1 — PoC**

| No | Aktivitas |
| --- | --- |
| 1 | Integrasi data lowongan pekerjaan dari satu sumber utama melalui API atau data aggregator. |
| 2 | Pengembangan pipeline ekstraksi CV menggunakan Deepseek V4 Flash untuk mengidentifikasi skill, pengalaman, pendidikan, dan preferensi karier. |
| 3 | Normalisasi data lowongan serta implementasi skill gap analysis dasar. |
| 4 | Implementasi skill gap analysis dasar dengan membandingkan kompetensi kandidat terhadap kebutuhan lowongan. |
| 5 | Pengembangan prototipe Knowledge Graph untuk memetakan hubungan kompetensi dan menghitung kandidat job matching score secara kontekstual. |
| 6 | Validasi awal akurasi ekstraksi skill dan kualitas rekomendasi pada dataset terbatas. |

**Fase 2 — Core Development**

| No | Aktivitas |
| --- | --- |
| 1 | Integrasi agregasi lowongan multi-platform melalui API dan scraping terjadwal. |
| 2 | Pengembangan Knowledge Graph Embeddings (KGE) dan Graph Neural Network (GNN) untuk rekomendasi pekerjaan multidimensi. |
| 3 | Peningkatan skill gap analysis agar mampu mengidentifikasi kesenjangan kompetensi secara lebih granular. |
| 4 | Pengembangan Personalized Learning Roadmap menggunakan Deepseek V4 Pro. |
| 5 | Implementasi semantic search menggunakan Qdrant Vector Database. |
| 6 | Integrasi FastAPI, React.js, BigQuery, GCS, dan pipeline AI ke dalam satu ekosistem terhubung. |

**Fase 3 — MVP**

| No | Aktivitas |
| --- | --- |
| 1 | Penggabungan seluruh modul menjadi platform web end-to-end yang mencakup rekomendasi lowongan real-time, skill gap analysis, dan personalized learning path. |
| 2 | Implementasi keamanan sesuai prinsip Security by Design melalui TLS 1.3, AES-256, JWT, RBAC, dan Audit Logging. |
| 3 | Kontainerisasi Docker serta deployment pada Kubernetes dengan autoscaling untuk mendukung pertumbuhan pengguna. |
| 4 | Pengujian performa, keamanan, dan reliabilitas sistem. |
| 5 | Uji coba internal bersama 20–50 pengguna awal untuk mengukur akurasi job matching, kualitas roadmap pembelajaran, pengalaman pengguna, serta mengumpulkan masukan untuk iterasi pengembangan berikutnya. |

---

## Slide 18

### Value Proposition (Max 220 kata)

Apa nilai utama yang diterima oleh pengguna?

**Bagi Jobseeker**

| No | Value |
| --- | --- |
| 1 | Rekomendasi kerja yang relevan berbasis skill, bukan sekadar keyword. |
| 2 | Akses ke lowongan terbaru dari berbagai platform dalam satu tempat. |
| 3 | Analisis skill gap yang transparan sehingga pengguna memahami alasan kecocokan maupun ketidaksesuaian terhadap suatu lowongan. |
| 4 | Personalized learning roadmap yang membantu pengguna meningkatkan kompetensi sesuai kebutuhan pasar kerja terkini. |
| 5 | Evaluasi dan rekomendasi perbaikan CV agar lebih kompatibel dengan sistem ATS. |
| 6 | Simulasi interview berbasis AI untuk meningkatkan kesiapan menghadapi proses seleksi. |
| 7 | Proses pencarian dan pelamaran kerja yang lebih akurat, terarah, dan efisien. |

**Bagi Employer**

| No | Value |
| --- | --- |
| 1 | Shortlist kandidat lebih akurat sesuai kebutuhan perusahaan. |
| 2 | Mengurangi waktu dan biaya rekrutmen melalui proses screening yang lebih otomatis dan relevan. |
| 3 | Meningkatkan kualitas kandidat yang masuk ke tahap interview. |
| 4 | Membantu mengidentifikasi talenta yang memiliki potensi berkembang meskipun belum memenuhi seluruh kebutuhan skill saat ini. |
| 5 | Mendukung pengambilan keputusan rekrutmen berbasis data dan kompetensi, bukan hanya kata kunci pada CV. |

**Bagi Industri**

| No | Value |
| --- | --- |
| 1 | Kontribusi penurunan tingkat mismatch tenaga kerja dan pengangguran secara nasional. |
| 2 | Mempercepat penyerapan tenaga kerja di sektor yang kekurangan kandidat terampil. |
| 3 | Mendorong peningkatan kompetensi tenaga kerja Indonesia melalui rekomendasi pembelajaran yang tepat sasaran. |
| 4 | Menyediakan insight tren kebutuhan skill industri yang dapat dimanfaatkan oleh institusi pendidikan, pelatihan, dan pembuat kebijakan. |
| 5 | Mendukung terciptanya ekosistem ketenagakerjaan digital yang lebih efisien, adaptif, dan berbasis kompetensi. |

---

## Slide 19

### Model Revenue / Funding (Max 200 kata)

Bagaimana solusi menghasilkan revenue atau pendanaan?

| Tahap | Strategi Monetisasi / Pendanaan |
| --- | --- |
| Tahap Awal | Revenue GaskeunKerja akan memaksimalkan hasil funding dari hackathon agar aplikasi dapat berjalan hingga grade production, setelah itu, kami selanjutnya akan menargetkan pendapatan dari employer dan partnership awal, sementara jobseeker dapat menggunakan platform secara gratis atau freemium untuk mempercepat pertumbuhan user-base. Sumber pendapatan awal meliputi employer subscription untuk posting lowongan, AI-based candidate matching, shortlist kandidat, dan dashboard rekrutmen dasar. Selain itu, platform dapat memperoleh pendanaan dari pilot project dengan perusahaan, kampus, pemerintah daerah, grant, CSR, hackathon funding, dan inkubasi startup. |
| Tahap Menengah | Monetisasi diperluas melalui premium employer package dengan fitur seperti advanced filtering, bulk hiring, analytics kandidat, dan talent pool management. GaskeunKerja juga dapat menerapkan success fee recruitment berdasarkan kandidat yang berhasil direkrut, serta partnership dengan training provider melalui rekomendasi course yang relevan dengan skill gap pengguna. |
| Tahap Lanjut | GaskeunKerja dapat berkembang menjadi infrastruktur ketenagakerjaan digital berbasis data melalui labor market intelligence dashboard, enterprise talent intelligence platform, API-as-a-Service untuk integrasi dengan HRIS, LMS, job portal, serta program kemitraan nasional atau regional dengan pemerintah dan industri. |

---

## Slide 20

### Cost Structure & Sustainability (Max 200 kata)

Apa komponen biaya utama dan keberlanjutan finansialnya?

Komponen biaya GaskeunKerja terbagi ke dalam empat kategori utama.

| Kategori Biaya | Penjelasan |
| --- | --- |
| Infrastructure Cost | Mencakup biaya teknis untuk menjalankan platform, seperti cloud hosting, Kubernetes cluster, database, analytics, object storage untuk CV dan data lowongan, monitoring, logging, domain, serta kebutuhan dasar keamanan sistem. |
| AI Cost | Mencakup seluruh proses berbasis kecerdasan buatan, seperti CV parsing, embedding generation, vector search untuk pencocokan kandidat dan lowongan, skill gap analysis, model evaluation, serta batch processing dan caching hasil AI agar proses matching lebih efisien dan scalable. |
| Operational Cost | Meliputi biaya operasional harian dan pengembangan produk, termasuk honor SDM untuk tim engineering, AI/data, product, dan business support. Selain itu, biaya ini juga mencakup customer support, legal dan compliance, serta maintenance sistem dan bug fixing untuk menjaga kualitas layanan. |
| Marketing & Business Development Cost | Mencakup biaya pertumbuhan pengguna dan mitra, seperti digital marketing campaign, partnership dengan employer, lembaga pelatihan, kampus, dan komunitas, outreach ke pemerintah daerah, customer acquisition, serta employer onboarding. |

Keberlanjutan finansial dijaga melalui efisiensi infrastruktur, optimasi biaya AI, dan pendapatan dari subscription, success fee, partnership, serta dashboard analitik.

---

## Slide 21

### Scalability (Max 170 kata)

Bagaimana solusi dapat berkembang ke skala yang lebih besar?

| Komponen | Mekanisme Skalabilitas |
| --- | --- |
| Auto Scaling via GKE & HPA | Menggunakan Horizontal Pod Autoscaler (HPA) di Google Kubernetes Engine (GKE) untuk menambah/mengurangi jumlah pod (FastAPI, LLM Inference, ML) secara otomatis mengikuti lonjakan pengguna yang mengakses website. |
| Asynchronous AI Pipeline | Proses inferensi AI yang berat (Deepseek V4 Flash/Pro) dipisah ke beban kerja asinkron, mencegah bottleneck pada gateway utama sehingga respons aplikasi tetap cepat. |
| Penyimpanan data embedding (Qdrant Vector DB) | Menangani jutaan data embedding kompetensi untuk semantic search yang cepat. |
| Penyimpanan data tabular dan object (BigQuery & GCS) | Solusi serverless Google Cloud yang otomatis membesar untuk menyimpan data tabular, riwayat, dan dokumen CV berskala besar tanpa batas server fisik. |
| Skalabilitas proses scraping | Pipeline agregasi lowongan kerja (LinkedIn, Glassdoor, dll.) dijadwalkan secara harian menggunakan jobs data queue, memisahkan beban scraping dari lalu lintas pengguna aktif. |
| Global Distribution (Cloud CDN) | Integrasi Cloud CDN mempercepat distribusi konten statis ke pengguna di berbagai lokasi. |

---

## Slide 22

### Partnership & Distribution (Max 170 kata)

Bagaimana strategi distribusi dan peran mitra Anda?

Berikut adalah beberapa strategi kami untuk Partnership & Distribution:

| No | Strategi | Penjelasan |
| --- | --- | --- |
| 1 | Distribusi dengan Networking | GaskeunKerja masuk melalui komunitas jobseeker yang sudah aktif di LinkedIn, Telegram, dan Discord sebagai saluran distribusi awal yang rendah biaya. Strategi ini memanfaatkan kepercayaan antar sesama pencari kerja untuk memperluas jangkauan secara organik tanpa bergantung pada iklan berbayar di tahap awal. |
| 2 | Kemitraan Job Portal | Integrasi dengan job portal seperti Jobstreet dan Glints sebagai sumber data lowongan harian menjadi fondasi utama sistem rekomendasi. Kemitraan ini memastikan ketersediaan data lowongan yang selalu relevan, terkini, dan mencakup berbagai sektor industri. |
| 3 | Kemitraan Platform Pembelajaran | GaskeunKerja bermitra dengan platform pembelajaran online sebagai penyedia konten pelatihan yang direkomendasikan kepada jobseeker berdasarkan skill gap mereka. Model referral fee diterapkan setiap kali pengguna mengakses konten berbayar melalui rekomendasi platform. |
| 4 | Kemitraan Institusi Pendidikan | Universitas dan politeknik menjadi mitra strategis untuk menjangkau fresh graduate sebagai segmen pengguna utama. Kolaborasi ini sekaligus membuka saluran distribusi yang terstruktur dan berkelanjutan langsung dari lingkungan akademik ke dunia kerja. |

---

## Slide 23

### Problem–Market Fit (Max 120 kata)

Mengapa masalah ini penting bagi target pengguna Anda?

| Aspek | Penjelasan |
| --- | --- |
| Masalah | Banyak jobseeker kesulitan menemukan lowongan yang benar-benar sesuai dengan skill mereka, sehingga proses melamar sering tidak terarah dan kurang efektif. Di sisi lain, employer juga menghadapi tantangan dalam menemukan kandidat yang relevan karena proses seleksi masih banyak bergantung pada keyword CV. |
| Solusi | GaskeunKerja menjawab masalah ini melalui AI-based job matching yang menganalisis CV, profil kandidat, dan kebutuhan skill dari lowongan kerja, lalu memberikan rekomendasi berdasarkan matching score. Selain itu, fitur skill gap analysis dan personalized training roadmap membantu jobseeker memahami kekurangan kompetensi, mengikuti jalur belajar yang tepat, serta berlatih interview dengan AI virtual assistant agar lebih siap masuk ke dunia kerja. |

---

## Slide 24

### Evidence of Demand (Max 220 kata)

Apa bukti bahwa solusi ini dibutuhkan? (Survey, interview, dll)

**Bukti Statistik**

| No | Fakta |
| --- | --- |
| a | Pengangguran Indonesia terus naik dari 7,2 juta (Feb 2024) menjadi 7,28 juta (Feb 2025) dan 7,36 juta (Nov 2025). |
| b | 46% perusahaan kesulitan mencari kandidat akibat skill gap. 50% menilai keterampilan teknis pelamar masih pemula, dan 35% menyebut kemampuan software belum memadai. |

**Observasi Lapangan**

| No | Observasi |
| --- | --- |
| a | Platform job portal yang ada (Jobstreet, LinkedIn) telah menyediakan fitur pencocokan lowongan berbasis AI, namun belum memberikan analisis skill gap yang personal dan transparan sehingga pencari kerja tidak mengetahui alasan rendahnya kecocokan terhadap suatu lowongan. |
| b | Pencari kerja umumnya melamar banyak lowongan secara manual tanpa memahami tingkat kecocokan kompetensinya, sehingga proses pencarian kerja menjadi kurang terarah dan efisien. |
| c | Insight karier seperti analisis skill gap, evaluasi CV ATS, dan rekomendasi pembelajaran yang dipersonalisasi masih terbatas atau hanya tersedia pada fitur premium di beberapa platform. |
| d | Belum tersedia platform yang mengintegrasikan agregasi lowongan terkini, AI-based job matching, skill gap analysis, dan personalized learning roadmap dalam satu alur pengembangan karier yang terhubung. |
| e | Pencari kerja umumnya melamar banyak lowongan secara manual tanpa memahami tingkat kecocokan kompetensinya, sehingga proses pencarian kerja menjadi kurang terarah dan efisien. |
| f | Feedback terhadap hasil lamaran kerja umumnya tidak tersedia sehingga pencari kerja kesulitan memahami kelemahan kompetensi. |
| g | Banyak platform rekrutmen masih berfokus pada proses pencarian lowongan, bukan pada pendampingan berkelanjutan untuk meningkatkan kesiapan kerja kandidat. |

---

## Slide 25

### Target Market (Max 150 kata)

Siapa target market utama Anda? Jelaskan secara spesifik.

| Segmen | Penjelasan |
| --- | --- |
| Jobseeker | Fresh graduate, lulusan bootcamp, mahasiswa tingkat akhir, dan pekerja awal karier yang kesulitan menemukan lowongan sesuai skill serta belum memahami skill gap mereka. Mereka membutuhkan rekomendasi kerja yang lebih terarah dan roadmap peningkatan kompetensi. |
| Employer | Perusahaan skala kecil hingga menengah, startup, dan tim HR yang membutuhkan proses rekrutmen lebih efisien. Mereka membutuhkan shortlist kandidat yang relevan untuk mengurangi waktu screening, biaya rekrutmen, dan risiko salah rekrut. |
| Institusi Pendidikan dan Pelatihan | Kampus, bootcamp, dan lembaga pelatihan yang membutuhkan insight skill gap serta kebutuhan industri agar kurikulum dan program pelatihan lebih sesuai pasar kerja. |
| Pemerintah dan Pembuat Kebijakan | Pemerintah daerah dan pembuat kebijakan yang membutuhkan data tren tenaga kerja, skill gap, dan kebutuhan upskilling untuk merancang program penyerapan kerja yang lebih tepat sasaran. |

---

## Slide 26

### Adoption Readiness (Max 180 kata)

Seberapa mudah solusi Anda diadopsi oleh pengguna?

GaskeunKerja dirancang agar mudah diadopsi oleh jobseeker, employer, dan mitra institusi karena menggunakan alur yang familiar seperti job portal, tetapi ditingkatkan dengan AI-based skill matching dan personalized roadmap.

| Aspek | Penjelasan |
| --- | --- |
| Jobseeker | Proses onboarding sederhana: pengguna cukup mengunggah CV atau mengisi profil skill, lalu sistem akan memberikan rekomendasi lowongan, matching score, skill gap analysis, dan learning roadmap. Pengguna tidak perlu memahami teknologi AI karena hasil ditampilkan dalam bentuk insight yang mudah dipahami dan langsung dapat ditindaklanjuti. |
| Employer | Adopsi juga mudah karena alurnya menyerupai proses rekrutmen digital yang sudah umum: membuat lowongan, menerima shortlist kandidat, melihat matching score, dan mengelola kandidat melalui dashboard. Hal ini mengurangi kebutuhan training tambahan. |
| Teknis | Platform berbasis web sehingga dapat diakses tanpa instalasi khusus. Arsitektur Docker dan Kubernetes memudahkan deployment ke berbagai environment, baik cloud maupun on-premise untuk mitra institusi. |
| Strategi Adopsi | Untuk mempercepat adopsi, GaskeunKerja dapat memulai dari pilot project dengan employer, kampus, lembaga pelatihan, dan pemerintah daerah sebelum diperluas secara nasional. |

---

## Slide 27

### Progress Since the 1st Submission (Max 150 kata)

Apa perkembangan utama sejak submission sebelumnya?

Sejak submission awal, proyek ini telah berkembang dari konsep POC menjadi prototype aplikasi AI-Powered Skill Gap Analysis yang sudah dikontainerisasi dengan Docker, dibangun dengan backend FastAPI, dan frontend interaktif. Perkembangan utama mencakup beberapa fitur yang terimplementasi melalui pipeline multi-agen berbasis LangGraph dan LLM yang mencakup beberapa fitur diantaranya:

| Fitur | Penjelasan |
| --- | --- |
| Parsing CV | Mengekstrak data terstruktur dari CV pengguna secara akurat. |
| Klasifikasi spesialisasi keterampilan | Mengkategorikan keterampilan secara eksplisit dan implisit dari pengalaman pengguna. |
| Ekstraksi lowongan kerja | Menganalisis kebutuhan lowongan kerja menggunakan grounded search. |
| Penyusunan laporan rekomendasi otomatis | Menghasilkan analisis kesenjangan keterampilan dan saran perbaikan secara otomatis. |
| Roadmap learning yang simpel | Menyediakan estimasi waktu belajar berdasarkan tingkat kesulitan upskilling. |

Saat ini, sistem masih bergantung penuh pada kapabilitas LLM yang memiliki potensi halusinasi. Integrasi Knowledge Graph Embeddings dan infrastruktur kubernetes belum diimplementasikan. Selain itu, pengambilan data lowongan job requirement masih terbatas pada artikel online yang selanjutnya akan difokuskan pada pengambilan langsung dari job portal.

---

## Slide 28

### Current Status (Max 50 kata)

Status solusi saat ini (idea/mockup/prototype/pilot).

Status keseluruhan: **Half Prototype**

| Komponen | Status |
| --- | --- |
| Skill Gap Advisor | Prototype awal, namun masih memerlukan pengembangan untuk mengimplementasikan knowledge graph embeddings. |
| Personalized Training | Saat ini masih berupa roadmap pembelajaran sederhana dengan estimasi durasi belajar berdasarkan tingkat kesulitan. |
| Job Matching | Pengambilan lowongan kerja masih bersumber dari artikel online dan belum terintegrasi langsung dengan platform job portal. |

---

## Slide 29

### Attachment

Lampiran dapat berupa demo, screenshot, atau file. Masukkan link atau unggah file.

| Jenis | Link / Status |
| --- | --- |
| Link Github | https://github.com/nugrahazikry/AI-Powered-Skill-Gap-Analysis |
| Link Demo | Nyusul |
| Link flow kerja dan diagram | Done |

---
