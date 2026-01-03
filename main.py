#!/usr/bin/env python3
"""
Created by SURYOX, heartbroken and fed up with everything
FUCK YOU ALL, SHIT!
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
import time
import random
import json
import os
import re
from difflib import SequenceMatcher
from tqdm import tqdm
from colorama import Fore, init
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import hashlib
from playwright.async_api import async_playwright
import asyncio
from tqdm import tqdm

# initialize colorama
init(autoreset=True)

# ---------------- Configuration ----------------
DEFAULT_PATHS = [
    "", "/",  # redirect/root checks

    # Generic admin
    "admin/", "administrator/", "admin/login/", "admin/index.php",
    "admin/dashboard/", "admin/home/", "admin/panel/", "adminarea/",
    "admin_area/", "admin-console/", "admincontrol/", "admincp/",
    "admin1/", "admin2/", "admin3/", "admin123/", "admin4/",

    # Auth/login routes
    "auth/", "auth/login/", "login/", "signin/", "user/login/",
    "users/login/", "account/login/", "access/", "secure/login/",

    # Dashboard/backoffice
    "dashboard/", "backend/", "panel/", "console/", "system/",
    "manage/", "management/", "control/", "root/", "staff/", "private/",
    "internal/", "secure/", "restricted/", "settings/", "cpanel/",

    # WordPress
    "wp-admin/", "wp-login.php", "wp-admin/install.php",
    "wp-content/admin/",

    # Joomla
    "administrator/index.php", "administrator/login.php",

    # Drupal
    "admin/people/", "admin/config/",

    # Magento
    "adminhtml/", "backend/admin/",

    # Laravel & frameworks
    "admin.php", "admin/home", "cp/login",
    "dashboard/login", "controlpanel/",

    # Hosting panels
    "whm/", "webadmin/",

    # Variants + extensions
    "admin.html", "admin.asp", "admin.aspx", "admin.jsp",
    "login.php", "login.html", "login.asp", "login.aspx",

    # Deep guesses
    "superadmin/", "master/", "godmode/", "hidden/", "secret/",
    "secureadmin/", "siteadmin/", "portal/admin/", "cms/admin/",

    # Company patterns
    "internal/admin/", "ops/admin/", "team/admin/", "office/admin/",

    # Admin Umum Indonesia
    "adm/", "panel-admin/", "adminweb/", "adminweb/login/",
    "adminweb/index.php", "adminkita/", "admin_sekolah/",
    "admin_sekolah/login/", "admin_sekolah/index.php",
    "adminppdb/", "ppdb/admin/", "operator/", "operator/login/",
    "operator/index.php",

    # Sekolah / Kampus
    "siakad/", "siakad/login/", "siakad/admin/",
    "elearning/", "elearning/login/", "elearning/admin/",
    "e-learning/", "e-learning/login/", "e-learning/admin/",
    "cbt/", "cbt/login/", "cbt/admin/",
    "ujian/", "ujian/admin/", "ujian/login/",
    "school/admin/", "siswa/admin/", "guru/admin/",

    # PPDB
    "ppdb/", "ppdb/login/", "ppdb/operator/",
    "pendaftaran/admin/", "pendaftaran/login/",

    # Pemerintah
    "simdesa/", "simdesa/admin/", "desa/admin/",
    "sipd/", "sipd/admin/", "e-office/", "e-office/admin/",
    "dinas/admin/", "pemda/admin/", "gov/admin/",

    # Toko Online
    "toko/admin/", "toko/login/", "shop-admin/", "toko_online/admin/",
    "seller/", "seller/login/", "penjual/admin/", "merchant/admin/",

    # Kasir
    "kasir/", "kasir/login/", "kasir/admin/",
    "pos/admin/", "pos/login/", "pos/backend/",

    # Developer Indonesia
    "users/admin/", "dashboard/admin/",
    "manajemen/", "manajemen/admin/",
    "pengaturan/", "pengaturan/admin/",
    "backend/login/", "backend/admin/",

    # CMS lokal
    "batara/admin/", "batara/login/",
    "max/b-admin/", "max/b-admin/login/",
    "ci-admin/", "ci-admin/login/",

    # Variasi path umum
    "login-admin/", "admin-login/", "loginadmin/",
    "masteradmin/",

    # File populer
    "adm.php", "dashboard.php",

    # ========= JOOMLA EXTRA =========
    "administrator/components/", "administrator/templates/",

    # ========= DRUPAL EXTRA =========
    "user/reset/", "admin/content/", "admin/structure/",

    # ========= MAGENTO EXTRA =========
    "adminhtml/login/",

    # ========= LARAVEL EXTRA =========
    "admin/login", "admin/auth/login", "admin/auth",
    "admincp/login", "cp/admin/", "panel/login", "panel/admin/",
    "portal/admin/",

    # ========= CODEIGNITER =========
    "ci-panel/", "ci-panel/login/",

    # ========= NODEJS / REACT / VUE =========
    "admin/dashboard", "admin/signin", "admin/auth/login",
    "admin/auth", "api/admin/", "api/admin/login/",
    "api/auth/login/", "api/backoffice/", "api/management/",

    # ========= HOSTING PANELS EXTRA =========
    "plesk/", "webmail/", "directadmin/", "vps/admin/", "server/admin/",

    # ========= FILE EXT =========
    "signin.php", "signin.html",

    # ========= Modern framework assets =========
    "admin/_next/", "admin/_nuxt/", "admin/_app/",
    "dashboard/_next/", "dashboard/_nuxt/",

    # ========= AUTO-GENERATED GUESS PATTERNS =========
    *[
        f"{prefix}{suffix}/"
        for prefix in [
            "admin", "administrator", "manage", "panel", "dashboard",
            "system", "secure", "root", "internal", "private", "portal"
        ]
        for suffix in [
            "", "1", "2", "3", "4", "5", "123", "login", "cp",
            "system", "home", "main", "panel", "console", "area"
        ]
    ],

    # ========= API ENDPOINTS =========
    "api/v1/admin/", "api/v2/admin/",

    # ========= 1000+ RANDOMIZED =========
    *[f"admin{n}/" for n in range(1, 501)],
    *[f"panel{n}/" for n in range(1, 301)],
    *[f"login{n}/" for n in range(1, 151)],
    *[f"dashboard{n}/" for n in range(1, 151)],
    *[f"system{n}/" for n in range(1, 101)],
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"
]

# default thresholds
SIMILARITY_THRESHOLD = 0.90  # ratio above which page considered same as homepage
DEFAULT_THREADS = 20
DEFAULT_DELAY = 0.0  # seconds between requests per worker (helps throttle)
DEFAULT_RETRIES = 2
REQUEST_TIMEOUT = 8  # seconds


# ---------------- Helpers ----------------
def similar(a: str, b: str) -> float:
    """Return similarity ratio between two strings (0..1)."""
    return SequenceMatcher(None, a, b).ratio()


def normalize_url(base: str, path: str) -> str:
    """Construct absolute url from base and path; handles leading slashes."""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return urljoin(base.rstrip("/") + "/", path.lstrip("/"))


def contains_password_field(html: str) -> bool:
    """Simple heuristic: check for <input ... type='password' ...>"""
    if not html:
        return False
    # use regex to catch variations like type="password" or type='password' or type=password
    return bool(re.search(r'<input[^>]+type\s*=\s*["\']?password', html, re.I))


# ---------------- Main Class ----------------
class AdminFinderAdvanced:
    def __init__(
        self,
        target,
        wordlist=None,
        threads=DEFAULT_THREADS,
        delay=DEFAULT_DELAY,
        retries=DEFAULT_RETRIES,
        proxy=None,
        similarity_threshold=SIMILARITY_THRESHOLD,
        timeout=REQUEST_TIMEOUT,
        user_agents=None,
        save_screenshots=True,
    ):
        self.target = target.rstrip("/")
        self.threads = threads
        self.delay = float(delay)
        self.retries = int(retries)
        self.similarity_threshold = float(similarity_threshold)
        self.timeout = timeout
        self.proxy = proxy  # str like "http://127.0.0.1:8080" or None
        self.user_agents = user_agents or USER_AGENTS

        # paths
        self.paths = wordlist or DEFAULT_PATHS

        self.save_screenshots = save_screenshots
        self.skip_screenshot_notified = False

        # session base
        self.session = requests.Session()
        self.session.headers.update({"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})

        if proxy:
            self.session.proxies.update({
                "http": proxy,
                "https": proxy
            })

    def _get(self, url):
        """Perform GET with retries, random UA, timeout, and optional small delay."""
        last_exc = None
        for attempt in range(self.retries + 1):
            try:
                ua = random.choice(self.user_agents)
                headers = {"User-Agent": ua}
                resp = self.session.get(url, headers=headers, timeout=self.timeout, allow_redirects=False)
                if self.delay > 0:
                    time.sleep(self.delay)
                return resp
            except requests.RequestException as e:
                last_exc = e
                time.sleep(0.2)
                continue
        raise last_exc

    def fetch_homepage(self):
        """Fetch homepage content for similarity comparison."""
        try:
            resp = self._get(self.target + "/")
            content = resp.text or ""
            return {"status": resp.status_code, "content": content, "headers": dict(resp.headers)}
        except Exception:
            try:
                r2 = self._get(self.target)
                return {"status": r2.status_code, "content": r2.text or "", "headers": dict(r2.headers)}
            except Exception:
                return {"status": None, "content": "", "headers": {}}

    def analyze_path(self, path, homepage_content, max_redirects=3):
        """Improved redirect-following version with login-form detection."""
        url = normalize_url(self.target, path)

        result = {
            "url": url,
            "path": path,
            "status": None,
            "redirect_chain": [],
            "final_url": url,
            "content_length": None,
            "is_admin_candidate": False,
            "note": ""
        }

        try:
            resp = self._get(url)
            status = resp.status_code
            result["status"] = status

            redirect_hops = 0
            current_url = url
            current_resp = resp

            # follow redirects up to max_redirects
            while status in (301, 302, 303, 307, 308) and redirect_hops < max_redirects:
                loc = current_resp.headers.get("Location", "")
                if not loc:
                    break

                loc = urljoin(current_url, loc)
                result["redirect_chain"].append(loc)

                parsed = urlparse(loc)

                # if redirect to root -> likely homepage
                if parsed.path in ("", "/"):
                    result["note"] = "redirects to homepage/root"
                    result["is_admin_candidate"] = False
                    result["final_url"] = loc
                    return result

                # if redirect to similar path (e.g. trailing slash), mark and continue
                if path.strip("/").lower() in parsed.path.lower():
                    result["note"] = f"redirects to same admin-like path: {loc}"

                # if redirect to login/admin-related path, consider candidate
                if any(k in parsed.path.lower() for k in ("login", "wp-login", "wp-admin", "admin", "cpanel")):
                    result["is_admin_candidate"] = True
                    result["note"] = f"redirects to login/admin: {loc}"

                # follow next hop
                current_resp = self._get(loc)
                current_url = loc
                status = current_resp.status_code
                redirect_hops += 1

            final_content = current_resp.text or ""
            result["final_url"] = current_url
            result["content_length"] = len(final_content)
            result["status"] = status

            # 403 is a good indicator
            if status == 403:
                result["is_admin_candidate"] = True
                result["note"] += " | 403 Forbidden (exists)"
                return result

            # 200 -> similarity check + login form detection
            if status == 200:
                ratio = similar(homepage_content, final_content) if homepage_content else 0.0

                # detect password fields (strong signal of login/admin)
                has_pw = contains_password_field(final_content)
                if has_pw:
                    result["is_admin_candidate"] = True
                    result["note"] += " | contains <input type=password> (likely login/admin)"
                    # still compute similarity for info
                    result["note"] += f" | similarity {ratio:.3f}"
                    return result

                if ratio >= self.similarity_threshold:
                    result["is_admin_candidate"] = False
                    result["note"] += f" | 200 but similarity {ratio:.3f} -> homepage-like (ignored)"
                else:
                    result["is_admin_candidate"] = True
                    result["note"] += f" | 200 OK but content differs (similarity {ratio:.3f})"
                return result

            # other statuses
            result["note"] += f" | final status {status} ignored"
            result["is_admin_candidate"] = False
            return result

        except Exception as e:
            result["note"] = f"error: {e}"
            return result


    def run(self, save_json_path=None, show_only_candidates=True):
        print("[" + colored("*", "green") + "]" + f" Starting advanced admin finder on: " + colored(f"{self.target}", "green"))
        print("[" + colored("*", "green") + "]" + f" Threads: " + colored(f"{self.threads}", "green") + ", Delay: " + colored(f"{self.delay}s", "green") + ", Retries: " + colored(f"{self.retries}", "green"))
        if self.proxy:
            print("[" + colored("+", "green") + "]" + f" Proxy enabled: {self.proxy}")

        homepage = self.fetch_homepage()
        homepage_content = homepage.get("content", "") if homepage else ""
        if homepage.get("status"):
            print("[" + colored("*", "green") + "]" + f" Homepage status: {homepage.get('status')} (length={len(homepage_content)})")
        else:
            print("[" + colored("!", "red") + "]" + " Could not fetch homepage content; similarity checks will be limited.")

        results = []
        candidates = []

        # Use ThreadPoolExecutor with progress bar
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_path = {executor.submit(self.analyze_path, p, homepage_content): p for p in self.paths}
            progress = tqdm(as_completed(future_to_path), total=len(future_to_path), desc="[" + colored("*", "green") + "]" + " Scanning", unit="req", dynamic_ncols=True, leave=False, position=0)
            for fut in progress:
                try:
                    res = fut.result()
                except Exception:
                    continue
                results.append(res)
                if res.get("is_admin_candidate"):
                    candidates.append(res)

                    if not self.save_screenshots:
                        if not self.skip_screenshot_notified:
                            tqdm.write("[" + colored("!", "red") + "]" +" Screenshot skipped by user choice")
                            self.skip_screenshot_notified = True
                        continue


                    # ambil index kandidat ke berapa
                    if candidates:
                        tqdm.write(colored("[" + colored("*", "cyan") + "]" + f" Taking screenshots for " + colored(f"{len(candidates)}", "cyan") + " admin candidates..."))

                        # kandidat terbaru saja
                        i = len(candidates)
                        c = candidates[-1]
                        
                        screenshot = asyncio.run(
                            screenshot_page(
                                url=c["final_url"],
                                base_output_folder=os.path.dirname(save_json_path),
                                index=i
                            )
                        )
                        
                        if screenshot:
                            tqdm.write(colored("[" + colored("*", "green") + "]" + f" Screenshot saved: " + colored(f"{screenshot}", "green")))
                        else:
                            tqdm.write(colored("[" + colored("!", "red") + "]" + f" Failed to screenshot: " + colored(f"{c['final_url']}", "red")))


        final_list = candidates if show_only_candidates else results

        print("\n[" + colored("*", "green") + "]" + " Scan complete.")
        print("[" + colored("*", "green") + "]" + f" Candidate admin pages found: {len(candidates)}")
        if len(candidates) > 0:
            for c in candidates:
                print(f" - " + colored(f"{c['url']}", "green") + f" (status: {c['status']}) note: {c['note']}")

        if save_json_path:
            try:
                with open(save_json_path, "w", encoding="utf-8") as f:
                    json.dump({"target": self.target, "results": results, "candidates": candidates}, f, indent=2, ensure_ascii=False)
                print("[" + colored("*", "green") + "]" + f" Results saved to: " + colored(f"{save_json}", "green"))
            except Exception as e:
                print("[" + colored("!", "red") + "]" + f" Failed saving JSON: {e}")

        return final_list


# ---------------- CLI / Interactive ----------------
def load_wordlist_from_file(path):
    if not path:
        return None
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    return lines


def title():
    sub = Fore.RESET + "V1.0"
    print(Fore.GREEN + rf"""
    ___       __          _          _______           __
   /   | ____/ /___ ___  (_)___     / ____(_)___  ____/ /__  _____
  / /| |/ __  / __ `__ \/ / __ \   / /_  / / __ \/ __  / _ \/ ___/
 / ___ / /_/ / / / / / / / / / /  / __/ / / / / / /_/ /  __/ /
/_/  |_\__,_/_/ /_/ /_/_/_/ /_/  /_/   /_/_/ /_/\__,_/\___/_/    {sub}""")
    print()
    print("[" + colored(" Admin Finder ", "green") + "] Made By " + colored("SURYOX", "green"))
    print()
    print("[" + colored(" github.com/suryox666 ", "green") + "] | [ " + colored("saweria.co/suryos", "green") + " ] | [ " + colored("trakteer.id/suryos", "green") + " ]")
    print()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def ensure_result_folder():
    folder = "results"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

async def screenshot_page(url, base_output_folder, index):
    screenshot_folder = os.path.join(base_output_folder, "screenshots")
    os.makedirs(screenshot_folder, exist_ok=True)

    filename = os.path.join(screenshot_folder, f"candidate_{index}.png")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url, timeout=20000, wait_until="networkidle")
            await page.screenshot(path=filename, full_page=True)
            await browser.close()

        return filename
    except Exception:
        return None


def build_output_path(base_folder, target):
    parsed = urlparse(target)
    domain = parsed.netloc or parsed.path  # handle input tanpa http/https
    domain = re.sub(r'[^A-Za-z0-9]', '_', domain)  # sanitize

    # buat folder per target/domain
    folder = os.path.join(base_folder, domain)
    os.makedirs(folder, exist_ok=True)

    # filename berdasarkan tanggal
    filename = f"{time.strftime('%Y%m%d_%H%M%S')}.json"

    return os.path.join(folder, filename)

if __name__ == "__main__":
    clear()
    title()
    try:
        target = input("[" + colored("+", "green") + "]" + " Masukkan URL target (contoh: https://example.com): ").strip()
        choice = input("[" + colored("+", "green") + "]" + " Default/Custom Wordlist? (D/C): ").strip()
        wordlist = None
        if choice.lower() == "c":
            wl_path = input("[" + colored("+", "green") + "]" + " Masukkan path wordlist: ").strip()
            try:
                wordlist = load_wordlist_from_file(wl_path)
                print("[" + colored("*", "green") + "]" + f" Loaded {len(wordlist)} paths from " + colored(f"{wl_path}", "green"))
            except FileNotFoundError:
                print("[" + colored("!", "red") + "]" + " Wordlist '" + colored(f"{wl_path}", "green") + "' tidak ditemukan. Menggunakan default.")
                wordlist = None

        threads = input("[" + colored("+", "green") + "]" + f" Jumlah thread (default {DEFAULT_THREADS}): ").strip()
        threads = int(threads) if threads.isdigit() else DEFAULT_THREADS

        delay = input("[" + colored("+", "green") + "]" + f" Delay antar request per worker (detik, default {DEFAULT_DELAY}): ").strip()
        try:
            delay = float(delay) if delay != "" else DEFAULT_DELAY
        except ValueError:
            delay = DEFAULT_DELAY

        retries = input("[" + colored("+", "green") + "]" + f" Retries saat error (default {DEFAULT_RETRIES}): ").strip()
        retries = int(retries) if retries.isdigit() else DEFAULT_RETRIES

        proxy = input("[" + colored("+", "green") + "]" + " Gunakan proxy? masukkan (http://127.0.0.1:8080) atau kosong: ").strip() or None

        sim_thr = input("[" + colored("+", "green") + "]" + f" Similarity threshold 0..1 (default {SIMILARITY_THRESHOLD}): ").strip()
        try:
            sim_thr = float(sim_thr) if sim_thr != "" else SIMILARITY_THRESHOLD
        except ValueError:
            sim_thr = SIMILARITY_THRESHOLD

        save_sc = input("[" + colored("+", "green") + "]" + " Simpan hasil screenshot? (Y/N, default Y): ").strip().lower()
        save_screenshots = False if save_sc == "n" else True

        print()

        af = AdminFinderAdvanced(
            target=target,
            wordlist=wordlist,
            threads=threads,
            delay=delay,
            retries=retries,
            proxy=proxy,
            similarity_threshold=sim_thr,
            save_screenshots=save_screenshots
        )

        folder = ensure_result_folder()
        save_json = build_output_path(folder, target)

        af.run(save_json_path=save_json)
    except KeyboardInterrupt:
        print()
        print(colored("[" + colored("ERROR!", "red") + "]" + "System rejected your input 🔒"))
        time.sleep(3)
        exit
