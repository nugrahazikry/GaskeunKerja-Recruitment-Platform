# Submission Tahap 3 — Jawaban (Draft)

> Draft mengikuti `tahap 3 proposal.md` (panduan) dan keputusan brainstorming di `plan.md` (Direction B — Company-Focused). Item bertanda **[ISI: ...]** perlu diisi langsung oleh tim sebelum submit — lihat catatan di bagian akhir dokumen.

---

### 1. ID Tim
P0804

### 2. Nama Tim
Keprof Reborn

### 3. Final Solution Title
**GaskeunKerja for Business — Platform AI Terintegrasi untuk Rekrutmen, Skill-Gap Analysis, dan Pengembangan Kandidat**

### 4. Problem Statement
Digitalisasi Penciptaan Lapangan Kerja

### 5. Sub-Problem Statement
1. Platform Job Matching Berbasis Kecerdasan Artifisial
2. Skill Gap Advisor
3. Personalized Training

---

### 6. Final Team Composition *(maks. 100 kata)*
Siapa saja anggota aktif tim dan apa peran utamanya?

Tim Keprof Reborn beroperasi dengan tiga anggota aktif.
1. Zikry Adjie Nugraha sebagai Project Lead & Frontend/Product Engineer: mengarahkan strategi produk serta merancang dashboard HR dan portal kandidat.

2. Diki Rustian sebagai AI/ML Engineer & Data Engineer: membangun pipeline Deepseek V4, skema database, dan modul AI Interview.

3. Muhammad Fikri Fadillah sebagai Backend Engineer, Security, & Cloud Infrastructure, mengelola REST API, autentikasi, dan migrasi cloud pada fase pilot. 

Seluruh anggota terlibat aktif sejak submission pertama dan turut merumuskan pivot strategi ke company-focus pada Tahap 3.

---

### 7. Final Solution Summary *(maks. 150 kata)*
Apa solusi akhir yang dikembangkan oleh tim Anda?

GaskeunKerja for Business adalah platform rekrutmen berbasis AI yang membantu perusahaan skala kecil-menengah untuk menemukan, menilai, dan mengembangkan kandidat pencari kerja secara lebih akurat, cepat dan efisien. Perusahaan cukup mengunggah deskripsi pekerjaan yang kemudian akan diproses oleh sistem kami dalam proses parsing CV kandidat, menghitung skor kecocokan kontekstual berbasis analisis skill-gap, lalu kandidat akan menjalankan AI Interview video berbasis pertanyaan yang dihasilkan dari kebutuhan lowongan.

Setiap jawaban dinilai menggunakan rubrik dan metrik yang transparan yang nantinya akan dirangkum untuk evaluasi lebih lanjut dengan keputusan akhir kandidat akan selalu berada di tangan HRD. Setiap kandidat, baik lolos maupun tidak, akan menerima laporan pengembangan kompetensi personal melalui email sebagai bentuk upskilling plan.

Dengan satu alur tertutup dari deskripsi pekerjaan hingga laporan pengembangan, GaskeunKerja for Business menghadirkan proses rekrutmen yang lebih cepat dan terukur bagi HRD, sekaligus tetap manusiawi dan bertujuan untuk meningkatkan kompetensi setiap kandidat yang dinilai.

---

### 8. Progress and Change Log *(maks. 150 kata)*
Apa perkembangan dan perubahan utama sejak 2nd submission?

Sejak submission kedua, tim mengevaluasi kelayakan arah jobseeker-focus dan memutuskan pivot ke company-focus karena tiga kendala berikut:

1. Sumber lowongan (scraping) rapuh secara teknis dan berisiko hukum, sekarang digantikan input lowongan langsung dari perusahaan.
2. Kebutuhan infrastruktur berat untuk ribuan pengguna, kini lebih ringan karena hanya melayani sedikit klien B2B di tahap awal, bukan ribuan pengguna individu.
3. Model freemium dengan ROI lemah digantikan model subscription B2B yang dibayar langsung oleh perusahaan.

Selain pivot strategi, tim merealisasikan progress teknis nyata:
1. Input lowongan dengan ekstraksi kompetensi otomatis, CV diunggah lewat folder.
2. Pemrosesan CV dengan redaksi PII dan analisis visual AI.
3. Matching dan ranking kandidat berbasis skill-gap yang detail.
4. AI interview video dengan fitur uji kamera mikrofon, rekam berbatas waktu, dan penilaian rubrik.
5. Laporan pengembangan personal untuk semua kandidat lolos maupun tidak dikirim melalui email.
6. Dashboard HR untuk visualisasi alur kandidat lintas lowongan.

---

