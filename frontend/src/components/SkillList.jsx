import { Check, X } from "lucide-react";

// variant is "matched" or "missing".
// Matched skills look highlighted, like marker on paper.
// Missing skills get a wavy red underline, like a correction mark.
// Each one also has an icon and sits under a text heading, so colour is never the only clue.
export default function SkillList({ title, skills, variant, emptyText }) {
  const Icon = variant === "matched" ? Check : X;

  return (
    <div className="skill-group">
      <h3>
        {title} ({skills.length})
      </h3>
      {skills.length === 0 ? (
        <p className="hint">{emptyText}</p>
      ) : (
        <ul className="skills">
          {skills.map((skill) => (
            <li key={skill}>
              <Icon size={14} aria-hidden="true" />
              {variant === "matched" ? (
                <mark>{skill}</mark>
              ) : (
                <span className="skill-missing">{skill}</span>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}