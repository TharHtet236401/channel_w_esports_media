"""
Seed dummy esports blog posts and regions.
Usage:
  python manage.py seed_posts           # add seeds (skips if posts already exist)
  python manage.py seed_posts --clear   # delete all posts & regions, then seed
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.posts.models import Post, Region


REGIONS = [
    "NA",
    "EMEA",
    "APAC",
    "LATAM",
    "KR",
]

DUMMY_POSTS = [
    {
        "caption": "Worlds 2026: Format Changes and Regional Seeds Explained",
        "description": "Riot Games has announced updates to the League of Legends World Championship format. "
        "The tournament will feature a new double-elimination stage and increased regional representation. "
        "Fans and analysts weigh in on how the changes could reshape the competitive landscape.",
        "regions": ["NA", "EMEA", "APAC", "KR"],
    },
    {
        "caption": "Rising Star Team Secures First LEC Title in Historic Finals",
        "description": "A breakout squad claimed the LEC trophy after a nail-biting five-game series. "
        "We break down the meta, standout performances, and what this means for the region heading into MSI.",
        "regions": ["EMEA"],
    },
    {
        "caption": "Valorant Champions 2026: All Qualified Teams and Schedule",
        "description": "The full lineup for Valorant Champions is set. From NA powerhouses to APAC dark horses, "
        "here’s every team, their path to qualification, and the complete schedule for the event.",
        "regions": ["NA", "EMEA", "APAC", "LATAM"],
    },
    {
        "caption": "LCK Spring Split Preview: Favorites, Sleepers, and Storylines",
        "description": "The LCK returns with roster shuffles and new contenders. We look at the favorites, "
        "underdogs to watch, and the biggest storylines heading into the spring split.",
        "regions": ["KR"],
    },
    {
        "caption": "How Esports Orgs Are Navigating the 2026 Revenue Landscape",
        "description": "Sponsorship shifts, media rights, and new revenue streams are reshaping how organizations "
        "operate. Industry insiders share how top orgs are adapting and where the market is heading.",
        "regions": ["NA", "EMEA"],
    },
    {
        "caption": "Dota 2 The International: Regional Qualifier Results and Meta Snapshot",
        "description": "Regional qualifiers for TI have concluded. We recap the results, the current meta, "
        "and which heroes and strategies are defining the run-up to the main event.",
        "regions": ["NA", "EMEA", "APAC"],
    },
    {
        "caption": "Channel W Esports Awards 2026: Nominees and Voting Open",
        "description": "Cast your vote for players, teams, and moments of the year. We reveal the nominees "
        "across categories and how the community can participate in the Channel W Esports Awards.",
        "regions": ["NA", "EMEA", "APAC", "LATAM", "KR"],
    },
    {
        "caption": "Console to PC: Cross-Platform Esports and What’s Next",
        "description": "Cross-play and cross-platform competition are expanding. We explore how titles are "
        "handling balance, fairness, and viewership as console and PC ecosystems converge.",
        "regions": ["NA", "EMEA"],
    },
]


class Command(BaseCommand):
    help = "Seed dummy esports blog posts and regions. Use --clear to delete existing data first."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing posts and regions before seeding.",
        )

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                if options["clear"]:
                    Post.objects.all().delete()
                    Region.objects.all().delete()
                    self.stdout.write(self.style.WARNING("Cleared all posts and regions."))

                regions_by_name = {}
                for name in REGIONS:
                    region, _ = Region.objects.get_or_create(name=name)
                    regions_by_name[name] = region

                existing_count = Post.objects.count()
                if existing_count > 0 and not options["clear"]:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Found {existing_count} existing post(s). Skipping seed. Use --clear to reset and reseed."
                        )
                    )
                    return

                created = 0
                for data in DUMMY_POSTS:
                    post, created_post = Post.objects.get_or_create(
                        caption=data["caption"],
                        defaults={"description": data["description"]},
                    )
                    if created_post:
                        for region_name in data["regions"]:
                            post.region.add(regions_by_name[region_name])
                        created += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Seeding complete. Created {created} new post(s) and ensured {len(REGIONS)} region(s) exist."
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Seeding failed: {e}"))
            raise
