#!/usr/bin/env python3
"""
Export cardinal data to multiple formats: JSON, CSV, XML, YAML
"""
import json
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom


def export_to_csv(json_file='cardinals.json', csv_file='cardinals.csv'):
    """Export cardinals data to CSV format"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cardinals = data['Cardinals']

    if not cardinals:
        print("No cardinals found in JSON file")
        return

    # Get all possible keys
    fieldnames = list(cardinals[0].keys())

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cardinals)

    print(f"✓ CSV exported: {csv_file} ({len(cardinals)} cardinals)")


def export_to_xml(json_file='cardinals.json', xml_file='cardinals.xml'):
    """Export cardinals data to XML format"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cardinals = data['Cardinals']

    # Create XML structure
    root = ET.Element('Cardinals')
    root.set('total', str(len(cardinals)))

    for cardinal in cardinals:
        cardinal_elem = ET.SubElement(root, 'Cardinal')
        for key, value in cardinal.items():
            child = ET.SubElement(cardinal_elem, key)
            child.text = str(value)

    # Pretty print
    xml_str = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent="  ")

    with open(xml_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)

    print(f"✓ XML exported: {xml_file} ({len(cardinals)} cardinals)")


def export_to_yaml(json_file='cardinals.json', yaml_file='cardinals.yaml'):
    """Export cardinals data to YAML format"""
    try:
        import yaml
    except ImportError:
        print("⚠ PyYAML not installed. Skipping YAML export.")
        print("  Install with: pip install pyyaml")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cardinals = data['Cardinals']

    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump({'Cardinals': cardinals}, f, allow_unicode=True, sort_keys=False)

    print(f"✓ YAML exported: {yaml_file} ({len(cardinals)} cardinals)")


def export_all_formats(json_file='cardinals.json'):
    """Export to all available formats"""
    print("Exporting cardinal data to multiple formats...")
    export_to_csv(json_file)
    export_to_xml(json_file)
    export_to_yaml(json_file)
    print("\n✓ All exports completed!")


if __name__ == '__main__':
    export_all_formats()
