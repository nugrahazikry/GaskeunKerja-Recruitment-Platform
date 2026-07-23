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

*(Dipertahankan dari Tahap 2 — ketiganya tetap relevan, kini diwariskan ke persona perusahaan/employer. Lihat pemetaan masalah di `plan.md` §4b.)*

---

### 6. Final Team Composition *(maks. 100 kata)*

Tim Keprof Reborn beroperasi dengan empat anggota aktif: **[Nama 1]** sebagai Project Lead yang mengarahkan strategi produk dan riset pasar; **[Nama 2]** sebagai AI/ML Engineer yang mengembangkan pipeline Deepseek V4, Knowledge Graph Embeddings, dan modul AI Interview; **[Nama 3]** sebagai Backend Engineer yang membangun REST API Gateway, integrasi Cloud Run, BigQuery, dan GCS; serta **[Nama 4]** sebagai Frontend & Product Engineer yang merancang dashboard HR dan portal kandidat. Seluruh anggota terlibat aktif sejak submission pertama dan turut merumuskan pivot strategi ke company-focus pada Tahap 3.

*(~90 kata — ganti [Nama 1-4] dengan nama anggota tim yang sebenarnya.)*

---

### 7. Final Solution Summary *(maks. 150 kata)*

GaskeunKerja for Business adalah platform rekrutmen berbasis AI yang membantu perusahaan skala kecil-menengah menemukan, menilai, dan mengembangkan kandidat secara lebih akurat dan efisien. Perusahaan cukup mengunggah deskripsi pekerjaan; sistem kami mem-parsing CV kandidat, menghitung matching score kontekstual menggunakan Knowledge Graph Embeddings, lalu menjalankan AI Interview asinkron berbasis pertanyaan yang dihasilkan dari kebutuhan lowongan. Setiap jawaban dinilai menggunakan rubrik transparan, dirangkum untuk HR, namun keputusan akhir selalu berada di tangan manusia. Setiap kandidat, baik lolos maupun tidak, menerima laporan pengembangan kompetensi personal melalui email. Solusi ini menggantikan pipeline scraping lowongan yang rentan secara hukum dengan input langsung dari perusahaan, menghasilkan infrastruktur yang lebih ringan, model bisnis B2B yang lebih jelas ROI-nya, serta tetap memberi nilai nyata bagi jobseeker.

*(~140 kata)*

---

### 8. Progress and Change Log *(maks. 150 kata)*

Sejak submission kedua, tim melakukan evaluasi menyeluruh terhadap kelayakan arah jobseeker-focus dan menemukan empat kendala signifikan: sumber data lowongan (scraping) yang rapuh secara teknis dan berisiko hukum, learning roadmap yang tidak konsisten dan sulit diukur, kebutuhan infrastruktur berat untuk ribuan pengguna, serta model freemium dengan ROI lemah. Berdasarkan temuan ini, tim melakukan pivot terarah ke company-focus: pipeline scraping dihapus dan digantikan input JD langsung dari perusahaan, learning roadmap dirombak menjadi hybrid competency framework dengan resource database terkurasi agar deterministik dan terukur, serta ditambahkan modul AI Interview berbasis rubrik dengan human-in-the-loop. Seluruh empat masalah inti Tahap 2 tetap relevan dan diwariskan ke persona perusahaan, sehingga pivot ini merupakan evolusi strategi, bukan awal baru.

*(~135 kata)*

---

### 9. Validated User Problem and Evidence *(maks. 250 kata)*

