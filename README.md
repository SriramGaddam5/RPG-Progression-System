# RPG Progression System

A Python-based simulation system for modeling and balancing RPG progression mechanics, including combat, loot, experience, and story progression.

## Overview

This project simulates a player's journey through an RPG campaign, tracking progression through levels, equipment, and story beats. It's designed to help game designers test and balance progression curves, difficulty scaling, and reward systems before implementing them in a game.

## Features

- **Player Progression Simulation**: Models XP gain, leveling, and character growth
- **Combat & Non-Combat Systems**: Simulates both combat encounters and skill-based challenges
- **Loot System**: Equipment generation with quality tiers and item power scaling
- **Story Beat Integration**: Follows the Hero's Journey structure with configurable story stages
- **Configurable Parameters**: CSV-based configuration for easy balance tuning
- **Data Logging**: Outputs detailed simulation results for analysis

## Project Structure

```
RPG-Progression-System/
├── main.py              # Entry point for running simulations
├── simulate.py          # Core simulation loop and encounter logic
├── structs.py           # Data structures (Player, World, Equipment, etc.)
├── story.py             # Story beat progression logic
├── loot.py              # Loot generation and drop tables
├── parser.py            # CSV parsing utilities
├── log.py               # Data logging for analysis
├── utils.py             # Helper functions
└── data/
    ├── Progression.csv       # Level and XP curve definitions
    ├── Params.csv            # Tunable simulation parameters
    ├── StoryBeats.csv        # Story stage definitions
    ├── Stats.csv             # Player stat configurations
    ├── LootTable.csv         # Item drop tables
    ├── NonCombat.csv         # Non-combat challenge definitions
    ├── Curve.csv             # Progression curve data
    └── output.csv            # Simulation results
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/RPG-Progression-System.git
cd RPG-Progression-System
```

2. Ensure you have Python 3.10+ installed (requires match/case syntax)

3. No external dependencies required - uses Python standard library only

## Usage

### Basic Simulation

Run a basic simulation with default settings:

```python
python main.py
```

### Custom Configuration

Modify `main.py` to customize simulation parameters:

```python
import simulate
import structs

if __name__ == "__main__":
    inputs = structs.Inputs()
    inputs.combat_chance = 100  # Percentage chance of combat vs non-combat

    simulate.simulate(50, inputs)  # Run for 50 turns
```

### Configuration Files

#### Progression.csv

Defines level progression and rewards:

- `Level`: Character level
- `XP_to_Next`: Experience required to reach next level
- `Gold_Combat`: Gold earned from combat encounters
- `Gold_NonCombat`: Gold earned from non-combat encounters

#### Params.csv

Tunable parameters for difficulty and progression:

- `Cap_Success`: Maximum success chance (0-1)
- `Floor_Success`: Minimum success chance (0-1)
- `AttemptSlope`: Difficulty scaling factor
- `Combat_Slope`: Combat difficulty curve
- `NC_Slope`: Non-combat difficulty curve

#### StoryBeats.csv

Defines narrative progression using Hero's Journey structure:

- `BeatNum`: Sequential beat number
- `Stage`: Story stage name
- `BeatName`: Descriptive name for the beat
- `BeatStartStep`: Turn when this beat becomes active
- `ZoneLevel`: Recommended character level
- `BeatDC`: Difficulty class for challenges

## Data Structures

### Player

- Experience and level tracking
- Equipment system (Weapon, Helm, Chest, Legs, Accessory)
- Loot inventory
- Gold accumulation

### World

- Current story beat
- Zone difficulty
- Stage progression

### Equipment

- Slot-based equipment system
- Item power calculation
- Auto-equip best items

## Output

Simulation results are logged to `data/output.csv` and include:

- Turn-by-turn player progression
- Level changes
- Equipment upgrades
- Resource accumulation

## Use Cases

- **Game Balance Testing**: Test XP curves and progression pacing
- **Difficulty Tuning**: Adjust encounter difficulty and success rates
- **Economy Design**: Balance gold rewards and loot drop rates
- **Narrative Pacing**: Ensure story beats align with player power levels
