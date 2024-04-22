import os
import os.path as osp
import json

SUBMISSION_ROOT = osp.join(".", "submission")
STATUS_ROOT = osp.join(".", "submission", "status")
TEAM_NUM = 17
STAGE_NUM = 4
TEAMS = ["team" + str(i).zfill(2) for i in range(1, TEAM_NUM + 1)]


def parse_unfinished(unfinished):
    status_txt = ""
    status_json = {}
    for i in range(STAGE_NUM):
        status_txt += f"Stage {i}: {TEAM_NUM - len(unfinished[i])} / {TEAM_NUM}\n"
        status_json.update(
            {f"stage{i}": f"{TEAM_NUM - len(unfinished[i])} / {TEAM_NUM}"}
        )
        if len(unfinished[i]) == TEAM_NUM:
            status_txt += "  All teams are unfinished.\n"
        elif len(unfinished[i]) == 0:
            status_txt += "  All teams are finished.\n"
        else:
            for team in unfinished[i]:
                status_txt += f"  {team}\n"
        status_txt += "\n"
    return status_txt, status_json


def track():
    unfinished = [[] for _ in range(STAGE_NUM)]
    for team in TEAMS:
        team_id = int(team[4:])
        team_dir = osp.join(SUBMISSION_ROOT, team)
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


if not osp.exists(STATUS_ROOT):
    os.makedirs(STATUS_ROOT)

status_txt, status_json = parse_unfinished(track())
with open(osp.join(STATUS_ROOT, "status.txt"), "w") as f:
    f.write(status_txt)
json.dump(status_json, open(osp.join(STATUS_ROOT, "status.json"), "w"))