Masalah inti yang kami selesaikan adalah inefisiensi rekrutmen akibat skill mismatch yang sulit dideteksi melalui proses seleksi konvensional. Berdasarkan ManpowerGroup Talent Shortage Survey (2024), 46% perusahaan kesulitan menemukan kandidat sesuai kebutuhan, 50% menilai keterampilan teknis pelamar masih level pemula, dan 35% menyebut kemampuan software pelamar belum memadai. Di sisi makro, BPS (2025) mencatat pengangguran Indonesia naik dari 7,28 juta (Februari 2025) menjadi 7,36 juta (November 2025), menunjukkan bahwa lapangan kerja yang tersedia tidak terserap secara efektif akibat mismatch kompetensi yang tidak transparan bagi kedua pihak. WEF Future of Jobs Report (2023) turut menegaskan bahwa program upskilling jarang terhubung langsung dengan kebutuhan skill aktual dari lowongan, sehingga proses pengembangan kandidat tidak terarah. Perusahaan skala kecil-menengah particularly kesulitan karena tidak memiliki tim rekrutmen sebesar korporasi besar untuk melakukan screening manual yang mendalam terhadap setiap pelamar. Kami mengakui bahwa validasi kami saat ini masih bersumber dari data sekunder (laporan industri), belum dari wawancara langsung dengan HR; ini menjadi prioritas riset lanjutan dalam dua minggu ke depan melalui percakapan pilot dengan 3-5 perusahaan SME sebagai bukti awal sebelum dan selama pengembangan MVP.

*(~210 kata)*

---

### 10. End-to-End Use Case and Feature-to-Pain Mapping *(maks. 300 kata)*

Alur penggunaan dimulai ketika HR mengunggah deskripsi pekerjaan (JD) ke dashboard GaskeunKerja for Business, menggantikan proses posting lowongan konvensional yang memakan waktu. Deepseek V4 Flash merangkum kompetensi yang dibutuhkan dari JD, sekaligus mem-parsing CV kandidat yang melamar atau diunggah HR. Knowledge Graph Embeddings kemudian menghitung matching score kontekstual antara kandidat dan JD, menghasilkan ranking kandidat teratas — ini menjawab pain point rekrutmen konvensional yang masih bergantung pada keyword matching sederhana. Kandidat dengan skor tertinggi diundang mengikuti AI Interview asinkron: sistem menghasilkan pertanyaan dari JD (misalnya "Jelaskan proses A dalam satu menit"), merekam jawaban kandidat, mentranskripsi, lalu menilai berdasarkan rubrik tetap menggunakan Deepseek V4 Pro. Skor dan ringkasan dikirim ke dashboard HR sebagai bahan keputusan — bukan keputusan otomatis, sehingga HR tetap memiliki kontrol penuh dan risiko bias algoritmik diminimalkan. HR dapat langsung melihat shortlist kandidat beserta skill gap masing-masing untuk kebutuhan interview lanjutan atau onboarding. Setelah proses seleksi selesai, seluruh kandidat—baik yang lolos maupun tidak—menerima laporan pengembangan kompetensi personal melalui email, berisi area yang perlu ditingkatkan dan rekomendasi pembelajaran terstruktur dari resource database terkurasi. Fitur ini secara langsung menjawab keluhan umum jobseeker bahwa feedback lamaran kerja hampir tidak pernah tersedia. Dengan demikian, satu alur end-to-end ini menghubungkan empat pain point utama: mismatch kompetensi, inefisiensi rekrutmen manual, minimnya transparansi skill gap, dan terputusnya pembelajaran dari kebutuhan industri riil.

*(~270 kata)*

---

### 11. Operational Context, Solution Boundary, and Adoption *(maks. 200 kata)*

GaskeunKerja for Business digunakan pada tahap screening dan interview awal proses rekrutmen, ketika perusahaan memiliki satu atau lebih lowongan terbuka dan menerima volume pelamar yang menyulitkan screening manual. Target utama adalah perusahaan skala kecil-menengah (SME) di Indonesia yang belum mampu berlangganan platform ATS enterprise seperti HireVue. Solusi ini memiliki batas jelas: sistem tidak menggantikan keputusan akhir rekrutmen, melainkan berperan sebagai alat bantu keputusan (decision-support) — HR selalu menjadi pengambil keputusan akhir atas hasil AI Interview. Sistem juga tidak menangani proses pasca-rekrutmen seperti kontrak kerja, payroll, atau administrasi HR lainnya; fokus tetap pada matching, skill-gap analysis, dan interview awal. Adopsi dirancang menyerupai alur rekrutmen digital yang sudah familiar (posting lowongan, menerima shortlist, mengelola kandidat), sehingga tidak memerlukan pelatihan teknis tambahan bagi HR. Kandidat mengakses AI Interview melalui tautan web tanpa instalasi. Persetujuan eksplisit (consent checkbox) diminta dari kandidat sebelum data interview diproses, sesuai UU PDP.