### 9. Validated User Problem and Evidence *(maks. 250 kata)*
Masalah utama apa yang diselesaikan dan apa bukti bahwa masalah tersebut nyata?

Masalah inti yang kami selesaikan adalah inefisiensi rekrutmen akibat skill mismatch yang sulit dideteksi melalui proses seleksi konvensional. Berdasarkan ManpowerGroup Talent Shortage Survey (2024), 46% perusahaan kesulitan menemukan kandidat sesuai kebutuhan, 50% menilai keterampilan teknis pelamar masih level pemula, dan 35% menyebut kemampuan software pelamar belum memadai. Di sisi makro, BPS (2025) mencatat pengangguran Indonesia naik dari 7,28 juta (Februari 2025) menjadi 7,36 juta (November 2025), menunjukkan bahwa lapangan kerja yang tersedia tidak terserap secara efektif akibat mismatch kompetensi yang tidak transparan bagi kedua pihak. WEF Future of Jobs Report (2023) turut menegaskan bahwa program upskilling jarang terhubung langsung dengan kebutuhan skill aktual dari lowongan, sehingga proses pengembangan kandidat tidak terarah. Perusahaan skala kecil-menengah kesulitan karena tidak memiliki tim rekrutmen sebesar korporasi besar untuk melakukan screening manual yang mendalam terhadap setiap pelamar. Kami mengakui bahwa validasi kami saat ini masih bersumber dari data sekunder (laporan industri), belum dari wawancara langsung dengan HR; ini menjadi prioritas riset lanjutan dalam dua minggu ke depan melalui percakapan pilot dengan 3-5 perusahaan SME sebagai bukti awal sebelum dan selama pengembangan MVP.

---

### 10. End-to-End Use Case and Feature-to-Pain Mapping *(maks. 300 kata)*
Bagaimana solusi digunakan dari awal sampai menghasilkan manfaat bagi pengguna?

Alur Penggunaan End-to-End
1. HR login lalu mengunggah deskripsi pekerjaan, sistem mengekstrak kompetensi yang dibutuhkan secara otomatis menggunakan Deepseek V4 Flash.
2. CV kandidat masuk lewat folder khusus per lowongan. Kemudian, teks diekstrak dan data pribadi (nama/email/telepon) dihilangkan sebelum diproses AI.
3. Sistem menghitung skor kecocokan tiap kandidat dari kombinasi cakupan kompetensi wajib (90%) dan tingkat kemahiran (10%) yang menghasilkan shortlist berperingkat yang dapat dirunut ke kompetensi spesifik.
4. HR menyetujui dan mengundang kandidat terpilih lewat email.
5. Kandidat menguji kamera dan mikrofon, lalu menjalani AI Interview video dengan batas waktu per pertanyaan. Selanjutnya, jawaban direkam dan ditranskripsi dengan Whisper Large V3, dan dinilai otomatis dengan rubrik tetap dengan Deepseek V4 Pro.
6. HR meninjau skor interview AI, ringkasan skill-gap, dan rekaman video di halaman laporan, lalu mengambil keputusan akhir. Di tahap ini, AI hanya merangkum dan merekomendasikan, keputusan tetap di tangan manusia.
7. Setiap kandidat, lolos maupun tidak, menerima laporan upskilling plan otomatis lewat email.

Feature-to-Pain Mapping
1. Mismatch kompetensi: Matching berbasis analisis skill-gap yang rinci, bukan keyword matching sederhana dan skor dapat dirunut ke kompetensi spesifik yang cocok atau tidak.
2. Inefisiensi rekrutmen manual: AI Interview video menggantikan wawancara satu-per-satu di tahap awal dengan HR cukup meninjau ringkasan dan skor yang dihasilkan AI, bukan menyaring seluruh kandidat dari nol.
3. Minimnya transparansi skill-gap: Shortlist dan laporan kandidat menampilkan rincian kompetensi yang terpenuhi maupun belum, bukan hanya skor tunggal tanpa penjelasan dengan penilaian yang dijaga konsisten.
4. Terputusnya pembelajaran dari kebutuhan industri: Setiap kandidat, lolos maupun tidak, menerima laporan pengembangan personal berisi feedback CV dan interview serta rekomendasi upskilling plan yang menjawab langsung keluhan umum jobseeker bahwa feedback lamaran kerja nyaris tidak pernah tersedia.
5. Bias rekrutmen dari penilaian subjektif: rubrik tetap dan voting konsistensi menjaga skor AI konsisten, tidak bergantung mood atau preferensi personal reviewer.

---

### 11. Operational Context, Solution Boundary, and Adoption *(maks. 200 kata)*
Dalam kondisi apa solusi digunakan dan apa batas penggunaannya?

