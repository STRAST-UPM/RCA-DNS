import argparse
import json

from .ripeatlas_provider import RIPEAtlasProvider


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="Create global RIPE Atlas HTTP measurements (default: 10 probes/country, every 6h, 7 days)."
	)
	parser.add_argument("target_url", help="HTTP/HTTPS URL to measure, e.g. https://global.example.com/health")
	parser.add_argument("--probes-per-country", type=int, default=10)
	parser.add_argument("--interval-seconds", type=int, default=21600, help="21600 = 6 hours")
	parser.add_argument("--duration-days", type=int, default=7)
	parser.add_argument(
		"--exclude-country",
		action="append",
		default=[],
		help="ISO country code to exclude. Repeat the flag for multiple countries.",
	)
	parser.add_argument("--description-prefix", default="RCA-DNS HTTP")
	parser.add_argument("--dry-run", action="store_true", help="Compute countries and print plan without creating measurements")
	return parser


def main() -> None:
	args = build_parser().parse_args()
	provider = RIPEAtlasProvider()

	results = provider.create_global_http_measurements(
		target_url=args.target_url,
		probes_per_country=args.probes_per_country,
		interval_seconds=args.interval_seconds,
		duration_days=args.duration_days,
		excluded_countries=args.exclude_country,
		description_prefix=args.description_prefix,
		dry_run=args.dry_run,
	)

	print(json.dumps(results, indent=2))


if __name__ == "__main__":
	main()
