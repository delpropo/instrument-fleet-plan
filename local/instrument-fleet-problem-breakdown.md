# Instrument fleet: problem breakdown and planning notes

Date: 2026-10-01. Status: personal working notes, to do later. Companion to [[instrument-fleet-potential-problems]] (ranked problems), [[instrument-fleet-problem-statement]], and [[instrument-fleet-plan-detailed-explanation]].

Each problem from the ranked list is broken into smaller parts that can be done one at a time. Numbers match the ranks in [[instrument-fleet-potential-problems]]. Checkboxes are for tracking progress.

## Getting started: general planning suggestions

These are broader actions to take before or alongside the per-problem steps.

### Frame the work
- [ ] Write a one-paragraph goal statement centered on turnaround time and get it agreed with your manager and key stakeholders.
- [ ] Define "turnaround time" precisely: which start event and which end event. Everyone must measure it the same way.
- [ ] Decide what is in scope for you personally and what belongs to other teams (assay owners, facilities, IT, purchasing).
- [ ] List the decisions that are not yours to make, and who makes each one.

### Find out what already exists
- [ ] Ask whether anyone already tracks turnaround, outsourcing cost, instrument inventory, or sample tracking. Reuse before building.
- [ ] Collect existing spreadsheets, inventories, contracts, and procedures in one folder.
- [ ] Find out which LIMS, sample tracking, or scheduling systems are already licensed or in use.
- [ ] Ask other sites or groups in the organization that have brought assays in-house what went wrong for them.

### Talk to people
- [ ] Make a stakeholder list:
  - assay owners;
  - lab staff;
  - requesters;
  - facilities;
  - IT and security;
  - purchasing;
  - finance;
  - vendors.
- [ ] Hold short interviews with each group. Ask:
  - where they lose time;
  - what they would fix first;
  - what worries them about bringing assays in-house.
- [ ] Record the interview notes in this folder so the reasoning stays available.

### Start small and show results
- [ ] Pick one pilot assay family, for example one ELISA family, and take it end to end before scaling.
- [ ] Choose a small number of measures to report regularly:
  - turnaround per assay;
  - rerun rate;
  - instrument downtime;
  - share of assays outsourced.
- [ ] Share an early before-and-after result to build support and budget.

### Keep a decision log
- [ ] Start a decision log (what was decided, why, by whom, and what was rejected). Link it from this note.
- [ ] Record assumptions explicitly, for example "assay X can be brought in-house," and mark them confirmed or rejected later.

### Plan the resources
- [ ] Draft a rough multi-wave plan: wave 1 (pilot), wave 2 (high-volume families), later waves.
- [ ] For each wave, list the people, equipment, space, and budget it needs.
- [ ] Learn the budget cycle and capital request deadlines so requests are ready in time.

### Protect yourself from scope creep
- [ ] Keep the data platform (logs, registry) separate from the assay in-house program in planning, even though they connect.
- [ ] Re-rank [[instrument-fleet-potential-problems]] after the turnaround baseline exists, and drop or defer low-ranked items.

## Per-problem breakdown

### Tier 1: largest impact (ranks 1-9)

#### 1. No measured baseline of turnaround time per assay
- [ ] Define turnaround stages: request, sample receipt, queue, run start, run end, analysis, review, release.
- [ ] Find which of these timestamps already exist in any system.
- [ ] Build a simple spreadsheet or table template to capture them per assay.
- [ ] Collect data for a sample of assays first (for example the 20 highest-volume ones).
- [ ] Extend to all about 400 assays, marking each as in-house or outsourced.
- [ ] Summarize: median and worst-case turnaround per assay, and which stage takes the longest.

#### 2. Outsourcing delays
- [ ] List every outsourced assay with its vendor.
- [ ] Record per vendor:
  - shipping time;
  - queue time;
  - promised versus actual turnaround;
  - cost per sample.
- [ ] Identify the vendors and assays with the longest delays.
- [ ] Review contracts for service-level terms that can be enforced or renegotiated now.
- [ ] Mark candidates for in-house transfer (feeds problem 5).

#### 3. Not enough people with assay-specific expertise
- [ ] Group the about 400 assays into assay families (for example ELISA, qPCR, cell-based, chromatography).
- [ ] Make a skills matrix: who can run, troubleshoot, and review each family today.
- [ ] Find families with zero or one qualified person.
- [ ] Estimate the staffing each wave needs, by family.
- [ ] Decide hire versus train for each gap, and draft job descriptions or training plans.
- [ ] Set a target of at least two qualified people per assay in use.

