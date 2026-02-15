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
    "INDO",
    "PH",
    "MM",
    "SG",
    "MY",
    "HK",
    "TW",
    "JP",
    "KR",
    "CN",
    "AU",
    "NZ",
    "IE",
]

DUMMY_POSTS = [
    {
        "caption": "Worlds 2026: Format Changes and Regional Seeds Explained",
        "description": "Riot Games has announced updates to the League of Legends World Championship format. "
        "The tournament will feature a new double-elimination stage and increased regional representation. "
        "Fans and analysts weigh in on how the changes could reshape the competitive landscape.",
        "regions": ["INDO", "PH"],
    },
    {
        "caption": "Rising Star Team Secures First LEC Title in Historic Finals",
        "description": "A breakout squad claimed the LEC trophy after a nail-biting five-game series. "
        "We break down the meta, standout performances, and what this means for the region heading into MSI.",
        "regions": ["INDO", "PH"],
    },
    {
        "caption": "Valorant Champions 2026: All Qualified Teams and Schedule",
        "description": "The full lineup for Valorant Champions is set. From NA powerhouses to APAC dark horses, "
        "here’s every team, their path to qualification, and the complete schedule for the event.",
        "regions": ["INDO", "PH"],
    },
    {
        "caption": "LCK Spring Split Preview: Favorites, Sleepers, and Storylines",
        "description": "The LCK returns with roster shuffles and new contenders. We look at the favorites, "
        "underdogs to watch, and the biggest storylines heading into the spring split.",
        "regions": ["MM"],
    },
    {
        "caption": "How Esports Orgs Are Navigating the 2026 Revenue Landscape",
        "description": "Sponsorship shifts, media rights, and new revenue streams are reshaping how organizations "
        "operate. Industry insiders share how top orgs are adapting and where the market is heading.",
        "regions": ["INDO", "PH", "MM"],
    },
    {
        "caption": "Dota 2 The International: Regional Qualifier Results and Meta Snapshot",
        "description": "Regional qualifiers for TI have concluded. We recap the results, the current meta, "
        "and which heroes and strategies are defining the run-up to the main event.",
        "regions": ["CN", "AU", "NZ", "IE"],
    },
    {
        "caption": "Channel W Esports Awards 2026: Nominees and Voting Open",
        "description": "Cast your vote for players, teams, and moments of the year. We reveal the nominees "
        "across categories and how the community can participate in the Channel W Esports Awards.",
        "regions": ["AU", "NZ", "IE"],
    },
    {
        "caption": "Console to PC: Cross-Platform Esports and What’s Next",
        "description": "Cross-play and cross-platform competition are expanding. We explore how titles are "
        "handling balance, fairness, and viewership as console and PC ecosystems converge.",
        "regions": ["SG"],
    },
    {
        "caption": "Mobile Legends M5: SEA Teams Dominate Group Stage",
        "description": "Southeast Asian squads showed up strong in the M5 group stage. We recap key matches, "
        "picks and bans, and what to expect heading into the knockout rounds.",
        "regions": ["INDO", "PH", "MM", "SG", "MY"],
    },
    {
        "caption": "VCT Pacific League: Playoffs Bracket and Predictions",
        "description": "The Valorant Champions Tour Pacific playoffs are set. A look at the bracket, "
        "head-to-head form, and our predictions for who advances to the international finals.",
        "regions": ["KR", "JP", "TW", "HK", "SG"],
    },
    {
        "caption": "Biggest Roster Moves of the Off-Season So Far",
        "description": "Star players are on the move. We round up the most impactful signings and "
        "departures across League, Valorant, and Dota as teams prepare for the new season.",
        "regions": ["KR", "CN", "JP", "AU"],
    },
    {
        "caption": "Patch 14.4 Breakdown: What Changed and Why It Matters",
        "description": "The latest League of Legends patch shakes up the meta. We break down item and "
        "champion changes and how they're affecting pro play and solo queue.",
        "regions": ["INDO", "PH", "KR", "TW"],
    },
    {
        "caption": "Esports Viewership in 2026: Trends and Surprises",
        "description": "New data on peak viewership, watch time, and platform split. Which events and "
        "regions grew the most, and what it means for the industry.",
        "regions": ["AU", "NZ", "IE", "SG", "MY"],
    },
    {
        "caption": "Behind the Scenes: How One Org Built Its Academy Roster",
        "description": "From tryouts to contracts, we go inside how a top org assembled its academy "
        "lineup and how the pipeline feeds into the main roster.",
        "regions": ["KR", "CN", "IE"],
    },
    {
        "caption": "Wild Rift Icons Global Championship: Format and Favorites",
        "description": "Wild Rift's premier event is back. Here's the format, qualified teams by region, "
        "and early favorites to take the title.",
        "regions": ["CN", "KR", "JP", "SG", "MY"],
    },
    {
        "caption": "CS2 Major: Map Pool and Meta Ahead of the Event",
        "description": "The first CS2 Major is around the corner. We look at the current map pool, "
        "meta shifts, and which teams have adapted best to the new game.",
        "regions": ["IE", "AU", "NZ", "KR"],
    },
    {
        "caption": "Women in Esports: Progress and Challenges in 2026",
        "description": "A look at representation, initiatives, and barriers in competitive gaming. "
        "Players and org leads share their experiences and hopes for the future.",
        "regions": ["AU", "NZ", "IE", "PH", "SG"],
    },
    {
        "caption": "Coach Spotlight: The Minds Behind This Season's Top Teams",
        "description": "We profile the coaches driving results at the top of League and Valorant. "
        "Their philosophies, preparation habits, and how they handle pressure.",
        "regions": ["KR", "CN", "JP", "MM"],
    },
    {
        "caption": "Arena Clash: Regional Showdown Results and Highlights",
        "description": "The cross-region Arena Clash wrapped with surprise upsets and standout plays. "
        "Full results and the best moments from the broadcast.",
        "regions": ["INDO", "PH", "MM", "HK", "TW"],
    },
    {
        "caption": "New Sponsorship Deals Reshape Team Budgets",
        "description": "Several major brands have signed new esports deals. We look at who's investing, "
        "where the money is going, and how it affects team operations.",
        "regions": ["KR", "CN", "SG", "AU", "IE"],
    },
    {
        "caption": "Tier List: Top 20 Players to Watch This Split",
        "description": "Our editorial tier list of the players we're watching this split across regions. "
        "Rookies, veterans, and comeback stories.",
        "regions": ["KR", "CN", "JP", "PH", "AU"],
    },
    {
        "caption": "Community Tournaments: How Amateur Circuits Are Growing",
        "description": "Amateur and semi-pro circuits are expanding. We look at formats, prizing, "
        "and how they connect to the path-to-pro pipeline.",
        "regions": ["INDO", "PH", "MM", "MY", "NZ"],
    },
    {
        "caption": "MSI 2026: Host City and Venue Announced",
        "description": "The Mid-Season Invitational has a host. Details on the city, venue, dates, "
        "and what to expect from the first international LoL event of the year.",
        "regions": ["KR", "CN", "JP", "TW", "AU"],
    },
    {
        "caption": "Valorant Agent Meta: Who's In and Who's Out",
        "description": "The latest balance patch has shifted the agent meta. We break down pick rates "
        "in pro play and what it means for ranked and upcoming events.",
        "regions": ["KR", "JP", "SG", "PH", "IE"],
    },
    {
        "caption": "Dota 2 Patch Analysis: Item and Hero Changes",
        "description": "A major Dota patch has landed. We go through the biggest item and hero changes "
        "and how they're likely to affect the competitive meta.",
        "regions": ["CN", "KR", "SG", "AU", "NZ"],
    },
    {
        "caption": "Streaming and Pro Play: How Pros Balance Both",
        "description": "Many pros stream when they're not in bootcamp. We talk to players about "
        "scheduling, content, and keeping form while building their brand.",
        "regions": ["INDO", "PH", "KR", "AU", "IE"],
    },
    {
        "caption": "Youth Esports: Age Rules and Development Paths",
        "description": "Different titles and regions have different age rules. We summarize the landscape "
        "and how young players can progress toward pro play.",
        "regions": ["KR", "CN", "JP", "SG", "MY", "AU"],
    },
    {
        "caption": "Channel W Podcast: Episode 50 – Year in Review",
        "description": "Our 50th episode looks back at the biggest storylines of the year: roster chaos, "
        "upsets, and the state of esports. Listen now on all platforms.",
        "regions": ["INDO", "PH", "MM", "SG", "AU", "NZ", "IE"],
    },
    {
        "caption": "Bootcamp Diaries: Life Inside a Pre-Tournament Camp",
        "description": "We follow a team through their pre-event bootcamp: schedule, scrims, and "
        "how they prepare mentally and strategically for the main stage.",
        "regions": ["KR", "CN", "JP", "PH", "SG"],
    },
    {
        "caption": "Fantasy Esports: Tips for Your League Draft",
        "description": "Draft season is here. We share tips on valuing players, balancing regions, "
        "and building a roster that can compete in your fantasy league.",
        "regions": ["AU", "NZ", "IE", "SG", "MY", "HK", "TW"],
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
