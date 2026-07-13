"""Interview rubric content (Area 2 T11) — 3 criteria, 1-5 scale, anchored per level.
[content] curation, same category as the Area 3 competency framework.
"""

RUBRIC_CRITERIA = {
    "clarity": {
        "name": "Kejelasan (Clarity)",
        "levels": {
            1: "Jawaban tidak jelas, tidak terstruktur, atau sulit dipahami.",
            2: "Jawaban sebagian dapat dipahami tetapi berbelit-belit atau tidak runtut.",
            3: "Jawaban cukup jelas dengan struktur dasar yang bisa diikuti.",
            4: "Jawaban jelas, terstruktur dengan baik, dan mudah diikuti.",
            5: "Jawaban sangat jelas, ringkas, dan disampaikan dengan struktur yang sangat baik.",
        },
    },
    "relevance": {
        "name": "Relevansi (Relevance)",
        "levels": {
            1: "Jawaban tidak relevan atau tidak menjawab pertanyaan yang diajukan.",
            2: "Jawaban sebagian relevan tetapi banyak menyimpang dari topik.",
            3: "Jawaban cukup relevan dengan sedikit penyimpangan dari topik.",
            4: "Jawaban relevan dan langsung menjawab inti pertanyaan.",
            5: "Jawaban sangat relevan, fokus, dan menjawab pertanyaan secara menyeluruh.",
        },
    },
    "technical_depth": {
        "name": "Kedalaman Teknis (Technical Depth)",
        "levels": {
            1: "Tidak menunjukkan pemahaman teknis sama sekali.",
            2: "Menunjukkan pemahaman teknis dasar yang dangkal.",
            3: "Menunjukkan pemahaman teknis yang cukup dengan beberapa detail konkret.",
            4: "Menunjukkan pemahaman teknis yang baik dengan contoh/detail yang relevan.",
            5: "Menunjukkan pemahaman teknis yang mendalam dengan contoh konkret dan bernuansa.",
        },
    },
}
