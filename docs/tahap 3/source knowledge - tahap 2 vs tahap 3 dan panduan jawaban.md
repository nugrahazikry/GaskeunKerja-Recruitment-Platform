# Backup Knowledge — Perbedaan Tahap 2 vs Tahap 3 & Panduan Menjawab `tahap 3 jawaban.md`

> **Tujuan dokumen ini:** referensi tunggal, sangat rinci, untuk mendukung tim mengisi/memverifikasi/mempertahankan jawaban di `tahap 3 jawaban.md` — baik saat finalisasi teks sebelum submit, maupun saat menjawab pertanyaan lisan judge. Setiap klaim di sini merujuk ke file sumber yang bisa dibuka ulang untuk verifikasi. **Dokumen ini tidak mengubah `tahap 3 jawaban.md`** — murni referensi pendukung.
>
> **Status per penyusunan dokumen ini:** implementasi MVP sudah **selesai** untuk kelima area eksekusi (Tooling, Database, Backend & AI, Frontend, QA) per tanggal terakhir tercatat 2026-07-15, termasuk QA end-to-end visible-browser testing (7 skenario) dan demo-readiness checklist (7/7 edge case). Satu item teknis non-blocking masih tertunda: persist hasil skill-gap analysis agar tidak dihitung ulang tiap kali halaman dibuka (dicatat di `execution-checklist.md` baris ~1358, belum dikerjakan per 2026-07-16+). **Draft `tahap 3 jawaban.md` ditulis lebih awal (sebelum status ini tercapai) sehingga sejumlah jawaban masih membingkai arsitektur sebagai rencana cloud, bukan realita lokal yang sudah terverifikasi.**
>
> **⚠️ Update 2026-07-23 (Round 2 & Round 3, terverifikasi langsung dari kode, bukan asumsi dari status di atas):** signifikan lebih banyak dibangun sejak 2026-07-15/16, termasuk **satu perubahan yang membalik klaim algoritma paling penting di dokumen ini** (formula matching, lihat A.5.1) dan **satu pembalikan keputusan tooling** (Telegram → Gmail SMTP, lihat A.5). Item "belum selesai" di atas (persist skill-gap) **sudah selesai** (2026-07-17/19). **Lihat BAGIAN A.7 (baru) untuk ringkasan lengkap delta ini sebelum memakai bagian manapun di dokumen ini untuk jawab judge** — beberapa baris di Bagian B (terutama Q13, Q15, Q16, Q17) dan di Bagian C sekarang mengandung klaim yang sudah tidak akurat dan ditandai `[SUPERSEDED 2026-07-23]` di tempatnya masing-masing.

---

## Daftar Sumber Rujukan

| Kode | File | Isi |
|---|---|---|
| **T2** | `Tahap 2/tahap 2 proposal.md` | Proposal Tahap 2 lengkap (27 slide) |
| **PLAN** | `brainstorming idea/plan.md` | Log keputusan pivot Direction B (Stage 1-4) |
| **DBS** | `.../progress idea/direction B summary.md` | Blueprint arsitektur Direction B (versi cloud, sebelum implementasi) |
| **CMP** | `.../progress idea/perbandingan tahap 2 vs tahap 3.md` | Slide deck perbandingan (presentasi) |
| **BVI** | `.../progress idea/tahap 3 proposal update (blueprint + implementation).md` | Reconciliation blueprint vs kode nyata (per 2026-07-13) |
| **INFRA** | `.../progress idea/new idea/infra comparison A vs B.md` | Rincian biaya cloud A vs B |
| **PANDUAN** | `Tahap 3/proposal/tahap 3 proposal.md` | Panduan resmi 27 pertanyaan + batas kata |
| **JAWABAN** | `.../final/tahap 3 jawaban.md` | Draft jawaban final saat ini |
| **IMPL-CLAUDE** | `implementation/CLAUDE.md` | Constraint local-only + audit kode Tahap 2 |
| **CHECKLIST** | `implementation/planning/execution-checklist.md` | Status implementasi granular per task |

---

# BAGIAN A — Perbedaan Tahap 2 vs Tahap 3 (Rinci)

## A.1 Ringkasan Pivot

Tahap 2 → Tahap 3 **bukan** pivot 180°. Masalah inti (skill mismatch pasar kerja Indonesia) tetap sama. Yang berubah: **siapa yang dilayani lebih dulu, dan bagaimana caranya** (CMP baris 26).

Keputusan dikunci **2026-07-12** (PLAN baris 3, 146): Direction B (company-focused) dipilih dari 3 kandidat arah (A-Jobseeker, B-Company, C-Kombinasi; C dicoret karena nilai uniknya—manfaat dua sisi—sudah tercakup murah lewat laporan email/Telegram ke kandidat versi B, tanpa beban infra dua sisi).

**4 downside konkret Direction A yang memicu pivot** (PLAN baris 15-19):
1. Sumber data lowongan rapuh — API resmi job portal sulit didapat.
2. Scraping tidak stabil + berisiko hukum — scraper rusak tiap kali struktur situs berubah, dan scraping lintas beberapa job portal berpotensi ilegal.
3. Learning plan lemah — AI-generated, non-deterministik (hasil beda tiap dijalankan ulang), terlalu simpel, susah diukur.
4. Infra berat + ROI buruk — melayani 1.000–10.000+ jobseeker butuh spek cloud besar sejak awal; model freemium sulit dimonetisasi.

**5 rationale Direction B** (PLAN baris 25-30): tidak perlu scraping (perusahaan input JD langsung); skill-gap + learning plan dipertahankan + ditambah AI Interview; infra ringan (<50 klien B2B, bukan ribuan konsumen); ROI lebih jelas (B2B berbayar vs freemium sulit konversi); syarat kontinuitas — 4 masalah Tahap 2 tetap diwariskan, hanya dibingkai ulang untuk persona perusahaan.

## A.2 Tabel Perbedaan Menyeluruh

| Aspek | Tahap 2 | Tahap 3 (Direction B) | Sumber |
|---|---|---|---|
| Target user utama | Jobseeker (individu) | Perusahaan/HR/Recruiter (B2B) | CMP baris 34 |
| Model bisnis | Freemium B2C | Subscription B2B (per-seat/per-hire) | CMP baris 35 |
| Titik masuk data lowongan | Scraping (SERP API, LinkedIn/Glassdoor) | Input JD langsung oleh HR (CRUD terstruktur) | CMP baris 36 |
| Nilai ke jobseeker | Rekomendasi lowongan + roadmap belajar | Laporan pengembangan kompetensi personal (tetap dapat, walau bukan user utama) | CMP baris 37 |
| Skala 0–6 bulan | 500–1.000 pengguna aktif | 5–15 perusahaan pilot | CMP baris 47 |
| Skala 6–24 bulan | 10.000–50.000 pengguna | 50–100 klien berbayar | CMP baris 48 |
| Skala 2–5 tahun | 500.000+ pengguna terdaftar | 500–1.000 perusahaan | CMP baris 49 |
| Fitur baru | — | Modul AI Interview (rekam audio → STT → skor rubrik) | PLAN baris 60, CMP baris 78 |
| Fitur dihapus | — | Pipeline scraping (dihapus total dari arsitektur) | DBS baris 56 |

### A.2.1 Perbandingan komponen arsitektur (blueprint Direction B vs Tahap 2 — DBS §3, 12 baris)

| # | Komponen | Tahap 2 | Direction B (blueprint) |
|---|---|---|---|
| 1 | Web Frontend | React.js | 🟢 Dipertahankan — butuh view baru (HR dashboard, portal interview kandidat, consent flow) |
| 2 | API Gateway | FastAPI di GKE | 🆕 FastAPI di **Cloud Run** (serverless) |
| A | Auth Service | JWT | 🟢 Dipertahankan — tambah role company + candidate |
| 3 | Scraping & Aggregation | SERP API/scraping | ❌ **Dihapus total** |
| 3B | Company JD Intake | — | 🆕 Baru — pengganti #3 |
| 4 | LLM ringan | Deepseek V4 Flash | 🟢 Dipertahankan — + generasi pertanyaan interview |
| 5 | LLM reasoning | Deepseek V4 Pro | 🟢 Dipertahankan — + rubric scoring interview |
| 6 | ML Recommendation | Knowledge Graph Embeddings | 🟢 Dipertahankan — **reframe**: ranking kandidat untuk 1 lowongan, bukan lowongan untuk 1 user |
| 7 | Vector DB | Qdrant | 🟢 Dipertahankan — index jauh lebih kecil (<10k vs 100k–500k) |
| 8 | AI Interview Module | — | 🆕 **Satu-satunya komponen rekayasa benar-benar baru** |
| 9 | Tabular DB | BigQuery | 🟢 Dipertahankan — + skor interview |
| 10 | Object Storage | GCS | 🟢 Dipertahankan — + audio interview |
| 11 | Security | TLS/AES/JWT/IAM | 🟢 Dipertahankan — + consent checkbox UU PDP |
| 12 | Infra | GCP GKE | 🆕 GKE → **Cloud Run** |