Konteks Operasional:
1. Digunakan pada tahap screening dan interview awal rekrutmen, saat perusahaan punya lowongan terbuka dan volume pelamar menyulitkan screening manual.
2. Target utama: perusahaan skala kecil-menengah Indonesia yang belum mampu berlangganan platform ATS enterprise seperti HireVue.
3. Kondisi ideal: perusahaan yang menghadapi volume pelamar besar (puluhan hingga ratusan per lowongan), sehingga screening manual menjadi bottleneck nyata bagi tim rekrutmen.

Batasan Solusi:
1. Bukan pengambil keputusan akhir, namun berperan sebagai alat bantu keputusan. HRD selalu memutuskan hasil akhir, AI tidak pernah menolak kandidat secara otomatis.
2. Tidak menangani proses pasca-rekrutmen (kontrak kerja, payroll, administrasi HR), fokus hanya pada matching, analisa skill-gap, interview awal, dan pemberian laporan pengembangan skill.
3. Interview dan transkripsi saat ini hanya mendukung Bahasa Indonesia.
4. Skala baru diverifikasi untuk puluhan kandidat per lowongan, volume ratusan pelamar sekaligus belum divalidasi.

Strategi Adopsi:
1. Alur menyerupai proses rekrutmen digital yang sudah familiar (posting lowongan, menerima shortlist, mengelola kandidat), tanpa pelatihan teknis tambahan bagi HR.
2. Dashboard terpusat dengan funnel kandidat lintas semua lowongan aktif tampil dalam satu layar, tanpa berpindah tool.
3. Kandidat mengakses AI Interview lewat tautan web tanpa instalasi apa pun.
4. Persetujuan eksplisit diminta dari kandidat sebelum data interview diproses, sesuai UU PDP.

---

### 12. Innovation Level
Pada tahap perkembangan apa solusi Anda saat ini? (Bukti pendukung dapat dilengkapi pada lampiran)

LEVEL 3: Prototype, validasi, atau implementasi awal

---

### 13. Current Technical Reality, Data, and Integration *(maks. 300 kata)*
Sejauh mana solusi Anda sudah dibangun dan siap diintegrasikan?

Status Implementasi:
1. Proses end-to-end: 18 tabel PostgreSQL, 12 router backend, dan 32 modul service mencakup seluruh alur dari data lowongan dan CV, matching skill-gap, hingga interview dan pengiriman laporan. 16 halaman frontend React melayani sisi HR (dashboard, lowongan, shortlist kandidat) dan portal kandidat (persetujuan penggunaan data, wawancara) dengan bukti skala kode nyata yang siap pakai.
2. Pemrosesan CV: Deepseek V4 Flash dan visual AI untuk CV hasil scan dan data pribadi (nama/email/telepon) diganti alias sebelum ekstraksi skill dan pengalaman.
3. Matching kandidat-lowongan: Analisis skill-gap yang terverifikasi dengan skor gabungan cakupan kompetensi wajib (90%) dan tingkat kemahiran (10%), sumber data identik dengan yang ditampilkan ke HR di halaman detail kandidat.
4. Efektivitas matching: Sudah diuji pada data kandidat dengan tingkat kemahiran kuat/sedang/lemah, sistem terbukti memisahkan kualitas kandidat secara konsisten dan signifikan.
5. Modul AI Interview: Rekam video, speech-to-text Whisper Large V3, penilaian rubrik dengan Deepseek V4 Pro sudah dibangun dan diverifikasi end-to-end, termasuk pengiriman laporan via email yang terkonfirmasi diterima.

Data yang Dikelola:
1. Data lowongan: Pipeline scraping lowongan resmi dihapus dan sumber langsung dari input terstruktur HRD.
2. CV kandidat: Diproses jadi profil terstruktur dengan daftar skill, pengalaman, dan ringkasan CV untuk matching.
3. Rekaman dan transkrip interview: Dinilai jadi skor rubrik dan ringkasan per jawaban, hanya diproses setelah kandidat memberi persetujuan eksplisit.
4. Seluruh data di atas diolah menjadi laporan pengembangan kandidat yang memuat ringkasan skill-gap, feedback interview, dan rencana upskilling.

Kesiapan Integrasi:
1. MVP: Berjalan 100% lokal dan containerized penuh (Docker Compose: Frontend, Backend, PostgreSQL dan file sistem CV/video)
2. Rencana migrasi: Implementasi ke Cloud Run/BigQuery/GCS pada fase pilot produksi.
3. Autentikasi terstandar: JWT untuk HR, token unik untuk kandidat dengan pola auth siap pakai.
4. Endpoint teruji: Seluruh request alur inti (lowongan, CV, matching, interview laporan) sudah terverifikasi.

---

