# Milestone 3 – SWAM (Spherical Weighted Arithmetic Mean)

## Objective
Implement the SWAM operator (Equation A8) to aggregate multiple expert spherical fuzzy evaluations into a single Spherical Fuzzy Number.

## Responsibilities
- Validate expert weights
- Aggregate membership values
- Aggregate non-membership values
- Aggregate hesitancy values
- Return a valid SFN

## Workflow
Expert Evaluations
    ↓
Linguistic Terms
    ↓
Spherical Fuzzy Numbers
    ↓
SWAM
    ↓
Aggregated SFN

## Mathematical Components
- Membership: μ = √(1 − ∏(1 − μ²)^w)
- Non-membership: ν = ∏(ν^w)
- Hesitancy: π = √(∏(1−μ²)^w − ∏(1−μ²−π²)^w)

## Verification
The implementation was tested and produced a valid spherical fuzzy number satisfying:
μ² + ν² + π² ≤ 1.

## Outcome
SWAM is fully implemented and is reused by both SF-SWARA and SF-EDAS.