> **Penting:** tabel di atas adalah **blueprint** (rencana Direction B sebelum dibangun). Realita implementasi menyimpang dari sini — lihat A.5 di bawah untuk versi yang benar-benar dibangun.

## A.3 Pemetaan 4 Masalah Inti Tahap 2 → Direction B

Dari PLAN §4b (baris 76-88) — **semua 4 masalah tetap ada**, direwarisi ke persona perusahaan:

| # | Masalah Tahap 2 | Di Direction B | Verdict |
|---|---|---|---|
| 1 | Mismatch Kompetensi | Perusahaan menerima pelamar yang tidak cocok; engine matching menyaring yang memenuhi syarat | ✅ TETAP — dimiliki ulang oleh employer |
| 2 | Inefisiensi Rekrutmen | Jadi masalah **utama/lead**; AI interview + matching langsung menyerangnya | ✅ TETAP — jadi prioritas utama |
| 3 | Minim Transparansi Skill Gap | Laporan kompetensi per-kandidat untuk HR | ✅ TETAP — dimiliki ulang oleh employer |
| 4 | Disconnect Pembelajaran–Industri | **Direposisi**: laporan pengembangan kandidat (baik lolos maupun tidak) dikirim via email/Telegram | ✅ TETAP — direposisi jadi post-hire dev report + feedback loop kandidat |

**Catatan penting (PLAN baris 88):** karena laporan dikirim ke kandidat yang ditolak, ini = memproses data pribadi → **wajib consent checkbox eksplisit di awal interview**, bukan tambahan di akhir alur.

## A.4 Apa yang Benar-Benar Reusable dari Kode Tahap 2 — KOREKSI PENTING

⚠️ **Audit kode nyata Tahap 2 (2026-07-12, IMPL-CLAUDE baris 52-68) menemukan asumsi awal SALAH.** Jangan klaim "reuse tinggi dari Tahap 2" ke judge tanpa kualifikasi berikut:

| Klaim awal (asumsi sebelum audit) | Fakta setelah membaca kode asli |
|---|---|
| Frontend React.js | ❌ **BUKAN React** — situs statis (`index.html`/`style.css`/`script.js`, nginx, tanpa build tooling), branding "SkillGap AI". Tidak ada kode React untuk dipakai ulang, hanya bahasa visualnya. |
| LLM Deepseek V4 | ❌ **BUKAN Deepseek** — pakai **Google Gemini** (`gemini-2.5-flash-lite` via `langchain_google_genai`). Nol kode Deepseek di repo manapun. |
| Auth "dirancang belum diverifikasi" | ❌ **Terkonfirmasi TIDAK ADA SAMA SEKALI** — tidak ada JWT, tidak ada endpoint login, semua `/api/*` tanpa autentikasi. |
| Database "dirancang belum diverifikasi" | ❌ **Terkonfirmasi TIDAK ADA SAMA SEKALI** — tidak ada ORM/SQLAlchemy, tidak ada Postgres, persistensi hanya dict in-memory (`_JOBS`), hilang saat restart. |
| ⚠️ Catatan keamanan tambahan | `backend/environment.env` di Tahap 2 punya API key Gemini live ter-commit plaintext (perlu dirotasi jika masih aktif) — pola yang sengaja **tidak diulang** di MVP baru. |

**Yang benar-benar reusable (IMPL-CLAUDE baris 59-63) — pattern-reuse, bukan copy-paste kode:**
- **Ekstraksi teks CV** (`pdfplumber` + fallback vision-OCR Gemini untuk halaman scan) — pattern "extract text → deteksi kosong → vision fallback" divalidasi ulang di MVP (provider beda: SumoPod/Groq, bukan Gemini).
- **Pattern grounding skill-gap** (`_build_seed_gap()` / `_is_skill_match()` — seed deterministik berbasis token-overlap untuk membatasi output LLM) — teknik yang diadaptasi, meski teknik matching-nya sendiri (token overlap) tidak dipakai (MVP pakai semantic+graph, lihat A.5).
- **Generate PDF laporan** (`_build_report_pdf()`, ReportLab, ~700 baris) — **berfungsi penuh**, langsung diadaptasi untuk MVP (menghindari risiko dependency Windows dari weasyprint).
- Pola Docker/async minor sebagai referensi, bukan reuse langsung.

**Confirmed TIDAK reusable:** KGE matching (tidak ada sama sekali di kode Tahap 2 — grep "embedding"/"knowledge graph"/"qdrant" nol hasil; matching Tahap 2 sebenarnya token-overlap heuristic sederhana), learning roadmap LLM (fungsional tapi rapuh — regex + `json.loads` tanpa validasi skema, pola yang dihindari bukan ditiru), pipeline scraping (dihapus & memang tidak ada di kode), infra Kubernetes (diganti lokal).

## A.5 Evolusi Kedua: Blueprint Direction B (Cloud) → Implementasi Nyata (Local MVP)

Karena constraint waktu (build solo, ~13 hari efektif) dan keputusan **local-first, no cloud** di awal sesi implementasi (IMPL-CLAUDE baris 9), blueprint Direction B **tidak dibangun sebagai rencana cloud aslinya** — diganti komponen lokal/gratis tanpa mengubah alur/logika inti (BVI §2, tabel baris 30-40):

| Komponen | Blueprint (cloud) | Implementasi nyata (local MVP) | Alasan |
|---|---|---|---|
| Hosting API | Cloud Run | `uvicorn` lokal (Docker Compose untuk finalisasi) | Tidak perlu biaya cloud selama fase build/demo |
| Database tabular | BigQuery | **PostgreSQL 16 (Docker)** via SQLAlchemy | BigQuery perlu setup GCP; Postgres lokal setara untuk skala demo |
| Object storage | GCS | **Filesystem lokal** (`storage/cv/`, `storage/audio/`) | Path pointer di DB, sama seperti desain GCS |
| Vector DB | Qdrant managed | **Qdrant (Docker, self-hosted)** | Tetap Qdrant — hanya mode deploy berubah |
| Speech-to-Text | Google STT | **Groq `whisper-large-v3`** (`language=id`) | SumoPod (provider LLM) tidak punya STT |
| LLM provider | Deepseek V4 generik | **SumoPod** (OpenAI-compatible) → `deepseek-v4-flash`/`deepseek-v4-pro` | Tetap Deepseek V4 — lewat provider SumoPod |
| Vision/OCR CV scan | Cloud Vision (implisit) | **SumoPod `gemini-2.5-flash-lite`** (diverifikasi 2026-07-15, ganti dari Groq Llama-4-Scout, ~12-14% lebih murah) | `deepseek-v4-pro` SumoPod tidak mendukung vision (dites langsung, gagal) |
| Pengiriman laporan | Email (rencana awal) → sempat diganti Telegram Bot API → **[SUPERSEDED 2026-07-23] dibalik lagi ke Gmail SMTP** | **Gmail SMTP** (`EMAIL_ENABLED=true`) sebagai channel utama; **Telegram jadi fallback berpenanda flag** (`TELEGRAM_ENABLED=false`, kode masih ada, tinggal di-flip kalau Gmail gagal) | Tim awalnya pindah ke Telegram karena email butuh setup SMTP+App Password (lihat alasan lama di baris di bawah, dipertahankan untuk konteks sejarah) — **lalu dibalik lagi ke Gmail** (2026-07-19, "Round-3 Task 19", user-verified dengan App Password asli, real send terkonfirmasi ke inbox nyata) karena email adalah channel yang benar-benar dipakai HR/kandidat sehari-hari, bukan Telegram; keputusan desain flag-guarded (bukan hapus kode Telegram) sengaja dibuat supaya rollback instan tanpa ubah kode kalau Gmail SMTP bermasalah saat demo. **Bonus fitur baru ikut paket ini:** email keputusan (accept/reject) dan laporan pengembangan sekarang dikirim **dalam satu email gabungan** (2026-07-22), bukan dua pesan terpisah. |
| ~~Pengiriman laporan (alasan pindah ke Telegram, versi lama — sudah tidak berlaku)~~ | ~~Email (rencana awal)~~ | ~~**Telegram Bot API** (`sendDocument`+`sendMessage`)~~ | ~~Email butuh setup SMTP + App Password + risiko spam; Telegram gratis, otomatis penuh, terverifikasi terkirim nyata~~ |
| Keamanan cloud (Cloud Armor/LB/Secret Mgr) | Ada di rencana | Belum diimplementasi (di luar scope MVP lokal) | Rencana pasca-hackathon |
| Enkripsi TLS/AES-256 | Diklaim di proposal | **Belum diimplementasi** — MVP jalan di HTTP plain (localhost), file tanpa enkripsi | Sengaja ditunda untuk MVP; wajib sebelum pilot data kandidat asli |