### 14. MVP Execution and Deployment Plan *(maks. 250 kata)*
Bagaimana rencana tim membawa solusi ke tahap MVP atau pilot berikutnya?

Eksekusi MVP:
1. Fondasi tooling: LLM (Deepseek V4 flash dan pro), speech-to-text (Whisper Large V3), dan vision-LLM untuk CV scan sudah terverifikasi dengan panggilan API nyata.
2. Database: Skema 18 tabel PostgreSQL dirancang dan dibangun, dilengkapi kerangka kompetensi, serta uji coba 30 data kandidat awal yang sudah diproses lewat pipeline nyata.
3. Backend & AI pipeline: input lowongan, ekstraksi kompetensi, pemrosesan CV, matching skill-gap, hingga AI Interview (video, transkripsi, penilaian rubrik) sudah diuji secara menyeluruh.
4. Frontend: 16 halaman React (Vite + TypeScript) tersambung ke API nyata. Sisi HR (dashboard, lowongan, shortlist kandidat, kelola pertanyaan, laporan) dan portal kandidat (persetujuan data, uji kamera/mikrofon, wawancara) sudah terverifikasi dengan data sungguhan, bukan mockup statis.
5. QA: konsistensi skor, redaksi PII, akurasi matching, dan tujuh skenario end-to-end di browser sudah ditemukan dan diperbaiki yang diantaranya (1) alur lengkap HR-interview-keputusan-laporan, (2) jalur yang diblokir untuk kandidat, (3) jalur yang diblokir untuk HR, (4) kegagalan dan percobaan kirim ulang email, (5) status kandidat lintas tahap, (6) integritas data lintas tabel, (7) kebersihan data uji.

Rencana Pilot Berikutnya:
1. Migrasi infrastruktur: PostgreSQL lokal ke BigQuery, penyimpanan file CV/video ke GCS, backend (Docker Compose) ke Cloud Run.
2. Stress test: Mencoba banyak lowongan dengan CV berjumlah ratusan, untuk menemukan batas kapasitas nyata platform dan memperbaiki bottleneck yang ditemukan.
3. Pilot: Setelah platform terbukti stabil dari stress test, baru onboarding 3-5 perusahaan skala kecil dan menengah nyata dalam 1-2 bulan untuk memvalidasi asumsi ROI dengan data nyata.

---

### 15. Problem and System Complexity *(maks. 200 kata)*
Apa yang membuat masalah dan solusi ini tidak dapat ditangani dengan cara sederhana?

Kompleksitas Masalah:
1. Screening manual ratusan CV dan interview tahap awal untuk banyak lowongan sekaligus menjadi bottleneck nyata. Otomatisasi sederhana (filter keyword) sanggup menangani volume tinggi tapi gagal menangkap kompetensi akurat, sementara penilaian manual yang teliti hanya bisa diskalakan dengan menambah rekruter, namun menambah biaya mahal yang memberatkan perusahaan kecil-menengah.
2. Kecocokan kompetensi bersifat kontekstual dan multidimensi, contohnya dua kandidat bisa sama mencantumkan "Python", tapi satu baru tutorial dasar dan yang lain tiga tahun pengalaman kerja. Kasus lainnya kompetensi seperti "leadership" tersirat dari pengalaman ("memimpin tim lima engineer") tanpa pernah jadi kata kunci literal. Keyword matching sederhana tidak menangkap kedalaman maupun sinonim semacam ini.

Kompleksitas Solusi:
1. Skala tanpa menambah biaya linear: Seluruh CV dan tahap awal interview diproses otomatis oleh AI (pemrosesan CV, matching, hingga interview video tahap awal) yang memangkas waktu interview tahap awal yang jadi bottleneck nyata dengan biaya yang sama tanpa harus menambah rekruter tambahan.
2. Kecocokan kontekstual: Analisis skill-gap terverifikasi dengan skor gabungan dari kompetensi wajib yang benar-benar terpenuhi (90%) dan tingkat kemahiran (10%). Proses matching ini menilai konteks kompetensi yang tertulis eksplisit maupun yang tersirat dari pengalaman, bukan sekadar kata kunci, sehingga skor tetap terukur karena dapat dirunut ke kompetensi spesifik per kandidat.

---

### 16. Processing Pipeline and Engineering Depth *(maks. 250 kata)*
Bagaimana alur pemrosesan dan rancangan teknis solusi Anda?

