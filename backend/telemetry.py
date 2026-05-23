from __future__ import annotations

import datetime as dt
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests


ROUTING = "https://americas.api.riotgames.com"
C_DRAGON_AUGMENTS_URL = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/cherry-augments.json"


ASSASSIN_NAMES = {
    "Akali",
    "Katarina",
    "Zed",
    "Talon",
    "Qiyana",
    "Naafiri",
    "KhaZix",
    "Rengar",
    "Shaco",
    "Evelynn",
    "Pyke",
    "Kayn",
    "LeBlanc",
    "Fizz",
    "Diana",
    "Ekko",
    "Nocturne",
}


def _to_utc(ts: int | None) -> str | None:
    if not ts:
        return None
    value = int(ts)
    if value > 10**12:
        value //= 1000
    return dt.datetime.fromtimestamp(value, dt.UTC).strftime("%Y-%m-%d %H:%M UTC")


def _read_local_augments(augments_path: Path) -> dict[int, str]:
    out: dict[int, str] = {}
    if not augments_path.exists():
        return out
    data = requests.models.complexjson.loads(augments_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return out
    for _, arr in data.items():
        if not isinstance(arr, list):
            continue
        for item in arr:
            if not isinstance(item, dict):
                continue
            aug_id = item.get("id")
            name = item.get("name")
            if isinstance(aug_id, int) and isinstance(name, str) and name:
                out[aug_id] = name
    return out


def _read_cdragon_augments(session: requests.Session) -> dict[int, str]:
    out: dict[int, str] = {}
    response = session.get(C_DRAGON_AUGMENTS_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        return out
    for item in payload:
        if not isinstance(item, dict):
            continue
        aug_id = item.get("id")
        name = item.get("nameTRA") or item.get("name")
        if isinstance(aug_id, int) and isinstance(name, str) and name:
            out[aug_id] = name
    return out


def _merge_augment_maps(local: dict[int, str], cdragon: dict[int, str]) -> dict[int, str]:
    merged = dict(local)
    for aug_id, name in cdragon.items():
        if aug_id not in merged or not merged[aug_id] or merged[aug_id] == "Unknown":
            merged[aug_id] = name
    return merged


def _api_get_json(session: requests.Session, url: str) -> Any:
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def _fetch_account(session: requests.Session, api_key: str, riot_name: str, riot_tag: str) -> dict[str, Any]:
    url = f"{ROUTING}/riot/account/v1/accounts/by-riot-id/{quote(riot_name)}/{riot_tag}?api_key={api_key}"
    payload = _api_get_json(session, url)
    if not isinstance(payload, dict):
        raise ValueError("Unexpected account response")
    if "puuid" not in payload:
        raise ValueError("Account response missing puuid")
    return payload


def _fetch_match_ids(session: requests.Session, api_key: str, puuid: str, max_matches: int) -> list[str]:
    match_ids: list[str] = []
    start = 0
    page_size = 100

    while len(match_ids) < max_matches:
        count = min(page_size, max_matches - len(match_ids))
        url = f"{ROUTING}/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&api_key={api_key}"
        page = _api_get_json(session, url)
        if not isinstance(page, list) or not page:
            break
        page_ids = [str(mid) for mid in page]
        match_ids.extend(page_ids)
        if len(page_ids) < count:
            break
        start += count

    # Preserve order while dropping duplicates.
    return list(dict.fromkeys(match_ids))


def _extract_rows_from_match(match: dict[str, Any], puuid: str, aug_map: dict[int, str]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    info = match.get("info", {})
    participants = info.get("participants", [])
    if not isinstance(participants, list):
        return None, None

    me = next((p for p in participants if isinstance(p, dict) and p.get("puuid") == puuid), None)
    if not isinstance(me, dict):
        return None, None

    team_id = me.get("teamId")
    teammates: list[str] = []
    enemies: list[str] = []
    for participant in participants:
        if not isinstance(participant, dict):
            continue
        if participant.get("puuid") == puuid:
            continue
        name = participant.get("riotIdGameName") or participant.get("summonerName") or "UNKNOWN"
        if participant.get("teamId") == team_id:
            teammates.append(str(name))
        else:
            enemies.append(str(name))

    ts = info.get("gameEndTimestamp") or info.get("gameStartTimestamp") or 0
    metadata = match.get("metadata", {})
    match_id = metadata.get("matchId") if isinstance(metadata, dict) else None

    row: dict[str, Any] = {
        "matchId": match_id,
        "queueId": info.get("queueId"),
        "gameMode": info.get("gameMode"),
        "timestamp": ts,
        "timestampUTC": _to_utc(ts),
        "champion": me.get("championName"),
        "win": bool(me.get("win")),
        "kills": me.get("kills", 0),
        "deaths": me.get("deaths", 0),
        "assists": me.get("assists", 0),
        "placement": me.get("placement"),
        "subteamPlacement": me.get("subteamPlacement"),
        "goldEarned": me.get("goldEarned"),
        "damageToChamps": me.get("totalDamageDealtToChampions"),
        "teammateNames": teammates,
        "enemyNames": enemies,
    }

    augment_ids = [me.get(f"playerAugment{i}") for i in range(1, 7)]
    clean_ids = [aid for aid in augment_ids if isinstance(aid, int) and aid > 0]
    if not clean_ids:
        return row, None

    arena_row = dict(row)
    arena_row["augmentIds"] = clean_ids
    arena_row["augmentNames"] = [aug_map.get(aid, "Unknown") for aid in clean_ids]
    return row, arena_row


def _build_summary(account: dict[str, Any], rows: list[dict[str, Any]], arena_rows: list[dict[str, Any]], aug_map: dict[int, str]) -> dict[str, Any]:
    teammates: Counter[str] = Counter()
    enemies: Counter[str] = Counter()
    champions: Counter[str] = Counter()
    queues: Counter[int] = Counter()
    augments: Counter[int] = Counter()
    aug_pairs: Counter[tuple[int, int]] = Counter()
    assassin_stats: dict[str, dict[str, int]] = defaultdict(lambda: {"games": 0, "wins": 0})

    for row in rows:
        champ = row.get("champion")
        if isinstance(champ, str) and champ:
            champions[champ] += 1
        queue_id = row.get("queueId")
        if isinstance(queue_id, int):
            queues[queue_id] += 1
        for name in row.get("teammateNames", []):
            if isinstance(name, str):
                teammates[name] += 1
        for name in row.get("enemyNames", []):
            if isinstance(name, str):
                enemies[name] += 1
        if isinstance(champ, str) and champ in ASSASSIN_NAMES:
            assassin_stats[champ]["games"] += 1
            assassin_stats[champ]["wins"] += 1 if row.get("win") else 0

    for row in arena_rows:
        ids = [aid for aid in row.get("augmentIds", []) if isinstance(aid, int)]
        for aid in ids:
            augments[aid] += 1
        for a, b in combinations(sorted(ids), 2):
            aug_pairs[(a, b)] += 1

    wins = sum(1 for row in rows if row.get("win"))
    kills = sum(int(row.get("kills", 0) or 0) for row in rows)
    deaths = sum(int(row.get("deaths", 0) or 0) for row in rows)
    assists = sum(int(row.get("assists", 0) or 0) for row in rows)
    arena_wins = sum(1 for row in arena_rows if row.get("win"))
    placements = [row.get("placement") for row in arena_rows if isinstance(row.get("placement"), int)]

    timestamps = [row.get("timestamp") for row in rows if isinstance(row.get("timestamp"), int)]
    window = {
        "fromUTC": _to_utc(min(timestamps)) if timestamps else None,
        "toUTC": _to_utc(max(timestamps)) if timestamps else None,
    }

    assassin_rows: list[dict[str, Any]] = []
    for champ, stats in assassin_stats.items():
        games = stats["games"]
        win_rate = round(100.0 * stats["wins"] / games, 2) if games else 0.0
        assassin_rows.append({"champion": champ, "games": games, "winRate": win_rate})
    assassin_rows.sort(key=lambda item: (item["games"], item["winRate"]), reverse=True)

    return {
        "account": {
            "gameName": account.get("gameName"),
            "tagLine": account.get("tagLine"),
            "puuid": account.get("puuid"),
        },
        "sample": {
            "matchesFetched": len(rows),
            "matchesParsed": len(rows),
            "arenaMatches": len(arena_rows),
            "timeWindow": window,
        },
        "performance": {
            "overall": {
                "wins": wins,
                "losses": len(rows) - wins,
                "winRate": round(100.0 * wins / len(rows), 2) if rows else None,
                "kda": round((kills + assists) / deaths, 2) if deaths else None,
                "avgKills": round(kills / len(rows), 2) if rows else None,
                "avgDeaths": round(deaths / len(rows), 2) if rows else None,
                "avgAssists": round(assists / len(rows), 2) if rows else None,
            },
            "arena": {
                "wins": arena_wins,
                "losses": len(arena_rows) - arena_wins,
                "winRate": round(100.0 * arena_wins / len(arena_rows), 2) if arena_rows else None,
                "avgPlacement": round(sum(placements) / len(placements), 2) if placements else None,
            },
        },
        "mostCommonChampions": [{"champion": champ, "games": count} for champ, count in champions.most_common(15)],
        "mostCommonTeammates": [{"name": name, "games": count} for name, count in teammates.most_common(20)],
        "mostCommonEnemies": [{"name": name, "games": count} for name, count in enemies.most_common(20)],
        "queues": [{"queueId": queue_id, "games": count} for queue_id, count in queues.most_common()],
        "topAugments": [
            {"augmentId": aid, "name": aug_map.get(aid, "Unknown"), "picks": count}
            for aid, count in augments.most_common(20)
        ],
        "topAugmentPairs": [
            {
                "augmentIds": [a, b],
                "names": [aug_map.get(a, "Unknown"), aug_map.get(b, "Unknown")],
                "coPicks": count,
            }
            for (a, b), count in aug_pairs.most_common(15)
        ],
        "assassinChampionStats": assassin_rows,
    }


def collect_riot_telemetry(
    riot_id: str,
    api_key: str,
    max_matches: int = 500,
    augments_path: str = "augments.json",
) -> dict[str, Any]:
    """Collect and summarize Riot match telemetry for a Riot ID like Name#TAG."""
    if "#" not in riot_id:
        raise ValueError("riot_id must be in the format Name#TAG")
    riot_name, riot_tag = riot_id.split("#", 1)
    if not riot_name or not riot_tag:
        raise ValueError("riot_id must include both game name and tag")
    if max_matches <= 0:
        raise ValueError("max_matches must be greater than 0")

    with requests.Session() as session:
        account = _fetch_account(session, api_key=api_key, riot_name=riot_name, riot_tag=riot_tag)
        puuid = str(account["puuid"])
        match_ids = _fetch_match_ids(session, api_key=api_key, puuid=puuid, max_matches=max_matches)

        local_map = _read_local_augments(Path(augments_path))
        cdragon_map = _read_cdragon_augments(session)
        aug_map = _merge_augment_maps(local_map, cdragon_map)

        rows: list[dict[str, Any]] = []
        arena_rows: list[dict[str, Any]] = []
        for match_id in match_ids:
            match = _api_get_json(session, f"{ROUTING}/lol/match/v5/matches/{match_id}?api_key={api_key}")
            if not isinstance(match, dict):
                continue
            row, arena_row = _extract_rows_from_match(match, puuid=puuid, aug_map=aug_map)
            if row is not None:
                rows.append(row)
            if arena_row is not None:
                arena_rows.append(arena_row)

    rows.sort(key=lambda row: int(row.get("timestamp", 0)), reverse=True)
    arena_rows.sort(key=lambda row: int(row.get("timestamp", 0)), reverse=True)

    summary = _build_summary(account=account, rows=rows, arena_rows=arena_rows, aug_map=aug_map)
    return {
        "summary": summary,
        "matches": rows,
        "arenaMatches": arena_rows,
    }