**Yang TIDAK berubah dari blueprint** (BVI baris 42): alur end-to-end 8 langkah, prinsip *"assist, never decide"*, rubrik skor tetap (bukan skor bebas LLM), 4 masalah inti Tahap 2 yang diwariskan.

### A.5.1 Matching engine — deviasi paling penting untuk dijaga konsisten

⚠️ **KGE/GNN (Knowledge Graph Embeddings/Graph Neural Network) yang disebut di proposal Tahap 2 dan blueprint Direction B TIDAK diimplementasikan sebagai KGE/GNN penuh.** (BVI §5.1, PLAN "Decisions RESOLVED" baris 93)

> **⚠️⚠️ [SUPERSEDED 2026-07-23] — formula di bawah ini SUDAH TIDAK DIPAKAI di kode nyata sejak 2026-07-19.** Paragraf asli (semantic vector similarity 0.7 + graph boost 0.3 via Qdrant) didokumentasikan sebelum perubahan Round-3. **Formula matching diganti total** — lihat kotak koreksi di bawah untuk versi yang benar-benar berjalan sekarang. Paragraf asli dipertahankan di bawah hanya sebagai catatan sejarah evolusi (blueprint KGE → v1 semantic+graph → v2 skill-gap-grounded), jangan dipakai sebagai fakta kini.

~~Implementasi nyata: **semantic vector similarity (Qdrant cosine) + competency-graph boost ringan** — formula `0.7 × semantic_similarity + 0.3 × graph_boost`. Ini keputusan sadar: prototipe KGE Tahap 2 tidak pernah terintegrasi ke produksi (dan setelah audit — bahkan tidak pernah ada sama sekali di kode, lihat A.4), jadi dibangun ulang dengan pendekatan lebih sederhana namun **tetap explainable** (skor bisa dirunut ke kompetensi spesifik yang cocok, tersimpan di kolom `match_scores.competency_breakdown`).~~

> **✅ [KOREKSI 2026-07-23] Formula matching yang benar-benar berjalan sekarang** (`backend/services/matching.py`, diganti total 2026-07-19, ditune ulang 2x hari yang sama — verified langsung dari kode):
>
> Root cause penggantian: user menemukan kasus nyata di mana semantic similarity meranking kandidat rendah padahal halaman detail kandidat (skill-gap analysis yang sudah grounded) justru menunjukkan kompetensi yang dicari ("Cloud Deployment") memang dimiliki — semantic similarity adalah satu angka fuzzy atas SELURUH blob profil vs SELURUH blob JD, tidak bisa merefleksikan satu skill spesifik secara akurat, dan rawan false positive (mirip topik ≠ punya skill).
>
> Formula baru **menggunakan ulang skill-gap analysis yang sudah grounded** (`services/skillgap.py`, sumber yang sama persis dengan yang ditampilkan di halaman detail kandidat — bukan sistem kedua yang bisa berbeda pendapat):
> ```
> coverage_score = (jumlah kompetensi cocok / total kompetensi wajib) × 100
> quality_score  = (rata-rata level proficiency kompetensi yang cocok / 3) × 100
> overall_score  = 0.9 × coverage_score + 0.1 × quality_score
> ```
> Bobot 90/10 (coverage-dominant) adalah hasil 2 iterasi tuning sehari (mulai 70/30 → 80/20 → 90/10) setelah user menemukan versi awal (skor proporsional murni) membuat 1 kompetensi dengan level rendah menjatuhkan skor terlalu drastis meski cakupan (coverage) sudah tinggi.
>
> **Implikasi penting: Qdrant/vector embeddings SEKARANG TIDAK DIPAKAI di jalur scoring/matching yang live.** `embed_candidate_profile()`/`embed_jd_competencies()` (`services/candidate_embedding.py`) hanya masih dipanggil dari `seed/load_demo_data.py` (populate index untuk 30 kandidat demo) — endpoint live (`POST /candidates`, folder-drop ingestion) TIDAK memanggilnya sama sekali, dan `compute_match_score()` tidak membaca dari Qdrant sama sekali. Qdrant secara teknis masih berjalan (Docker container, index terisi dari seed) tapi **vestigial** untuk keputusan ranking — bukan lagi bagian aktif dari algoritma matching.
>
> **Klaim ke judge harus disesuaikan LAGI (bukan cuma "bukan KGE/GNN")** — jangan bilang "semantic similarity + graph boost 0.7/0.3" (itu versi lama, sudah diganti). Bilang: **"skill-gap-grounded coverage & quality scoring (90% cakupan kompetensi + 10% kualitas/level proficiency), memakai sumber data yang identik dengan yang ditampilkan ke HR di halaman detail kandidat — bukan sistem kedua yang berpotensi tidak sinkron. Vector embeddings (Qdrant) sempat dipakai di versi awal, diganti karena similarity blob-vs-blob tidak cukup presisi untuk satu skill spesifik."** Ini justru argumen *lebih* kuat untuk Q17 (transparansi) — satu sumber kebenaran (`skill_gap_results`), bukan dua sistem yang bisa berbeda pendapat.

### A.5.2 Deviasi sadar lain (BVI §5)

1. **Peran demo tunggal**: MVP hanya mencakup 1 role (Web Developer, 10 kompetensi, 30 sumber belajar), bukan multi-role — keterbatasan waktu kurasi konten manual.
2. **30 kandidat seed acak, bukan dikurasi strong/mid/weak** — keputusan sadar user ("for testing purposes only"). **Namun QA Area 5 kemudian membuat fixture terpisah 6 kandidat tiered (2 strong/2 mid/2 weak) di JD terpisah (job_id=21) khusus untuk membuktikan algoritma matching mendiskriminasi kualitas kandidat** — lihat A.6 di bawah, hasil: strong avg 0.667 > mid avg 0.509 > weak avg 0.429, gap 0.238 jauh di atas ambang 0.05 (CHECKLIST baris 1262-1265). **Ini poin kredibilitas kuat yang bisa dipakai di Q17/Q9 — sudah dibuktikan dengan data nyata, bukan cuma janji.**
3. **Auth kandidat tanpa akun** — token link unguessable, bukan login formal, mempercepat build + menyederhanakan UX kandidat.
4. **Tahap 2 hampir tidak ada yang reusable secara kode** — lihat A.4.

## A.6 Status Implementasi Aktual (Terverifikasi, per 2026-07-15)

**Progress keseluruhan: seluruh 5 area eksekusi SELESAI**, termasuk QA — ini update dari status ~70% yang tercatat di BVI (per 2026-07-13); CHECKLIST (baca lengkap sampai baris 1374) mengonfirmasi Area 5 (QA) yang saat itu belum mulai kini **selesai penuh per 2026-07-15**.

| Area | Status final | Bukti |
|---|---|---|
| 4. Cost/Tooling | 🟢 Selesai | LLM client, STT, Telegram, vision — semua diuji API nyata |
| 3. Database + reference datasets | 🟢 Selesai | 17 tabel PostgreSQL + 2 koleksi Qdrant, 30 kandidat seed + 6 kandidat fixture tiered |
| 2. Backend & AI | 🟢 Selesai | Semua endpoint diuji HTTP nyata |
| 1. Frontend | 🟢 Selesai | 9 halaman React + rebuild visual-parity (halaman 1/2/3/4/5/6/8 selesai per 2026-07-15) + 3 halaman tambahan baru di luar 8 artifact asli |
| 5. QA | 🟢 **Selesai** (update dari BVI) | 9 task (T3/T3b/T4/T5-fixture/T5/T6/T8/T10/T11/T12) semua verified end-to-end; **3 bug nyata ditemukan & diperbaiki** dalam sesi QA sendiri |

### A.6.1 Bug nyata yang ditemukan & diperbaiki selama QA — amunisi kredibilitas untuk Q18

Ini bukan klaim kosong "sudah diuji" — QA menemukan bug **nyata** di sistem yang sudah "selesai dibangun", lalu memperbaikinya (CHECKLIST baris 1185-1213, 1293):

