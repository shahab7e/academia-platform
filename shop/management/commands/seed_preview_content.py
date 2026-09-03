"""Seed the shop and the homepage gallery with the live site's content.

Local development starts from an empty database, so the shop and the homepage
gallery render as empty states and the site can't be previewed properly. This
command loads the catalogue captured from the production site
(`data/preview/*.json`) whose images live under `MEDIA_ROOT`.

It is idempotent: rows are matched by title and updated in place, so it can be
re-run after refreshing the JSON files.
"""

import json

from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.models import User
from contents.models import GalleryImage
from shop.models import Product

PREVIEW_DIR = settings.BASE_DIR / "data" / "preview"


class Command(BaseCommand):
    help = "Load preview shop products and gallery images captured from the live site."

    def add_arguments(self, parser):
        parser.add_argument(
            "--creator",
            help="Username to own the seeded products (defaults to the first superuser).",
        )

    def handle(self, *args, **options):
        creator = self._get_creator(options.get("creator"))
        self.stdout.write(f"Products are owned by: {creator.username}")
        self._seed_products(creator)
        self._seed_gallery()

    def _get_creator(self, username):
        if username:
            return User.objects.get(username=username)
        creator = (
            User.objects.filter(is_superuser=True).order_by("id").first()
            or User.objects.filter(role="admin").order_by("id").first()
            or User.objects.order_by("id").first()
        )
        if creator is None:
            raise SystemExit("No user exists to own the products - create one first.")
        return creator

    def _load(self, filename):
        path = PREVIEW_DIR / filename
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)

    def _check_image(self, relative_path):
        """Warn about (but don't skip) rows whose image wasn't downloaded."""
        if not relative_path:
            return None
        if not (settings.MEDIA_ROOT / relative_path).exists():
            self.stdout.write(self.style.WARNING(f"  missing image file: {relative_path}"))
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
                    "image": self._check_image(item["image"]) or "",
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
                    "image": self._check_image(item["image"]) or "",
                    "is_published": True,
                },
            )
            created += was_created
            updated += not was_created
        self.stdout.write(self.style.SUCCESS(f"Gallery images: {created} created, {updated} updated"))
