#!/usr/bin/env python3
"""
Update README.md with the current list of cardinals
"""
import json
import re


def update_readme_with_cardinals(json_file='cardinals.json', readme_file='README.md'):
    """
    Updates the README.md file with a list of all cardinals from the JSON file.
    """
    # Load cardinal data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cardinals = data['Cardinals']

    # Generate cardinal list markdown
    cardinal_list = ["## Complete List of Cardinals\n"]
    cardinal_list.append(f"Total: **{len(cardinals)} cardinals**\n\n")

    # Group by eligibility
    eligible = [c for c in cardinals if c.get('PapalConclaveEligible', False)]
    ineligible = [c for c in cardinals if not c.get('PapalConclaveEligible', False)]

    cardinal_list.append(f"- **Eligible to vote in Papal Conclave**: {len(eligible)}\n")
    cardinal_list.append(f"- **Ineligible to vote** (over 80 years old): {len(ineligible)}\n\n")

    # Create table
    cardinal_list.append("| Rank | Name | Country | Born | Office |\n")
    cardinal_list.append("|------|------|---------|------|--------|\n")

    for cardinal in cardinals:
        rank = cardinal.get('Rank', '')
        name = cardinal.get('Name', '')
        country = cardinal.get('Country', '')
        born = cardinal.get('Born', '')
        office = cardinal.get('Office', '')[:80]  # Truncate long offices

        # Add asterisk for ineligible cardinals
        if not cardinal.get('PapalConclaveEligible', False):
            name = f"{name}*"

        cardinal_list.append(f"| {rank} | {name} | {country} | {born} | {office} |\n")

    cardinal_list.append("\n*\\* Cardinals over 80 years old are ineligible to vote in a papal conclave*\n")

    cardinal_list_md = ''.join(cardinal_list)

    # Read existing README
    with open(readme_file, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Define markers for the cardinal list section
    start_marker = "<!-- CARDINAL_LIST_START -->"
    end_marker = "<!-- CARDINAL_LIST_END -->"

    # Check if markers exist
    if start_marker in readme_content and end_marker in readme_content:
        # Replace content between markers
        pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
        new_section = f"{start_marker}\n{cardinal_list_md}\n{end_marker}"
        readme_content = re.sub(pattern, new_section, readme_content, flags=re.DOTALL)
    else:
        # Append to end of file
        readme_content += f"\n\n{start_marker}\n{cardinal_list_md}\n{end_marker}\n"

    # Write updated README
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✓ README updated with {len(cardinals)} cardinals")
    print(f"  - Eligible for conclave: {len(eligible)}")
    print(f"  - Ineligible (over 80): {len(ineligible)}")


if __name__ == '__main__':
    update_readme_with_cardinals()
