export function CandidateHeader({ step }: { step: string }) {
  return (
    <div className="cand-header">
      <div className="brand">
        Gaskeun<span>Kerja</span>
      </div>
      <div className="step">{step}</div>
    </div>
  );
}
