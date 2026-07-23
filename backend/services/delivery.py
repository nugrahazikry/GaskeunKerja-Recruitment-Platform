import os
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from config import EMAIL_ENABLED, STORAGE_DIR, TELEGRAM_ENABLED
from db import repositories as repo
from services import email_client, telegram_client
from services.report import build_interview_answers, build_report
from services.report_pdf import render_report_pdf


class NoTelegramLinkError(Exception):
    """Raised when the candidate hasn't linked their Telegram chat yet."""


class NoEmailAddressError(Exception):
    """Raised when the candidate has no contact_email on file (Round-3 Task 19)."""


def _write_report_pdf(candidate_id: int, report: dict, interview_answers: list[dict]) -> str:
    pdf_bytes = render_report_pdf(report, interview_answers)
    pdf_path = f"{STORAGE_DIR}/reports/{candidate_id}/laporan.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    return pdf_path


def _decision_email_content(candidate_alias: str, job_title: str, company_name: str, decision: str) -> tuple[str, str]:
    """2026-07-22 (user-requested): the "Ambil Keputusan" action on ReportPage.tsx sends the
    decision AND the development report together in one email — this composes that combined
    subject+body, decision-aware, replacing the old generic "Laporan Pengembangan" + gap_summary
    body that said nothing about the outcome itself."""
    if decision == "advance":
        subject = f"Selamat — Anda Melanjutkan ke Tahap Berikutnya di {company_name}"
        body = (
            f"Halo {candidate_alias},\n\n"
            f"Selamat! Setelah meninjau hasil CV dan wawancara Anda untuk posisi {job_title} di "
            f"{company_name}, kami dengan senang hati mengabarkan bahwa Anda dinyatakan lolos dan "
            "akan melanjutkan ke tahap berikutnya dalam proses rekrutmen kami.\n\n"
            "Tim kami akan segera menghubungi Anda untuk informasi lebih lanjut mengenai tahap "
            "selanjutnya. Sebagai referensi, kami turut melampirkan laporan feedback CV dan "
            "wawancara Anda pada email ini.\n\n"
            "Terima kasih atas usaha dan waktu yang telah Anda berikan sepanjang proses ini. "
            "Sampai jumpa di tahap berikutnya!\n\n"
            f"Salam,\nTim Rekrutmen {company_name}"
        )
    else:
        subject = f"Pembaruan Status Lamaran — {job_title} di {company_name}"
        body = (
            f"Halo {candidate_alias},\n\n"
            f"Terima kasih telah meluangkan waktu untuk mengikuti seluruh proses rekrutmen kami "
            f"untuk posisi {job_title} di {company_name}, mulai dari pengiriman CV hingga sesi "
            "wawancara.\n\n"
            "Setelah mempertimbangkan dengan saksama, saat ini kami memutuskan untuk melanjutkan "
            "proses dengan kandidat lain yang profilnya paling sesuai dengan kebutuhan posisi ini. "
            "Keputusan ini sama sekali bukan cerminan dari kualitas maupun potensi Anda secara "
            "keseluruhan.\n\n"
            "Sebagai bentuk apresiasi atas partisipasi Anda, kami melampirkan laporan feedback CV "
            "dan wawancara Anda pada email ini — semoga dapat menjadi masukan yang bermanfaat untuk "
            "langkah karier Anda selanjutnya.\n\n"
            f"Kami sangat menghargai minat Anda terhadap {company_name}, dan berharap dapat "
            "menjumpai Anda kembali pada kesempatan lain di masa mendatang.\n\n"
            "Terima kasih dan sukses selalu!\n\n"
            f"Salam,\nTim Rekrutmen {company_name}"
        )
    return subject, body


def send_report(db: Session, candidate_id: int) -> dict:
    """Generates the PDF, saves it, and delivers it + the decision outcome to the candidate in one
    combined email — this is now the ONLY report-delivery path (2026-07-22: the standalone "Kirim
    Laporan via Email" button on ReportPdfPage.tsx was removed in favor of "Ambil Keputusan" on
    ReportPage.tsx, which calls POST /decisions then this endpoint right after), so an hr_decisions
    row is required, not just optional bookkeeping.

    Round-3 Task 19: email (Gmail SMTP) is now the primary channel, Telegram kept intact as a
    flag-guarded fallback (EMAIL_ENABLED / TELEGRAM_ENABLED in config.py) — flipping the flags is
    the entire rollback path, no code change needed.
    """
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate:
        raise ValueError(f"Candidate {candidate_id} not found")

    decisions = repo.hr_decisions.list(db, candidate_id=candidate_id)
    if not decisions:
        raise ValueError(f"Candidate {candidate_id} has no recorded decision yet")
    decision = decisions[0]

    job = repo.jobs.get(db, candidate.job_id)
    company = repo.companies.get(db, job.company_id) if job else None
    job_title = job.title if job else "?"
    company_name = company.name if company else ""

    report = build_report(db, candidate_id, candidate.job_id)
    interview_answers = build_interview_answers(db, candidate_id)
    pdf_path = _write_report_pdf(candidate_id, report, interview_answers)
    subject, body = _decision_email_content(candidate.alias, job_title, company_name, decision.decision)

    result: dict
    if EMAIL_ENABLED:
        if not candidate.contact_email:
            raise NoEmailAddressError(f"Candidate {candidate_id} has no contact_email on file")
        email_client.send_email(to=candidate.contact_email, subject=subject, body=body, attachment_path=pdf_path)
        result = {"pdf_path": pdf_path, "channel": "email", "to": candidate.contact_email}
    elif TELEGRAM_ENABLED:
        if not candidate.telegram_chat_id:
            raise NoTelegramLinkError(f"Candidate {candidate_id} has not linked Telegram yet")
        chat_id = int(candidate.telegram_chat_id)
        telegram_client.send_document(
            chat_id, pdf_path, caption=f"Laporan pengembangan untuk {candidate.alias}"
        )
        telegram_client.send_message(chat_id, body)
        result = {"pdf_path": pdf_path, "channel": "telegram", "chat_id": chat_id}
    else:
        raise RuntimeError("No delivery channel enabled — set EMAIL_ENABLED or TELEGRAM_ENABLED")

    decision.report_sent_at = datetime.now(timezone.utc)
    db.commit()

    return result


