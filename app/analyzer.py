from app.ai_agent import ask_ai
from app.db_metadata import get_database_schema

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


def analyze_change(change_description: str):

    # ---------------------------------------
    # 1. Load engineering knowledge
    # ---------------------------------------

    architecture = load_json("architecture.json")

    dependencies = load_json("dependencies.json")

    incidents = load_json("incidents.json")

    field_dependencies = load_json(
        "field_dependencies.json"
    )

    # ---------------------------------------
    # 2. Read actual SQLite database schema
    # ---------------------------------------

    database_schema = get_database_schema()

    # ---------------------------------------
    # 3. Prepare AI prompt
    # ---------------------------------------

    prompt = f"""
You are an AI Engineering Change Impact Analyzer.

Analyze the proposed engineering change using ONLY the
engineering information provided below.

PROPOSED CHANGE:
{change_description}


SYSTEM ARCHITECTURE:
{json.dumps(architecture, indent=2)}


COMPONENT DEPENDENCIES:
{json.dumps(dependencies, indent=2)}


ACTUAL DATABASE SCHEMA:
{json.dumps(database_schema, indent=2)}


FIELD-LEVEL DEPENDENCIES:
{json.dumps(field_dependencies, indent=2)}


HISTORICAL INCIDENTS:
{json.dumps(incidents, indent=2)}


Your analysis must cover:

1. Overall risk level.
2. Directly affected components.
3. Indirectly affected downstream components.
4. Why each component may be affected.
5. Relevant historical incidents.
6. Potential downstream consequences.
7. Recommended validation and testing actions.
8. Rollback considerations.


IMPORTANT RULES:

- Only mention components that exist in the provided architecture.
- Only mention database tables and columns that exist in the actual database schema.
- Use the provided component dependencies when determining downstream impact.
- Use the provided field-level dependencies when determining column-level impact.
- Use historical incidents when they are relevant.
- Do not invent historical incidents.
- Do not invent dependencies.
- Do not invent database columns.
- Do not assume a component is affected without a dependency or reasonable relationship in the provided data.
- Risk must be LOW, MEDIUM, or HIGH.
- Component impact must be LOW, MEDIUM, or HIGH.
- Explain the reasoning clearly.
- Return ONLY valid JSON.
- Do not add markdown.
- Do not add explanations outside the JSON.


Return JSON using exactly this structure:

{{
  "risk_level": "HIGH",

  "affected_components": [
    {{
      "name": "component name",
      "impact": "HIGH",
      "reason": "why this component may be affected"
    }}
  ],

  "historical_incidents": [
    {{
      "id": "incident id",
      "impact": "incident impact",
      "relevance": "why this incident is relevant"
    }}
  ],

  "downstream_consequences": [
    "potential consequence 1",
    "potential consequence 2"
  ],

  "recommendations": [
    "recommended action 1",
    "recommended action 2"
  ],

  "rollback_plan": [
    "rollback action 1",
    "rollback action 2"
  ]
}}
"""

    # ---------------------------------------
    # 4. Ask local Llama AI
    # ---------------------------------------

    ai_analysis = ask_ai(prompt)

    # ---------------------------------------
    # 5. Return final analysis
    # ---------------------------------------

    return {
        "change": change_description,
        "database_schema": database_schema,
        **ai_analysis
    }