*(~185 kata)*

---

### 12. Innovation Level

Tingkat inovasi solusi saat ini berada pada tahap **MVP fungsional end-to-end, terverifikasi berjalan secara lokal**: seluruh lima area eksekusi (tooling AI, database, backend & AI pipeline, frontend, QA) telah selesai dan diverifikasi lewat panggilan API, query database, dan permintaan HTTP nyata — bukan sekadar kode tertulis. Modul AI Interview, komponen paling baru dan berisiko tinggi (rekam audio, transkripsi, rubric scoring), sudah diverifikasi end-to-end termasuk pengiriman laporan nyata ke kandidat. Yang membedakan solusi ini bukan algoritma baru, melainkan integrasi baru: matching, skill-gap, AI Interview, dan laporan pengembangan kandidat dalam satu alur tertutup yang terlokalisasi untuk SME Indonesia — termasuk fitur bahwa kandidat yang ditolak pun tetap menerima laporan pengembangan, sesuatu yang jarang ditemukan pada platform sejenis. Bukti pendukung (arsitektur sistem, demo alur, dan dokumentasi teknis) dilampirkan pada bagian Link/File Attachment.

---

### 13. Current Technical Reality, Data, and Integration *(maks. 300 kata)*

Solusi ini sudah berupa MVP yang berjalan penuh secara lokal dan terverifikasi end-to-end, bukan sekadar rencana. Parsing CV menggunakan Deepseek V4 Flash (via SumoPod) sudah berfungsi akurat, termasuk fallback vision-LLM untuk halaman CV hasil scan dan redaksi PII (nama/email/telepon) sebelum data mencapai LLM. Backend FastAPI dan database PostgreSQL (17 tabel, berjalan via Docker) sudah dibangun dan diverifikasi lewat query nyata, begitu pula frontend React yang sudah tersambung ke API sungguhan. Matching kandidat-JD menggunakan semantic vector similarity (Qdrant, cosine) dikombinasikan dengan competency-graph boost (formula 0.7:0.3) — pendekatan yang lebih ringan dari rencana Knowledge Graph Embeddings penuh di Tahap 2, karena prototipe KGE sebelumnya tidak pernah terintegrasi ke produksi; pendekatan baru ini tetap explainable dan terbukti mendiskriminasi kandidat kuat/sedang/lemah secara statistik pada pengujian internal. Pipeline scraping lowongan resmi dihapus; data lowongan kini bersumber langsung dari input JD terstruktur perusahaan. Modul AI Interview (rekam audio, speech-to-text via Groq Whisper Bahasa Indonesia, rubric scoring dengan Deepseek V4 Pro) sudah dibangun dan diverifikasi berjalan end-to-end, termasuk pengiriman laporan pengembangan kandidat via Telegram yang terkonfirmasi diterima. MVP berjalan 100% lokal (Docker Compose: PostgreSQL + Qdrant, filesystem untuk CV/audio) — ini keputusan kecepatan-build yang disengaja untuk jendela hackathon, bukan pekerjaan tertunda; migrasi ke Cloud Run/BigQuery/GCS direncanakan pada fase pilot produksi, dengan jenis layanan cloud yang identik antara evolusi Tahap 2 dan Tahap 3. Data yang dikelola: JD perusahaan, CV kandidat, hasil ekstraksi kompetensi dan skor matching, embedding vektor, serta rekaman dan transkrip interview (dengan consent eksplisit). Sistem tetap bergantung pada kapabilitas LLM yang berpotensi berhalusinasi pada kasus tepi; mitigasi utamanya rubrik tetap dan human-in-the-loop, diperkuat self-consistency voting untuk menjaga determinisme skor.