def send_invite_email(
    candidate_id: int,
    invite_link: str,
    candidate_alias: str,
    contact_email: str,
    job_title: str,
    company_name: str,
) -> None:
    """New notification (Round-3 Task 19): emails the interview invite link — previously only
    ever manually copy-pasted by HR.

    Round-3 follow-up #11 (2026-07-19): template polished (job title + company context, clearer
    expectations) and moved from Kandidat Detail's decision card to being the primary post-
    "Lanjutkan" action there — the "Kirim Laporan via Email" button that used to live in that spot
    was premature (development report should only be sent once CV analysis AND interview results
    both exist; laporan page now owns that send action instead)."""
    email_client.send_email(
        to=contact_email,
        subject=f"Undangan Wawancara — {job_title} di {company_name}",
        body=(
            f"Halo {candidate_alias},\n\n"
            "Setelah meninjau profil dan CV Anda, kami dengan senang hati mengundang Anda untuk "
            f"melanjutkan ke tahap wawancara untuk posisi {job_title} di {company_name}.\n\n"
            "Wawancara ini dilakukan secara online melalui platform AI kami. Silakan klik tautan "
            f"berikut untuk memberikan persetujuan dan memulai proses wawancara:\n\n{invite_link}\n\n"
            "Catatan penting:\n"
            "- Tautan ini berlaku selama 72 jam sejak email ini dikirim.\n"
            "- Pastikan Anda berada di lingkungan yang tenang dengan koneksi internet stabil, dan "
            "mengizinkan akses kamera serta mikrofon saat diminta.\n\n"
            "Jika Anda memiliki pertanyaan, jangan ragu untuk menghubungi kami.\n\n"
            "Terima kasih dan semoga sukses!\n\n"
            f"Salam,\nTim Rekrutmen {company_name}"
        ),
    )


def send_interview_finished_email(
    candidate_alias: str, contact_email: str, job_title: str, company_name: str
) -> None:
    """2026-07-22 (user-requested): fires automatically the moment the candidate's post-interview
    pipeline (transcription, scoring, summary, and the recommendation-extras/upskilling-plan LLM
    chain) has fully finished — the exact same instant the candidate's own "please wait" screen
    (CandidateInterviewPage.tsx) clears and shows "Wawancara selesai". Sets expectations on when
    they'll hear back so they aren't left wondering. Called from
    services/interview_answers.py::process_answer(), guarded by candidates.
    interview_finished_notified_at so it only ever sends once per candidate."""
    email_client.send_email(
        to=contact_email,
        subject=f"Wawancara Anda Telah Kami Terima — {job_title} di {company_name}",
        body=(
            f"Halo {candidate_alias},\n\n"
            f"Terima kasih telah menyelesaikan tahap wawancara untuk posisi {job_title} di "
            f"{company_name}. Kami menghargai waktu dan usaha yang telah Anda luangkan dalam "
            "proses ini.\n\n"
            "Tim rekrutmen kami akan meninjau hasil wawancara Anda bersama profil dan CV yang "
            "telah Anda kirimkan sebelumnya. Kami akan menghubungi Anda dengan hasil keputusan "
            "selambat-lambatnya dalam 2 minggu sejak wawancara ini selesai.\n\n"
            "Jika Anda memiliki pertanyaan, jangan ragu untuk menghubungi kami.\n\n"
            "Terima kasih atas kesabaran Anda, dan semoga sukses!\n\n"
            f"Salam,\nTim Rekrutmen {company_name}"
        ),
    )


def send_decision_notice(candidate_alias: str, contact_email: str, decision: str) -> None:
    """New notification (Round-3 Task 19): a candidate-facing accept/reject notice. Manually
    triggered by HR (a button), never automatic on decision — avoids accidental sends while
    testing, consistent with the existing manual send-report trigger."""
    if decision == "advance":
        subject = "Selamat — Anda Lolos ke Tahap Berikutnya"
        body = f"Halo {candidate_alias},\n\nSelamat! Anda telah lolos ke tahap berikutnya dalam proses rekrutmen kami."
    else:
        subject = "Pembaruan Status Lamaran"
        body = (
            f"Halo {candidate_alias},\n\nTerima kasih telah mengikuti proses rekrutmen kami. "
            "Saat ini kami memutuskan untuk tidak melanjutkan ke tahap berikutnya."
        )
    email_client.send_email(to=contact_email, subject=subject, body=body)
