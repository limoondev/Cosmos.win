# Cosmos.win — Upgrade Task

/ = In Progress 
X = Done
Nothing = Not Done

## 1. API Keys Embedded into Software
- [x] Embed default API keys directly in [utils/api_keys.py](file:///c:/Users/bruck/Downloads/Code/Cosmos.win/utils/api_keys.py) as hardcoded fallbacks
- [x] Remove dependency on external [api-keys.json](file:///c:/Users/bruck/Downloads/Code/Cosmos.win/api-keys.json) for default keys
- [x] Keep user-override capability (if user adds their own key, use that instead)

## 2. License Key Website (10-min wait → 24h key) -> Handled Internally
- [X] Create `website/` folder with HTML/CSS/JS for the key distribution site (Skipped, keys are generated internally now)
- [X] Implement 10-minute countdown timer with animated UI (Internal proof-of-work implemented)
- [X] Generate time-limited 24h license keys via JS (Now generated dynamically internally)
- [X] Update [utils/ui.py](file:///c:/Users/bruck/Downloads/Code/Cosmos.win/utils/ui.py) license gate to generate and validate internal unique session keys
- [X] Keep "Lifetime-Developer" as a master bypass key

## 3. Improve Modules
- [X] Fix broken [threat_intel_lookup.py](file:///c:/Users/bruck/Downloads/Code/Cosmos.win/modules/threat_intel_lookup.py) (syntax error in [run()](file:///c:/Users/bruck/Downloads/Code/Cosmos.win/utils/api_keys.py#240-313) method)
- [X] Add export-to-file capability to key modules
- [X] Improve error handling across modules (graceful API failures)
- [X] Add result caching to avoid redundant API calls

## 4. General Improvements
- [X] Upgrade version to v6.0
- [X] Improve boot animation with smoother transitions
- [X] Add system info to dashboard (CPU, RAM, disk)
- [X] Update [build.py](file:///c:/Users/bruck/Downloads/Code/Cosmos.win/build.py) to include website assets (Not needed anymore since it's internal)

## 5. Font and UI Aesthetics
- [X] Investigate applying SF Pro Bold programmatically via `ctypes` (Not natively supported by `conhost.exe`)
- [X] Implement programmatic fallback to "SF Mono" or "Cascadia Code" via `ctypes`
- [X] Add startup prompt recommending Windows Terminal for full custom font support
