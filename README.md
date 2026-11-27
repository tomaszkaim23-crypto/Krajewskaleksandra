# Strona Aleksandra Krajewska Studio

## Pliki
- `index.html`: strona gabinetu (zdjęcia są wbudowane w plik)
- `karta-opinii.html`: karty z kodem QR do opinii Google (do druku)
- `img/`: zdjęcia (oryginały, używane m.in. jako podgląd przy udostępnianiu linku)
- `js/qrcode.js`: biblioteka do kodów QR (licencja MIT, nie ruszać)

## Publikacja (Cloudflare)
Strona działa na Cloudflare jako Worker ze stroną statyczną (projekt `krajewskastudio`) połączony z tym repozytorium. Każda zmiana na gałęzi `main` (także wpis opublikowany przez bota) automatycznie aktualizuje stronę po około minucie.

- Strona: https://krajewskastudio.pl/
- Karty z QR: https://krajewskastudio.pl/karta-opinii

Konfiguracja: `wrangler.jsonc`. Lista plików, które nie trafiają na stronę (kod bota, README): `.assetsignore`.

## Własna domena (później)
Kup domenę (np. `krajewskastudio.pl`) u polskiego rejestratora (OVH, nazwa.pl, home.pl). Potem w Cloudflare: **Workers & Pages → krajewskastudio → Settings → Domains & Routes → Add → Custom domain**. Po podłączeniu domeny zmień adres w `bot/wrangler.toml` (`SITE_URL`), `sitemap.xml` i `robots.txt`.

## Bot „Efekty” na Telegramie
Folder `bot/` zawiera bota, przez którego Ola publikuje wpisy w sekcji **Efekty** prosto z telefonu (zdjęcie + krótki opis → tekst pisany przez AI → zatwierdzenie → publikacja). Instrukcja uruchomienia: [`bot/README.md`](bot/README.md).
