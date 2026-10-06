write a powershell script that pulls all the information off of the computer and saves it.

Software installed, versions, how much space.  What else?  Don't want to interfere with the computer.

Issues with virus and flash drives.


Updates needed.

Update the main readme.  Add an image to the top.  Make it look professional.  Add a summary of what the other readme sections are.


Create a new folder with assay information.  Move the assay information there. I want to create new files based on the information from the assay list.  Split the turnaround time column into minimum and maximum days with a single value both min and max being that value.  i also want to try to define what instrument type is used for each assay and have a new column with that informaiton.  For each of those, I want to have a new table which defines what those assays are for instance, define ELISA,   ICP-MS, HPLC, etc.  Ask me questions if you don't understand something.


Based on the turn around time information, I want to make a guess as to whether or not the assay is in house.

After all the new charts are created, I want to plot all of them out.  The idea behind the plots is to undertand which ones take the most time.  We don't have any information about how many of each are run so that will be left as an open question.


We need a corpus of knowledge.  Equipment manuals, troubleshooting documentation, vendor info.  
Should also make a page which contains websites where equipment updates can be looked at.  This could include newsletters, tech notes, etc.  
For example,
https://www.sartorius.com/en/products/biolayer-interferometry/bli-resources

https://www.sartorius.com/download/552304/generating-reliable-kinetic-data-for-protein-ligand-interactions-application-note-en-sartorius-data.pdf


Additional notes about the future.  By using AI to analyze multi-instrument lab data without upfront human bias, you could find complex biological patterns hidden across assays. The software automatically filters out noise and integrates subtle signals to create novel multivariant assays.  Assays like this have been found using machine learning and extensive data collections, but with AI tools, it becomes far easier to implement.  To do this effectively, you need to capture absolutely everything.  Even the actual person running an assay might be the cause of an anomaly and you don't want to go chasing everything because a lot will fail during validation.



Basic ideas

### 1. Organic Fraud & Origin Verification Signature

* **Assay Inputs Combined:** Heavy metal trace elements (ICP-MS), pesticide residue panels (LC-MS/MS), phytochemical polyphenol profiles (HPLC), and vitamin levels.
* **The Discovered Multianalyte Assay:** An algorithmic **"Organic & Provenance Authenticity Score."** Fraudulent produce or high-value foods (like organic olive oil, honey, or coffee) often pass individual testing because pesticides fall just below legal detection limits. However, an AI analyzing cross-panel data can discover that a specific ratio of soil heavy metals (like strontium or cadmium) combined with subtle, sub-threshold pesticide degradation products and altered phytochemical stress markers forms an unmistakable "fingerprint" of synthetic fertilizer use or misdeclared geographical origin. Counterfeiting is huge.  Makukia honey, etc.

### 2. Early Pathogen & Spoilage Risk Predictor

* **Assay Inputs Combined:** Protein degradation peptides (MALDI-TOF), vitamin oxidation ratios (HPLC), volatile phytochemical metabolites (GC-MS), and indicator microbe counts (qPCR).
* **The Discovered Multianalyte Assay:** A **"Pre-Symptomatic Contamination Risk Score"** for fresh produce or dairy. Standard microbial culture tests for *Listeria* or *Salmonella* can take 24–48 hours. By analyzing historical food safety runs, AI can spot a multi-panel pattern: as pathogens begin colonizing a crop, plants release subtle stress phytochemicals while bacteria secrete specific protein-cleaving enzymes that oxidize local vitamins. The AI creates a software signature that flags high-risk food batches in minutes—well before bacteria reach culturable detection limits.

### 3. Bioavailable Heavy Metal Toxicity Index

* **Assay Inputs Combined:** Heavy metal levels (lead, cadmium, arsenic via ICP-MS), phytate/polyphenol phytochemical profiles, protein concentration, and essential mineral co-factors (zinc, iron).
* **The Discovered Multianalyte Assay:** A **"Functional Toxicity & Bioavailability Score"** for plant-based foods and infant formulas. Standard assays measure total heavy metal content, but certain phytochemicals (like phytates and polyphenols) bind to heavy metals and prevent the human gut from absorbing them. By training an algorithm across toxicology and nutritional panels, AI can discover a multi-analyte formula that predicts *true bioavailable toxicity*, preventing safe, nutrient-dense crops from being needlessly discarded due to harmless, bound trace elements.
Here are additional examples of multianalyte assays that can be discovered by applying machine learning to multi-instrument food testing datasets:

### 4. Thermal Processing Toxin Index (Acrylamide & AGE Risk)

* **Assay Inputs Combined:** Free amino acid/protein panels, reducing sugar levels, trace heavy metal catalysts (iron/copper via ICP-MS), and processing contaminants (acrylamide, hydroxymethylfurfural via LC-MS/MS).
* **The Discovered Multianalyte Assay:** A **"Thermal Degradation & Process-Toxin Score"** for baked goods, coffee, and fried foods. High-heat industrial processing triggers the Maillard reaction, forming hazardous compounds like acrylamide and advanced glycation end-products (AGEs). While measuring individual heat-toxins requires slow, expensive chromatography, an AI trained on multi-panel historical runs discovers that combining raw amino acid profiles, sugar ratios, and trace oxidation markers creates a rapid computational proxy. This proxy predicts overall processing toxicity and nutrient loss before individual toxins exceed safety thresholds.

