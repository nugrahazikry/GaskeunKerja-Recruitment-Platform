export const RUBRIC_LABELS: Record<string, string> = {
  clarity: "Kejelasan",
  relevance: "Relevansi",
  technical_depth: "Kedalaman Teknis",
};

export function RubricDots({ score }: { score: number }) {
  return (
    <span className="rubric-dots">
      {[1, 2, 3, 4, 5].map((n) => (
        <span key={n} className={n <= score ? "on" : ""} />
      ))}
    </span>
  );
}