*(~290 kata)*

---

### 14. MVP Execution and Deployment Plan *(maks. 250 kata)*

Eksekusi MVP telah selesai dijalankan menjelang deadline Tahap 3, dibagi ke lima area kerja berurutan selama sekitar 13 hari efektif. **Fondasi (tooling AI & dev environment):** klien LLM (Deepseek V4 via SumoPod), speech-to-text (Groq Whisper), vision-LLM untuk CV scan, dan bot Telegram — seluruhnya diverifikasi dengan panggilan API nyata. **Database & reference dataset:** skema 17 tabel PostgreSQL dan 2 koleksi Qdrant dibangun, termasuk kurasi competency framework dan resource library untuk satu peran demo (Web Developer), lalu 30 kandidat seed diproses lewat pipeline nyata. **Backend & AI pipeline:** JD intake, ekstraksi kompetensi, parsing CV dengan redaksi PII, matching semantic+graph boost, hingga modul AI Interview (rekam audio → transkripsi → rubric scoring) — seluruh endpoint diuji lewat request HTTP sungguhan. **Frontend:** sembilan halaman React tersambung ke API nyata, termasuk komponen perekam audio yang menjadi bagian berisiko tertinggi. **QA:** pengujian determinisme skor, redaksi PII, diskriminasi matching pada data kandidat berjenjang (kuat/sedang/lemah), hingga tujuh skenario end-to-end yang diamati langsung di browser — proses ini menemukan dan memperbaiki beberapa celah nyata sebelum submission, termasuk memastikan skor rubrik benar-benar konsisten dan laporan pengembangan benar-benar terkirim ke Telegram kandidat. Saat ini MVP berjalan lokal (Docker Compose); satu item follow-up teknis yang belum dikerjakan adalah menyimpan hasil analisis skill-gap agar tidak dihitung ulang setiap kali halaman dibuka. Pasca-hackathon, target berikutnya adalah pilot dengan 3-5 perusahaan SME nyata dalam 1-2 bulan untuk memvalidasi asumsi ROI dengan data riil, sekaligus memulai migrasi bertahap ke infrastruktur cloud produksi (Cloud Run, BigQuery, GCS) sebelum ekspansi ke skala 50+ klien.

*(~250 kata)*

---

### 15. Problem and System Complexity *(maks. 200 kata)*

Masalah ini tidak dapat diselesaikan dengan cara sederhana karena kecocokan kompetensi bersifat kontekstual dan multidimensi — dua kandidat dengan kata kunci CV yang sama dapat memiliki kedalaman kompetensi sangat berbeda, sesuatu yang tidak tertangkap oleh keyword matching atau filter Boolean sederhana pada ATS konvensional. Sistem kami menggunakan semantic vector embeddings yang dikombinasikan dengan graph relasional antar kompetensi (competency-graph boost) untuk menghitung kedekatan makna, bukan sekadar kecocokan istilah — dan tetap explainable karena setiap skor dapat dirunut ke kompetensi spesifik yang cocok atau tidak. Penilaian interview menambah lapisan kompleksitas lain: jawaban kandidat berbentuk audio tidak terstruktur harus ditranskripsi, dinilai secara konsisten terhadap rubrik tetap, dan dirangkum agar dapat ditindaklanjuti HR — sebuah proses reasoning yang memerlukan LLM tingkat lanjut (Deepseek V4 Pro), bukan aturan if-else statis. Konsistensi skor sendiri ternyata bukan hal sepele: pengujian internal menemukan bahwa temperature=0 saja tidak cukup menjamin determinisme di level provider LLM, sehingga sistem menerapkan self-consistency voting (beberapa panggilan independen, diambil median/mayoritas) untuk menjamin skor yang sama pada input yang sama. Kompleksitas sistem juga muncul dari kebutuhan menjaga proses tetap explainable dan bebas bias, sehingga desain human-in-the-loop dan rubrik transparan menjadi bagian tak terpisahkan dari arsitektur, bukan sekadar fitur tambahan.

