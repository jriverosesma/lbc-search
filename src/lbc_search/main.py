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
        "--limit",
        "-l",
        type=int,
        default=100,
        help="Maximum number of ads to return.",
    )
    parser.add_argument(
        "--sort",
        "-s",
        type=str,
        default="relevance",
        help=f"Sorting type. Available values are: {[member.name.lower() for member in lbc.enums.Sort]} (default: 'relevance').",
    )
    parser.add_argument(
        "--out",
        "-o",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output JSON file path (default: {DEFAULT_OUT}).",
    )

    args = parser.parse_args()

    search_and_export(
        url=args.url,
        limit=args.limit,
        sort=lbc.enums.Sort[args.sort.upper()],
        out=args.out,
    )


def search_and_export(url: str, limit: int, sort: lbc.enums.Sort, out: Path) -> None:
    # Search
    client = lbc.Client()
    preliminary_search = client.search(url=url, limit=1, sort=sort)

    results = []
    nb_pages = preliminary_search.max_pages
    add_count = 0
    for page in range(1, nb_pages + 1):
        if add_count >= limit:
            break
        search = client.search(url=url, page=page)
        for add in search.ads:
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
            add_count += 1
            if add_count >= limit:
                break

    # Export
    with open(out, mode="w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False, default=str)

    # Display results summary
    print(f"Successfully retrieved and exported {len(results)} results to {out}")


if __name__ == "__main__":
    main()
