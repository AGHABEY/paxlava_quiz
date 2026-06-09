"""One-off import of the published standings into the database.

Run inside the container after deploying:

    docker compose exec web python import_scores.py

Idempotent: re-running replaces this date's results with the same data.
"""

import db

# Date these results belong to. Change if the game was on another day.
GAME_DATE = "2026-06-09"

# (team name, [Tur1, Tur2, Tur3, Tur4, Tur5, Tur6, Tur7, Tur8(1), Tur8(2), Tur8(3)])
STANDINGS = [
    ("Команда Али Кязимова",          [6, 4, 2, 5, 5, 7, 26, -25, 35, 45]),   # 110
    ("Koqnitiv Dissonans",            [5, 6, 5, 5, 6, 0, 26, 45, -25, 35]),   # 108
    ("5+1",                           [5, 5, 2, 8, 6, 0, 26, 45, -25, 35]),   # 107
    ("Casus Belli",                   [6, 4, 3, 4, 6, 7, 16, -25, 45, 35]),   # 101
    ("Şeyx Bakıda",                   [6, 3, 0, 2, 4, 5, 20, 0, 45, 0]),      # 85
    ("Morningstar",                   [5, 5, 0, 6, 6, 7, 28, -25, 0, 45]),    # 77
    ("Zuzula Tribe",                  [4, 1, 0, 2, 3, 0, 14, 0, 0, 45]),      # 69
    ("S7",                            [6, 5, 2, 6, 6, 6, 28, -25, 35, 0]),    # 69
    ("Amiqos",                        [6, 6, 2, 4, 4, 6, 28, 0, -35, 45]),    # 66
    ("Black Cat",                     [4, 2, 3, 3, 4, 0, 12, -35, 45, 0]),    # 38
    ("Теоретически правы",            [5, 3, 2, 7, 5, 7, 22, -25, -35, 45]),  # 36
    ("Mütəşəkkil İntellektual Dəstə", [4, 3, 2, 3, 5, 6, 20, 0, 0, -25]),     # 18
    ("Xəmsə",                         [6, 2, 5, 4, 6, 6, 22, -25, 0, -45]),   # -19
    ("Natural İntelligence",          [2, 2, 1, 11, 3, 6, 17, -25, -35, -45]),  # -63
]


def main():
    db.init_db()

    # Create teams (idempotent) and map name -> id.
    for name, _ in STANDINGS:
        db.add_team(name)
    team_ids = {team["name"]: team["id"] for team in db.load_teams_list()}

    rows = []
    for name, values in STANDINGS:
        rounds = dict(zip(db.ROUND_KEYS, values))
        rows.append({"team_id": team_ids[name], "team_name": name, "rounds": rounds})

    db.replace_date_results(GAME_DATE, rows)
    print(f"Imported {len(rows)} teams for {GAME_DATE} into {db.DB_PATH}")


if __name__ == "__main__":
    main()
