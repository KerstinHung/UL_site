## Dependencies
```bash
# macOS Sonoma 14.6.1
brew install node
# Auto-updating Homebrew... <= waiting for auto updating 5~15 min
node -v
npm -v
```
```bash
cd frontend
# 1. Install Playwright
npm init -y 
npm install -D @playwright/test
# 2. Install browser(necessary) env
npx playwright install
# 3. Test
npx playwright test
```