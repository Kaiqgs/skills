import json
import logging
from typing import Dict
from app.markdown_llm import get_anthropic_client, MODEL, MAX_OUTPUT_TOKENS


def build_quality_evaluation_prompt(original_sample: str, cleaned_sample: str, iteration_num: int) -> str:
    return f"""You are evaluating the quality of documentation cleaning. You will see a BEFORE and AFTER sample.

**ITERATION:** {iteration_num}

**YOUR TASK:**
Evaluate how well the cleaning removed noise while preserving valuable documentation content.

**BEFORE CLEANING (excerpt - first 3000 chars):**
```
{original_sample[:3000]}
```

**AFTER CLEANING (excerpt - first 3000 chars):**
```
{cleaned_sample[:3000]}
```

**EVALUATION CRITERIA:**

Good cleaning should:
1. Remove navigation bars, footers, breadcrumbs, social media links
2. Remove duplicate/repetitive sections
3. Preserve ALL documentation headings, code examples, and core content
4. Maintain readability and structure

Bad cleaning would:
1. Remove actual documentation content
2. Remove code examples or headings
3. Be too conservative (leave obvious noise)
4. Be too aggressive (remove useful content)

**CRITICAL: YOU MUST PROVIDE ACTIONABLE FEEDBACK**

Even if the cleaning quality is already high (0.85+), you MUST provide specific, actionable improvements in the "improvements_needed" field. Never return empty arrays.

Examples of actionable feedback by quality level:
- **Quality 0.90+**: "Remove 'Edit this page' links", "Clean up redundant whitespace", "Strip version badges"
- **Quality 0.70-0.90**: "More aggressive footer removal", "Target language selector patterns", "Remove social media icons"
- **Quality <0.70**: "Critical: preserving too much navigation", "Remove duplicate 'Getting Started' sections"

**OUTPUT FORMAT (JSON only, no markdown):**
{{
  "quality_score": 0.85,
  "assessment": "Brief 2-3 sentence summary of cleaning quality",
  "issues_found": ["Specific issue 1", "Specific issue 2"],
  "improvements_needed": ["Actionable improvement 1", "Actionable improvement 2", "Actionable improvement 3"],
  "patterns_removed": ["footer", "navigation"],
  "content_preserved": true
}}

**IMPORTANT:**
- Return ONLY valid JSON, no markdown formatting, no code blocks
- "improvements_needed" MUST contain at least 2-3 specific, actionable items
- Be specific about what patterns or elements to target"""


def evaluate_cleaning_quality_with_llm(
    original_sample: str,
    cleaned_sample: str,
    iteration_num: int
) -> Dict:
    client = get_anthropic_client()

    prompt = build_quality_evaluation_prompt(original_sample, cleaned_sample, iteration_num)

    logging.info(f"  → Asking Claude to evaluate cleaning quality...")

    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_OUTPUT_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()

    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "", 1)
    if response_text.startswith("```"):
        response_text = response_text.replace("```", "", 1)
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    response_text = response_text.strip()

    try:
        evaluation = json.loads(response_text)
    except json.JSONDecodeError as e:
        logging.warning(f"  ⚠ Failed to parse LLM evaluation as JSON: {e}")
        logging.warning(f"  Response was: {response_text[:200]}...")
        evaluation = {
            "quality_score": 0.5,
            "assessment": "Failed to parse evaluation",
            "issues_found": ["JSON parse error"],
            "improvements_needed": ["Fix evaluation response format"],
            "patterns_removed": [],
            "content_preserved": False
        }

    evaluation["token_usage"] = {
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens
    }

    logging.info(f"  ✓ Quality score: {evaluation.get('quality_score', 'N/A')}")
    logging.info(f"  → Assessment: {evaluation.get('assessment', 'N/A')}")

    return evaluation
