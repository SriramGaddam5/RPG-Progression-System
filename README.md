# RPG Progression System

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)

A Python-based simulation system for modeling and balancing RPG progression mechanics, including combat, loot, experience, and story progression.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Basic Simulation](#basic-simulation)
  - [Custom Configuration](#custom-configuration)
  - [Visualizing Progression Curves](#visualizing-progression-curves)
  - [Configuration Files](#configuration-files)
- [Core Modules](#core-modules)
- [Data Structures](#data-structures)
- [Output](#output)
- [Configuration Tips](#configuration-tips)
- [Understanding the Visualizations](#understanding-the-visualizations)
- [Use Cases](#use-cases)
- [Example Workflow](#example-workflow)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

This project simulates a player's journey through an RPG campaign, tracking progression through levels, equipment, and story beats. It's designed to help game designers test and balance progression curves, difficulty scaling, and reward systems before implementing them in a game.

## Features

- **Player Progression Simulation**: Models XP gain, leveling, and character growth with configurable XP curves
- **Combat & Non-Combat Systems**: Simulates both combat encounters and skill-based challenges with dynamic success rates
- **Death & Repair System**: Includes death mechanics with equipment repair costs and gold penalties
- **Loot System**: Equipment generation with quality tiers (Common/Rare/Epic/Legendary) and item power scaling across zones
- **Multi-Tier Gear System**: Zone-based gear tiers (T1-T4) with different quality distributions
- **Story Beat Integration**: Follows the Hero's Journey structure with configurable story stages
- **JSON-Based Configuration**: Primary configuration via `Inputs.json` with comprehensive parameter control
- **Regression Testing**: Built-in assertion and regression testing framework for balance validation
- **Detailed Data Logging**: Outputs detailed simulation results with turn-by-turn tracking
- **Data Dictionary**: Comprehensive documentation of all data fields and calculations
- **Visual Analytics**: Matplotlib-based curve visualization for success rates and XP progression

## Project Structure

```
RPG-Progression-System/
├── main.py                   # Entry point for running simulations
├── simulate.py               # Core simulation loop and encounter logic
├── structs.py                # Data structures (Player, World, Equipment, etc.)
├── story.py                  # Story beat progression logic
├── loot.py                   # Loot generation and drop tables
├── parser.py                 # CSV parsing utilities
├── log.py                    # Data logging for analysis
├── utils.py                  # Helper functions
├── inputs.py                 # Input parameter constants
├── params.py                 # Simulation parameter constants
├── curve.py                  # Visualization tool for progression curves
├── requirements.txt          # Python dependencies (matplotlib)
└── data/
    ├── Inputs.json           # Primary configuration file (JSON)
    ├── Progression.csv       # Level and XP curve definitions
    ├── Params.csv            # Tunable simulation parameters
    ├── StoryBeats.csv        # Story stage definitions
    ├── Stats.csv             # Player stat configurations
    ├── LootTable.csv         # Item drop tables
    ├── NonCombat.csv         # Non-combat challenge definitions
    ├── NC_Categories.csv     # Non-combat category definitions
    ├── NC_Rules.csv          # Non-combat rule configurations
    ├── Curve.csv             # Progression curve data
    ├── Simulator.csv         # Simulation output and state tracking
    ├── Dashboard.csv         # High-level simulation metrics
    ├── Assertions.csv        # Test assertions for validation
    ├── REGRESSION.csv        # Regression test results
    ├── DebugConfig.csv       # Debug configuration settings
    └── DATA_DICTIONARY.csv   # Documentation of all data columns
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/RPG-Progression-System.git
cd RPG-Progression-System
```

2. Ensure you have Python 3.10+ installed (requires match/case syntax)

3. Install dependencies (optional, only required for visualization):

```bash
pip install -r requirements.txt
```

Note: The core simulation uses Python standard library only. Matplotlib is only needed for curve visualization.

## Quick Start

```bash
# Run simulation
python main.py

# Generate visualizations
python curve.py
```

Results will be saved to the `data/` directory as CSV files, and visualizations will be saved as PNG images in the root directory.

## Usage

### Basic Simulation

Run a basic simulation with default settings:

```bash
python main.py
```

This will run a 50-step simulation using the default configuration from `data/Inputs.json`.

### Custom Configuration

Modify `main.py` to customize the number of simulation steps:

```python
import simulate

if __name__ == "__main__":
    simulate.simulate(50)  # Run for 50 turns
```

To adjust simulation parameters, edit the configuration files:

- **`data/Inputs.json`**: Primary configuration for all simulation parameters
- **`inputs.py`**: Python constants loaded from Inputs.json
- **`params.py`**: Simulation algorithm parameters (success rates, slopes, etc.)

### Visualizing Progression Curves

Generate visual graphs of the progression system:

```bash
python curve.py
```

This will create three PNG files:

**Simulation Results (from output.csv):**

- **`simulation_results.png`**: Actual gameplay data from your last simulation run
  - Player level progression over time
  - Player ability (gear score) vs challenge difficulty (zone level)
  - Gold accumulation over time
  - Power ratio and success rate tracking

**Theoretical Curves (from Curve.csv & Progression.csv):**

- **`success_curves.png`**: Success chance curves for combat and non-combat encounters vs power delta
- **`xp_progression.png`**: XP requirements, cumulative XP, growth rates, and gold rewards by level

The visualizations help understand:

- **Player progression pacing**: How quickly players level up and gain power
- **Challenge balance**: Whether players are ahead or behind the zone difficulty
- **Economy flow**: Gold accumulation rate and resource availability
- **Success rates**: How player power translates to encounter success chances
- **Difficulty scaling**: How the game maintains challenge as players progress

### Configuration Files

#### Inputs.json (Primary Configuration)

The main configuration file containing all simulation parameters in JSON format:

**Parameters Section:**

- `XPExponent`: Experience curve steepness (default: 1.35)
- `CombatChance`: Probability of combat encounter (0-1, default: 0.6)
- `DeathChance`: Base chance of death in combat (default: 0.08)
- `RepairCostPct`: Equipment repair cost percentage (default: 0.05)
- `BaseXP_Combat/NonCombat`: Base XP rewards
- `ZoneTier`: Starting zone tier
- `StepCount`: Default simulation length
- `Seed`: Random seed for reproducibility

**GearQualityWeights:** Drop rates for Common/Rare/Epic/Legendary items per tier (T1-T4)

**DropThresholds:** Probability thresholds for equipment slot drops

**ScoreWeights:** Scoring multipliers for quality tiers and zone scaling

#### Progression.csv

Defines level progression and rewards:

- `Level`: Character level
- `XP_to_Next`: Experience required to reach next level
- `Gold_Combat`: Gold earned from combat encounters
- `Gold_NonCombat`: Gold earned from non-combat encounters

#### Params.csv

Tunable parameters for difficulty and progression:

- `FLOOR_SUCCESS`: Minimum success chance (default: 0.05)
- `CEIL_SUCCESS`: Maximum success chance (default: 0.95)
- `ATTEMPT_SLOPE`: Difficulty scaling factor
- `COMBAT_SLOPE`: Combat difficulty curve (default: 0.55)
- `NC_SLOPE`: Non-combat difficulty curve (default: 1.3)
- `FAIL_STEP`: Difficulty increase on failure
- `SUCCESS_STEP`: Difficulty change on success

#### StoryBeats.csv

Defines narrative progression using Hero's Journey structure:

- `BeatNum`: Sequential beat number
- `Stage`: Story stage name
- `BeatName`: Descriptive name for the beat
- `BeatStartStep`: Turn when this beat becomes active
- `ZoneLevel`: Recommended character level
- `BeatDC`: Difficulty class for challenges

#### DATA_DICTIONARY.csv

Complete documentation of all data columns used across the simulation system. Reference this file to understand the purpose and usage of any field in the output files.

## Core Modules

### inputs.py

Python constants module containing all primary simulation parameters loaded from `Inputs.json`:

- Economy parameters (repair costs, vendor taxes, respec costs)
- Experience and leveling parameters
- Combat and death mechanics
- Zone and gear scaling factors
- Random seed configuration

### params.py

Algorithm-specific parameters controlling simulation behavior:

- Success rate floors and ceilings
- Difficulty slopes for combat and non-combat encounters
- Combat shift and scaling factors
- Live roll settings

### simulate.py

Main simulation engine that orchestrates the turn-by-turn progression:

- Encounter generation (combat vs non-combat)
- Success/failure resolution
- Loot generation and distribution
- Player state updates

### structs.py

Core data structures:

- `Player`: Character state, equipment, and resources
- `World`: Story beats, zones, and environmental state
- `Equipment`: Item management and power calculations
- `Inputs`: Configuration data container

### curve.py

Visualization module for progression analysis:

- Loads data from `Curve.csv` and `Progression.csv`
- Generates success chance curves showing combat vs non-combat difficulty
- Creates XP progression graphs with multiple metrics
- Produces high-resolution PNG outputs for documentation and analysis
- Helps visualize power delta effects on encounter outcomes

### loot.py

Loot generation system:

- Equipment drops with zone-appropriate power levels
- Quality tier selection (Common/Rare/Epic/Legendary)
- Drop slot determination using threshold probabilities
- Item power calculation with quality and zone multipliers

### story.py

Story progression handler:

- Manages Hero's Journey narrative beats
- Updates world state based on simulation progress
- Tracks zone transitions and difficulty scaling

### log.py

Data logging and output management:

- Records turn-by-turn simulation results
- Writes to multiple CSV outputs (Simulator.csv, Dashboard.csv)
- Tracks player state, encounter outcomes, and resource changes

### utils.py

Helper functions and calculations:

- Success chance calculations for combat and non-combat
- Power ratio computations
- Statistical utilities and random number generation
- Difficulty curve implementations

### parser.py

CSV data loading utilities:

- Reads configuration files from `data/` directory
- Parses progression tables and story beats
- Loads parameter configurations

## Data Structures

### Player

- Experience and level tracking
- Equipment system (Weapon, Helm, Chest, Legs, Accessory)
- Loot inventory
- Gold accumulation
- Gear score calculation

### World

- Current story beat
- Zone difficulty and tier
- Stage progression

### Equipment

- Slot-based equipment system (5 slots)
- Item power calculation with quality modifiers
- Zone-scaled item generation
- Auto-equip best items by power

## Output

Simulation results are logged to multiple CSV files in the `data/` directory:

### Simulator.csv

Detailed turn-by-turn simulation log including:

- Player progression (XP, levels, gear score)
- Combat and non-combat encounter results
- Success/failure rates and power ratios
- Equipment drops and upgrades
- Resource accumulation (gold, reputation)
- Death events and repair costs

### Dashboard.csv

High-level metrics and summary statistics for quick analysis:

- Overall progression rates
- Success rate trends
- Economy balance metrics
- Gear progression summary

### Assertions.csv / REGRESSION.csv

Test validation and regression testing results to ensure simulation consistency across runs

## Configuration Tips

### Adjusting Difficulty

- Modify `COMBAT_SLOPE` and `NC_SLOPE` in `params.py` to change how difficulty scales with power differences
- Adjust `FLOOR_SUCCESS` and `CEIL_SUCCESS` to set minimum/maximum success rates
- Change `DeathChance` in `Inputs.json` to control combat lethality

### Tuning Progression Speed

- Adjust `XPExponent` to change how quickly level requirements increase
- Modify `BaseXP_Combat` and `BaseXP_NonCombat` for faster/slower leveling
- Edit `Progression.csv` to customize level-by-level XP requirements

### Balancing Economy

- Set `RepairCostPct` to control the cost of dying
- Adjust `VendorTaxPct` for selling item penalties
- Modify gold rewards in `Progression.csv` per level

### Loot Drop Rates

- Edit `GearQualityWeights` in `Inputs.json` to change rarity distributions per tier
- Adjust `DropThresholds` to control which equipment slots drop more frequently
- Modify `ScoreWeights` to balance item power calculations

## Understanding the Visualizations

### Simulation Results

The simulation results visualization shows actual gameplay data from your simulation run, with four key graphs:

**1. Player Level Progression Over Time**

- Shows how quickly the player levels up through the simulation
- Helps identify if XP pacing is too fast or too slow
- Level plateaus indicate where more XP is required

**2. Player Ability vs Challenge Difficulty**

- Green shading: Player gear score is above zone difficulty (player ahead)
- Red shading: Player gear score is below zone difficulty (player behind)
- The gap between lines shows the power difference
- Ideal balance keeps players slightly ahead but not overwhelming

**3. Gold Accumulation Over Time**

- Shows economic growth throughout the simulation
- Steep slopes indicate periods of high gold income
- Flat sections may indicate deaths or high expenses
- Helps balance reward rates and gold sinks

**4. Power Ratio & Success Rate Over Time**

- Purple line: Power ratio (positive = player advantage, negative = disadvantage)
- Orange line: Success chance percentage
- Shows how power differences translate to success probability
- Helps identify if encounters are too easy or too difficult

### Success Curves

The success curves visualization shows how encounter difficulty changes based on the power difference between player and zone:

- **Power Delta = 0**: Player and zone are evenly matched
- **Negative Delta**: Player is weaker than the zone (harder encounters)
- **Positive Delta**: Player is stronger than the zone (easier encounters)

**Key Insights:**

- Non-combat encounters use a steeper curve (NC_SLOPE = 1.3), making them more sensitive to power differences
- Combat encounters use a gentler curve (COMBAT_SLOPE = 0.55), creating more consistent challenge
- Success rates are clamped between 5% (floor) and 95% (cap) to prevent trivial or impossible encounters
- The difference plot shows where non-combat is easier/harder than combat

### XP Progression

The XP progression visualization includes four key metrics:

1. **XP per Level**: Shows the increasing XP requirement as you level up
2. **Cumulative XP**: Total experience needed to reach each level from level 1
3. **Growth Rate**: The rate of increase in XP requirements (indicates difficulty scaling)
4. **Gold Rewards**: Comparison of rewards between combat and non-combat encounters

**Balance Considerations:**

- A consistent growth rate indicates smooth difficulty scaling
- Large jumps in XP requirements can create pacing issues
- Gold reward ratios should reflect the relative difficulty of encounter types

## Use Cases

- **Game Balance Testing**: Test XP curves and progression pacing across multiple zones
- **Difficulty Tuning**: Adjust encounter difficulty and success rates using power-based formulas
- **Economy Design**: Balance gold rewards, repair costs, and loot drop rates
- **Narrative Pacing**: Ensure story beats align with player power levels using zone tiers
- **Regression Testing**: Validate balance changes don't break intended progression
- **Data Analysis**: Export simulation results for statistical analysis and visualization
- **Design Documentation**: Use generated graphs to communicate balance decisions to team members

## Example Workflow

### Iterative Balance Tuning

1. **Initial Setup**: Configure your progression parameters in `data/Inputs.json`
2. **Run Simulation**: Execute `python main.py` to generate baseline data
3. **Visualize**: Run `python curve.py` to see current balance state
4. **Analyze**: Review generated graphs for issues:
   - Check `simulation_results.png` for actual gameplay balance
   - Look for player getting too far ahead/behind in ability vs difficulty graph
   - Verify gold accumulation rate is reasonable
   - Ensure success rates stay in acceptable range (not too easy/hard)
5. **Adjust**: Modify parameters in configuration files based on findings
6. **Re-test**: Run simulation again and compare new graphs to previous run
7. **Validate**: Check `REGRESSION.csv` to ensure changes don't break intended behavior

### Testing a New XP Curve

```python
# 1. Modify XPExponent in data/Inputs.json
{
  "Parameters": {
    "XPExponent": 1.5,  # Changed from 1.35
    ...
  }
}

# 2. Run simulation
python main.py

# 3. Generate visualization
python curve.py

# 4. Compare cumulative XP graph to previous version
```

### Balancing Combat vs Non-Combat

```python
# 1. Adjust slopes in params.py
COMBAT_SLOPE = 0.6   # Increase from 0.55 for harder combat
NC_SLOPE = 1.2       # Decrease from 1.3 for easier non-combat

# 2. Run simulation and visualize
python main.py && python curve.py

# 3. Check success curve difference plot
# - Should show more balanced difficulty between encounter types
```

## Contributing

This is a personal project for RPG progression system design and testing. Feel free to fork and adapt for your own game projects.

## Acknowledgments

- Inspired by classic RPG progression systems and modern game design principles
- Uses Hero's Journey narrative structure for story beat progression
- Built with Python 3.10+ for modern language features
