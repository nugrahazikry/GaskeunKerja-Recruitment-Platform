from db.repository import Repository
from models import (
    AuditLog,
    Candidate,
    Company,
    CompetencyFramework,
    ConsentRecord,
    HRDecision,
    HRUser,
    InterviewAnswer,
    InterviewQuestion,
    InterviewSummary,
    JDCompetency,
    Job,
    MatchScore,
    ParsedProfile,
    ResourceLibrary,
    RubricScore,
    Transcript,
)

companies = Repository(Company)
hr_users = Repository(HRUser)
jobs = Repository(Job)
jd_competencies = Repository(JDCompetency)
candidates = Repository(Candidate)
parsed_profiles = Repository(ParsedProfile)
match_scores = Repository(MatchScore)
interview_questions = Repository(InterviewQuestion)
interview_answers = Repository(InterviewAnswer)
transcripts = Repository(Transcript)
rubric_scores = Repository(RubricScore)
interview_summaries = Repository(InterviewSummary)
hr_decisions = Repository(HRDecision)
consent_records = Repository(ConsentRecord)
audit_log = Repository(AuditLog)
competency_framework = Repository(CompetencyFramework)
resource_library = Repository(ResourceLibrary)