#### 4. Manual assay execution does not scale
- [ ] List which assays are fully manual today and their weekly sample volume.
- [ ] Mark which steps are automatable (pipetting, plate washing, dilutions, plate reading).
- [ ] Group assays by the automation they need (liquid handler, plate washer, integrated workcell).
- [ ] Collect vendor options for each automation type and arrange demos.
- [ ] Compare manual versus automated hands-on time per plate for a pilot assay.

#### 5. No method for prioritizing assays
- [ ] Choose scoring criteria:
  - turnaround gain;
  - volume;
  - cost;
  - feasibility;
  - platform fit;
  - scientific importance.
- [ ] Agree on weights with stakeholders.
- [ ] Score a small set of assays as a trial and adjust the criteria.
- [ ] Score all assays and sort them into waves.
- [ ] Review the ranking with assay owners and management.

#### 6. Method transfer and validation take a long time
- [ ] Write a validation template per assay family:
  - accuracy;
  - precision;
  - range;
  - comparison to the outsourced vendor.
- [ ] Agree acceptance criteria with assay owners before starting.
- [ ] Plan sample sourcing for comparison runs (split samples between vendor and in-house).
- [ ] Run validation for the pilot assay and record how long each step took.
- [ ] Use the pilot to refine the template for later waves.

#### 7. Batching and queueing
- [ ] Measure queue time separately from run time for in-house assays.
- [ ] List each assay's batch size and why it was chosen (reagent cost, plate size, instrument time).
- [ ] Identify assays where samples routinely wait more than a set number of days.
- [ ] Explore:
  - smaller plate formats;
  - partial plates;
  - mixed-assay runs;
  - more frequent scheduled runs.
- [ ] Set a maximum wait time per assay and track it.

#### 8. Failed runs and reruns
- [ ] Start recording every rerun with assay, date, instrument, and cause.
- [ ] Define cause categories:
  - pipetting;
  - reagent;
  - instrument;
  - sample;
  - quality-control failure;
  - other.
- [ ] Review rerun data regularly to find the top causes.
- [ ] Address the top cause first (training, automation, reagent change, maintenance).
- [ ] Link instrument-caused reruns to instrument logs once the platform exists.

#### 9. Instrument downtime and slow troubleshooting
- [ ] Start a simple downtime log: instrument, start, end, cause, fix.
- [ ] Identify instruments with the most downtime and the assays they block.
- [ ] Gather manuals and past fixes for those instruments first.
- [ ] Follow the data platform phases in [[instrument-fleet-plan-detailed-explanation]], starting with the instrument types that block high-priority assays.

### Tier 2: large impact (ranks 10-19)

#### 10. Robot programming, scheduling, and integration
- [ ] Decide whether method programming will be done in-house, by the vendor, or by a contractor.
- [ ] List integration points: sample tracking, barcode readers, plate readers, data export.
- [ ] Require integration support (APIs, file export formats) in vendor evaluations.
- [ ] Build a method library structure so methods are versioned and reused across assays.
- [ ] Plan who maintains methods after go-live.

#### 11. Sample logistics, accessioning, and tracking
- [ ] Map the current sample path from arrival to assay to storage.
- [ ] Identify where samples wait or get lost.
- [ ] Check whether barcoding and a LIMS or tracking system exist.
- [ ] Define the minimum data to record at receipt: sample ID, time, location, requested assays.
- [ ] Pilot barcoded tracking for the pilot assay family.

#### 12. Manual data handoff and result transcription
- [ ] List every place results are copied by hand.
- [ ] Record the export formats each instrument supports.
- [ ] Define one standard result file format.
- [ ] Automate one export-import path for the pilot assay.
- [ ] Add sample ID checks on import.

#### 13. Post-run analysis is manual
- [ ] List the analysis steps per assay family (curve fitting, Ct calls, control checks).
- [ ] Find existing scripts or vendor software that already do this.
- [ ] Write or adopt a versioned analysis script for the pilot assay.
- [ ] Compare automated and manual results on past runs.
- [ ] Add automatic quality-control flags.

#### 14. Result review and sign-off
- [ ] Measure how long results wait for review.
- [ ] List who is authorized to review each assay.
- [ ] Train and authorize backup reviewers.
- [ ] Define rules under which results passing all checks can be released automatically, and get them approved.
- [ ] Make the review queue visible to the team.

#### 15. Capital procurement and budget
- [ ] Learn the capital request process, deadlines, and approval levels.
- [ ] Draft a capital list per wave from problems 4 and 18.
- [ ] Gather quotes and lead times from vendors.
- [ ] Write a business case using turnaround and outsourcing cost data (problems 1 and 2).
- [ ] Submit requests for wave 1 first.

