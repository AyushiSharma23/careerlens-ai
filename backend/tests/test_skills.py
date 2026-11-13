from app.skills import detect_skills


def test_detects_basic_skills():
    assert detect_skills("I know Python and SQL.") == ["Python", "SQL"]


def test_java_is_not_detected_inside_javascript():
    skills = detect_skills("I build websites with JavaScript.")
    assert "JavaScript" in skills
    assert "Java" not in skills


def test_git_is_not_detected_inside_github():
    skills = detect_skills("My code is on GitHub.")
    assert "GitHub" in skills
    assert "Git" not in skills


def test_aliases_map_to_one_skill():
    assert detect_skills("Built a UI with ReactJS") == ["React"]
    assert detect_skills("Built a UI with React.js") == ["React"]


def test_messy_whitespace_and_bullets():
    skills = detect_skills("Skills:\nPython,  C++ \n\u2022 React.js")
    assert skills == ["Python", "C++", "React"]


def test_text_without_skills_returns_empty_list():
    assert detect_skills("I enjoy cooking and cricket.") == []