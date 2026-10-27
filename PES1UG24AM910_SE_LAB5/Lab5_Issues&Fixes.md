# Lab 5: Static Code Analysis — Issues and Fixes

| Issue | Type / Severity | Original line | 
Description | Fix Approach |
|---|---|---:|---|---|
| TLS certificate verification disabled (B501) | Security — High | 60 | The ERP request used `verify=False`, disabling certificate verification. | Removed `verify=False` so normal TLS certificate verification is used. |
| Shell command with wildcard (B609, B602, B607) | Security — High / Low | 64 | The backup used `subprocess` with `shell=True` and a wildcard-based tar command. | Replaced the shell command with Python `pathlib` and `zipfile`; no shell is launched. |
| ERP request without timeout (B113) | Security / reliability — Medium | 60 | The request could wait indefinitely. | Added `timeout=10` and `response.raise_for_status()`. |
| Insecure TLS protocol default (B503) | Security — Medium | 6 | The original code used the legacy TLSv1 protocol. | Changed to `ssl.create_default_context()`. |
| Reminder job with `shell=True` (B604) | Security — Medium | 73 | The reminder command was represented as shell execution. | Uses a list of arguments and `shell=False`; the function describes the job and does not execute it. |
| Mutable default dictionary | Correctness / maintainability | 18 | A mutable default dictionary can be shared between calls. | Changed `register={}` to `register=None` and initializes it inside the function. |

The before Bandit report recorded eight findings (2 High, 3 Medium, 3 Low); the after report recorded zero. Pylint improved from 4.55/10 to 10.00/10. Flake8 reported style issues before and no output after.
