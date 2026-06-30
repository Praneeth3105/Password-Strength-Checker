# 🔐 Password Strength Checker

A Python-based GUI application that evaluates password security using industry-standard metrics, entropy analysis, and real-world breach data.

## ✨ Key Highlights
- Uses **zxcvbn** for realistic password strength estimation
- Calculates password entropy based on character set complexity
- Displays estimated crack times under multiple attack scenarios
- Checks password exposure using **Have I Been Pwned (k-Anonymity model)**
- Clean, intuitive Tkinter GUI
- Exportable password security report

## 📸 Application Features
- Strength score from *Very Weak* to *Very Strong*
- Actionable security suggestions
- Visual feedback using color-coded indicators
- Secure password breach verification (SHA-1 range query)
- Show/Hide password toggle
- Save analysis report as `.txt`

## 🧩 Tech Stack
| Category | Tools |
|--------|------|
| Language | Python |
| GUI | Tkinter |
| Security | zxcvbn, hashlib |
| API | Have I Been Pwned |
| Networking | requests |

## ⚙️ Installation & Usage
```bash
git clone https://github.com/Praneeth3105/Password-Strength-Checker.git
cd Password-Strength-Checker
pip install zxcvbn requests
python main.py
