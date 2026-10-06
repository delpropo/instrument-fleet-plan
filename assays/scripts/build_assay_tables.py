"""Build assay reference tables from lightlabs-assays.tsv.

Reads the untouched original and writes (next to it):
  assays-instrument-turnaround.csv  one row per assay: turnaround min/max days, in-house guess, instrument type guess
  instrument-types.csv / .md        definition table for every instrument type used

Instrument types are a guess, not vendor data. Each row records how the guess was made
(stated in text, inferred from the assay name, or category default) and a confidence.
Run from anywhere:  python assays/scripts/build_assay_tables.py
"""
import re
from pathlib import Path

import pandas as pd

ASSAY_DIR = Path(__file__).resolve().parent.parent
SOURCE = ASSAY_DIR / "lightlabs-assays.tsv"

# --- Instrument type definitions -------------------------------------------------------------
# name -> (group, what it is, what it is used for in these assays)
INSTRUMENT_TYPES = {
    "HPLC": (
        "Chromatography",
        "High-performance liquid chromatography. A pump pushes a liquid sample through a packed column that "
        "separates the compounds; a detector (UV/DAD, fluorescence, ELSD, refractive index) measures each one.",
        "Quantifying known actives, vitamins, and phytochemicals by retention time and peak area.",
    ),
    "LC-MS/MS": (
        "Chromatography + mass spectrometry",
        "Liquid chromatography coupled to a tandem (triple-quadrupole) mass spectrometer. The LC separates "
        "compounds and the MS identifies and quantifies them by mass, to very low levels.",
        "Trace contaminants (pesticides, mycotoxins, PFAS, residues) and complex matrices.",
    ),
    "GC-MS": (
        "Chromatography + mass spectrometry",
        "Gas chromatography coupled to a mass spectrometer. Volatile compounds are separated in a heated "
        "column and identified by mass.",
        "Volatile and semi-volatile compounds such as solvent residues and some pesticides.",
    ),
    "GC-FID": (
        "Chromatography",
        "Gas chromatography with a flame ionization detector. Volatile compounds are separated in a heated "
        "column and measured by the current they produce when burned.",
        "Fatty acid (FAME) profiles and other volatile organic compounds.",
    ),
    "ICP-MS": (
        "Elemental analysis",
        "Inductively coupled plasma mass spectrometry. A sample is turned into a plasma, and a mass "
        "spectrometer counts the ions of each element.",
        "Heavy metals and trace elements at very low levels (lead, arsenic, cadmium, mercury, and others).",
    ),
    "ICP-OES": (
        "Elemental analysis",
        "Inductively coupled plasma optical emission spectrometry. A plasma excites the elements, which emit "
        "light at element-specific wavelengths.",
        "Minerals and nutritional elements at higher concentrations (calcium, magnesium, zinc, and others).",
    ),
    "ELISA": (
        "Immunoassay",
        "Enzyme-linked immunosorbent assay. Antibodies bind a target protein in a multi-well plate, and an "
        "enzyme reaction produces a color or signal read by a plate reader.",
        "Allergens, specific proteins, and some toxins.",
    ),
    "PCR / qPCR": (
        "Molecular biology",
        "Polymerase chain reaction. A thermal cycler copies a chosen DNA sequence; in qPCR (real-time PCR) "
        "the signal is measured each cycle to detect and count the target.",
        "Detecting or identifying organisms, species, and GMOs by DNA.",
    ),
    "UV-Vis spectrophotometer": (
        "Spectroscopy",
        "Measures how much ultraviolet or visible light a sample absorbs. Used with a color-forming "
        "(colorimetric) or enzymatic reaction, often in a plate reader.",
        "Total content assays, enzyme activities, and colorimetric tests.",
    ),
    "FTIR": (
        "Spectroscopy",
        "Fourier-transform infrared spectroscopy. Measures infrared absorption to produce a chemical "
        "fingerprint of the material.",
        "Identity confirmation and screening.",
    ),
    "HPTLC": (
        "Chromatography",
        "High-performance thin-layer chromatography. Samples are separated on a coated plate and compared "
        "by the pattern of bands.",
        "Botanical identification (fingerprint comparison with a reference).",
    ),
    "Ion chromatography": (
        "Chromatography",
        "Separates ions (such as nitrate, sulfate, and fluoride) on an ion-exchange column and measures "
        "them with a conductivity detector.",
        "Anions and cations in water, food, and ingredients.",
    ),
    "Ion-selective electrode": (
        "Electrochemistry",
        "A probe that responds to the activity of one specific ion in solution.",
        "Fluoride and similar single-ion measurements.",
    ),
    "Titration (incl. Karl Fischer)": (
        "Wet chemistry",
        "A reagent of known concentration is added until a reaction endpoint is reached, then the amount "
        "used is converted to a result. An automatic titrator or Karl Fischer titrator detects the endpoint.",
        "Peroxide value, free fatty acids, sulfur dioxide, and water by Karl Fischer.",
    ),
    "Gravimetric (balance, oven, furnace)": (
        "Wet chemistry",
        "The sample is weighed before and after drying, heating, ashing, or digestion; the weight change "
        "is the result.",
        "Moisture, ash, fiber, and total dissolved solids.",
    ),
    "Combustion nitrogen analyzer": (
        "Elemental analysis",
        "Burns the sample at high temperature and measures the released nitrogen gas (Dumas method). "
        "Nitrogen is converted to protein.",
        "Total protein.",
    ),
    "Microbial culture (plating and incubation)": (
        "Microbiology",
        "Samples are diluted, spread on selective or general agar, incubated, and colonies are counted or "
        "identified. Uses incubators, a biosafety cabinet, and plate counting.",
        "Plate counts, yeast and mold, coliforms, and specific pathogens.",
    ),
    "Flow cytometer": (
        "Microbiology",
        "Passes stained cells one at a time through a laser and counts them by their fluorescence.",
        "Counting viable organisms such as probiotics (AFU).",
    ),
    "pH meter": (
        "Physical measurement",
        "A glass electrode that measures hydrogen-ion activity.",
        "pH.",
    ),
    "Water activity meter": (
        "Physical measurement",
        "Measures the relative humidity of the air in a sealed chamber over the sample, which gives water "
        "activity (aw).",
        "Stability and microbial-risk assessment.",
    ),
    "Viscometer": (
        "Physical measurement",
        "Measures resistance to flow (for example a Brookfield spindle viscometer).",
        "Viscosity.",
    ),
    "Refractometer": (
        "Physical measurement",
        "Measures how much light bends in a liquid, which reports dissolved solids (Brix).",
        "Brix.",
    ),
    "Turbidimeter": (
        "Physical measurement",
        "Measures light scattered by suspended particles.",
        "Turbidity.",
    ),
    "Particle size analyzer": (
        "Physical measurement",
        "Laser diffraction instrument that reports the size distribution of particles in a powder or liquid.",
        "Particle size distribution.",
    ),
    "Sieve shaker": (
        "Physical measurement",
        "Mechanical agitator with stacked mesh sieves; the fraction retained on each is weighed.",
        "Particle size by sieve.",
    ),
    "Melting point apparatus": (
        "Physical measurement",
        "Heats a sample in a capillary tube and records the temperature at which it melts.",
        "Melting point.",
    ),
    "Headspace gas analyzer": (
        "Physical measurement",
        "Samples the gas inside a sealed package and measures oxygen and carbon dioxide.",
        "Package headspace O2 and CO2.",
    ),
    "Disintegration tester": (
        "Physical measurement",
        "Moves tablets or capsules in a heated bath and times how long they take to break apart.",
        "Disintegration and rupture.",
    ),
    "Analytical balance": (
        "Physical measurement",
        "A precision scale.",
        "Weight and count checks (unit weight, average piece weight, pieces per container).",
    ),
    "Visual / sensory inspection": (
        "Manual",
        "A trained analyst examines the sample by eye, smell, or touch against a standard. No instrument "
        "is required.",
        "Appearance, odor, color match, foreign matter, and container closure.",
    ),
}

