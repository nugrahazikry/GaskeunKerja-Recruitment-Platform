"""Competency framework + resource library content for the Web Developer demo role (Area 3 T6/T7).

Ten competencies, each with a level description (used by the report to describe proficiency)
and lightweight relations to related competencies (feeds Area 2 T7's matching graph boost).
Three curated resources per competency (feeds the deterministic development report).
"""

JOB_ROLE = "Web Developer"

# key -> (competency_name, level_description, related_keys)
COMPETENCIES = {
    "html_css": (
        "HTML & CSS",
        "1=hanya bisa membuat halaman statis sederhana; 3=mahir layout responsif dengan Flexbox/Grid dan "
        "CSS terstruktur; 5=mahir animasi CSS, aksesibilitas, dan cross-browser compatibility tingkat lanjut.",
        ["javascript", "responsive_design"],
    ),
    "javascript": (
        "JavaScript",
        "1=baru paham sintaks dasar; 3=mahir manipulasi DOM, async/await, dan fetch API; "
        "5=mahir arsitektur aplikasi kompleks, optimasi performa, dan debugging tingkat lanjut.",
        ["frontend_framework", "html_css"],
    ),
    "frontend_framework": (
        "Framework Frontend (React/Vue/Angular)",
        "1=belum pernah membangun aplikasi dengan framework; 3=mahir component-based development, "
        "state management dasar, dan routing; 5=mahir arsitektur skala besar, optimasi render, dan custom hooks/composables.",
        ["javascript", "state_management"],
    ),
    "backend_development": (
        "Backend Development (Node.js/Python/PHP)",
        "1=belum bisa membangun API dasar; 3=mahir membangun REST API dengan validasi dan autentikasi; "
        "5=mahir arsitektur backend skalabel, microservices, dan optimasi query database.",
        ["database", "api_design"],
    ),
    "database": (
        "Database (SQL/NoSQL)",
        "1=hanya paham query SELECT dasar; 3=mahir desain skema, JOIN, dan indexing; "
        "5=mahir optimasi query kompleks, replikasi, dan pemilihan database sesuai use-case.",
        ["backend_development", "api_design"],
    ),
    "api_design": (
        "API Design & Integration",
        "1=belum pernah merancang/mengonsumsi API; 3=mahir REST API design, dokumentasi, dan integrasi pihak ketiga; "
        "5=mahir GraphQL, versioning API, dan desain API untuk skala tinggi.",
        ["backend_development", "database"],
    ),
    "version_control": (
        "Version Control (Git)",
        "1=hanya bisa commit dan push dasar; 3=mahir branching, merge, dan resolve conflict; "
        "5=mahir workflow tim skala besar (Git Flow), code review, dan rebase/cherry-pick tingkat lanjut.",
        ["deployment", "responsive_design"],
    ),
    "responsive_design": (
        "Responsive & Mobile-First Design",
        "1=hanya membuat layout untuk satu ukuran layar; 3=mahir mendesain untuk berbagai breakpoint dan perangkat; "
        "5=mahir pendekatan mobile-first, performa loading di perangkat rendah, dan progressive web app.",
        ["html_css", "version_control"],
    ),
    "deployment": (
        "Deployment & DevOps Dasar",
        "1=belum pernah men-deploy aplikasi sendiri; 3=mahir deploy ke platform cloud dasar (Vercel/Netlify/VPS) "
        "dan konfigurasi CI/CD sederhana; 5=mahir containerization (Docker), monitoring produksi, dan skalabilitas infrastruktur.",
        ["version_control", "backend_development"],
    ),
    "state_management": (
        "State Management",
        "1=hanya menggunakan state lokal komponen; 3=mahir state management global (Redux/Zustand/Pinia/Context); "
        "5=mahir arsitektur state kompleks, caching data, dan optimasi re-render skala besar.",
        ["frontend_framework", "javascript"],
    ),
}