*(~195 kata)*

---

### 16. Processing Pipeline and Engineering Depth *(maks. 250 kata)*

Pipeline pemrosesan dimulai saat HR login (JWT) dan membuat JD lewat frontend React, diteruskan ke backend FastAPI yang mengorkestrasi alur secara asinkron. Deepseek V4 Flash (via SumoPod) mengekstrak kompetensi dari JD. CV kandidat diunggah, teksnya diekstrak (pypdf), halaman hasil scan dideteksi dan dilewatkan ke vision-LLM untuk transkripsi, seluruh teks di-redaksi PII (nama/email/telepon dihapus) sebelum dikirim ke Deepseek V4 Flash untuk parsing menjadi data terstruktur (skill, pengalaman, kualifikasi) — disimpan di PostgreSQL, dokumen asli di filesystem lokal. Profil kandidat dan kompetensi JD diubah menjadi vektor embedding dan disimpan di Qdrant; skor matching dihitung dari kombinasi semantic similarity dan competency-graph boost, menghasilkan ranking kandidat yang explainable. HR meninjau shortlist, mengedit/menyetujui pertanyaan interview yang dihasilkan AI (human-in-the-loop di tahap ini juga, bukan hanya di keputusan akhir), lalu mengundang kandidat lewat token link. Kandidat merekam jawaban audio, ditranskripsi oleh Groq Whisper (Bahasa Indonesia), lalu Deepseek V4 Pro menilai transkrip terhadap rubrik tetap menggunakan self-consistency voting (beberapa panggilan independen untuk menjamin skor konsisten) dan menghasilkan ringkasan. Skor dan ringkasan ditampilkan di dashboard HR sebagai bahan keputusan manusia. Setelah keputusan diambil, sistem menyusun development report dari competency framework dan resource library terkurasi, dirender jadi PDF, lalu dikirim otomatis via Telegram Bot ke seluruh kandidat — lolos maupun tidak. Saat ini seluruh proses berjalan lokal (Docker Compose); migrasi ke layanan container cloud terkelola direncanakan pada fase pilot produksi.

*(~245 kata)*

---

### 17. Algorithm or Rule Quality and Decision Transparency *(maks. 300 kata)*

Kualitas keputusan sistem dijaga melalui dua mekanisme utama: matching yang explainable dan rubric scoring yang transparan dan diverifikasi konsisten. Pada tahap matching, skor dihitung dari kombinasi semantic similarity dan competency-graph boost antar kompetensi, sehingga setiap skor dapat ditelusuri ke kompetensi spesifik yang cocok atau tidak cocok — HR dapat melihat rincian ini, bukan hanya angka akhir; pada pengujian internal dengan kandidat berjenjang (kuat/sedang/lemah), sistem terbukti mendiskriminasi kualitas kandidat secara konsisten. Pada tahap AI Interview, penilaian jawaban kandidat menggunakan rubrik tetap dengan kriteria dan level penilaian yang telah didefinisikan sebelumnya (kejelasan penjelasan, relevansi terhadap pertanyaan, kedalaman teknis), bukan skor bebas yang dihasilkan LLM tanpa struktur. Determinisme skor sempat menjadi temuan penting saat pengujian: temperature=0 saja ternyata belum cukup menjamin hasil identik pada input yang sama, karena perilaku serving LLM di level provider. Sistem karenanya menerapkan self-consistency voting — beberapa panggilan independen per penilaian, hasil akhir diambil dari median (skor rubrik) atau mayoritas (kompetensi skill-gap) — yang setelah diverifikasi menghasilkan nol variasi pada pengujian berulang. Yang terpenting, sistem dirancang dengan prinsip "assist, never decide": AI tidak pernah menolak kandidat secara otomatis. Setiap skor dan ringkasan interview hanya berfungsi sebagai rekomendasi kepada HR, yang selalu menjadi pengambil keputusan akhir — hal ini diverifikasi langsung di kode, tidak ada jalur mana pun yang memutuskan kandidat tanpa aksi HR. Desain ini mengurangi risiko bias algoritmik dan tanggung jawab hukum terkait keputusan rekrutmen otomatis, sekaligus menjaga kepercayaan pengguna. Seluruh keputusan AI — mulai dari matching score hingga hasil interview — dicatat ke audit log, mendukung akuntabilitas dan evaluasi berkelanjutan terhadap kualitas rubrik dan model dari waktu ke waktu.