Processing Pipeline:
1. HR login (JWT) dan membuat lowongan lewat frontend React → backend FastAPI mengorkestrasi alur asinkron.
2. Deepseek V4 Flash mengekstrak kompetensi dari lowongan.
3. Kumpulan CV diekstrak dengan pypdf, seluruh teks diredaksi PII (nama/email/telepon) sebelum dikirim ke LLM untuk parsing jadi data terstruktur (skill, pengalaman, kualifikasi). Hasil ekstraksi disimpan di PostgreSQL, dokumen asli di filesystem.
4. Profil kandidat dibandingkan dengan kompetensi lowongan lewat analisis skill-gap dengan skor dari kombinasi cakupan kompetensi (90%) dan tingkat kemahiran (10%). Sumber data sama dengan yang ditampilkan ke HR, sehingga ranking dapat diukur.
5. HR meninjau shortlist kandidat, mengedit dan menyetujui pertanyaan interview yang sudah dibuat AI, lalu mengundang kandidat lewat email.
6. Kandidat menguji kamera/mikrofon, merekam jawaban video dan audio yang akan ditranskripsi oleh Whisper Large V3. Deepseek V4 Pro menilai dengan rubrik tetap lalu menghasilkan laporan ringkasan analisa skill-gap, feedback interview, dan rencana upskilling kompetensi.
7. Skor dan ringkasan ditampilkan di halaman laporan dan HR akan mereview laporan per kandidat untuk keputusan akhir.
8. Sistem menyusun laporan pengembangan yang dibuat menjadi PDF yang dikirim otomatis via email ke seluruh kandidat dengan pesan keputusan dan laporan digabung ke satu pesan.

Engineering Depth:
1. Redaksi PII: Email/telepon dihapus via regex, sedangkan nama dideteksi dan diganti alias sebelum teks dipakai untuk analisis kompetensi menggunakan LLM.
2. Human-in-the-loop diterapkan di level: persetujuan pertanyaan interview, dan keputusan akhir kandidat.
3. Penilaian rubrik: Menggunakan voting konsistensi menutup celah LLM yang tidak cukup diatasi hanya dengan temperature=0.
4. Proses berjalan lokal, migrasi cloud direncanakan saat fase pilot.

---

### 17. Algorithm or Rule Quality and Decision Transparency *(maks. 300 kata)*
Bagaimana sistem menghasilkan dan menjelaskan hasil atau keputusannya?

Algorithm or Rule Quality:
1. Matching: Skor dihitung dari kombinasi cakupan kompetensi wajib yang benar-benar terpenuhi secara kontekstual (90%) dan tingkat kemahiran (10%), bukan kesamaan vektor satu blok utuh yang rawan false positive atau filter kata kunci, melainkan analisis kompetensi yang berpijak pada data terstruktur (skill eksplisit dan tersirat dari profil kandidat dibandingkan satu per satu dengan daftar kompetensi wajib lowongan).
2. Penilaian rubrik: Kriteria dan level penilaian didefinisikan tetap sejak awal (kejelasan, relevansi, kedalaman teknis) dengan model dipaksa menilai sesuai struktur ini, bukan menghasilkan skor bebas tanpa pedoman.
3. Konsistensi: Pengujian internal menemukan temperature=0 saja tidak cukup menjamin hasil identik pada input sama, karena variasi nyata di level LLM. Maka dari itu, sistem menerapkan voting konsistensi (beberapa panggilan independen dan hasil diambil median untuk skor rubrik atau mayoritas untuk kompetensi skill-gap) yang diverifikasi menghasilkan nol variasi pada pengujian berulang.
4. Terbukti berfungsi: Pada data kandidat berjenjang kuat/sedang/lemah, algoritma membedakan kualitas kandidat secara konsisten dan signifikan.

Decision Transparency:
1. Penelusuran skor rubrik: Setiap skor dapat ditelusuri ke kompetensi spesifik yang cocok atau tidak cocok, bukan hanya angka akhir tanpa penjelasan. HR bisa melihat rincian kompetensi yang sama persis di halaman detail kandidat dan laporan dan dapat dibaca dari satu sumber data yang sama dengan yang menentukan skor ranking, bukan dari dua sistem terpisah yang berisiko tidak sinkron.
2. Keputusan akhir di HR: AI tidak pernah menolak kandidat secara otomatis, skor dan ringkasan interview murni jadi bahan rekomendasi dengan keputusan akhir selalu di tangan HR. Hal ini diverifikasi langsung di kode (tidak ada satu pun jalur API yang bisa memutuskan status kandidat tanpa aksi eksplisit dari HR).
3. Desain ini mengurangi risiko bias algoritmik dan tanggung jawab hukum atas keputusan rekrutmen otomatis, sekaligus menjaga kepercayaan pengguna terhadap sistem.

---

### 18. User Flow, Usability Testing, and Product Iteration *(maks. 250 kata)*
Bagaimana pengalaman pengguna telah diuji dan diperbaiki?

