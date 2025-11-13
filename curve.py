import matplotlib.pyplot as plt
import csv
from pathlib import Path


def load_simulation_data():
    """Load simulation output data from output.csv"""
    output_file = Path("data") / "output.csv"
    
    steps = []
    player_levels = []
    zone_levels = []
    gear_scores = []
    cumulative_gold = []
    cumulative_xp = []
    power_ratios = []
    success_chances = []
    xp_earned = []
    combat_chances = []
    
    with open(output_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Parse all values first before appending
                step = int(row['Step'])
                player_level = int(row['PlayerLevel'])
                zone_level = int(row['ZoneLevel'])
                gear_score = int(row['GearScore'])
                cumulative_gold_val = int(row['CumulativeGold'])
                cumulative_xp_val = int(row['CumulativeXP'])
                power_ratio = float(row['PowerRatio'])
                xp_earned_val = int(row['XP_Earned'])
                
                # Track combat chances specifically for filtering
                combat_chance = float(row.get('SuccessChanceCombat', 0))
                
                # Get success chance (prioritize combat, fallback to non-combat)
                success = float(row.get('SuccessChanceCombat', 0))
                if success == 0:
                    success = float(row.get('SuccessChance_NonCombat', 0))
                
                # Only append if all parsing succeeded
                steps.append(step)
                player_levels.append(player_level)
                zone_levels.append(zone_level)
                gear_scores.append(gear_score)
                cumulative_gold.append(cumulative_gold_val)
                cumulative_xp.append(cumulative_xp_val)
                power_ratios.append(power_ratio)
                xp_earned.append(xp_earned_val)
                combat_chances.append(combat_chance)
                success_chances.append(success)
            except (ValueError, KeyError) as e:
                continue
    
    return {
        'steps': steps,
        'player_levels': player_levels,
        'zone_levels': zone_levels,
        'gear_scores': gear_scores,
        'cumulative_gold': cumulative_gold,
        'cumulative_xp': cumulative_xp,
        'power_ratios': power_ratios,
        'success_chances': success_chances,
        'xp_earned': xp_earned,
        'combat_chances': combat_chances
    }


def load_curve_data():
    """Load success chance curves from Curve.csv"""
    curve_file = Path("data") / "Curve.csv"
    
    deltas = []
    nc_chances = []
    combat_chances = []
    
    with open(curve_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Strip all keys and values to handle spacing issues
            row = {k.strip(): v.strip() for k, v in row.items()}
            
            delta = float(row['Delta'])
            nc_chance = float(row['NC_Chance'])
            combat_chance = float(row['Combat_Chance'])
            
            deltas.append(delta)
            nc_chances.append(nc_chance)
            combat_chances.append(combat_chance)
    
    return deltas, nc_chances, combat_chances


def load_progression_data():
    """Load XP progression from Progression.csv"""
    progression_file = Path("data") / "Progression.csv"
    
    levels = []
    xp_to_next = []
    cumulative_xp = [0]
    gold_combat = []
    gold_noncombat = []
    
    with open(progression_file, 'r') as f:
        reader = csv.DictReader(f)
        total_xp = 0
        for row in reader:
            level = int(row['Level'])
            xp = int(row['XP_to_Next'])
            gold_c = int(row['Gold_Combat'])
            gold_nc = int(row['Gold_NonCombat'])
            
            levels.append(level)
            xp_to_next.append(xp)
            total_xp += xp
            cumulative_xp.append(total_xp)
            gold_combat.append(gold_c)
            gold_noncombat.append(gold_nc)
    
    return levels, xp_to_next, cumulative_xp, gold_combat, gold_noncombat


def plot_simulation_results():
    """Plot simulation results from output.csv"""
    data = load_simulation_data()
    
    if data is None:
        return
    
    # Load curve data for Plot 3
    deltas, nc_chances, combat_chances_curve = load_curve_data()
    
    # Filter out non-combat steps (keep only where combat_chances > 0)
    filtered_data = {key: [] for key in data.keys()}
    for i in range(len(data['steps'])):
        if data['combat_chances'][i] > 0:  # Keep only combat steps
            for key in data.keys():
                filtered_data[key].append(data[key][i])
    data = filtered_data
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot 1: Player Level vs Steps
    ax1.plot(data['steps'], data['player_levels'], 'o-', color='darkblue', 
             linewidth=2, markersize=4, label='Player Level')
    ax1.fill_between(data['steps'], 0, data['player_levels'], alpha=0.3, color='skyblue')
    ax1.set_xlabel('Step', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Player Level', fontsize=11, fontweight='bold')
    ax1.set_title('Player Level Progression Over Time', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(loc='best', fontsize=9)
    
    # Add level milestones
    unique_levels = sorted(set(data['player_levels']))
    if len(unique_levels) > 1:
        for level in unique_levels[1::2]:  # Every other level
            level_step = next((s for s, l in zip(data['steps'], data['player_levels']) if l == level), None)
            if level_step:
                ax1.axhline(y=level, color='gray', linestyle=':', alpha=0.3, linewidth=0.8)
    
    # Plot 2: Player Ability (Gear Score) vs Challenge Difficulty (Zone Level)
    ax2.plot(data['steps'], data['gear_scores'], 's-', color='green', 
             linewidth=2, markersize=3, label='Player Gear Score', alpha=0.8)
    ax2.plot(data['steps'], data['zone_levels'], '^-', color='red', 
             linewidth=2, markersize=3, label='Zone Difficulty', alpha=0.8)
    ax2.fill_between(data['steps'], data['gear_scores'], data['zone_levels'], 
                     where=[gs >= zl for gs, zl in zip(data['gear_scores'], data['zone_levels'])],
                     alpha=0.2, color='green', label='Player Ahead')
    ax2.fill_between(data['steps'], data['gear_scores'], data['zone_levels'],
                     where=[gs < zl for gs, zl in zip(data['gear_scores'], data['zone_levels'])],
                     alpha=0.2, color='red', label='Behind Zone')
    ax2.set_xlabel('Step', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Power Level', fontsize=11, fontweight='bold')
    ax2.set_title('Player Ability vs Challenge Difficulty', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(loc='best', fontsize=9)
    
    # Plot 3: Success Chance vs Power Delta
    ax3.plot(deltas, combat_chances_curve, 'r-', linewidth=2, label='Combat Success', marker='o', markersize=3)
    ax3.plot(deltas, nc_chances, 'b-', linewidth=2, label='Non-Combat Success', marker='s', markersize=3)
    ax3.axhline(y=0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='50% Success')
    ax3.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Even Power')
    ax3.axhline(y=0.05, color='orange', linestyle=':', linewidth=1, alpha=0.5, label='Floor (5%)')
    ax3.axhline(y=0.95, color='green', linestyle=':', linewidth=1, alpha=0.5, label='Cap (95%)')
    
    ax3.set_xlabel('Power Delta (Player - Zone)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Success Chance', fontsize=11, fontweight='bold')
    ax3.set_title('Success Chance vs Power Delta', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3, linestyle='--')
    ax3.legend(loc='best', fontsize=9)
    ax3.set_ylim(-0.05, 1.05)
    
    # Add annotations
    ax3.annotate('Player Weaker', xy=(-5, 0.1), fontsize=9, ha='center', style='italic', color='red')
    ax3.annotate('Player Stronger', xy=(5, 0.9), fontsize=9, ha='center', style='italic', color='green')
    
    # Plot 4: Power Ratio and Combat Success Chance
    ax4_twin = ax4.twinx()
    
    line1 = ax4.plot(data['steps'], data['power_ratios'], 'o-', color='purple', 
                     linewidth=2, markersize=3, label='Power Ratio', alpha=0.7)
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5)
    ax4.fill_between(data['steps'], 0, data['power_ratios'],
                     where=[pr > 0 for pr in data['power_ratios']],
                     alpha=0.2, color='green', label='Advantage')
    ax4.fill_between(data['steps'], 0, data['power_ratios'],
                     where=[pr < 0 for pr in data['power_ratios']],
                     alpha=0.2, color='red', label='Disadvantage')
    
    line2 = ax4_twin.plot(data['steps'], [s * 100 for s in data['combat_chances']], 
                          'd-', color='orange', linewidth=2, markersize=3, 
                          label='Combat Success Chance', alpha=0.7)
    
    ax4.set_xlabel('Step', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Power Ratio (Player/Zone)', fontsize=10, fontweight='bold', color='purple')
    ax4_twin.set_ylabel('Combat Success Chance (%)', fontsize=10, fontweight='bold', color='orange')
    ax4.set_title('Power Ratio & Combat Success Chance Over Time', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3, linestyle='--')
    ax4.tick_params(axis='y', labelcolor='purple')
    ax4_twin.tick_params(axis='y', labelcolor='orange')
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax4.legend(lines, labels, loc='upper left', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('simulation_results.png', dpi=300, bbox_inches='tight')
    print("Saved: simulation_results.png")
    print("Plotting simulation results...")
    plt.show()


def plot_all():
    """Generate all progression curve visualizations"""
    print("\n" + "="*50)
    print("  RPG PROGRESSION SYSTEM - CURVE VISUALIZATION")
    print("="*50 + "\n")
    
    # Plot simulation results from output.csv
    print("Generating simulation result graphs...")
    plot_simulation_results()
    
    print("\n" + "="*50)
    print("  All visualizations complete!")
    print("="*50 + "\n")
