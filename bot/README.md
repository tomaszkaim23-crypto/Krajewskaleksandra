# Bot „Efekty” na Telegramie

Ola wysyła botowi **zdjęcie z zabiegu** i krótki opis (może go podyktować mikrofonem na klawiaturze telefonu). Bot:

1. pisze z tego wpis na stronę słowami, których ludzie szukają w Google (Claude, model Opus 5.5),
2. odsyła szkic do Oli z przyciskami **✅ Publikuj / ✏️ Popraw / ❌ Anuluj**,
3. po zatwierdzeniu publikuje nową podstronę w sekcji `/efekty/`, aktualizuje listę wpisów, sekcję „Najnowsze efekty” na stronie głównej i mapę strony dla Google (`sitemap.xml`),
4. odsyła gotowy **post do wizytówki Google** do skopiowania.

## Jak to działa

```
Telegram (Ola) ──► Cloudflare Worker (ten folder) ──► Claude API (tekst ze zdjęcia)
                           │
                           └──► GitHub API (commit) ──► GitHub Pages (strona)
```

Bot działa na **Cloudflare Workers** (plan darmowy wystarczy). Szkice trzyma przez 3 dni w Cloudflare KV.

## Koszty

| Usługa | Koszt |
|---|---|
| Telegram, Cloudflare Workers (plan darmowy), GitHub | 0 zł |
| Claude API (Anthropic) | szacunkowo kilkanaście–kilkadziesiąt groszy za wpis (zdjęcie + tekst, model Opus 5.5) |

Do Anthropic wpłacasz z góry, np. 5 USD, i to wystarczy na bardzo wiele wpisów. W panelu można ustawić limit wydatków.

> ⚠️ **Zawsze uruchamiaj komendy `npx wrangler …` i `npm run deploy` w folderze `bot`.** Konfiguracja bota jest w `bot/wrangler.jsonc`, a w folderze głównym leży osobna konfiguracja **strony** (`wrangler.jsonc`). Pomylenie folderów nadpisze stronę.

## Uruchomienie (jednorazowo, ok. 30–40 minut na komputerze)

