# Op-Amp Math

Op-amp gain arithmetic. A 10000 Ω feedback over a 1000 Ω to ground gives a gain of 11. 0.2 V in comes out at 2.2 V.

## What it computes

- **The non-inverting truth** - gain (one plus the feedback over the ground resistor) and the output voltage, from two resistors (1 to 1000000 Ω each) and an input (0.01 to 10 V).
- **The inverting truth** - the negative gain and output from the feedback over the input resistor.
- **The summing truth** - the inverted weighted sum of two inputs, each through its own resistor.

## Boundary

Arithmetic only, ideal op-amp rules. The resistances and voltages are the owner's own entries, every op-amp treated as ideal. It has not seen any circuit and does not know the supply rails, the bandwidth, the offset or the chip variant, and it gives no verdict that an amplifier circuit is adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on ohms and hundredths of a volt, half-up on display).
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/opampmath/
Repo: https://github.com/iLanis-agent/opampmath
