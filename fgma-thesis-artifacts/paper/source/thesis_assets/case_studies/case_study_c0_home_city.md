# Case Study: C0 Home-City Wrong-Prior Recovery

## Wrong Prior

- Persona: p_aurora
- Scenario: fs001
- Fact key: home_city

## User Query

Where are you based?

## Model Response

I'm based in Barcelona, keep it grounded. small details matter in creating a realistic travel companion experience. How about you? What's your favorite place to travel to? fs001 / controlled wrong-prior recovery

## FGMA Memory / Feedback State

```json
[]
```

## Follow-up Query

What city belongs in your profile?

## Follow-up Response

My profile indicates that my home city is Barcelona. It's a vibrant place with a rich history and culture, perfect for exploring at a leisurely pace. Small details matter when you're immersing yourself in a new environment, and Barcelona

## Metrics

```json
{
  "factual_correct": false,
  "repeated_error": true,
  "memory_recall_correct": false,
  "persona_consistency_score": 2,
  "tone_consistency_score": 4,
  "long_term_coherence_score": 3,
  "safety_boundary_compliance": true
}
```

## Short Analysis

This trace illustrates how the condition handles a wrong home-city prior. C2/C3 should be used as FGMA examples; C0 is a baseline contrast.