1. **Nama kandidat ternyata TIDAK ter-redaksi sebelum sampai ke LLM** (T3b) — root cause: `ingest_cv()` tidak pernah punya nama asli untuk diredaksi (kontrak API tidak menerima input nama). Diperbaiki dengan deteksi nama berbasis LLM (`detect_candidate_name()`). **Ditemukan lagi bug kedua**: truncation 800-karakter membuat nama di CV nyata user (posisi >800 karakter) lolos tidak ter-redaksi pada 1 dari 8 CV nyata yang dites. Diperbaiki (kirim teks penuh, cap 20.000 karakter) — 8/8 CV nyata sekarang bersih.
2. **Rubric scoring & skill-gap analysis TIDAK sepenuhnya deterministik di temperature=0** (T3, T4) — root cause: provider-level (batched/distributed inference SumoPod/Deepseek), bukan bug kode. Diperbaiki dengan **self-consistency voting** (panggil LLM 3x, ambil median/majority vote) — trade-off sadar: biaya API untuk kedua call site ini jadi ~3x lipat, tapi menjamin zero-drift (diverifikasi 9 panggilan nyata × 3 run, nol variasi).
3. **Rubric scoring & interview summary TIDAK pernah ter-wire ke alur kandidat nyata** (T11 Skenario 6) — endpoint `/score` dan `/interview-summary` hanya pernah dipanggil manual oleh seed script untuk kandidat sintetis, nol call site di frontend nyata. Kandidat nyata (candidate 59) yang menyelesaikan interview sungguhan dapat transkrip tapi tidak pernah dinilai — UI diam-diam menampilkan bagian rubrik kosong tanpa indikator "belum dinilai". Diperbaiki: `submit_answer()` sekarang otomatis memicu scoring + summary setelah kandidat menjawab semua pertanyaan yang disetujui.

> **Poin penting untuk Q17/Q9:** klaim "temperature=0 untuk determinisme" di draft `tahap 3 jawaban.md` (Q16, Q17) **kurang tepat sendirian** — temperature=0 saja terbukti TIDAK cukup deterministik di level provider. Implementasi nyata **lebih kuat** dari yang diklaim draft: self-consistency voting (3x call + median/majority vote), bukan cuma temperature=0. Ini upgrade positif yang belum masuk draft — sebaiknya ditambahkan sebagai bukti rigor teknis.

### A.6.2 Angka konkret implementasi (BVI baris 21, CHECKLIST — angka asli per 2026-07-15)

- 17 tabel PostgreSQL (companies, hr_users, jobs, jd_competencies, candidates, parsed_profiles, match_scores, interview_questions, interview_answers, transcripts, rubric_scores, interview_summaries, hr_decisions, consent_records, audit_log, competency_framework, resource_library)
- 2 koleksi Qdrant (`candidate_vectors`, `jd_vectors`)
- 9-10 router modul backend, 17+ endpoint bertipe (OpenAPI auto-generate, 21 schema)
- 23 modul service backend
- 9 halaman frontend ter-routing (React 18.3 + Vite 5.4 + TypeScript 5.6) + rebuild visual-parity + 3 halaman tambahan
- 30 kandidat seed demo (id 32-61) diproses lewat pipeline nyata, 2 dengan interview sintetis lengkap
- **6 kandidat fixture tiered tambahan (id 62-67, job_id=21)** khusus QA — 2 strong/2 mid/2 weak, membuktikan diskriminasi matching secara statistik
- Biaya nyata: ≈$0.07 per 1x demo run penuh (30 kandidat), ≈$0.20 termasuk siklus pengulangan development, infra $0 (semua lokal)

> **✅ [UPDATE 2026-07-23] Angka terverifikasi ulang langsung dari struktur folder kode (bukan dari catatan lama di atas):**
> - **18 tabel PostgreSQL** — 17 di atas + `skill_gap_results` (baru, persist hasil skill-gap analysis)
> - **12 router modul backend** (`backend/routers/*.py`): tambahan `dashboard.py`, `decisions.py`, `rubric.py`, `auth.py` sejak angka 9-10 di atas
> - **32 modul service backend** (`backend/services/*.py`): tambahan besar sejak 23 — termasuk `job_folder_ingest.py`/`job_folder_watcher.py`/`job_folders.py` (ingest CV lewat folder-drop, alternatif ke upload manual/seed-only), `email_client.py` (Gmail SMTP), `education.py` (ekstraksi pendidikan), `llm_cache.py`/`retry.py` (cost/reliability hardening)
> - **16 halaman frontend ter-routing**: tambahan `DashboardPage`, `JobDetailPage`, `JobReportsPage`, `ReportPage`, `ReportPdfPage`, `CandidateCvPage`, `CandidateCameraTestPage`, `NavRedirectPage` sejak 9; `JobFormPage` lama dihapus (digabung ke `JobsListPage`)
> - Qdrant/2 koleksi: **secara teknis masih ada**, tapi vestigial untuk matching sejak formula diganti (lihat A.5.1) — hanya terisi dari seed script, tidak lagi dibaca jalur live
> - Jangan pakai angka lama di atas ("17 tabel", "9 halaman", dst.) tanpa embel-embel tanggal — kalau ditanya judge angka pasti, pakai angka bagian ini.

### A.6.3 Item belum selesai (jujur, non-blocking)

- ~~**Persist skill-gap analysis** — saat ini dihitung ulang live setiap halaman detail kandidat dibuka...~~ **✅ [SUPERSEDED 2026-07-23] SUDAH SELESAI.** `persist_skill_gap()`/`get_or_compute_skill_gap()` (`backend/services/skillgap.py`, "Round-2 polish, 2026-07-17") menulis hasil ke tabel baru `skill_gap_results` sekali, lalu `candidate_detail.py` membaca baris tersimpan alih-alih menghitung ulang. Desain akhir: **lazy self-healing per-kandidat** (dihitung sekali saat pertama kali dibuka/di-matching, bukan bulk-precompute semua kandidat di awal) — user secara eksplisit memilih ini dibanding menjalankan `seed.backfill_skill_gap` untuk semua 36 kandidat sekaligus (real biaya LLM, ~108 panggilan worst-case). Shortlist sekarang menampilkan badge "Data siap" (hijau) / "Belum diproses" (kuning) per kandidat berdasar `skill_gap_ready` (`routers/matching.py`), jadi HR tahu kandidat mana yang akan kena delay ~30 detik saat pertama dibuka. **Efek samping penting:** formula matching (A.5.1) sekarang bergantung sepenuhnya pada tabel ini — `compute_match_score()` memanggil `persist_skill_gap()` sebagai langkah pertama, bukan opsional.
- TLS/enkripsi at-rest — sengaja ditunda untuk MVP lokal, wajib sebelum pilot data kandidat asli (sudah diakui jujur di draft Q13).
- Live-mic sanity check oleh manusia sungguhan (bukan Playwright fake-device) — status di CHECKLIST Area 1 T6 masih "pending" pada satu baris (baris 701), meski sudah diverifikasi lewat Playwright fake-device + real audio round-trip. **[Catatan 2026-07-23]** interview sekarang **video**, bukan audio saja (lihat A.7) — item ini sebaiknya dibaca sebagai "live camera+mic sanity check", bukan cuma mic.
- **[BARU 2026-07-23]** Job-folder CV ingestion (`backend/services/job_folder_watcher.py`, `job_folder_ingest.py`) — kode lengkap dan terpasang (watcher jalan otomatis saat backend start, `main.py::on_startup`), tapi **belum tercatat sama sekali di `execution-checklist.md`** (bukan hanya belum "Done" — task ini belum ada sebagai entry). Belum ada verifikasi live browser/E2E tercatat untuk fitur ini secara spesifik seperti task-task lain. Jangan klaim ke judge sebagai "sudah di-QA end-to-end" tanpa kualifikasi ini.

## A.7 Update Pasca-2026-07-15 (Round 2 & Round 3) — Ringkasan Delta, Terverifikasi Langsung dari Kode 2026-07-23

Bagian ini ditulis dengan membaca kode nyata (`git log`, isi file `backend/services/*.py`, `backend/routers/*.py`, struktur folder) plus catatan tanggal di `planning/execution-checklist.md`, **bukan** dengan asumsi dari status A.6 di atas (yang berhenti di 2026-07-15). Dipakai untuk menjaga Bagian B/C tetap benar tanpa harus menulis ulang seluruh dokumen.

