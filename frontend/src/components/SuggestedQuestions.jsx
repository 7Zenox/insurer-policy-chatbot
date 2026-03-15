const QUESTIONS = [
  "Is bariatric surgery covered for BMI > 35?",
  "What are the prior auth requirements for MRI?",
  "What does CPT code 64493 cover?",
  "When is genetic testing covered?",
];

export default function SuggestedQuestions({ onSelect }) {
  return (
    <div className="suggested-questions">
      <p>Try asking:</p>
      {QUESTIONS.map((q) => (
        <button key={q} onClick={() => onSelect(q)} className="suggestion-btn">
          {q}
        </button>
      ))}
    </div>
  );
}