# competency_key -> [(title, duration, milestone_description, url), ...]
RESOURCES = {
    "html_css": [
        ("Responsive Web Design dengan Flexbox & Grid", "6 jam", "Mampu membangun layout responsif tanpa framework CSS", None),
        ("CSS Animation Fundamentals", "3 jam", "Mampu membuat transisi dan animasi CSS yang halus", None),
        ("Web Accessibility (a11y) Basics", "3 jam", "Memahami prinsip aksesibilitas dasar untuk halaman web", None),
    ],
    "javascript": [
        ("Modern JavaScript (ES6+) Deep Dive", "8 jam", "Mahir async/await, destructuring, dan module system", None),
        ("DOM Manipulation & Events Praktis", "4 jam", "Mampu membangun interaksi UI dinamis tanpa framework", None),
        ("Debugging JavaScript di Browser DevTools", "2 jam", "Mampu menelusuri dan memperbaiki bug secara sistematis", None),
    ],
    "frontend_framework": [
        ("React untuk Pemula sampai Mahir", "10 jam", "Mampu membangun aplikasi multi-halaman dengan komponen reusable", None),
        ("Vue.js Fundamentals", "8 jam", "Mampu membangun aplikasi reaktif dengan Composition API", None),
        ("Component Design Patterns", "4 jam", "Mampu merancang komponen yang scalable dan mudah dites", None),
    ],
    "backend_development": [
        ("Membangun REST API dengan Node.js/Express", "8 jam", "Mampu membangun API CRUD lengkap dengan validasi", None),
        ("Autentikasi & Otorisasi (JWT)", "4 jam", "Mampu mengimplementasikan sistem login yang aman", None),
        ("Backend Architecture Fundamentals", "5 jam", "Memahami pemisahan layer controller/service/repository", None),
    ],
    "database": [
        ("SQL untuk Web Developer", "6 jam", "Mampu menulis query JOIN dan agregasi untuk aplikasi web", None),
        ("Desain Skema Database yang Efisien", "4 jam", "Mampu merancang relasi dan indexing yang tepat", None),
        ("Pengantar NoSQL (MongoDB)", "4 jam", "Mampu memilih antara SQL dan NoSQL sesuai kebutuhan aplikasi", None),
    ],
    "api_design": [
        ("RESTful API Design Best Practices", "4 jam", "Mampu merancang endpoint API yang konsisten dan terdokumentasi", None),
        ("Integrasi API Pihak Ketiga (Payment Gateway, dll)", "3 jam", "Mampu mengintegrasikan layanan eksternal ke aplikasi", None),
        ("Pengantar GraphQL", "5 jam", "Memahami perbedaan REST dan GraphQL serta kapan menggunakannya", None),
    ],
    "version_control": [
        ("Git & GitHub Fundamentals", "3 jam", "Mampu melakukan branching, merge, dan resolve conflict dasar", None),
        ("Git Workflow untuk Tim (Git Flow)", "3 jam", "Mampu mengikuti alur kerja kolaborasi tim skala menengah", None),
        ("Code Review Best Practices", "2 jam", "Mampu memberikan dan menerima review kode secara konstruktif", None),
    ],
    "responsive_design": [
        ("Mobile-First Design Principles", "4 jam", "Mampu mendesain UI dengan pendekatan mobile-first", None),
        ("Progressive Web Apps (PWA) Dasar", "5 jam", "Mampu membangun aplikasi web yang bisa diinstal dan offline-ready", None),
        ("Optimasi Performa Loading Halaman Web", "4 jam", "Mampu mengukur dan meningkatkan kecepatan loading halaman", None),
    ],
    "deployment": [
        ("Deploy Aplikasi Web ke Vercel/Netlify", "3 jam", "Mampu men-deploy aplikasi frontend ke produksi dengan cepat", None),
        ("Docker untuk Web Developer", "6 jam", "Mampu containerize aplikasi web untuk deployment yang konsisten", None),
        ("Pengantar CI/CD Pipeline", "4 jam", "Mampu mengatur pipeline testing dan deployment otomatis dasar", None),
    ],
    "state_management": [
        ("State Management dengan Redux/Zustand", "6 jam", "Mampu mengelola state global aplikasi secara terstruktur", None),
        ("React Context API Praktis", "3 jam", "Mampu menggunakan Context API untuk state skala menengah", None),
        ("Optimasi Re-render pada Aplikasi Frontend", "4 jam", "Mampu mengidentifikasi dan memperbaiki re-render yang tidak perlu", None),
    ],
}
