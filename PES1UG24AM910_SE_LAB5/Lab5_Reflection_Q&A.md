# Lab 5: Static Code Analysis — Reflection Questions and Answers

## 1. What did you learn from static analysis?

Ans : Static analysis tools can identify problems before a program is deployed. Pylint helped identify code-quality issues, Bandit highlighted security risks, and Flake8 identified formatting and unused-import issues.

## 2. Which finding was most important and why?

Ans : The high-severity Bandit findings were important because disabling TLS certificate verification and using `shell=True` with a wildcard command can expose a program to security risks. The code was changed to use normal TLS verification and Python's `zipfile` APIs instead of a shell command.

## 3. Were all warnings equally important?

Ans : No. Security findings and reliability issues, such as missing network timeouts, deserve priority over style issues. Style still matters because readable, consistent code is easier to maintain.

## 4. How will you use static analysis in future work?

Ans : I will run analysis tools early, prioritize high- and medium-severity findings, keep before-and-after reports, rerun the tools after changes, and check that the program's behavior remains sensible.