#### 16. Space, facilities, and lab layout
- [ ] Inventory the available lab space.
- [ ] List space, power, HVAC, and network needs per planned instrument.
- [ ] Design pre- and post-PCR separation if PCR is coming in-house.
- [ ] Meet with facilities about lead times for changes.
- [ ] Draft a lab layout that follows the sample flow.

#### 17. Reagent and consumable supply
- [ ] List reagents and consumables per pilot assay with suppliers and lead times.
- [ ] Set up inventory tracking with reorder points.
- [ ] Identify single-source items and look for alternatives.
- [ ] Define the lot qualification procedure and schedule it ahead of need.
- [ ] Standardize consumables across assays where possible.

#### 18. Too many platforms; little standardization
- [ ] Map each assay to its platform and format.
- [ ] Identify clusters that could share a platform.
- [ ] Discuss with assay owners which assays could move to a shared format.
- [ ] Choose a small number of target platforms.
- [ ] Feed the result into procurement (problem 15) and prioritization (problem 5).

#### 19. Shared robotic platforms as single points of failure
- [ ] For each planned shared platform, list the assays that depend on it.
- [ ] Decide where a second unit or a backup instrument is justified.
- [ ] Write manual fallback procedures for critical assays.
- [ ] Negotiate service response times for shared platforms.

### Tier 3: moderate impact (ranks 20-35)

#### 20. Unclear assay ownership once in-house
- [ ] List the current owner of each assay.
- [ ] Define what "owner" means in-house (changes, validation, troubleshooting decisions).
- [ ] Assign an owner and a backup for each in-house assay.
- [ ] Record owners in the assay reference registry.

#### 21. Assay version changes not communicated or tracked
- [ ] Define what counts as a new assay version (reagent change, protocol change, cutoffs).
- [ ] Set up a change notification process with assay owners.
- [ ] Create the versioned assay reference registry (see [[instrument-fleet-plan-detailed-explanation]] section 3.8).

#### 22. Results not traceable
- [ ] Define the minimum metadata every result must carry: instrument key, software version, assay version, run ID.
- [ ] Check which metadata the current systems already capture.
- [ ] Add missing fields to the pilot assay's result format.

#### 23. Silent software updates
- [ ] Record the current software version of each instrument supporting a priority assay.
- [ ] Agree a rule that updates on these instruments need notice or approval.
- [ ] Ask vendors and IT how updates are pushed.
- [ ] Use declared-versus-observed version tracking once the platform exists.

#### 24. Vendor service response times and spare parts
- [ ] List service contracts and their response-time terms.
- [ ] Find instruments with no contract or slow response.
- [ ] Identify common failure parts and consider stocking them.
- [ ] Train staff in first-line fixes the vendor allows.

#### 25. Calibration and preventive maintenance downtime
- [ ] Collect maintenance schedules for priority instruments.
- [ ] Put them on a shared calendar.
- [ ] Schedule maintenance around demand and stagger redundant units.
- [ ] Track missed maintenance.

#### 26. PCR contamination
- [ ] Review the current PCR workflow and area separation.
- [ ] Define the one-way workflow and cleaning procedures.
- [ ] Set up routine environmental or no-template-control monitoring.
- [ ] Write a contamination response procedure.

#### 27. Training and competency on low-volume assays
- [ ] Write a training plan template per assay family.
- [ ] Define competency checks and their frequency.
- [ ] Identify low-volume assays at risk of skill loss.
- [ ] Schedule refresher runs or rotate staff.

#### 28. Staff turnover and knowledge loss
- [ ] Identify single-person knowledge areas from the skills matrix (problem 3).
- [ ] Have experts write down procedures and troubleshooting tips.
- [ ] Store them in the type packs or procedure library.
- [ ] Pair each expert with a backup.

#### 29. Low-volume assays and in-house cost
- [ ] Calculate in-house cost per sample versus outsourced cost for candidate assays.
- [ ] Set a volume threshold below which assays stay outsourced.
- [ ] Negotiate better turnaround for assays that stay outsourced.
- [ ] Review the threshold periodically.

#### 30. No status visibility for requesters
- [ ] Ask requesters what status information they want.
- [ ] Define simple status stages (received, queued, running, in review, released).
- [ ] Publish status from sample tracking once it exists.

#### 31. Sample ID and plate map errors
- [ ] Record ID and plate map errors as a rerun cause (problem 8).
- [ ] Introduce barcode scanning at plate setup.
- [ ] Generate plate maps from the system rather than typing them.
- [ ] Add automatic ID checks on import.