User Flow:
1. HR: Alur rekrutmen digital yang familiar, kini dibantu AI (posting lowongan, shortlist, kelola kandidat) tanpa perlu pelatihan tambahan.
2. Kandidat: Portal sederhana tanpa akun — isi persetujuan, jawab interview, terima laporan pengembangan.

Usability Testing:
1. 30 sample kandidat + 6 kandidat uji berjenjang kuat/sedang/lemah diproses lewat pipeline nyata, membuktikan algoritma matching benar-benar memisahkan kualitas kandidat.
2. Tujuh skenario end-to-end diuji visual di browser asli: alur lengkap HR-interview-keputusan-laporan, jalur diblokir kandidat/HR, kegagalan+retry kirim email, status kandidat lintas tahap, integritas data lintas tabel, kebersihan data uji.

Product Iteration:
1. Nama kandidat lolos redaksi PII: CV tidak pernah menerima nama untuk diredaksi, ditambah pemotongan teks 800 karakter melewatkan nama di posisi lanjut. Diperbaiki dengan deteksi nama lewat 1 panggilan LLM khusus, nama sempat terkirim ke LLM untuk dideteksi dan hasilnya dipakai ganti nama jadi alias, sudah ditest 8/8 CV bersih.
2. Skor rubrik tidak konsisten: Penyebab di level LLM provider inferensi terdistribusi. Diperbaiki dengan voting konsistensi (3 panggilan mayoritas) dan sudah konsisten dengan 9 panggilan × 3 run, nol variasi.
3. Skor interview tidak tersambung: Endpoint penilaian ada tapi tidak pernah dipanggil dari frontend. Kandidat asli selesai interview tanpa pernah dinilai. Diperbaiki dengan submit jawaban kini otomatis memicu penilaian.
4. Seluruh kondisi skenario interview mengalami kegagalan di awal (izin kamera/mikrofon ditolak, submit interview kosong, kegagalan kirim laporan). Sudah diperbaiki dan diverifikasi berjalan benar, termasuk laporan nyata terkonfirmasi terkirim. Validasi dengan HR eksternal sungguhan belum dilakukan, menjadi prioritas fase pilot pasca-hackathon bersama 3-5 perusahaan kecil-menengah.

---

### 19. Team Capability and Execution Ownership *(maks. 250 kata)*
Bagaimana kompetensi dan tanggung jawab dibagi dalam tim?

Zikry Adjie Nugraha (Project Lead & Frontend/Product Engineer):
1. Mengarahkan strategi produk, riset problem-solution fit, dan penyusunan proposal untuk tiap klien B2B, termasuk analisis kelayakan yang menghasilkan keputusan pivot ke company-focus.
2. Merancang dan membangun dashboard HR (funnel kandidat lintas lowongan), portal kandidat, dan alur perizinan dari wireframe sampai implementasi React.
3. Mengumpulkan feedback usability dan mengkoordinasikan prioritas fitur antar-area kerja tim.

Diki Rustian (AI/ML Engineer & Data Engineer):
1. Membangun pipeline Deepseek V4 Flash untuk ekstraksi kompetensi lowongan, pemrosesan CV (redaksi PII, fallback vision untuk CV hasil scan), dan analisis skill-gap yang mendasari skor matching.
2. Mendesain skema database PostgreSQL dan struktur object storage untuk CV serta video interview.
3. Mengembangkan modul AI Interview termasuk pembuatan pertanyaan, penilaian rubrik dengan Deepseek V4 Pro, dan voting konsistensi untuk menjamin skor stabil.

Muhammad Fikri Fadillah (Backend Engineer, Security, & Cloud Infrastructure):
1. Membangun REST API dan mengorkestrasi alur asinkron backend FastAPI, termasuk autentikasi JWT untuk HR dan token link untuk kandidat.
2. Menangani redaksi PII sesuai UU PDP, serta keamanan endpoint.
3. Mengelola deployment lokal (Docker Compose) dan memimpin rencana migrasi ke Cloud Run/BigQuery/GCS pada fase pilot produksi.

Pembagian ini mencerminkan realita tim kecil: 3 orang menutupi area kompetensi lewat pairing berdasarkan kedekatan skill, bukan spesialisasi terpisah per orang. Seluruh anggota terlibat aktif sejak submission pertama dan familiar dengan stack ini (Deepseek V4, FastAPI, React, GCP), sehingga transisi ke ide baru tidak memerlukan pembentukan tim baru.

---

### 20. Continuation Readiness *(maks. 200 kata)*
Bagaimana tim akan melanjutkan solusi setelah hackathon?

