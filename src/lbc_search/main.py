import argparse
from dataclasses import dataclass
import json
from pathlib import Path

from dataclasses_json import dataclass_json
import lbc

DEFAULT_OUT = Path("lbc_results.json")


@dataclass_json
@dataclass
class AddRelevantFields:
    title: str
    description: str
    date: str
    price: float
    user_score: int
    nb_user_evaluations: int
    url: str


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        "-u",
        required=True,
        type=str,
        help="LeBonCoin search URL to query (copy/paste the full URL from your browser).",
    )
    parser.add_argument(
        "--page",
        "-p",
        type=int,
        default=1,
        help="Results page number to fetch (starts at 1).",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=999,
        help="Maximum number of ads to return (depends on what the API supports).",
    )
    parser.add_argument(
        "--out",
        "-o",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output JSON file path (default: {DEFAULT_OUT}).",
    )

    args = parser.parse_args()

    search_and_export(url=args.url, page=args.page, limit=args.limit, out=args.out)


def search_and_export(url: str, page: int, limit: int, out: Path) -> None:
    client = lbc.Client()

    result = client.search(
        url=url,
        page=page,
        limit=limit,
    )

    results = []
    for add in result.ads:
        results.append(
            AddRelevantFields(
                title=add.title,
                description=add.body,
                date=add.index_date,
                price=add.price,
                user_score=add.user.feedback.score,
                nb_user_evaluations=add.user.feedback.received_count,
                url=add.url,
            ).to_dict()
        )

    with open(out, mode="w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False, default=str)


if __name__ == "__main__":
    main()