*(~245 kata)*

---

### 18. User Flow, Usability Testing, and Product Iteration *(maks. 250 kata)*

Pengalaman pengguna dirancang menyerupai alur rekrutmen digital yang sudah dikenal HR (posting lowongan, melihat shortlist, mengelola kandidat) agar adopsi tidak memerlukan pelatihan tambahan, sementara kandidat berinteraksi melalui portal sederhana tanpa akun untuk mengisi consent, menjawab pertanyaan interview, dan menerima laporan pengembangan. Pengujian internal telah dilakukan secara ekstensif, bukan sekadar rencana: 30 kandidat seed diproses lewat pipeline nyata untuk simulasi demo, ditambah 6 kandidat uji berjenjang (kuat/sedang/lemah) khusus untuk membuktikan algoritma matching benar-benar mendiskriminasi kualitas kandidat. Tujuh skenario end-to-end diuji secara visual langsung di browser sungguhan — mencakup alur bahagia penuh, jalur yang seharusnya diblokir bagi kandidat maupun HR, jalur kegagalan dan percobaan ulang, hingga penelusuran integritas data lintas tabel. Proses ini menemukan dan langsung memperbaiki tiga celah nyata pada produk: nama kandidat yang sempat lolos tanpa ter-redaksi pada kasus tepi, skor rubrik yang belum sepenuhnya konsisten pada pengulangan, dan satu jalur skor interview yang belum tersambung sepenuhnya ke alur kandidat nyata. Seluruh tujuh kondisi tepi pada demo (izin mikrofon ditolak, submit kosong, token kedaluwarsa, kegagalan pengiriman laporan, dan lainnya) telah diverifikasi berjalan benar, termasuk pengiriman laporan nyata ke Telegram yang dikonfirmasi diterima. Kami secara jujur mengakui bahwa pengujian di atas seluruhnya bersifat internal (tim sendiri dan data simulasi) — validasi dengan pengguna eksternal riil (HR sungguhan) belum dilakukan dan menjadi prioritas pada fase pilot pasca-hackathon bersama 3-5 perusahaan SME.

*(~230 kata)*

---

### 19. Team Capability and Execution Ownership *(maks. 250 kata)*

Tim Keprof Reborn memiliki kompetensi yang saling melengkapi untuk mengeksekusi pivot ini. **[Nama 1]** (Project Lead) mengarahkan strategi produk, riset problem-solution fit, dan penyusunan proposal, serta memimpin proses evaluasi yang menghasilkan keputusan pivot ke company-focus berdasarkan analisis kelayakan teknis dan bisnis. **[Nama 2]** (AI/ML Engineer) bertanggung jawab penuh atas pipeline Deepseek V4, Knowledge Graph Embeddings, dan pengembangan AI Interview Module termasuk desain rubric scoring. **[Nama 3]** (Backend Engineer) memiliki ownership atas REST API Gateway, migrasi infrastruktur dari GKE ke Cloud Run, integrasi BigQuery/GCS/Qdrant, serta keamanan sistem sesuai UU PDP. **[Nama 4]** (Frontend & Product Engineer) bertanggung jawab atas dashboard HR, portal kandidat, dan alur consent, sekaligus mengumpulkan feedback usability. Pembagian tanggung jawab ini konsisten dengan struktur yang telah berjalan sejak submission pertama, sehingga transisi ke arsitektur Direction B dapat dieksekusi tanpa perlu membentuk ulang tim atau mempelajari stack teknologi baru — seluruh anggota telah familiar dengan Deepseek V4, FastAPI, GCP, dan React.js dari pengembangan Tahap 1-2.

