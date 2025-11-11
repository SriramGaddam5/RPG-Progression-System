import parser
import structs
import random
import math
import params
import inputs

_nc_categories = parser.read_csv("data/NC_Categories.csv", structs.NCCategory)
# _nc_rules ?
_non_combat = parser.read_csv("data/NonCombat.csv", structs.NonCombat)


def chance(percent: float) -> bool:
    return random.random() <= clamp(percent, floor=0, ceil=1)


def logistic(x: float, *, L: float = 1.0, k: float = 1.0, x0: float = 0.0) -> float:
    return L / (1 + math.exp(-k * (x - x0)))


def skill_check(
    ratio: float,
    DC: float,
    steepness: float = 1.0,
) -> tuple[bool, float]:
    """
    Determine success probability based on ratio vs. DC using a logistic curve. When ratio == DC, then there is a 50% chance of success.

    Parameters:
        ratio     : player's effective power ratio or stat score
        DC        : difficulty (d20 roll)
        steepness : how quickly probability ramps up around equality

    Returns:
        (success, chance)
    """

    x = ratio - DC
    chance = logistic(x, L=1.0, k=steepness, x0=0.0)
    success = random.random() < chance
    return success, chance


def clamp(x: float, *, floor: float, ceil: float):
    return max(floor, min(ceil, x))


def power_ratio(player: structs.Player, world: structs.World) -> float:
    return player.equipment.get_score() / (
        inputs.BASE_RECOMMENDED_GEAR
        * inputs.GEAR_GROWTH_PER_ZONE ** (world.ZoneLevel / inputs.ZONE_SCALE)
    )


def stat_score(player: structs.Player, stat_key: str) -> float:
    stat = player.get_stat(stat_key)

    return (
        stat.Base
        + (player.level * stat.PerLevel)
        + (player.equipment.get_score() / max(1, inputs.GEAR_STAT_SCALING))
    )


def combat_chance(player: structs.Player, world: structs.World) -> float:
    skill_noise = math.sqrt(-2 * math.log(random.random())) * math.cos(
        2 * math.pi * random.random()
    )
    skill_difficulty = inputs.SKILL_DIFF_TIER_MULT + world.ZoneTier * skill_noise

    success_chance = 1 - (
        skill_difficulty - (world.ZoneTier * inputs.SKILL_DIFF_TIER_MULT)
    ) / (10 * inputs.SKILL_DIFF_ST_DEV)
    success_chance = clamp(
        success_chance,
        floor=params.FLOOR_SUCCESS,
        ceil=params.CEIL_SUCCESS,
    )

    return success_chance


def non_combat_chance(
    player: structs.Player, world: structs.World, category_key: str
) -> float:
    category = _nc_categories[0]
    for cat in _nc_categories:
        if cat.OutcomeCategory == category_key:
            category = cat

    tn = category.CategoryDC + world.BeatDC
    uni = clamp(
        (21 - (tn - stat_score(player, category.StatKey))) / 20,
        floor=0,
        ceil=1,
    )
    success_chance = clamp(
        1 / (1 + math.exp(-params.ATTEMPT_SLOPE * (tn - uni))),
        floor=params.FLOOR_SUCCESS,
        ceil=params.CEIL_SUCCESS,
    )

    return success_chance


def death_chance(player: structs.Player, world: structs.World) -> float:
    return (1 - combat_chance(player, world)) * inputs.DEATH_SEVERITY


def non_combat_category(world: structs.World) -> structs.NCCategory:
    rand = random.random()

    scenario = _non_combat[0]
    for s in _non_combat:
        thresh = 0
        if world.ZoneTier == 1:
            thresh = s.T1Threshold
        elif world.ZoneTier == 2:
            thresh = s.T2Threshold
        elif world.ZoneTier == 3:
            thresh = s.T3Threshold
        elif world.ZoneTier == 4:
            thresh = s.T4Threshold
        if rand <= thresh:
            scenario = s
            break

    category = _nc_categories[0]
    for cat in _nc_categories:
        if cat.OutcomeCategory == scenario.Category:
            category = cat

    return category


def skill_difficulty(player: structs.Player, world: structs.World) -> float:
    skill_noise = math.sqrt(-2 * math.log(random.random())) * math.cos(
        2 * math.pi * random.random()
    )
    skill_difficulty = inputs.SKILL_DIFF_TIER_MULT + world.ZoneTier * skill_noise
    return skill_difficulty
