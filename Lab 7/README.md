# Lab 7: Fuzz Testing — Visa Application

**Deeptanshu Kumar — PES1UG24AM357**

## Run

```bash
python -m pip install -r requirements.txt
python visa_application.py
python -m pytest test_visa_application.py -q
```

The handout's processor.py and test_processor.py correspond to this repository's visa_application.py and test_visa_application.py.

## Validation contract

Invalid values return `None`; the interactive application displays `Invalid input`.
- Application: nonempty visa name, exactly one colon, positive integer entries.
- Days: nonempty CSV of nonnegative integers; arithmetic mean (not floor division).
- Fee: exactly two finite nonnegative numbers separated by `|`; apply 18% tax and subtract discount, retaining the original zero minimum. Reject non-finite computed totals.

These are explicit lab validation choices, not visa policy rules. Values outside floating-point representability are rejected. The CLI expects three input lines.

## Results and evidence

The final suite has six Hypothesis properties (300 generated examples per property, deterministic profile) and 18 parameterized regression cases. The original code produces **22 failed, 2 passed**; the fixed code produces **24 passed**. A test run is evidence of the tested properties, not a proof for every possible input.

The PDF contains four genuine terminal captures: original crash, failing tests, fixed interactive execution, and passing tests. Raw PNGs, test logs, and an unchanged original application are in `evidence/`. The overflow regression uses `1.7e308|0`; `1e308|0` is finite and is not classified as invalid.

To reproduce the baseline, copy `evidence/visa_application_original.py` as `visa_application.py` into a temporary directory along with the final test file, then run pytest there.