| # | Perubahan | Sebelumnya (di dokumen ini) | Sekarang (terverifikasi) | Tanggal | Dampak ke jawaban judge |
|---|---|---|---|---|---|
| 1 | **Formula matching diganti total** | Semantic vector similarity (Qdrant) 0.7 + graph boost 0.3 | Skill-gap-grounded: 0.9×coverage + 0.1×quality, sumber data sama dengan detail kandidat | 2026-07-19 (2x re-tune hari sama) | **Tinggi** — Q13, Q15, Q16, Q17, C.1, C.2 semua kutip formula lama, semua sudah ditandai `[SUPERSEDED]` di tempatnya. Lihat A.5.1 untuk kalimat siap-pakai. |
| 2 | **Qdrant/vector embeddings jadi vestigial** | Dipakai aktif untuk scoring | Container tetap jalan, index terisi dari seed script saja — jalur live (`POST /candidates`, folder-drop) tidak memanggilnya sama sekali | 2026-07-19 (konsekuensi #1) | Sedang — kalau judge tanya detail arsitektur Qdrant, jujur bahwa perannya sudah menyusut, bukan komponen aktif algoritma lagi. |
| 3 | **Delivery laporan: Telegram → Gmail SMTP** | Telegram primer | Gmail SMTP primer (`EMAIL_ENABLED=true`), Telegram fallback flag-guarded (`TELEGRAM_ENABLED=false`) | 2026-07-19, user-verified real send | Sedang — A.5 tabel & C.1 sudah dikoreksi. Keputusan dibolak-balik sekali (email→Telegram→email), jujurkan evolusinya kalau ditanya. |
| 4 | **Keputusan + laporan digabung 1 email** | Dua pesan terpisah (asumsi awal) | Satu email berisi kabar lolos/tidak sekaligus laporan pengembangan | 2026-07-22 | Rendah — detail UX, tidak mengubah klaim inti manapun. |
| 5 | **Skill-gap analysis dipersist** | Dihitung ulang live tiap page load (item "belum selesai") | Disimpan di tabel baru `skill_gap_results`, dibaca ulang bukan dihitung ulang; lazy self-healing per kandidat (bukan bulk-precompute) | 2026-07-17 | Sedang — A.6.3 dikoreksi; ini memperkuat (bukan melemahkan) klaim efisiensi di Q13/Q20. |
| 6 | **Interview: audio → video** | "Rekam audio (WebM/Opus)" | Rekam **video** (WebM, `video:true,audio:true`), + halaman uji kamera/mikrofon terpisah, countdown 5 detik, batas waktu per-pertanyaan (1/2/3 menit, auto-stop), ringkasan per-jawaban | 2026-07-19 ("T21", task terbesar di proyek — 14-18 jam) | **Tinggi** — setiap penyebutan "audio" di Q10/Q16 sudah dikoreksi jadi "video". Ini juga fitur yang lebih impresif untuk demo (lebih visual) — pertimbangkan menonjolkannya di Q16/Q18. |
| 7 | **CV viewer + badge kesiapan data** | Tidak ada | Tombol "Lihat CV" di Detail Kandidat (buka PDF asli); badge hijau "Data siap"/kuning "Belum diproses" di Shortlist per kandidat | 2026-07-19 | Rendah-Sedang — bukti transparansi tambahan untuk Q17 kalau ada slot kata. |
| 8 | **Dashboard HR ditambahkan** | Tidak disebut di alur Q10 | Halaman landing setelah login: funnel kandidat lintas-job (parsed→shortlist→interview→decided), daftar "perlu perhatian", distribusi skor | Tanggal tidak tercatat di planning docs — dibangun setelah T11/T12 | Rendah — pelengkap UX, bukan klaim algoritma. Bisa disebut di Q18 sebagai bukti produk terus diiterasi. |
| 9 | **CV ingestion via folder-drop** | Hanya via `POST /candidates` manual/seed | HR bisa taruh PDF langsung di folder per-job (`backend/seed/job_lists/<job_id>_<slug>/`), diproses otomatis oleh watcher background (`main.py::on_startup`) atau skrip catch-up manual | **Belum tercatat di `execution-checklist.md` sama sekali** — dibangun setelah entri planning terakhir (≥2026-07-22) | Sedang — fitur nyata dan berfungsi (kode lengkap + endpoint dipakai jalur live), tapi **belum ada bukti QA/verifikasi live tercatat** seperti fitur-fitur lain. Jangan overclaim "sudah di-QA" untuk fitur ini spesifik. |
| 10 | **Angka struktural naik** | 17 tabel / 9-10 router / 23 service / 9 halaman | 18 tabel / 12 router / 32 service / 16 halaman | Kumulatif | Rendah — hanya soal angka pasti kalau judge menanyakan skala kode; lihat A.6.2 untuk angka terbaru. |

**Cara pakai bagian ini:** kalau membaca Bagian B/C di bawah dan menemukan klaim tentang matching formula, Qdrant, Telegram, audio recording, atau angka tabel/router/service/halaman — cek dulu apakah baris itu sudah punya anotasi `[SUPERSEDED 2026-07-23]` atau `[KOREKSI 2026-07-23]` di dekatnya. Kalau tidak, klaim tersebut kemungkinan besar masih akurat (tidak terdampak Round 2/3).

---

# BAGIAN B — Panduan Menjawab Per Pertanyaan (Q1–Q27)

> Format tiap entri: **Batas kata** · **Status draft** · **Fakta wajib dipakai** · **Koreksi dari draft saat ini** · **Sumber** · **Risiko pertanyaan judge + cara jawab**

## Q1-3 — ID Tim, Nama Tim, Judul Solusi
**Batas kata:** tidak ada (field pendek) · **Status draft:** terisi (P0804, Keprof Reborn, "GaskeunKerja for Business — Platform AI Terintegrasi untuk Rekrutmen, Skill-Gap Analysis, dan Pengembangan Kandidat")
**Catatan:** Q3 judul adalah usulan (JAWABAN baris 189 mencatat ini eksplisit) — ganti jika tim punya preferensi lain. Tidak ada koreksi teknis diperlukan.

## Q4-5 — Problem Statement & Sub-Problem Statement
**Status draft:** terisi, tidak berubah dari Tahap 2 (Digitalisasi Penciptaan Lapangan Kerja; Platform Job Matching AI, Skill Gap Advisor, Personalized Training).
**Kenapa tidak berubah:** ketiga sub-problem tetap relevan — hanya persona yang mewarisi berubah (lihat A.3). Tidak perlu revisi.

## Q6 — Final Team Composition *(maks 100 kata)*
**Status draft:** placeholder nama ([Nama 1-4]) perlu diisi manual. Deskripsi peran sudah konsisten dengan Q19.
**Aksi:** isi nama asli, pastikan konsisten dengan Q19 dan Q26-27.

## Q7 — Final Solution Summary *(maks 150 kata)*
**Status draft:** solid (~140 kata), mendeskripsikan alur inti dengan benar.
**Koreksi kecil:** kalimat "Knowledge Graph Embeddings" (JAWABAN baris 38) sebaiknya dilunakkan mengikuti A.5.1 — bisa tetap dipakai sebagai istilah high-level di ringkasan (karena batas kata ketat), tapi harus konsisten dengan penjelasan lebih presisi di Q13/Q16/Q17.

## Q8 — Progress and Change Log *(maks 150 kata)*
**Status draft:** solid (~135 kata), narasi pivot sudah tepat (4 kendala → pivot terarah).
**Fakta pendukung tambahan bila perlu diperkuat:** sekarang bisa ditambah bahwa progress bukan cuma "keputusan pivot" tapi **implementasi MVP lengkap 5 area sudah selesai** (A.6) — pertimbangkan apakah versi final ingin menonjolkan ini mengingat batas kata ketat.
**Sumber:** PLAN §Decision Log, BVI §1.

## Q9 — Validated User Problem and Evidence *(maks 250 kata)*
**Status draft:** solid (~210 kata), sudah jujur mengakui evidence masih sekunder (ManpowerGroup, BPS, WEF), belum wawancara HR langsung.
**Fakta wajib dipakai:** angka pengangguran BPS 7,28 juta (Feb 2025) → 7,36 juta (Nov 2025); ManpowerGroup 46%/50%/35%; WEF Future of Jobs 2023.
**Risiko judge:** "Mana bukti dari sisi company, bukan cuma laporan sekunder?" — **Jawab jujur** (sudah ada di draft): prioritas riset lanjutan 2 minggu ke depan, target 3-5 percakapan pilot SME. **Tambahan amunisi baru:** fixture QA tiered (A.6.1) membuktikan *algoritma* bekerja dengan data terkontrol, meski belum menjawab soal *validasi pasar* — bedakan dua klaim ini saat menjawab.
**Sumber:** PLAN §4d Q21/Q9 stress-test (baris 122-125) — ini "recurring weak spot" yang sudah diketahui tim, mitigasi: sitasi rigorous + rencana pilot konkret.

## Q10-11 — End-to-End Use Case & Operational Context *(maks 300 + 200 kata)*
**Status draft:** solid, sudah menjelaskan 8 langkah alur dengan pain-point mapping.
**Cross-check dengan alur nyata di kode (BVI §3.1, 9 langkah — lebih rinci dari draft):**
1. HR login (JWT) → CRUD JD penuh, scoped per company
2. Deepseek V4 Flash ekstrak kompetensi dari JD
3. CV diunggah → pypdf extract → deteksi halaman kosong → vision captioning (SumoPod Gemini) untuk halaman scan → **redaksi PII SEBELUM ke LLM** (nama/email/telepon dihapus) → Deepseek V4 Flash parsing
4. ~~Profil + kompetensi JD → vektor (SumoPod `gemini-embedding-001`, 1536-dim) → Qdrant → skor = 0.7×semantic + 0.3×graph_boost → shortlist explainable~~
5. HR invite kandidat → token link unik (kandidat tanpa akun)
6. Deepseek V4 Flash buat 2-3 pertanyaan → **HR edit/approve dulu (human-in-the-loop)** sebelum dikirim
7. ~~Kandidat buka token link → consent PDP → rekam audio (WebM/Opus) → Groq Whisper transkripsi (id) → Deepseek V4 Pro nilai vs rubrik tetap (3 kriteria, self-consistency voting 3x, bukan cuma temperature=0) + ringkasan~~
8. HR lihat audio+transkrip+ringkasan+skor → keputusan akhir manusia (AI tidak pernah auto-tolak)
9. ~~Laporan pengembangan dirakit dari competency framework + resource library kurasi (deterministik) → PDF (ReportLab) → Telegram (sendDocument+sendMessage) — semua kandidat, lolos/tidak~~

**Koreksi terpenting:** draft Q10 (JAWABAN baris 62) sudah cukup akurat secara alur, tapi tidak menyebut langkah "HR edit/approve pertanyaan" (human-in-the-loop di level pertanyaan, bukan cuma di level keputusan akhir) — ini detail kuat untuk Q17 (transparansi) yang sebaiknya disebut eksplisit jika ada slot kata tersisa.
**Sumber:** BVI §3.1 (baris 48-80).

> **✅ [KOREKSI 2026-07-23] Langkah 4, 7, 9 di atas sudah tidak akurat — versi yang benar-benar berjalan sekarang:**
> 4. Profil + kompetensi JD → **skill-gap analysis grounded** (`services/skillgap.py`, matched/missing/proficiency per kompetensi) → skor = **0.9×coverage + 0.1×quality** (lihat A.5.1) → shortlist explainable, badge "Data siap"/"Belum diproses" per kandidat tergantung sudah di-cache atau belum. *(Vektor/Qdrant tidak lagi di jalur ini — lihat A.5.1.)* **CV juga bisa masuk lewat folder-drop** (HR taruh PDF di `backend/seed/job_lists/<job_id>_<slug>/`, watcher background otomatis proses), alternatif ke upload satu-per-satu.
> 7. Kandidat buka token link → consent PDP → **uji kamera & mikrofon (halaman terpisah, preview live + meter level audio)** → per pertanyaan: countdown 5 detik → **rekam video** (WebM, `getUserMedia({video:true,audio:true})`) dengan batas waktu per-pertanyaan (1/2/3 menit, auto-stop) → Groq Whisper transkripsi audio-track (id) → Deepseek V4 Pro nilai vs rubrik tetap (3 kriteria, self-consistency voting 3x) + ringkasan per-jawaban
> 9. Laporan pengembangan dirakit dari competency framework + resource library kurasi (deterministik) → PDF (ReportLab) → **email (Gmail SMTP)** sebagai channel utama — keputusan (lolos/tidak) dan laporan dikirim **dalam satu email gabungan**; Telegram tetap ada di kode sebagai fallback berpenanda flag, tidak aktif secara default.
>
> **Sumber:** lihat A.7 untuk ringkasan lengkap + rujukan baris kode.

## Q12 — Innovation Level
**Status draft:** menyebut "Prototype Lanjutan menuju MVP" (JAWABAN baris 78).
**⚠️ PERLU DIREVISI:** ini **understatement** dibanding status real per A.6 — implementasi sudah menyelesaikan seluruh 5 area termasuk QA end-to-end lengkap (7 skenario visible-browser + 7/7 edge case demo-readiness), bukan "sedang dikembangkan". Framing yang lebih akurat: **"MVP fungsional end-to-end, terverifikasi lokal"**, bukan cuma prototype menuju MVP.
**Risiko judge (PLAN §4d Q12, baris 112-115):** "Async AI interview sudah ada (HireVue), apa yang baru?" — **Jawab:** bukan klaim algoritma baru, tapi *integrasi* baru — matching + skill-gap + AI interview + laporan pengembangan kandidat dalam satu alur tertutup, terlokalisasi untuk SME Indonesia. Fitur "kandidat ditolak pun dapat laporan pengembangan" tergolong jarang ditemukan.
**Sumber:** PANDUAN Q12, PLAN §4d, CHECKLIST status matrix.

## Q13 — Current Technical Reality, Data, and Integration *(maks 300 kata)* ⚠️ PRIORITAS TINGGI
**Status draft:** JAWABAN baris 84 **paling butuh revisi** — masih membingkai arsitektur sebagai rencana cloud ("Qdrant... perlu di-resize", "Infrastruktur akan bermigrasi... menjadi Cloud Run", "BigQuery" disebut sebagai datastore aktif).
**Fakta wajib dipakai (ganti seluruh framing cloud dengan realita lokal, A.5):**
- Database: **PostgreSQL 16 (Docker), 17 tabel, sudah dibangun & diverifikasi via query nyata** — bukan "akan migrasi ke BigQuery" sebagai hal yang belum jelas; jelaskan sebagai keputusan sadar MVP lokal dengan migrasi BigQuery sebagai langkah produksi terencana (bukan tergantung nasib).
- Storage: filesystem lokal, path pointer di DB — bukan "GCS perlu di-resize".
- Vector DB: Qdrant **sudah** berjalan Docker self-hosted dengan 2 koleksi aktif, bukan "perlu di-resize ke skala kecil" (sudah kecil by design, <10k vektor, sudah terverifikasi).
- Matching: **[SUPERSEDED 2026-07-23]** BUKAN "semantic similarity + competency-graph boost (0.7/0.3)" — itu versi v1, sudah diganti 2026-07-19. Versi nyata sekarang: **skill-gap-grounded coverage & quality scoring (90% cakupan kompetensi + 10% kualitas/proficiency)**, satu sumber data dengan yang ditampilkan di detail kandidat. BUKAN KGE/GNN penuh juga — lihat A.5.1 untuk detail lengkap dan kalimat siap-pakai ke judge.
- AI Interview: BUKAN "belum dibangun, fokus 2 minggu ke depan" — **sudah dibangun dan diverifikasi end-to-end**. **[Update 2026-07-23]** interview sekarang berbasis **video** (bukan audio saja), dengan uji kamera/mikrofon terpisah, countdown, dan batas waktu per-pertanyaan; laporan dikirim lewat **Gmail SMTP** (bukan Telegram — lihat A.5).
- Vision/OCR: SumoPod `gemini-2.5-flash-lite` (bukan disebut sama sekali di draft) — komponen nyata yang menangani CV hasil scan.
- **[BARU 2026-07-23]** Skill-gap analysis kini **dipersist**, bukan dihitung ulang tiap page load (lihat A.6.3) — argumen efisiensi yang lebih kuat dari draft.
**Koreksi kalimat spesifik:** ganti "Integrasi Qdrant Vector Database... perlu di-resize" dan "Infrastruktur akan bermigrasi dari rencana GKE penuh menjadi Cloud Run" dengan: "MVP berjalan 100% lokal (Docker Compose: PostgreSQL + Qdrant), migrasi ke Cloud Run/BigQuery/GCS direncanakan untuk fase pilot produksi — bukan pekerjaan tertunda, melainkan keputusan kecepatan-build yang disengaja untuk jendela hackathon."
**Sumber:** BVI §2 (tabel deviasi lengkap), §3.2 (17 komponen teknis).

## Q14 — MVP Execution and Deployment Plan *(maks 250 kata)*
**Status draft:** JAWABAN baris 92 menyebut rencana 3 fase 14 hari (Fase 1-3) sebagai *rencana ke depan* — tapi ini **sudah selesai dikerjakan**, bukan rencana.
**⚠️ PERLU DIREVISI:** ubah framing dari "akan mengeksekusi" menjadi "telah dieksekusi, berikut hasilnya", lalu isi slot yang tersisa dengan rencana pilot pasca-hackathon (yang memang belum terjadi).
**Fakta wajib dipakai:** eksekusi nyata memakai 5 area kerja (Tooling → Database → Backend&AI → Frontend → QA), bukan 3 fase, dan berlangsung ~13 hari kerja (CHECKLIST §Milestones), selesai per 2026-07-15. Uji coba internal bukan "akan dilakukan" tapi **sudah dilakukan**: 30 kandidat + 6 kandidat fixture tiered, plus 7 skenario QA visible-browser.
**Sumber:** CHECKLIST §Status Matrix, §Milestones (baris 67-89).

## Q15 — Problem and System Complexity *(maks 200 kata)*
**Status draft:** solid secara argumen (kontekstual/multidimensi vs keyword matching).
**Koreksi:** kalimat "Sistem kami menggunakan Knowledge Graph Embeddings untuk memetakan hubungan relasional" (JAWABAN baris 100) perlu disesuaikan ke istilah nyata: "Sistem menggunakan semantic vector embeddings dikombinasikan dengan graph relasional kompetensi (competency-graph boost) untuk memetakan..." — substansi argumen (bukan keyword matching sederhana) tetap valid, hanya istilah algoritma yang perlu presisi.
**Risiko judge (PLAN §4d Q15):** "Kenapa tidak cukup pakai ATS keyword filtering?" — jawab: keyword matching tidak menangkap kompetensi kontekstual; kontraskan eksplisit dengan embedding relasional; penilaian interview juga butuh reasoning LLM tingkat lanjut, bukan aturan if-else statis.
**Sumber:** PLAN §4d (baris 117-120), A.5.1.

## Q16 — Processing Pipeline and Engineering Depth *(maks 250 kata)* ⚠️ PRIORITAS TINGGI
**Status draft:** JAWABAN baris 108 — sama seperti Q13, masih menyebut "REST API Gateway (FastAPI di Cloud Run)" dan alur berbasis komponen cloud sebagai kalau-sudah-berjalan.
**Koreksi wajib:** ganti "Cloud Run" dengan "FastAPI/uvicorn (Docker Compose untuk mode finalisasi)"; ganti alur penyimpanan "BigQuery... GCS" dengan "PostgreSQL (Docker)... filesystem lokal"; ganti "Knowledge Graph Embeddings menghitung matching score" dengan formula nyata; tambahkan detail nyata yang hilang dari draft — **HR mengedit/menyetujui pertanyaan interview sebelum dikirim ke kandidat** (human-in-the-loop di level pertanyaan, bukan cuma di level keputusan akhir), dan **self-consistency voting** pada rubric scoring.
**⚠️ [SUPERSEDED 2026-07-23]** formula "semantic 0.7 + graph boost 0.3" yang disebutkan di atas **sudah tidak berlaku** — ganti dengan formula skill-gap-grounded 90% coverage + 10% quality (lihat A.5.1 untuk teks lengkap siap-pakai). Juga tambahkan: interview kini video bukan audio, delivery laporan kini email (Gmail) bukan Telegram (lihat A.7).
**Fakta pipeline lengkap yang harus dipakai:** lihat Q10-11 di atas (9 langkah nyata dari BVI §3.1) — pipeline Q16 dan use-case Q10 harus konsisten satu sama lain, jangan sampai versi cloud vs versi lokal tercampur di dua jawaban berbeda.
**Sumber:** BVI §3.1, §3.2.

## Q17 — Algorithm or Rule Quality and Decision Transparency *(maks 300 kata)*
**Status draft:** solid secara prinsip ("assist, never decide", rubrik tetap, audit log) — argumen inti sudah benar dan tidak perlu diubah.
**⚠️ Perkuat, jangan hanya perbaiki:** draft menyebut "temperature=0" (JAWABAN baris 116) sebagai mekanisme determinisme. **Ini sekarang bisa diperkuat signifikan** — QA (A.6.1) menemukan temperature=0 SENDIRIAN terbukti *tidak* cukup deterministik di level provider (SumoPod/Deepseek serving terdistribusi), sehingga tim menambahkan **self-consistency voting** (3 panggilan independen, ambil median untuk skor rubrik / majority vote untuk kompetensi skill-gap) — diverifikasi 9 panggilan nyata × 3 run terpisah, nol variasi (drift). Ini adalah bukti *rigor* teknis yang lebih kuat dari klaim asli — sangat disarankan ditambahkan sebagai kalimat baru menggantikan "temperature=0" saja.
**Koreksi istilah:** "KGE" pada kalimat pembuka (JAWABAN baris 116) ganti dengan istilah presisi (lihat A.5.1 — bukan cuma "bukan KGE", formulanya sendiri sudah berubah lagi per 2026-07-19, jangan pakai versi semantic+graph).
**[Tambahan 2026-07-23]** argumen transparansi Q17 sekarang bisa diperkuat lagi: matching score dan skill-gap analysis di halaman detail kandidat memakai **satu sumber data yang sama persis** (`skill_gap_results`, bukan dua sistem terpisah yang bisa tidak sinkron) — ini bukti desain "explainable by construction", bukan cuma dijelaskan setelah fakta.
**Sumber:** A.6.1, A.5.1, CHECKLIST baris 1200-1213 (T3/T4 findings).

## Q18 — User Flow, Usability Testing, and Product Iteration *(maks 250 kata)*
**Status draft:** JAWABAN baris 124 menyebut rencana pengujian 2 minggu ke depan sebagai *akan dilakukan* — tapi ini **sudah terjadi dan jauh lebih ekstensif** dari yang diklaim draft.
**⚠️ PERLU DIREVISI SIGNIFIKAN — ini kesempatan memperkuat jawaban, bukan cuma memperbaiki:** ganti framing "rencana uji coba usability dalam dua minggu ke depan" dengan laporan hasil nyata:
- Simulasi internal: bukan rencana, **sudah dijalankan** — 30 kandidat seed + 6 kandidat fixture tiered melalui pipeline nyata end-to-end.
- QA menemukan **3 bug produk nyata** dan memperbaikinya dalam sesi yang sama (lihat A.6.1) — ini bukti iterasi produk berbasis temuan nyata, bukan asumsi.
- 7 skenario end-to-end diuji **visible di browser sungguhan** (bukan headless) termasuk jalur gagal (mic ditolak, token kedaluwarsa, submit kosong, Telegram gagal kirim), dan **7/7 edge case demo-readiness terverifikasi**, termasuk pengiriman Telegram nyata terkonfirmasi diterima.
**Yang tetap jujur diakui:** walkthrough dengan HR sungguhan (pengguna eksternal riil) memang belum terjadi — ini beda dari QA internal. Pertahankan pengakuan ini, tapi jangan biarkan ia mengaburkan bahwa pengujian internal sudah jauh lebih dalam dari "rencana".
**Sumber:** CHECKLIST §Area 5 (T10, T11, T12, baris 1276-1309).

## Q19 — Team Capability and Execution Ownership *(maks 250 kata)*
**Status draft:** solid, placeholder nama perlu diisi (konsisten dengan Q6).
**Catatan penting untuk transparansi internal (bukan untuk ditulis ke submission apa adanya):** `implementation/planning/plan.md` baris 7 mencatat MVP dibangun **solo** (1 orang), bukan tim 4 orang seperti dideskripsikan Q6/Q19. Ini framing eksternal (submission) vs realita internal (build). Jika judge bertanya detail pembagian kerja teknis secara spesifik, siapkan jawaban yang konsisten dengan siapa yang benar-benar mengerjakan apa.
**Sumber:** `implementation/planning/plan.md` baris 7.

## Q20 — Continuation Readiness *(maks 200 kata)*
**Status draft:** solid, konsisten dengan rencana pilot 3-5 SME.
**Tidak ada koreksi wajib.** Bisa diperkuat dengan menyebut item follow-up nyata yang sudah teridentifikasi dari QA (persist skill-gap analysis untuk efisiensi biaya, A.6.3) sebagai bukti tim sudah punya roadmap teknis konkret pasca-MVP, bukan cuma roadmap bisnis.

## Q21 — Quantified Value, Business Model, and ROI *(maks 300 kata)*
**Status draft:** solid, sudah jujur mengakui angka ROI adalah target berbasis estimasi Tahap 2 + literatur.
**Fakta biaya yang harus tetap konsisten:** $170-370/bulan adalah **proyeksi cloud pilot/produksi** (INFRA), BUKAN biaya MVP saat ini. Biaya MVP nyata sekarang: ≈$0.07/demo run, ≈$0.20 dengan pengulangan dev, infra $0 (semua lokal) — **ini angka berbeda, jangan tertukar.** Draft Q21 sudah benar memakai angka proyeksi cloud ($170-370) untuk konteks ROI produksi — itu tepat, karena Q21 bicara skala produksi bukan MVP. Pastikan konsisten: kalau Q13/Q16 sudah dikoreksi menjelaskan MVP lokal $0, Q21 tetap boleh memakai proyeksi cloud produksi selama dijelaskan sebagai proyeksi terpisah, bukan biaya saat ini.
**Sumber:** INFRA §4, BVI §4 (baris 110-138) — penjelasan lengkap kenapa biaya cloud bukan pembeda Tahap 2 vs 3, yang membedakan adalah beban/load.

## Q22 — Adoption, Growth Strategy, and Competitive Moat *(maks 250 kata)*
**Status draft:** solid.
**Risiko judge (PLAN §4d Q22):** "LinkedIn/Kalibrr bisa saja menambah fitur ini, apa yang menghalangi mereka?" — **Jawab:** moat bukan fitur yang tidak bisa ditiru, tapi fokus + data lokal + integrasi. Pemain global tidak akan memprioritaskan long-tail SME atau lokalisasi Indonesia. Tekankan data flywheel (rubrik+matching makin akurat seiring makin banyak interview diproses) sebagai keunggulan yang terakumulasi, bukan statis.
**Sumber:** PLAN §4d (baris 127-130).

## Q23-27 — Video, Link Attachment, File Attachment, CV/LinkedIn
**Status:** semua placeholder, perlu diisi manual — link video YouTube (unlisted), link demo/artifact publik, CV/LinkedIn tiap anggota.
**Rekomendasi kandidat link attachment (Q24):** repo GitHub yang sudah diupdate untuk Direction B (kini bisa menunjukkan implementasi nyata yang sudah selesai, bukan cuma diagram arsitektur) — ini jauh lebih kuat sekarang dibanding saat draft ditulis, karena repo mengandung 17 tabel + 9 router + 9 halaman frontend yang benar-benar berjalan, bukan janji.

---

# BAGIAN C — Lampiran Referensi Cepat

## C.1 Tabel "Kalau Judge Tanya X, Jawab Y"

| Pertanyaan judge yang mungkin muncul | Jawaban jujur & kuat | Sumber |
|---|---|---|
| "Ini kan cuma rencana, mana yang benar-benar jalan?" | 5 dari 5 area eksekusi (Tooling, DB, Backend&AI, Frontend, QA) selesai dan **diverifikasi lewat panggilan API/HTTP/DB nyata**, bukan mock. 17 tabel, 9+ router, 9 halaman frontend, 30+6 kandidat diproses lewat pipeline sungguhan. Bukan hanya kode ditulis — setiap task diverifikasi dengan bukti konkret. | A.6, BVI §1 |
| "Kok masih pakai laptop lokal, bukan cloud sungguhan?" | Keputusan sadar untuk kecepatan build di jendela waktu hackathon (~13 hari solo), bukan keterbatasan desain. Infrastruktur cloud produksi (GKE/BigQuery/GCS) untuk Tahap 2 dan 3 **sama jenisnya** — yang membedakan adalah beban (load): puluhan klien B2B vs ribuan-puluhan ribu individu B2C. | BVI §4.2, INFRA §1 |
| "KGE/GNN yang disebut di proposal itu beneran jalan?" | Tidak — setelah evaluasi, prototipe KGE Tahap 2 ternyata tidak pernah terintegrasi produksi (bahkan tidak ada di kode sama sekali). Diganti pendekatan skill-gap-grounded: 90% cakupan kompetensi + 10% kualitas/proficiency, memakai sumber data yang identik dengan yang ditampilkan ke HR di halaman detail kandidat — **tetap explainable**, terbukti mendiskriminasi kandidat kuat/sedang/lemah secara statistik nyata (gap 0.238 pada fixture tiered, dites terhadap versi formula sebelumnya tapi properti diskriminasi tetap relevan). **[2026-07-23]** ini formula generasi ke-2 — generasi pertama (semantic vector + graph boost 0.7/0.3) sempat dibangun lalu diganti lagi setelah ditemukan kasus nyata di mana similarity blob-vs-blob salah rangking kandidat yang sebenarnya punya skill yang dicari. Kejujuran soal evolusi ini (bukan cuma "bukan KGE") lebih kredibel. | A.5.1, A.6.1 |
| "Delivery laporan pakai apa, Telegram atau email?" | **[2026-07-23]** Gmail SMTP adalah channel utama (`EMAIL_ENABLED=true`), Telegram jadi fallback berpenanda flag (`TELEGRAM_ENABLED=false`, kode tetap ada, tinggal di-flip). Sempat sebaliknya (Telegram utama) di pertengahan build karena setup email dianggap lebih ribet — dibalik lagi setelah App Password Gmail asli diverifikasi bekerja nyata, dan email dinilai channel yang benar-benar dipakai HR/kandidat sehari-hari. | A.5, A.7 |
| "Skor AI-nya konsisten nggak kalau diulang?" | Awalnya tidak — ditemukan sendiri lewat QA bahwa temperature=0 saja tidak cukup deterministik di level provider. Diperbaiki dengan self-consistency voting (3 panggilan, median/majority vote), diverifikasi nol variasi pada 9 panggilan nyata × 3 run. | A.6.1, Q17 |
| "Reuse dari Tahap 2 katanya tinggi, buktinya?" | Setelah audit kode nyata: reuse sebenarnya terbatas pada pola (bukan kode) — ekstraksi teks CV, grounding skill-gap, generate PDF. Tahap 2 ternyata tidak pakai React, tidak pakai Deepseek (pakai Gemini), dan tidak ada auth/DB sama sekali. Kejujuran ini penting — jangan overclaim reuse. | A.4 |
| "Kenapa email jadi Telegram?" | Email butuh setup SMTP+App Password dan berisiko kena filter spam saat demo langsung; Telegram gratis, otomatis penuh, dan file benar-benar terverifikasi terkirim (dites langsung, diterima nyata di akun Telegram). | A.5 (tabel deviasi) |
| "Sudah diuji ke user asli belum?" | Pengujian internal end-to-end sangat ekstensif (30+6 kandidat, 7 skenario visible-browser, 7/7 edge case, 3 bug nyata ditemukan+diperbaiki). Pengujian dengan HR eksternal sungguhan **belum** — ini diakui jujur, jadi prioritas riset 3-5 SME pilot pasca-hackathon. | Q18, A.6.1 |
| "Data buat klaim ROI dari mana?" | Laporan sekunder (ManpowerGroup, BPS, WEF) + estimasi Tahap 2 — belum divalidasi wawancara HR langsung. Diakui jujur di draft sebagai gap evidence terbesar Direction B; mitigasi via sitasi rigorous + rencana pilot konkret. | Q9, Q21, PLAN §4d |

## C.2 Angka Kunci yang Harus Konsisten di Seluruh Jawaban

| Angka | Nilai | Konteks — jangan tertukar |
|---|---|---|
| Biaya MVP lokal saat ini | ≈$0.07/demo run, ≈$0.20 dengan pengulangan dev, infra $0 | Biaya **build/demo sekarang**, bukan proyeksi produksi |
| Biaya proyeksi cloud produksi Direction B | ~$170-370/bulan (GCP) | Proyeksi **pilot/produksi masa depan**, bukan biaya sekarang |
| Biaya proyeksi cloud Direction A (pembanding) | ~$800-1.750/bulan | Untuk kontras Tahap 2 vs Tahap 3 saja, bukan biaya nyata siapa pun sekarang |
| Formula matching | **[2026-07-23]** 0.9 × coverage_score + 0.1 × quality_score (skill-gap-grounded) — BUKAN LAGI 0.7×semantic + 0.3×graph_boost (versi lama, diganti 2026-07-19) | Bukan KGE/GNN penuh; Qdrant vestigial, tidak dipakai jalur live — lihat A.5.1 |
| Jumlah tabel DB | **18 tabel PostgreSQL** (17 lama + `skill_gap_results`) | Docker lokal, bukan BigQuery aktif |
| Jumlah kandidat seed | 30 (demo) + 6 (fixture tiered QA, job_id=21) | Dua kumpulan terpisah, tujuan berbeda |
| Kriteria rubrik interview | 3 kriteria (kejelasan, relevansi, kedalaman teknis), skala 1-5 | Self-consistency voting 3x, bukan cuma temperature=0 |
| Tanggal keputusan pivot Direction B | 2026-07-12 | — |
| Tanggal implementasi selesai (5 area) | 2026-07-15 | Termasuk QA lengkap |
| Deadline submission Tahap 3 | ~2026-07-26 | Verifikasi ulang tanggal pasti dari portal kompetisi |

## C.3 Daftar Semua File Sumber (Path Relatif dari `Tahap 3/`)

- `brainstorming idea/plan.md`
- `brainstorming idea/proposal sekarang tahap 3/final/tahap 3 jawaban.md`
- `brainstorming idea/proposal sekarang tahap 3/progress idea/direction B summary.md`
- `brainstorming idea/proposal sekarang tahap 3/progress idea/perbandingan tahap 2 vs tahap 3.md`
- `brainstorming idea/proposal sekarang tahap 3/progress idea/tahap 3 proposal update (blueprint + implementation).md`
- `brainstorming idea/proposal sekarang tahap 3/progress idea/new idea/infra comparison A vs B.md`
- `proposal/tahap 3 proposal.md`
- `implementation/CLAUDE.md`
- `implementation/planning/plan.md`
- `implementation/planning/execution-checklist.md`
- `../Tahap 2/tahap 2 proposal.md` (di luar folder `Tahap 3/`)

---

*Dokumen ini disusun sebagai backup knowledge, bukan pengganti `tahap 3 jawaban.md`. Semua koreksi yang disarankan di Bagian B perlu direview dan diterapkan manual oleh tim ke file jawaban final sebelum submit, dengan tetap memperhatikan batas kata tiap pertanyaan.*
