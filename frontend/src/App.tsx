import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { HrAuthGuard } from "./lib/HrAuthGuard";
import { LoginPage } from "./pages/LoginPage";
import { DashboardPage } from "./pages/DashboardPage";
import { JobsListPage } from "./pages/JobsListPage";
import { JobDetailPage } from "./pages/JobDetailPage";
import { ShortlistPage } from "./pages/ShortlistPage";
import { QuestionsPage } from "./pages/QuestionsPage";
import { CandidateDetailPage } from "./pages/CandidateDetailPage";
import { CandidateCvPage } from "./pages/CandidateCvPage";
import { JobReportsPage } from "./pages/JobReportsPage";
import { ReportPage } from "./pages/ReportPage";
import { ReportPdfPage } from "./pages/ReportPdfPage";
import { CandidateConsentPage } from "./pages/CandidateConsentPage";
import { CandidateCameraTestPage } from "./pages/CandidateCameraTestPage";
import { CandidateInterviewPage } from "./pages/CandidateInterviewPage";
import { InvalidLinkPage } from "./pages/InvalidLinkPage";
import { NavRedirectPage } from "./pages/NavRedirectPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={
            <HrAuthGuard>
              <DashboardPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs/:jobId/detail"
          element={
            <HrAuthGuard>
              <JobDetailPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs"
          element={
            <HrAuthGuard>
              <JobsListPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs/new"
          element={
            <HrAuthGuard>
              <JobsListPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs/:jobId/edit"
          element={
            <HrAuthGuard>
              <JobsListPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs/:jobId"
          element={
            <HrAuthGuard>
              <ShortlistPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs/:jobId/questions"
          element={
            <HrAuthGuard>
              <QuestionsPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs/:jobId/candidates/:candidateId"
          element={
            <HrAuthGuard>
              <CandidateDetailPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs/:jobId/candidates/:candidateId/cv"
          element={
            <HrAuthGuard>
              <CandidateCvPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs/:jobId/reports"
          element={
            <HrAuthGuard>
              <JobReportsPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs/:jobId/candidates/:candidateId/report"
          element={
            <HrAuthGuard>
              <ReportPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/jobs/:jobId/candidates/:candidateId/report/pdf"
          element={
            <HrAuthGuard>
              <ReportPdfPage />
            </HrAuthGuard>
          }
        />
        <Route
          path="/candidates"
          element={
            <HrAuthGuard>
              <NavRedirectPage target="kandidat" />
            </HrAuthGuard>
          }
        />
        <Route
          path="/reports"
          element={
            <HrAuthGuard>
              <NavRedirectPage target="laporan" />
            </HrAuthGuard>
          }
        />
        <Route path="/candidate/:candidateId/consent" element={<CandidateConsentPage />} />
        <Route path="/candidate/:candidateId/camera-test" element={<CandidateCameraTestPage />} />
        <Route path="/candidate/:candidateId/interview" element={<CandidateInterviewPage />} />
        <Route path="/link-invalid" element={<InvalidLinkPage />} />
        <Route path="*" element={<InvalidLinkPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
