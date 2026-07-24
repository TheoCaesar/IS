# Milestone 2 – Preparing the SWAM Operator

## Overview
This milestone prepares implementation of the Spherical Weighted Arithmetic Mean (SWAM), the aggregation operator used by both SF-SWARA and SF-EDAS.

## Objectives
- Create a reusable SWAM module
- Validate inputs
- Build helper functions
- Prepare fuzzy components

## Design Decisions
SWAM is implemented independently because both algorithms reuse it.

## Input Validation
- Number of fuzzy numbers must equal the number of weights.
- Weights must sum to one.

## Component Extraction
The implementation separates:

```
mus = [μ₁, μ₂, μ₃, ...]
nus = [ν₁, ν₂, ν₃, ...]
pis = [π₁, π₂, π₃, ...]
```

This matches the notation in the mathematical equations.

## Weighted Product Helper
A helper function computes weighted products:

Π(xᵢ^wᵢ)

This avoids duplicate code and improves readability.

## Outcome
The project is ready to implement the full SWAM equations for membership, non-membership, and hesitancy.