Pasca-hackathon, tim berencana melanjutkan pengembangan melalui tiga langkah utama. Pertama, menjalankan pilot dengan 3-5 perusahaan SME dalam 1-2 bulan untuk memvalidasi asumsi ROI (pengurangan waktu screening dan time-to-hire) dengan data riil, menggantikan estimasi dari laporan sekunder yang digunakan saat ini. Kedua, memperkuat modul AI Interview berdasarkan feedback pilot, termasuk penyempurnaan rubrik penilaian dan cakupan jenis pertanyaan per industri. Ketiga, mencari pendanaan lanjutan melalui kombinasi hasil hackathon, program inkubasi startup, serta pendapatan awal dari subscription B2B perusahaan pilot untuk menutup biaya infrastruktur (~$170-370/bulan pada skala awal). Tim juga akan menjajaki kemitraan dengan asosiasi UMKM/SME dan komunitas HR Indonesia sebagai saluran distribusi awal, mengikuti pendekatan networking organik yang telah terbukti relevan sejak Tahap 2. Roadmap jangka menengah mencakup ekspansi ke 50-100 klien berbayar dalam 6-24 bulan, didukung oleh data flywheel dari setiap interview yang memperkaya kualitas rubrik dan matching dari waktu ke waktu.

---

### 21. Quantified Value, Business Model, and ROI *(maks. 300 kata)*
Bagaimana solusi menciptakan nilai dan menghasilkan pengembalian yang terukur?

Model bisnis GaskeunKerja for Business adalah B2B subscription dengan opsi per-seat atau per-hire, menggantikan model freemium jobseeker yang sebelumnya sulit dikonversi menjadi revenue. Target awal adalah 5-15 perusahaan SME pilot dalam 6 bulan pertama, tumbuh menjadi 50-100 klien berbayar dalam 6-24 bulan, dan 500-1.000 perusahaan dalam 2-5 tahun. Nilai yang ditawarkan terukur secara langsung: target pengurangan waktu rekrutmen (time-to-hire) sebesar 30-40% — diwariskan dari estimasi Tahap 2 dan kini menjadi metrik utama, bukan sekunder — pengurangan waktu screening hingga 50% melalui otomatisasi AI Interview, serta peningkatan interview-to-hire rate sebesar 20-25% karena kandidat yang lolos ke tahap interview manusia telah melalui pra-seleksi yang lebih akurat. Dari sisi biaya, arsitektur Direction B jauh lebih efisien: estimasi infrastruktur cloud (GCP) berkisar $170-370 per bulan pada skala di bawah 50 klien — sekitar 4-6 kali lebih murah dibanding arsitektur jobseeker-focus (~$800-1.750/bulan) yang membutuhkan Kubernetes cluster penuh dan pipeline scraping harian. Karena biaya infrastruktur berskala kecil sementara setiap klien membayar langsung, ROI investasi menjadi lebih cepat tercapai dibanding model freemium jobseeker yang bergantung pada konversi pengguna gratis ke berbayar dalam jumlah besar. Kami secara jujur mencatat bahwa angka efisiensi rekrutmen di atas merupakan target berbasis estimasi Tahap 2 dan literatur industri, yang akan divalidasi lebih lanjut melalui pilot nyata sebelum dijadikan klaim final kepada investor.

---

### 22. Adoption, Growth Strategy, and Competitive Moat *(maks. 250 kata)*
Bagaimana solusi akan memperoleh pengguna, berkembang, dan mempertahankan keunggulannya?

Strategi adopsi dimulai dari segmen yang kurang terlayani: perusahaan SME Indonesia yang membutuhkan bantuan rekrutmen namun tidak mampu berlangganan platform enterprise seperti HireVue atau ATS global. Distribusi awal memanfaatkan jaringan komunitas HR, asosiasi UMKM, dan kemitraan kampus (sebagai sumber talent pool kandidat), mengikuti pendekatan networking organik berbiaya rendah yang telah terbukti relevan sejak Tahap 2. Fitur development report yang dikirimkan ke seluruh kandidat — baik lolos maupun tidak — menjadi nilai tambah employer branding bagi perusahaan klien, sekaligus mendorong word-of-mouth positif dari kandidat yang merasa dihargai meski tidak diterima. Competitive moat kami bukan satu fitur tunggal yang mudah ditiru, melainkan integrasi penuh matching, skill-gap analysis, AI Interview, dan development report dalam satu alur — sementara kompetitor seperti platform ATS global maupun job portal umumnya menyediakan fitur-fitur ini secara terpisah atau tidak sama sekali untuk segmen SME. Moat ini diperkuat oleh data flywheel: semakin banyak interview yang diproses, semakin kaya data kompetensi dan hasil rubrik yang memperbaiki akurasi matching dan kualitas pertanyaan interview secara khusus untuk konteks pasar kerja Indonesia — sesuatu yang tidak dimiliki pemain global generik.