### 5. Pre-Harvest Crop Stress & Mycotoxin Susceptibility Score

* **Assay Inputs Combined:** Plant defense phytochemicals (salicylic acid, flavonoids), essential mineral ratios (zinc, copper), nitrogen/protein content, and mold DNA or fungal mycotoxin panels (aflatoxins, ochratoxins).
* **The Discovered Multianalyte Assay:** A **"Fungal Contamination Susceptibility Index"** for stored grains, nuts, and corn. Fungi produce deadly mycotoxins when crops experience environmental stress. By sifting through historical field quality checks, an AI discovers that a specific drop in protective antioxidant phytochemicals—combined with elevated zinc-to-copper ratios and sub-clinical fungal DNA traces—creates a predictive signature. This signature flags grain batches that are at high risk of developing dangerous mycotoxin blooms during transport weeks before the toxins reach detectable levels.

### 6. High-Value Food Dilution & Botanical Authenticity Fingerprint

* **Assay Inputs Combined:** Polyphenol and flavonoid phytochemical profiles (HPLC), organic acid levels, vitamin isomers (like natural vs. synthetic Vitamin C), and background pesticide micro-traces.
* **The Discovered Multianalyte Assay:** A **"Synthetic Adulteration & Origin Fingerprint"** for premium olive oils, fruit juices, honey, and wine. Counterfeiters often dilute expensive products with cheap fruit juices or canola oil and pad them with synthetic vitamins or colorants to pass standard checks. While a single added vitamin might look genuine on a basic test, an AI analyzing the multi-analyte matrix discovers that the exact ratio of native phytochemicals to trace pesticide degradation products forms an un-fakeable fingerprint—detecting even a 1% to 2% synthetic dilution that standard tests miss.

### 7. Dynamic Meat & Seafood Freshness Predictor

* **Assay Inputs Combined:** Protein breakdown products (biogenic amines like histamine, putrescine), volatile microbial metabolites (GC-MS), lipid-soluble vitamin depletion rates (Vitamin E), and trace oxidation metals.
* **The Discovered Multianalyte Assay:** A **"Real-Time Spoilage Velocity Score"** for fresh fish and meat supply chains. Spoilage in seafood can lead to scombroid poisoning caused by histamine accumulation. Standard bacterial culture tests take days, but an AI running on historical storage datasets can link early-stage vitamin E depletion with trace biogenic amine ratios to create a real-time freshness score. This score accurately predicts the exact remaining shelf life and histamine risk for individual shipments under varying temperature conditions.

This is called **Forensic Origin Fingerprinting** or a **Source Attribution Model**.

Instead of just telling you *if* a sample is counterfeit, an AI trained on multi-instrument data can act like a chemical "GPS" to tell you *where* the counterfeit was produced or processed, pinpointing the specific region, farm, or clandestine factory.

Here is how an AI builds a multianalyte signature to track down counterfeiters:

### 1. Soil & Water "Geographic GPS" Fingerprint

* **Assay Inputs:** Stable isotope ratios (carbon, oxygen, hydrogen, strontium) and trace mineral profiles (ICP-MS).
* **How the AI Tracks the Source:** Local rainfall and regional soil geology leave permanent isotopic signatures in agricultural goods. If counterfeit coffee labeled as "Hawaiian Kona" is seized, an AI model compares its heavy metal ratios (e.g., strontium-to-rubidium) and water isotopes against environmental databases. The AI can discover that the chemical fingerprint matches the exact soil and groundwater profile of a specific region in a different country, exposing the supplier's location.

### 2. Processing Facility & Solvent "Batch DNA"

* **Assay Inputs:** Trace organic solvents (GC-MS), synthetic dye impurities, and background metal micro-contaminants.
* **How the AI Tracks the Source:** Counterfeit premium spirits, olive oils, or honey are often blended in illicit facilities using cheap, unregulated industrial equipment and local tap water. An AI analyzing cross-panel data can discover that micro-traces of specific industrial lubricants, distinct tap-water minerals, and unique chemical impurities always appear together in counterfeit batches sold across different cities—linking seemingly unrelated fake products back to the same underground bottling plant.

### 3. Agrochemical & Pesticide "Supply Chain Trail"

* **Assay Inputs:** Degradation sub-products of fertilizers, fungicides, and pesticides (LC-MS/MS).
* **How the AI Tracks the Source:** Different countries allow or ban specific agricultural chemicals. When fake "organic" produce or herbs enter the market, an AI running pattern recognition across pesticide panels can detect sub-clinical traces of region-specific synthetic fertilizers or banned local pesticides. By mapping these chemical residues, the AI narrows down the origin to a specific country or agricultural zone where those specific chemicals are commercially used.

### 4. Environmental Microbiome & DNA Footprinting

* **Assay Inputs:** Environmental DNA (eDNA) sequencing and fungal/bacterial microbiome profiles.
* **How the AI Tracks the Source:** Dust, pollen, and endemic microbes from the air get trapped in food during harvesting and packaging. An AI model can cross-reference the environmental micro-flora found inside a counterfeit sample against global biodiversity maps, identifying the plant species and regional mold strains native to the warehouse where the food was illegally packaged.