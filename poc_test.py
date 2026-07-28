#!/usr/bin/env python3
"""AutoPoC Test Script for Second-Inc/second"""
import json, os, sys, time, urllib.request, urllib.error

SERVICE_URL = os.environ.get("SERVICE_URL", sys.argv[1] if len(sys.argv) > 1 else "")
WORKER_URL = os.environ.get("WORKER_URL", sys.argv[2] if len(sys.argv) > 2 else "")
MAX_RETRIES = 5
RETRY_DELAY = 10
results = []

def test_scenario(name, description, method, path, body=None,
                  expected_status=200, expected_content=None, timeout=30, base_url=None):
    url_base = base_url or SERVICE_URL
    url = f"{url_base.rstrip('/')}{path}"
    start = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if body:
                data = json.dumps(body).encode() if isinstance(body, dict) else body.encode()
                req = urllib.request.Request(url, data=data, method=method)
                req.add_header("Content-Type", "application/json")
            else:
                req = urllib.request.Request(url, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                response_body = resp.read().decode()
                if status == expected_status:
                    if expected_content and expected_content not in response_body:
                        r = {"scenario_name": name, "status": "fail",
                             "output": response_body[:2000],
                             "error_message": f"Expected '{expected_content}' not in response",
                             "duration_seconds": round(time.time()-start, 2)}
                    else:
                        r = {"scenario_name": name, "status": "pass",
                             "output": response_body[:2000], "error_message": None,
                             "duration_seconds": round(time.time()-start, 2)}
                    results.append(r); return r
                elif attempt < MAX_RETRIES - 1:
                    print(f"  [{name}] Retry {attempt+1}/{MAX_RETRIES}: got status {status}", file=sys.stderr)
                    time.sleep(RETRY_DELAY); continue
                else:
                    r = {"scenario_name": name, "status": "fail",
                         "output": response_body[:2000],
                         "error_message": f"Expected {expected_status}, got {status}",
                         "duration_seconds": round(time.time()-start, 2)}
                    results.append(r); return r
        except urllib.error.HTTPError as e:
            resp_body = ""
            try:
                resp_body = e.read().decode()[:2000]
            except Exception:
                pass
            if e.code == expected_status:
                r = {"scenario_name": name, "status": "pass",
                     "output": resp_body, "error_message": None,
                     "duration_seconds": round(time.time()-start, 2)}
                results.append(r); return r
            if attempt < MAX_RETRIES - 1:
                print(f"  [{name}] Retry {attempt+1}/{MAX_RETRIES}: HTTP {e.code}", file=sys.stderr)
                time.sleep(RETRY_DELAY)
            else:
                r = {"scenario_name": name, "status": "fail", "output": resp_body,
                     "error_message": f"HTTP {e.code}: {e.reason}",
                     "duration_seconds": round(time.time()-start, 2)}
                results.append(r); return r
        except urllib.error.URLError as e:
            if attempt < MAX_RETRIES - 1:
                print(f"  [{name}] Retry {attempt+1}/{MAX_RETRIES}: {e}", file=sys.stderr)
                time.sleep(RETRY_DELAY)
            else:
                r = {"scenario_name": name, "status": "error", "output": "",
                     "error_message": f"Unreachable after {MAX_RETRIES} attempts: {e}",
                     "duration_seconds": round(time.time()-start, 2)}
                results.append(r); return r
        except Exception as e:
            r = {"scenario_name": name, "status": "error", "output": "",
                 "error_message": str(e),
                 "duration_seconds": round(time.time()-start, 2)}
            results.append(r); return r

# === SCENARIOS ===

# Scenario 1: Web health check
print("Testing: web-health-check", file=sys.stderr)
test_scenario("web-health-check",
              "Verify web app health endpoint",
              "GET", "/api/health",
              expected_status=200, timeout=30)

# Scenario 2: Web homepage
print("Testing: web-homepage", file=sys.stderr)
test_scenario("web-homepage",
              "Verify web frontend serves main page",
              "GET", "/",
              expected_status=200, timeout=30)

# Scenario 3: Worker health check  
if WORKER_URL:
    print("Testing: worker-health-check", file=sys.stderr)
    test_scenario("worker-health-check",
                  "Verify worker service responds",
                  "GET", "/",
                  expected_status=200, timeout=30,
                  base_url=WORKER_URL)
else:
    results.append({"scenario_name": "worker-health-check", "status": "skip",
                   "output": "No WORKER_URL provided", "error_message": None,
                   "duration_seconds": 0})

# === END SCENARIOS ===

print(json.dumps({"results": results}, indent=2))
sys.exit(1 if any(r["status"] in ("fail", "error") for r in results) else 0)