*(~180 kata — ganti [Nama 1-4], konsisten dengan Q6.)*

---

### 20. Continuation Readiness *(maks. 200 kata)*

Pasca-hackathon, tim berencana melanjutkan pengembangan melalui tiga langkah utama. Pertama, menjalankan pilot dengan 3-5 perusahaan SME dalam 1-2 bulan untuk memvalidasi asumsi ROI (pengurangan waktu screening dan time-to-hire) dengan data riil, menggantikan estimasi dari laporan sekunder yang digunakan saat ini. Kedua, memperkuat modul AI Interview berdasarkan feedback pilot, termasuk penyempurnaan rubrik penilaian dan cakupan jenis pertanyaan per industri. Ketiga, mencari pendanaan lanjutan melalui kombinasi hasil hackathon, program inkubasi startup, serta pendapatan awal dari subscription B2B perusahaan pilot untuk menutup biaya infrastruktur (~$170-370/bulan pada skala awal). Tim juga akan menjajaki kemitraan dengan asosiasi UMKM/SME dan komunitas HR Indonesia sebagai saluran distribusi awal, mengikuti pendekatan networking organik yang telah terbukti relevan sejak Tahap 2. Roadmap jangka menengah mencakup ekspansi ke 50-100 klien berbayar dalam 6-24 bulan, didukung oleh data flywheel dari setiap interview yang memperkaya kualitas rubrik dan matching dari waktu ke waktu.

*(~165 kata)*

---

### 21. Quantified Value, Business Model, and ROI *(maks. 300 kata)*

Model bisnis GaskeunKerja for Business adalah B2B subscription dengan opsi per-seat atau per-hire, menggantikan model freemium jobseeker yang sebelumnya sulit dikonversi menjadi revenue. Target awal adalah 5-15 perusahaan SME pilot dalam 6 bulan pertama, tumbuh menjadi 50-100 klien berbayar dalam 6-24 bulan, dan 500-1.000 perusahaan dalam 2-5 tahun. Nilai yang ditawarkan terukur secara langsung: target pengurangan waktu rekrutmen (time-to-hire) sebesar 30-40% — diwariskan dari estimasi Tahap 2 dan kini menjadi metrik utama, bukan sekunder — pengurangan waktu screening hingga 50% melalui otomatisasi AI Interview, serta peningkatan interview-to-hire rate sebesar 20-25% karena kandidat yang lolos ke tahap interview manusia telah melalui pra-seleksi yang lebih akurat. Dari sisi biaya, arsitektur Direction B jauh lebih efisien: estimasi infrastruktur cloud (GCP) berkisar $170-370 per bulan pada skala di bawah 50 klien — sekitar 4-6 kali lebih murah dibanding arsitektur jobseeker-focus (~$800-1.750/bulan) yang membutuhkan Kubernetes cluster penuh dan pipeline scraping harian. Karena biaya infrastruktur berskala kecil sementara setiap klien membayar langsung, ROI investasi menjadi lebih cepat tercapai dibanding model freemium jobseeker yang bergantung pada konversi pengguna gratis ke berbayar dalam jumlah besar. Kami secara jujur mencatat bahwa angka efisiensi rekrutmen di atas merupakan target berbasis estimasi Tahap 2 dan literatur industri, yang akan divalidasi lebih lanjut melalui pilot nyata sebelum dijadikan klaim final kepada investor.

*(~225 kata)*

---

### 22. Adoption, Growth Strategy, and Competitive Moat *(maks. 250 kata)*

