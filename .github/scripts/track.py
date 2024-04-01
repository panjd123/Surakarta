import os.path as osp

ROOT = osp.join(".", "submission")
TEAM_NUM = 17
STAGE_NUM = 4
TEAMS = ["team" + str(i).zfill(2) for i in range(1, TEAM_NUM + 1)]


def parse_unfinished(unfinished):
    print("Status:\n")
    for i in range(STAGE_NUM):
        print(f"Stage {i}: {len(unfinished[i])} / {TEAM_NUM}")
        if len(unfinished[i]) == TEAM_NUM:
            print("  All teams are unfinished.")
        elif len(unfinished[i]) == 0:
            print("  All teams are finished.")
        else:
            for team in unfinished[i]:
                print(f"  {team}")
        print("")


def main():
    unfinished = [[] for _ in range(STAGE_NUM)]
    for team in TEAMS:
        team_id = int(team[4:])
        team_dir = osp.join(ROOT, team)
        prefixes = [lambda _: "report", lambda _: "stage"]
        suffixes = [lambda x: str(x), lambda x: str(x).zfill(2)]

        for i in range(STAGE_NUM):
            exists = False
            if i == 0:
                for prefix in ["profile", "README", "team"]:
                    for suffix in suffixes + [lambda _: ""]:
                        path = osp.join(team_dir, f"{prefix}{suffix(team_id)}.md")
                        if osp.exists(path) and osp.getsize(path) > 10:
                            exists = True
                            break
                    if exists:
                        break
            else:
                for prefix in prefixes:
                    for suffix in suffixes:
                        path = osp.join(team_dir, f"{prefix(i)}{suffix(i)}.md")
                        if osp.exists(path) and osp.getsize(path) > 500:
                            exists = True
                            break
                    if exists:
                        break
            if not exists:
                unfinished[i].append(team)
    return unfinished


parse_unfinished(main())