#### 32. Demand peaks
- [ ] Collect historical demand per assay to find peaks.
- [ ] Ask requesters for upcoming study timelines.
- [ ] Keep an overflow outsourcing option for peaks.
- [ ] Plan capacity for typical peaks, not averages.

#### 33. Instrument booking conflicts
- [ ] Find out how shared instruments are booked today.
- [ ] Introduce or improve a booking system.
- [ ] Review usage data to find instruments that need more capacity.

#### 34. Vendor contracts, licensing, and proprietary methods
- [ ] For each priority assay, check whether the method or kit is proprietary.
- [ ] Review contract terms that limit moving the assay.
- [ ] Involve purchasing or legal where needed.

#### 35. Possible compliance requirements
- [ ] Ask assay owners whether any assay supports clinical or regulated decisions.
- [ ] If so, find which requirements apply and the time they add.
- [ ] Plan validation and documentation to meet them.

### Tier 4: smaller or indirect impact (ranks 36-51)

#### 36. Instruments that cannot be networked or run unsupported operating systems
- [ ] Inventory instrument PCs: operating system, network status, vendor support.
- [ ] Work with IT on isolated network segments or gateways.
- [ ] Set up manual export drop folders where networking is not possible.

#### 37. Closed vendor software and no APIs
- [ ] Record export and API options per instrument type.
- [ ] Add API and open-format export to purchasing requirements.
- [ ] Ask vendors about middleware for existing instruments.

#### 38. Logs may lack software version and assay ID
- [ ] Collect sample logs from each type (Phase 1).
- [ ] Record whether each contains a version and assay ID.
- [ ] Define fallbacks (manual check, vendor query) for types that lack them.

#### 39. Parser effort for about 100 types
- [ ] Rank instrument types by how many priority assays they support.
- [ ] Build the type-pack template and test harness.
- [ ] Write parsers for the top types first.
- [ ] Document how others can add a parser.

#### 40. Log volume and network load
- [ ] Measure actual log sizes per type.
- [ ] Identify the largest sources (for example sequencers).
- [ ] Plan bandwidth limits and reduction to digests for those.
- [ ] Choose storage tiers and estimate cost.

#### 41. Many moving parts and owners
- [ ] List every platform component.
- [ ] Assign an owner to each.
- [ ] Build in phases and pilot with three types.

#### 42. Team adoption and change management
- [ ] Involve future users in design reviews.
- [ ] Keep the first tasks simple (one-file instrument additions).
- [ ] Hold short training sessions.
- [ ] Share turnaround improvements to show value.

#### 43. Missing or outdated procedures
- [ ] Inventory existing procedures for priority assays and instruments.
- [ ] Mark missing or outdated ones.
- [ ] Write procedures as part of each assay transfer.
- [ ] Keep procedures versioned.

#### 44. Sample stability and time windows
- [ ] Record the stability limit per assay.
- [ ] Flag time-sensitive samples at receipt.
- [ ] Prioritize them in scheduling.

#### 45. Irreversible deletion of raw logs
- [ ] Draft retention policies per type.
- [ ] Get data owner approval.
- [ ] Confirm deletion runs only after a verified parse.

#### 46. No dashboard or search interface
- [ ] List the questions people need answered.
- [ ] Start with simple reports that answer them.
- [ ] Build the dashboard later (Phase 4).

#### 47. Central collector server security
- [ ] Review the server design with IT security.
- [ ] Decide credential storage and access rules.
- [ ] Schedule periodic security reviews.

#### 48. Policy on external AI services
- [ ] Ask IT and data owners what may be sent to external AI services.
- [ ] Write the policy down.
- [ ] Share it with anyone building tools.

#### 49. Vendor manual redistribution rights
- [ ] List the manuals needed for priority instruments.
- [ ] Check license terms for sharing.
- [ ] Store binaries in controlled storage.

#### 50. Documentation copies drift
- [ ] Decide where documentation copies are needed (wiki, Obsidian, Google Docs).
- [ ] Set up generation from git with a commit stamp.
- [ ] Add a drift check.

#### 51. Naming collisions and nickname reuse
- [ ] Adopt type plus serial as the permanent key.
- [ ] Keep nicknames as editable aliases in the registry.

## Suggested order to start

1. The general planning steps above (goal, stakeholders, existing systems, decision log).
2. Problem 1 (turnaround baseline), problem 2 (outsourcing data), and problem 3 (skills matrix), because most later decisions depend on them.
3. Problem 5 (prioritization), then pick the pilot assay family.
4. For the pilot family, work through problems 4, 6, 10, 15, and 16 together.
5. Start the instrument data platform for the instrument types that support the pilot.
