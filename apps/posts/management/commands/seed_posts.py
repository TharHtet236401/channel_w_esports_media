"""
Seed dummy esports blog posts and regions.
Uses apps.core.constants for Region enum and DUMMY_POSTS only.
Usage:
  python manage.py seed_posts           # add seeds (skips if posts already exist)
  python manage.py seed_posts --clear   # delete all posts & regions, then seed
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.constants import Region as RegionEnum
from apps.core.constants import DUMMY_POSTS
from apps.posts.models import Post, Region


REGIONS = [r.value for r in RegionEnum]


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
