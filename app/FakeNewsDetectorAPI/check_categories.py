import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FakeNewsDetectorAPI.settings')
django.setup()

from core.livenews.models import LiveNews

# Get all unique categories (pillarNames)
categories = LiveNews.objects.values_list('news_category', flat=True).distinct()
print("Pillar Names (news_category) in database:")
for cat in categories:
    count = LiveNews.objects.filter(news_category=cat).count()
    print(f"  {cat}: {count} articles")

print("\nTotal articles:", LiveNews.objects.count())

# Get all unique sections
sections = LiveNews.objects.values_list('section_id', flat=True).distinct()
print("\n\nSection IDs (section_id) in database:")
for section in sections:
    count = LiveNews.objects.filter(section_id=section).count()
    print(f"  {section}: {count} articles")
