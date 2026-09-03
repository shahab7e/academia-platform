"""Seed the shop, the homepage gallery, and demo accounts for a preview deploy.

A fresh database (local SQLite or a brand-new Render Postgres) starts empty,
so the shop and the homepage gallery render as empty states and there's no
account to log in with. This command loads the catalogue captured from the
production site (`data/preview/*.json`), copies its demo images from
`data/preview/assets/` into `MEDIA_ROOT`, and ensures a demo admin + student
account exist.

It is idempotent: rows are matched by title/username and updated in place, so
it can be safely re-run (e.g. on every deploy) after refreshing the JSON files.
"""

import json
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.models import User, UserProfile
from contents.models import GalleryImage
from shop.models import Product

PREVIEW_DIR = settings.BASE_DIR / "data" / "preview"
PREVIEW_MEDIA_DIR = PREVIEW_DIR / "assets"

# Demo login handed to whoever needs to click through the deployed preview.
DEMO_STUDENT_USERNAME = "employer_demo"
DEMO_STUDENT_PASSWORD = "Kanoon@2026Demo"
DEMO_STUDENT_NATIONAL_ID = "0012345679"  # passes the checksum, not a real person's ID
DEMO_STUDENT_PHONE = "09120000000"

DEMO_ADMIN_USERNAME = "admin_demo"
DEMO_ADMIN_PASSWORD = "Kanoon@2026Admin"


class Command(BaseCommand):
    help = "Load preview shop products, gallery images, and demo accounts captured from the live site."

    def add_arguments(self, parser):
        parser.add_argument(
            "--creator",
            help="Username to own the seeded products (defaults to the first superuser, "
            "creating a demo admin if none exists).",
        )

    def handle(self, *args, **options):
        self._ensure_demo_users()
        creator = self._get_creator(options.get("creator"))
        self.stdout.write(f"Products are owned by: {creator.username}")
        self._seed_products(creator)
        self._seed_gallery()

    def _ensure_demo_users(self):
        admin, created = User.objects.update_or_create(
            username=DEMO_ADMIN_USERNAME,
            defaults={"role": User.ADMIN, "is_staff": True, "is_superuser": True},
        )
        if created:
            admin.set_password(DEMO_ADMIN_PASSWORD)
            admin.save(update_fields=["password"])
            self.stdout.write(self.style.SUCCESS(f"Created demo admin: {DEMO_ADMIN_USERNAME}"))

        student, created = User.objects.update_or_create(
            username=DEMO_STUDENT_USERNAME,
            defaults={"role": User.STUDENT, "first_name": "کارفرما", "last_name": "دمو"},
        )
        if created:
            student.set_password(DEMO_STUDENT_PASSWORD)
            student.save(update_fields=["password"])
            self.stdout.write(self.style.SUCCESS(f"Created demo student: {DEMO_STUDENT_USERNAME}"))
        UserProfile.objects.update_or_create(
            user=student,
            defaults={
                "national_id": DEMO_STUDENT_NATIONAL_ID,
                "phone_number": DEMO_STUDENT_PHONE,
                "grade": "12",
            },
        )

    def _get_creator(self, username):
        if username:
            return User.objects.get(username=username)
        return (
            User.objects.filter(is_superuser=True).order_by("id").first()
            or User.objects.filter(role="admin").order_by("id").first()
            or User.objects.order_by("id").first()
        )

    def _load(self, filename):
        path = PREVIEW_DIR / filename
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)

    def _resolve_image(self, relative_path):
        """Copy a demo image into MEDIA_ROOT (if needed) and return its path."""
        if not relative_path:
            return None
        dest = settings.MEDIA_ROOT / relative_path
        if not dest.exists():
            src = PREVIEW_MEDIA_DIR / relative_path
            if src.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            else:
                self.stdout.write(self.style.WARNING(f"  missing demo image: {relative_path}"))
        return relative_path

    def _seed_products(self, creator):
        created = updated = 0
        for item in self._load("shop_products.json"):
            _, was_created = Product.objects.update_or_create(
                title=item["title"],
                defaults={
                    "description": item["description"],
                    "price": item["price"],
                    "product_type": item["product_type"],
                    "is_active": item["is_active"],
                    "image": self._resolve_image(item["image"]) or "",
                    "stock_quantity": item["stock_quantity"],
                    "requires_shipping": item["requires_shipping"],
                    "shipping_cost": item["shipping_cost"],
                    "weight": item["weight"],
                    "dimensions": item["dimensions"],
                    "creator": creator,
                },
            )
            created += was_created
            updated += not was_created
        self.stdout.write(self.style.SUCCESS(f"Products: {created} created, {updated} updated"))

    def _seed_gallery(self):
        created = updated = 0
        for item in self._load("gallery_images.json"):
            _, was_created = GalleryImage.objects.update_or_create(
                title=item["title"],
                defaults={
                    "description": item["description"],
                    "order": item["order"],
                    "image": self._resolve_image(item["image"]) or "",
                    "is_published": True,
                },
            )
            created += was_created
            updated += not was_created
        self.stdout.write(self.style.SUCCESS(f"Gallery images: {created} created, {updated} updated"))