# --- Instrument detection --------------------------------------------------------------------
# Instrument named in the testing text. Order is priority (most specific first).
TEXT_RULES = [
    ("LC-MS/MS", r"LC-MS|LC/MS|UPLC-MS|UHPLC-MS|liquid chromatography[ -]+(?:coupled with |with )?(?:tandem )?mass"),
    ("GC-MS", r"GC-MS|GC/MS|gas chromatography[ -]+(?:coupled with )?mass"),
    ("ICP-MS", r"ICP-MS|inductively coupled plasma[ -]+mass"),
    ("ICP-OES", r"ICP-OES|ICP-AES|optical emission"),
    ("HPLC", r"HPLC|UHPLC|high[- ]performance liquid|liquid chromatograph"),
    ("GC-FID", r"GC-FID|flame ionization|\bGC\b|gas chromatograph"),
    ("ELISA", r"ELISA|enzyme-linked immuno"),
    ("PCR / qPCR", r"qPCR|real-time PCR|\bPCR\b|polymerase chain"),
    ("FTIR", r"FTIR|infrared"),
    ("Ion chromatography", r"ion chromatograph|\bIC\b"),
    ("HPTLC", r"HPTLC|\bTLC\b"),
    ("Flow cytometer", r"flow cytometr"),
    ("Titration (incl. Karl Fischer)", r"Karl Fischer"),
    ("UV-Vis spectrophotometer", r"UV-Vis|spectrophotomet|colorimetric"),
]

