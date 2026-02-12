# config/gemini_prompt_builder.py

def build_gemini_prompt(friendly_summary, mode="paragraph"):
    """
    Builds a Gemini prompt requesting structured, readable paragraphs with emojis.
    """
    prompt_lines = []
    prompt_lines.append("You are an expert public-health aware environmental assistant.")
    prompt_lines.append("Below are detected environmental objects and how many were found in the image.")
    prompt_lines.append("For each unique label, create a short report like this:")

    prompt_lines.append("Detected Item : [Friendly name with emoji if appropriate]")
    prompt_lines.append("")
    prompt_lines.append("Plausible/Possible Diseases : [list plausible diseases or vectors]")
    prompt_lines.append("")
    prompt_lines.append("Explanation : [brief scientific explanation not more than 3 lines, keep it short]")
    prompt_lines.append("")
    prompt_lines.append("Advice and Precaution To Follow : [short bullet points, use • for bullets, add emojis when suitable, not more than 3 points]")
    prompt_lines.append("")
    prompt_lines.append("Use calm, evidence-based, concise language. Avoid long paragraphs and JSON.")
    prompt_lines.append("Be creative with emojis to make it friendly and easy to read.")
    prompt_lines.append("Group duplicates (e.g., multiple bottles) into one report mentioning the count.")

    prompt_lines.append("\nDetected items:")
    for s in friendly_summary:
        prompt_lines.append(f"- {s['friendly']}")

    return "\n".join(prompt_lines)
