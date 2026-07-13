import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { HrAuthGuard } from "./lib/HrAuthGuard";
import { LoginPage } from "./pages/LoginPage";
import { JobsListPage } from "./pages/JobsListPage";
import { CandidateConsentPage } from "./pages/CandidateConsentPage";
import { CandidateInterviewPage } from "./pages/CandidateInterviewPage";
import { InvalidLinkPage } from "./pages/InvalidLinkPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/jobs"
          element={
            <HrAuthGuard>
              <JobsListPage />
            </HrAuthGuard>
          }
        />
        <Route path="/candidate/:candidateId/consent" element={<CandidateConsentPage />} />
        <Route path="/candidate/:candidateId/interview" element={<CandidateInterviewPage />} />
        <Route path="/link-invalid" element={<InvalidLinkPage />} />
        <Route path="*" element={<InvalidLinkPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