# Used only when the text names no instrument: (regex on assay name, type, confidence).
NAME_RULES = [
    (r"^(appearance|odor|organoleptics|color match|foreign matter|container closure)", "Visual / sensory inspection", "high"),
    (r"^(unit bag weight|average piece)", "Analytical balance", "high"),
    (r"^ph$", "pH meter", "high"),
    (r"^water activity", "Water activity meter", "high"),
    (r"^viscosity", "Viscometer", "high"),
    (r"^brix", "Refractometer", "high"),
    (r"^turbidity", "Turbidimeter", "high"),
    (r"^particle size by sieve", "Sieve shaker", "high"),
    (r"^particle size", "Particle size analyzer", "high"),
    (r"^melting point", "Melting point apparatus", "high"),
    (r"^headspace", "Headspace gas analyzer", "high"),
    (r"^(disintegration|rupture)", "Disintegration tester", "medium"),
    (r"^(ash|moisture analysis|total dissolved solids|crude fiber|dietary fiber)", "Gravimetric (balance, oven, furnace)", "high"),
    (r"^protein( on dry basis)?$|^pdcaas", "Combustion nitrogen analyzer", "medium"),
    (r"^(peroxide value|free fatty acid|sulfur dioxide)", "Titration (incl. Karl Fischer)", "medium"),
    (r"^p-anisidine", "UV-Vis spectrophotometer", "high"),
    (r"^(beta glucan|bromelain|lactase|nattokinase)", "UV-Vis spectrophotometer", "medium"),
    (r"^afu enumeration", "Flow cytometer", "high"),
    (r"^fatty acid profile", "GC-FID", "high"),
    (r"^fluoride", "Ion-selective electrode", "medium"),
    (r"^(nitrate|nitrite|sulfate)", "Ion chromatography", "medium"),
    (r"^(hardness|iodine|thallium)", "ICP-OES", "medium"),
    (r"^(2,4-d|glyphosate|bpa|pfas|acrylamide|mycotoxins|low-level creatinine)", "LC-MS/MS", "medium"),
    (r"^(astaxanthin|ashwagandha total|ginsenoside|choline|hyaluronic|igg)", "HPLC", "medium"),
    (r"^casein", "ELISA", "medium"),
    (r"^cyanide", "UV-Vis spectrophotometer", "low"),
    (r"(\bID\b|root id|black pepper)", "HPTLC", "low"),
    (r"(bacillus|coliform|e\. coli|enterobacteriaceae|candida|listeria|pseudomonas|shigella|staphylococcus|"
     r"clostridia|lactic acid|lactospore|mold|yeast|plate count|micro panel|bacteria)", "Microbial culture (plating and incubation)", "medium"),
]

# Weak text hints, checked after name rules.
WEAK_TEXT_RULES = [
    ("Microbial culture (plating and incubation)", r"plated|plating|agar|incubat|cultured"),
    ("Titration (incl. Karl Fischer)", r"titrat"),
    ("Gravimetric (balance, oven, furnace)", r"weighed|gravimetric"),
]

# In-house guess from the longest quoted turnaround. A guess only: short turnaround suggests the work is
# done in the lab itself; long turnaround suggests shipping to and queuing at another lab.
IN_HOUSE_MAX_DAYS = 7
OUTSOURCED_MIN_DAYS = 11

CATEGORY_DEFAULTS = {
    "Contaminants": "LC-MS/MS",
    "Elemental": "ICP-MS",
    "Allergen": "ELISA",
    "Microbial": "Microbial culture (plating and incubation)",
    "Phytochemical, Vitamin, and Actives": "HPLC",
    "Preservatives and Additives": "HPLC",
}


def in_house_guess(max_days):
    if max_days <= IN_HOUSE_MAX_DAYS:
        return "likely in house"
    if max_days >= OUTSOURCED_MIN_DAYS:
        return "likely outsourced"
    return "uncertain"


def normalize(text):
    return re.sub(r"[\u2010-\u2015\u2212]", "-", text)