Potrzebujesz komputera z zainstalowanym **Node.js** (https://nodejs.org, wersja LTS).

### 1. Utwórz bota na Telegramie
1. W Telegramie napisz do **@BotFather** → `/newbot`.
2. Podaj nazwę (np. *Efekty Krajewska Studio*) i login kończący się na `bot`.
3. Skopiuj **token** (wygląda jak `123456:ABC-...`). To hasło do bota, nie pokazuj go nikomu.

### 2. Klucz do Claude API
1. Wejdź na https://console.anthropic.com i załóż konto.
2. **Billing** → doładuj saldo (np. 5 USD) i ustaw limit wydatków.
3. **API Keys** → *Create Key* → skopiuj klucz (`sk-ant-...`).

### 3. Token do GitHuba (bot publikuje przez niego stronę)
1. GitHub → zdjęcie profilowe → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. *Repository access:* **Only select repositories** → `Krajewskaleksandra`.
3. *Permissions → Repository permissions → Contents:* **Read and write**.
4. Ustaw ważność, np. 1 rok, i zapisz sobie w kalendarzu termin odnowienia.
5. Skopiuj token (`github_pat_...`).

### 4. Wdróż bota na Cloudflare
1. Załóż darmowe konto na https://dash.cloudflare.com.
2. Pobierz repozytorium na komputer (GitHub → *Code → Download ZIP*), rozpakuj i otwórz terminal w folderze `bot`.
3. Wpisz kolejno:

```bash
npm install
npx wrangler login                          # otworzy przeglądarkę – zaloguj się do Cloudflare
npx wrangler kv namespace create DRAFTS     # skopiuj zwrócone "id"
```

4. Otwórz `wrangler.jsonc` i w `kv_namespaces` wpisz to `id` (obecnie jest tam już id magazynu utworzonego dla tego gabinetu).
5. Ustaw sekrety. Każda komenda zapyta o wartość, którą wklejasz:

```bash
npx wrangler secret put TELEGRAM_BOT_TOKEN       # token z kroku 1
npx wrangler secret put ANTHROPIC_API_KEY        # klucz z kroku 2
npx wrangler secret put GITHUB_TOKEN             # token z kroku 3
npx wrangler secret put TELEGRAM_WEBHOOK_SECRET  # wymyśl długie hasło z liter i cyfr, np. 40 znaków
```

6. Wdróż bota:

```bash
npm run deploy
```

Na końcu zobaczysz adres bota, np. `https://gabinet-efekty-bot.twoja-nazwa.workers.dev`.

### 5. Połącz Telegram z botem
Wklej w przeglądarce (podmień 3 wartości) i naciśnij Enter:

```
https://api.telegram.org/bot<TOKEN_BOTA>/setWebhook?url=<ADRES_BOTA>&secret_token=<TELEGRAM_WEBHOOK_SECRET>&allowed_updates=["message","callback_query"]
```

Powinno się pokazać `"ok":true`.

### 6. Pozwól Oli publikować
1. Ola pisze do swojego bota w Telegramie cokolwiek, np. `/start`.
2. Bot odpowie, że jest prywatny, i poda **identyfikator czatu** (liczbę).
3. Wpisz go w `wrangler.jsonc` → `"ALLOWED_CHAT_IDS": "123456789"`. Kilka osób oddzielasz przecinkami.
4. Ponownie `npm run deploy`.
5. Ola pisze `/start`, a bot pokaże instrukcję. Gotowe! 🎉

## Codzienne używanie (dla Oli)
1. Zdjęcie z zabiegu → wyślij botowi **jako zdjęcie**, nie jako plik.
2. W podpisie albo w następnej wiadomości napisz (lub podyktuj mikrofonem na klawiaturze): *jaki zabieg, jaki był problem, jak poszło*.
3. Po ok. pół minuty dostaniesz szkic. **Publikuj**, **Popraw** (napisz, co zmienić) albo **Anuluj**.
4. Po publikacji bot przyśle link i gotowy post do wizytówki Google: wizytówka → *Dodaj aktualność* → wklej tekst + to samo zdjęcie.

⚠️ Publikuj wyłącznie zdjęcia, na które klientka wyraziła **pisemną zgodę** (RODO). Najbezpieczniej publikować zdjęcia bez rozpoznawalnej twarzy. Bot sam ostrzega, jeśli widzi twarz.

Usunięcie wpisu: na GitHubie usuń plik `efekty/<nazwa>.html` i jego wpis w `efekty/posts.json`. Możesz też poprosić Claude'a, żeby zrobił to za Ciebie.

## Google Search Console (darmowe statystyki z Google)
1. Wejdź na https://search.google.com/search-console → *Dodaj usługę* → **Prefiks URL** → `https://krajewskastudio.pl/`.
2. Metoda weryfikacji: **Tag HTML**. Skopiuj kod z `content="..."` i dodaj tag do `<head>` w `index.html` (albo poproś o to Claude'a).
3. Po weryfikacji: *Mapy witryn* → wpisz `sitemap.xml` → *Prześlij*. Bot aktualizuje tę mapę przy każdym wpisie.

Gdy pojawi się własna domena, dodaj w Search Console usługę typu **Domena** (weryfikacja rekordem DNS) i zmień `SITE_URL` w `wrangler.jsonc`.

## Publikowanie w wizytówce Google (opcjonalnie)

Gdy to skonfigurujesz, po każdej publikacji na stronie bot zapyta: **„📍 Opublikować ten wpis także w wizytówce Google?”**. Po kliknięciu „Tak” doda post (aktualność) ze zdjęciem i przyciskiem „Dowiedz się więcej” prowadzącym do wpisu. Bez tej konfiguracji bot przysyła gotowy tekst do ręcznego wklejenia.

### Etap 1: wniosek o dostęp do API (Google rozpatruje go od kilku dni do kilku tygodni)
1. Wejdź na https://console.cloud.google.com i zaloguj się **kontem Google, na którym jest wizytówka**.
2. U góry: lista projektów → **Nowy projekt** → nazwa np. `krajewskastudio-bot` → **Utwórz**.
3. Skopiuj **numer projektu** (*Project number*) ze strony głównej projektu (Dashboard / „Informacje o projekcie”).
4. Otwórz formularz wniosku o dostęp do Google Business Profile API. Link znajdziesz w dokumentacji Google Business Profile APIs, w części o rozpoczęciu pracy z API, pod hasłem *„Request access to the APIs”*. Wybierz w nim opcję **Application for Basic API Access** i wypełnij:
   - adres e-mail i numer projektu z punktu 3,
   - nazwa firmy: *Aleksandra Krajewska Studio*, strona: `https://krajewskastudio.pl`,
   - opis zastosowania, np.: *„Właścicielka gabinetu zarządza wyłącznie własną, zweryfikowaną wizytówką. Wewnętrzne narzędzie publikuje posty (aktualności) ze zdjęciami zabiegów z naszego gabinetu w Krakowie, po ręcznym zatwierdzeniu każdego posta przez właścicielkę.”*
5. Czekaj na maila od Google. Po akceptacji w projekcie pojawi się limit zapytań większy niż 0 (*APIs & Services → Quotas*).

### Etap 2: po akceptacji (ok. 20–30 minut)
1. **Włącz API.** W projekcie: *APIs & Services → Library*. Wyszukaj i włącz (**Enable**) trzy pozycje: **My Business Account Management API**, **My Business Business Information API** i **Google My Business API**.
2. **Ekran zgody OAuth.** *APIs & Services → OAuth consent screen* (lub *Google Auth Platform*):
   - typ użytkownika **External**, nazwa aplikacji np. `Bot Efekty`, Twój e-mail jako kontakt,
   - w **Audience / Test users** dodaj e-mail konta z wizytówką,
   - **Publishing status: In production** (kliknij *Publish app*). W trybie „Testing” Google co 7 dni unieważnia logowanie i bot przestałby publikować. Ostrzeżenie o niezweryfikowanej aplikacji jest normalne, bo korzystasz z niej tylko Ty.
3. **Dane logowania.** *APIs & Services → Credentials → Create credentials → OAuth client ID*:
   - typ **Web application**,
   - *Authorized redirect URIs*: dodaj `https://developers.google.com/oauthplayground`,
   - skopiuj **Client ID** i **Client secret**.
4. **Token odświeżania (refresh token).** Wejdź na https://developers.google.com/oauthplayground:
   - ⚙️ (prawy górny róg) → zaznacz **Use your own OAuth credentials** → wklej Client ID i Client secret,
   - w polu po lewej („Input your own scopes”) wpisz `https://www.googleapis.com/auth/business.manage` → **Authorize APIs**,
   - zaloguj się kontem z wizytówką i zezwól na dostęp (przy ostrzeżeniu wybierz *Zaawansowane → Przejdź do…*),
   - **Exchange authorization code for tokens** → skopiuj **Refresh token**.
5. **Zapisz sekrety w bocie** (w folderze `bot`):
   ```bash
   npx wrangler secret put GBP_CLIENT_ID
   npx wrangler secret put GBP_CLIENT_SECRET
   npx wrangler secret put GBP_REFRESH_TOKEN
   ```
6. **Odczytaj numery wizytówki.** Napisz do bota `/google`. Odpowie numerami `GBP_ACCOUNT_ID` i `GBP_LOCATION_ID`. Wpisz je w `wrangler.jsonc` (sekcja `vars`) i wpisz `npm run deploy`.
7. Gotowe. Po następnej publikacji bot zapyta o wysłanie posta do Google. Komenda `/google` potwierdzi też, czy wszystko jest włączone.

## Plany na później
- **Wiadomości głosowe.** Teraz trzeba dyktować mikrofonem na klawiaturze. Obsługa nagrań głosowych wymagałaby dodatkowej usługi zamiany mowy na tekst.

## Sprawdzanie i podgląd logów
```bash
npm run check   # sprawdzenie kodu (TypeScript)
npm run logs    # podgląd na żywo, co robi bot
```
