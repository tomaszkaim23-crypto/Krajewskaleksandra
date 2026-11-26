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

4. Otwórz `wrangler.toml` i w miejsce `WKLEJ_TUTAJ_ID_Z_KOMENDY` wklej to `id`.
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
3. Wpisz go w `wrangler.toml` → `ALLOWED_CHAT_IDS = "123456789"`. Kilka osób oddzielasz przecinkami.
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
1. Wejdź na https://search.google.com/search-console → *Dodaj usługę* → **Prefiks URL** → `https://tomaszkaim23-crypto.github.io/Krajewskaleksandra/`.
2. Metoda weryfikacji: **Tag HTML**. Skopiuj kod z `content="..."` i dodaj tag do `<head>` w `index.html` (albo poproś o to Claude'a).
3. Po weryfikacji: *Mapy witryn* → wpisz `sitemap.xml` → *Prześlij*. Bot aktualizuje tę mapę przy każdym wpisie.

Gdy pojawi się własna domena, dodaj w Search Console usługę typu **Domena** (weryfikacja rekordem DNS) i zmień `SITE_URL` w `wrangler.toml`.

## Plany na później
- **Automatyczne posty w wizytówce Google.** Wymaga zgłoszenia i akceptacji dostępu do Google Business Profile API przez Google. Do tego czasu bot przygotowuje gotowy tekst do wklejenia.
- **Wiadomości głosowe.** Teraz trzeba dyktować mikrofonem na klawiaturze. Obsługa nagrań głosowych wymagałaby dodatkowej usługi zamiany mowy na tekst.

## Sprawdzanie i podgląd logów
```bash
npm run check   # sprawdzenie kodu (TypeScript)
npm run logs    # podgląd na żywo, co robi bot
```