def detect(row):
    # Matched phrases are removed so that e.g. "liquid chromatography coupled with tandem mass
    # spectrometry" is not also counted as plain HPLC.
    text = normalize(row["TESTING PROCESS"]) + " || " + normalize(row["ABOUT THIS TEST"])
    found = []
    for name, pattern in TEXT_RULES:
        if re.search(pattern, text, re.I):
            found.append(name)
            text = re.sub(pattern, " ", text, flags=re.I)
    if found:
        # A UV-Vis/plate-reader mention beside HPLC or ELISA is just the detector, not a second method.
        others = [f for f in found[1:] if f != "UV-Vis spectrophotometer"]
        return found[0], found[1:], "stated in text", "medium" if others else "high"

    process = normalize(row["TESTING PROCESS"])
    about = normalize(row["ABOUT THIS TEST"])
    assay = normalize(row["Assay"]).lower()
    for pattern, name, confidence in NAME_RULES:
        if re.search(pattern, assay):
            return name, [], "inferred from assay name", confidence

    full = process + " " + about
    for name, pattern in WEAK_TEXT_RULES:
        if re.search(pattern, full, re.I):
            return name, [], "inferred from text", "medium"

    default = CATEGORY_DEFAULTS.get(row["CATEGORY"], "")
    if default:
        return default, [], "category default", "low"
    return "Unknown", [], "no information", "low"


def parse_turnaround(value):
    numbers = [int(n) for n in re.findall(r"\d+", value)]
    if not numbers:
        return None, None
    return numbers[0], numbers[-1]


def main():
    df = pd.read_csv(SOURCE, sep="\t", encoding="utf-8-sig", dtype=str).fillna("")

    out = pd.DataFrame({
        "assay": df["Assay"],
        "category": df["CATEGORY"],
        "turnaround_original": df["TURNAROUND"],
        "min_sample_size": df["MINIMUM SAMPLE SIZE"],
    })
    days = df["TURNAROUND"].map(parse_turnaround)
    out["turnaround_min_days"] = days.map(lambda d: d[0]).astype("Int64")
    out["turnaround_max_days"] = days.map(lambda d: d[1]).astype("Int64")
    out = out[["assay", "category", "turnaround_original", "turnaround_min_days", "turnaround_max_days", "min_sample_size"]]

    out["in_house_guess"] = out["turnaround_max_days"].map(in_house_guess)
    out["in_house_basis"] = out["turnaround_max_days"].map(
        lambda d: f"max turnaround {d} days (in house <= {IN_HOUSE_MAX_DAYS}, outsourced >= {OUTSOURCED_MIN_DAYS})"
    )

    detected = df.apply(detect, axis=1)
    out["instrument_type"] = detected.map(lambda d: d[0])
    out["other_instruments_mentioned"] = detected.map(lambda d: "; ".join(d[1]))
    out["instrument_basis"] = detected.map(lambda d: d[2])
    out["instrument_confidence"] = detected.map(lambda d: d[3])

    unknown = set(out["instrument_type"]) - set(INSTRUMENT_TYPES) - {"Unknown"}
    assert not unknown, f"missing definitions: {unknown}"
    assert out["turnaround_min_days"].notna().all(), "unparsed turnaround"

    out.to_csv(ASSAY_DIR / "assays-instrument-turnaround.csv", index=False)

    counts = out["instrument_type"].value_counts()
    types = pd.DataFrame(
        [
            {
                "instrument_type": name,
                "group": group,
                "what_it_is": what,
                "used_for_in_these_assays": use,
                "assay_count": int(counts.get(name, 0)),
            }
            for name, (group, what, use) in INSTRUMENT_TYPES.items()
        ]
    ).sort_values(["group", "instrument_type"])
    types.to_csv(ASSAY_DIR / "instrument-types.csv", index=False)

    lines = [
        "# Instrument types",
        "",
        "Generated by `scripts/build_assay_tables.py`; do not edit by hand.",
        "Counts are the number of assays whose primary instrument type is this one (a guess, see the README).",
        "",
        "| Instrument type | Group | What it is | Used for in these assays | Assays |",
        "|:--|:--|:--|:--|--:|",
    ]
    for _, r in types.iterrows():
        lines.append(
            f"| **{r.instrument_type}** | {r.group} | {r.what_it_is} | {r.used_for_in_these_assays} | {r.assay_count} |"
        )
    (ASSAY_DIR / "instrument-types.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(out)} assays")
    print(out["instrument_confidence"].value_counts().to_string())
    print(out["instrument_basis"].value_counts().to_string())
    print(counts.to_string())


if __name__ == "__main__":
    main()