Strategi adopsi dimulai dari segmen yang kurang terlayani: perusahaan SME Indonesia yang membutuhkan bantuan rekrutmen namun tidak mampu berlangganan platform enterprise seperti HireVue atau ATS global. Distribusi awal memanfaatkan jaringan komunitas HR, asosiasi UMKM, dan kemitraan kampus (sebagai sumber talent pool kandidat), mengikuti pendekatan networking organik berbiaya rendah yang telah terbukti relevan sejak Tahap 2. Fitur development report yang dikirimkan ke seluruh kandidat — baik lolos maupun tidak — menjadi nilai tambah employer branding bagi perusahaan klien, sekaligus mendorong word-of-mouth positif dari kandidat yang merasa dihargai meski tidak diterima. Competitive moat kami bukan satu fitur tunggal yang mudah ditiru, melainkan integrasi penuh matching, skill-gap analysis, AI Interview, dan development report dalam satu alur — sementara kompetitor seperti platform ATS global maupun job portal umumnya menyediakan fitur-fitur ini secara terpisah atau tidak sama sekali untuk segmen SME. Moat ini diperkuat oleh data flywheel: semakin banyak interview yang diproses, semakin kaya data kompetensi dan hasil rubrik yang memperbaiki akurasi matching dan kualitas pertanyaan interview secara khusus untuk konteks pasar kerja Indonesia — sesuatu yang tidak dimiliki pemain global generik.

*(~200 kata)*

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

**Update:** Q12–Q18 telah direvisi (2026-07-17) berdasarkan `final/backup knowledge - tahap 2 vs tahap 3 dan panduan jawaban.md`, menyinkronkan jawaban dengan realita implementasi MVP lokal yang sudah selesai per 2026-07-15 (bukan lagi rencana cloud/KGE yang belum dibangun). Lihat dokumen backup knowledge tersebut untuk rasional lengkap tiap perubahan dan sumber rujukannya.

**⚠️ BELUM BISA DIJAWAB / PERLU DIISI MANUAL OLEH TIM — butuh konteks yang tidak tersedia di dokumentasi proyek:**
- **Q6, Q19** — nama anggota tim menggantikan placeholder [Nama 1-4]. Tidak ada di dokumentasi manapun; harus diisi langsung oleh tim.
- **Q23** — link YouTube Elevator Pitch (unlisted). Video belum direkam.
- **Q24** — link attachment publik (demo/screenshot/file). Kandidat kuat sekarang: repo GitHub yang sudah menunjukkan implementasi nyata (17 tabel, 9 router, 9 halaman berjalan) — tapi link repo spesifik dan status publik/private-nya perlu dikonfirmasi tim.
- **Q25** — file attachment PDF (jika dipilih sebagai alternatif Q24) — belum dibuat.
- **Q26, Q27** — link CV/LinkedIn Ketua Tim dan Anggota 1-3. Tidak tersedia di dokumentasi manapun.
- **Q3** — "GaskeunKerja for Business" adalah usulan judul; perlu konfirmasi apakah tim setuju atau punya preferensi lain.

**Klaim yang masih butuh keputusan/verifikasi tim (bukan blocker teknis, tapi keputusan bisnis/redaksional):**
- Angka ROI di Q21 (time-to-hire −30–40%, screening −50%, interview-to-hire +20–25%) tetap berbasis estimasi Tahap 2 + literatur, bukan hasil pilot riil — draft sudah mengakui ini jujur. Tim perlu memutuskan apakah ingin melunakkan/memperkuat klaim ini.
- Q9: evidence masih dari laporan sekunder (ManpowerGroup, BPS, WEF) — belum ada wawancara HR langsung. Tidak bisa diperbaiki dari dokumentasi yang ada; butuh riset primer nyata (percakapan dengan HR/SME) yang belum dilakukan.
- Estimasi biaya cloud produksi (Q21: $170-370/bulan) mengacu ke `new idea/infra comparison A vs B.md` — perlu verifikasi terhadap harga API/cloud terkini sebelum dikutip final ke publik (harga bisa berubah sejak analisis dibuat).
- Tanggal deadline submission (~2026-07-26) disebut "verify" di beberapa dokumen sumber — pastikan tanggal & jam pasti dari portal kompetisi.