---

### 23. Video Submission
**[ISI: link YouTube Elevator Pitch, format unlisted]**

### 24. Link Attachment
**[ISI: satu link publik — demo, screenshot, atau file. Kandidat kuat: link ke artifact diagram arsitektur, atau repo GitHub yang diupdate untuk Direction B.]**

### 25. File Attachment
*(Jika memilih upload file: PDF maksimal 5MB, penamaan "P0804 - GaskeunKerja for Business.pdf")*

### 26. CV / Profil LinkedIn Ketua Tim
**[ISI: link CV/LinkedIn Project Lead]**

### 27. CV / Profil LinkedIn Anggota Tim 1, 2, 3
**[ISI: link CV/LinkedIn masing-masing anggota, jika ada]**

---

## Catatan untuk Tim (hapus sebelum submit)

**Update (2026-07-17):** Q12–Q18 direvisi berdasarkan `final/backup knowledge - tahap 2 vs tahap 3 dan panduan jawaban.md`, menyinkronkan jawaban dengan realita implementasi MVP lokal yang sudah selesai per 2026-07-15 (bukan lagi rencana cloud/KGE yang belum dibangun).

**Update (2026-07-23):** Q6, Q7, Q10, Q12–Q19 direvisi lagi berdasarkan `source knowledge - tahap 2 vs tahap 3 dan panduan jawaban.md` §A.7, karena implementasi berubah signifikan sejak revisi 2026-07-17: **(1) formula matching diganti total** dari "semantic similarity + competency-graph boost (0.7/0.3)" menjadi analisis skill-gap-grounded (coverage 90% + quality 10%) — Qdrant/embeddings kini vestigial, tidak lagi dipakai jalur scoring live; **(2) interview kini berbasis video**, bukan audio saja, dengan langkah uji kamera/mikrofon terpisah; **(3) delivery laporan kembali ke email (Gmail SMTP)** setelah sempat memakai Telegram — keputusan dan laporan kini digabung dalam satu email; **(4) skill-gap analysis kini dipersist** (bukan lagi item pending — item pending di Q14 diganti dengan gap QA folder-drop CV ingestion yang lebih akurat); **(5) angka struktur kode diperbarui** (18 tabel, 12 router, 32 service, 16 halaman). Lihat dokumen source knowledge §A.7 untuk tabel delta lengkap dan rasional tiap perubahan.

**⚠️ BELUM BISA DIJAWAB / PERLU DIISI MANUAL OLEH TIM — butuh konteks yang tidak tersedia di dokumentasi proyek:**
- **Q6, Q19** — nama anggota tim menggantikan placeholder [Nama 1-4]. Tidak ada di dokumentasi manapun; harus diisi langsung oleh tim.
- **Q23** — link YouTube Elevator Pitch (unlisted). Video belum direkam.
- **Q24** — link attachment publik (demo/screenshot/file). Kandidat kuat sekarang: repo GitHub yang sudah menunjukkan implementasi nyata (18 tabel, 12 router, 16 halaman berjalan) — tapi link repo spesifik dan status publik/private-nya perlu dikonfirmasi tim.
- **Q25** — file attachment PDF (jika dipilih sebagai alternatif Q24) — belum dibuat.
- **Q26, Q27** — link CV/LinkedIn Ketua Tim dan Anggota 1-3. Tidak tersedia di dokumentasi manapun.
- **Q3** — "GaskeunKerja for Business" adalah usulan judul; perlu konfirmasi apakah tim setuju atau punya preferensi lain.

**Klaim yang masih butuh keputusan/verifikasi tim (bukan blocker teknis, tapi keputusan bisnis/redaksional):**
- Angka ROI di Q21 (time-to-hire −30–40%, screening −50%, interview-to-hire +20–25%) tetap berbasis estimasi Tahap 2 + literatur, bukan hasil pilot riil — draft sudah mengakui ini jujur. Tim perlu memutuskan apakah ingin melunakkan/memperkuat klaim ini.
- Q9: evidence masih dari laporan sekunder (ManpowerGroup, BPS, WEF) — belum ada wawancara HR langsung. Tidak bisa diperbaiki dari dokumentasi yang ada; butuh riset primer nyata (percakapan dengan HR/SME) yang belum dilakukan.
- Estimasi biaya cloud produksi (Q21: $170-370/bulan) mengacu ke `new idea/infra comparison A vs B.md` — perlu verifikasi terhadap harga API/cloud terkini sebelum dikutip final ke publik (harga bisa berubah sejak analisis dibuat).
- Tanggal deadline submission (~2026-07-26) disebut "verify" di beberapa dokumen sumber — pastikan tanggal & jam pasti dari portal kompetisi.
