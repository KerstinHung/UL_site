run:
	@echo "=== Start Django ==="
	cd ulsite && ../myenv/bin/python manage.py runserver 0.0.0.0:8000

test:
	@echo "=== Start Playwright ==="
	cd frontend/tests && npx playwright test