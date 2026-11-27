#!/usr/bin/env python3
"""Generator podstron zabiegów (SEO).

Teksty i ceny zmieniasz w liście PAGES poniżej, potem uruchamiasz z folderu głównego repozytorium:
    python3 narzedzia/podstrony.py
Skrypt nadpisze pliki <slug>.html w folderze głównym i plik sitemap-strony.xml.
"""
import html
import json
from pathlib import Path

SITE = "https://krajewskastudio.pl"
BOOKSY = "https://booksy.com/pl-pl/dl/show-business/313287"
PHONE = "+48533292100"
PHONE_TXT = "533 292 100"
ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    {
        "slug": "modelowanie-ust-krakow",
        "nav": "Modelowanie ust",
        "title": "Modelowanie ust Kraków – naturalny efekt | Aleksandra Krajewska Studio",
        "description": "Modelowanie i nawilżanie ust w Krakowie (ul. Michała Żaka 19). Naturalny kontur bez przerysowania. Ratowniczka medyczna i mgr kosmetologii CM UJ. Od 599 zł, bezpłatna konsultacja online.",
        "h1": "Modelowanie ust w Krakowie",
        "lead": "Subtelnie podkreślony kontur, lepsze nawilżenie i symetria – tak, żeby usta wyglądały jak Twoje, tylko w najlepszej wersji. Bez efektu „kaczki” i bez przerysowania.",
        "keywords": ["ust"],
        "sections": [
            ("Dla kogo jest modelowanie ust?", [
                ("ul", [
                    "masz wąskie lub asymetryczne usta i chcesz je delikatnie wyrównać,",
                    "kontur ust zatarł się z wiekiem albo jest mało wyraźny,",
                    "usta są często przesuszone i tracą objętość,",
                    "kąciki ust opadają i twarz wygląda na zmęczoną,",
                    "chcesz poprawić wcześniejszy zabieg, po którym usta wyglądają nienaturalnie.",
                ]),
            ]),
            ("Modelowanie czy nawilżanie ust?", [
                ("p", "<b>Modelowanie ust</b> wykonuję kwasem hialuronowym. Pozwala podkreślić kontur, poprawić symetrię, delikatnie dodać objętości i uwydatnić łuk Kupidyna. Ilość preparatu dobieram do Twojej anatomii – często mniej znaczy lepiej."),
                ("p", "<b>Nawilżanie ust stymulatorem tkankowym</b> to opcja dla osób, które nie chcą zmieniać kształtu ust, a jedynie poprawić ich kondycję: nawilżenie, miękkość i gładkość czerwieni wargowej."),
                ("p", "Nie wiesz, co wybrać? Zacznij od bezpłatnej konsultacji online – podpowiem, co ma sens w Twoim przypadku."),
            ]),
            ("Jak wygląda zabieg?", [
                ("ol", [
                    "<b>Konsultacja i wywiad</b> – rozmawiamy o oczekiwaniach, oceniam proporcje twarzy i wykluczam przeciwwskazania.",
                    "<b>Znieczulenie</b> – krem znieczulający, a większość preparatów zawiera dodatkowo środek znieczulający.",
                    "<b>Podanie preparatu</b> – precyzyjnie, w małych porcjach, z bieżącą kontrolą symetrii.",
                    "<b>Zalecenia</b> – dostajesz instrukcję postępowania po zabiegu i kontakt do mnie w razie pytań.",
                ]),
                ("p", "Cały zabieg trwa około godziny."),
            ]),
            ("Po zabiegu", [
                ("ul", [
                    "obrzęk jest normalny i zwykle utrzymuje się 2–3 dni, mogą pojawić się drobne siniaki,",
                    "przez 24–48 godzin unikaj sauny, intensywnego wysiłku, alkoholu i całowania,",
                    "nie masuj ust i nie maluj ich przez około dobę,",
                    "ostateczny efekt oceniamy po około 2 tygodniach.",
                ]),
            ]),
            ("Przeciwwskazania", [
                ("p", "Zabiegu nie wykonuję m.in. w ciąży i podczas karmienia piersią, przy aktywnej opryszczce lub stanie zapalnym w okolicy ust oraz w aktywnej fazie chorób autoimmunologicznych. Jeśli masz skłonność do opryszczki, przyjmujesz leki lub masz choroby przewlekłe – powiedz mi o tym przed zabiegiem. Każdy przypadek omawiamy na konsultacji."),
            ]),
        ],
        "prices": [
            ("Modelowanie ust", "899 zł", "60 min"),
            ("Nawilżanie ust stymulatorem tkankowym", "599 zł", "40 min"),
            ("Bezpłatna konsultacja online", "0 zł", "15 min"),
        ],
        "faq": [
            ("Czy będzie widać, że mam zrobione usta?", "Moim celem jest efekt, który wygląda naturalnie – usta mają być wypielęgnowane i harmonijne, a nie „zrobione”. Zaczynamy ostrożnie, a w razie potrzeby można delikatnie uzupełnić efekt na wizycie kontrolnej."),
            ("Jak długo utrzymuje się efekt?", "Zwykle od kilku miesięcy do około roku. Zależy to od organizmu, metabolizmu, stylu życia i ilości preparatu."),
            ("Czy modelowanie ust boli?", "Stosuję znieczulenie, dlatego większość osób odczuwa jedynie lekki dyskomfort, porównywany do szczypania."),
            ("Kiedy umówić się przed ważnym wydarzeniem?", "Najlepiej 2–3 tygodnie wcześniej, żeby obrzęk całkowicie zszedł, a efekt się ustabilizował."),
            ("Czy poprawiasz usta po zabiegach w innym gabinecie?", "Tak. Na konsultacji oceniam stan ust i proponuję plan – czasem wystarczy uzupełnienie, a czasem lepiej zacząć od korekty."),
        ],
    },
    {
        "slug": "dermapen-krakow",
        "nav": "Dermapen",
        "title": "Dermapen Kraków – mezoterapia mikroigłowa | Aleksandra Krajewska Studio",
        "description": "Dermapen w Krakowie: mezoterapia mikroigłowa z ampułką lub z peelingiem chemicznym. Pory, blizny potrądzikowe, przebarwienia, szara skóra. Od 599 zł. ul. Michała Żaka 19.",
        "h1": "Dermapen – mezoterapia mikroigłowa w Krakowie",
        "lead": "Zabieg, który pobudza skórę do naturalnej regeneracji: wyrównuje koloryt, zwęża pory, spłyca blizny i przywraca blask. Efekty widać już po pierwszym zabiegu, a najlepsze daje seria.",
        "keywords": ["dermapen", "mezoterap", "mikroig"],
        "sections": [
            ("Dla kogo jest Dermapen?", [
                ("ul", [
                    "rozszerzone pory i nierówna struktura skóry,",
                    "blizny potrądzikowe i przebarwienia,",
                    "szara, zmęczona skóra bez blasku,",
                    "drobne zmarszczki i utrata jędrności,",
                    "skóra twarzy, szyi i dekoltu.",
                ]),
            ]),
            ("Jak to działa?", [
                ("p", "Urządzenie wykonuje tysiące mikronakłuć o precyzyjnie dobranej głębokości. Skóra traktuje je jak sygnał do odbudowy i zaczyna intensywniej produkować kolagen i elastynę. Jednocześnie przez mikrokanaliki znacznie lepiej wnikają składniki aktywne z ampułki dobranej do potrzeb Twojej skóry."),
                ("p", "<b>Dermapen z peelingiem chemicznym</b> to mocniejsza wersja zabiegu – połączenie mikronakłuć z kwasem, szczególnie przy przebarwieniach, porach i bliznach potrądzikowych."),
            ]),
            ("Jak wygląda zabieg?", [
                ("ol", [
                    "wywiad i ocena skóry,",
                    "demakijaż, oczyszczenie i krem znieczulający,",
                    "mikronakłucia z aplikacją ampułki (lub kwasu),",
                    "maska kojąca i zalecenia pielęgnacyjne.",
                ]),
                ("p", "Zabieg trwa 30–45 minut."),
            ]),
            ("Po zabiegu", [
                ("ul", [
                    "skóra jest zaczerwieniona jak po opalaniu – zwykle przez 1–3 dni, potem może się delikatnie łuszczyć,",
                    "przez dobę nie nakładaj makijażu,",
                    "codziennie stosuj krem z filtrem SPF 50,",
                    "przez kilka dni unikaj sauny, basenu, solarium i kosmetyków z retinoidami lub kwasami.",
                ]),
            ]),
            ("Ile zabiegów i kiedy?", [
                ("p", "Najczęściej polecam serię 3–6 zabiegów co 4–6 tygodni. Wersję z peelingiem chemicznym najlepiej wykonywać w okresie mniejszego nasłonecznienia – jesienią i zimą."),
            ]),
            ("Przeciwwskazania", [
                ("p", "M.in. aktywny trądzik zapalny, opryszczka, infekcje i stany zapalne skóry, świeża opalenizna, ciąża i karmienie piersią, skłonność do bliznowców oraz kuracja izotretynoiną (w trakcie i przez kilka miesięcy po). Wszystko omawiamy na konsultacji."),
            ]),
        ],
        "prices": [
            ("Dermapen – mezoterapia mikroigłowa z ampułką", "699 zł", "45 min"),
            ("Dermapen + peeling chemiczny", "599 zł", "30 min"),
            ("Bezpłatna konsultacja online", "0 zł", "15 min"),
        ],
        "faq": [
            ("Czy Dermapen boli?", "Przed zabiegiem nakładam krem znieczulający, dlatego większość osób czuje jedynie mrowienie lub lekkie drapanie."),
            ("Kiedy widać efekty?", "Skóra jest promienna już kilka dni po zabiegu. Efekty związane z produkcją kolagenu – jędrność, spłycenie blizn – narastają przez kolejne tygodnie."),
            ("Ile zabiegów potrzebuję?", "To zależy od problemu skóry. Zwykle 3–6 zabiegów w odstępach 4–6 tygodni. Plan ustalamy na konsultacji."),
            ("Czy Dermapen można robić latem?", "Wersję z ampułką – tak, przy codziennym stosowaniu filtra SPF 50. Wersję z peelingiem chemicznym polecam w okresie mniejszego nasłonecznienia."),
        ],
    },
    {
        "slug": "stymulator-tkankowy-krakow",
        "nav": "Stymulator tkankowy",
        "title": "Stymulator tkankowy Kraków – biostymulacja skóry | Aleksandra Krajewska Studio",
        "description": "Stymulator tkankowy w Krakowie: biostymulacja poprawiająca napięcie, gęstość i jakość skóry bez zmiany rysów twarzy. 990 zł. Ratowniczka medyczna i mgr kosmetologii CM UJ.",
        "h1": "Stymulator tkankowy w Krakowie",
        "lead": "Biostymulacja to sposób na lepszą skórę bez zmiany rysów twarzy. Stymulator pobudza skórę do produkcji kolagenu i elastyny, dzięki czemu z tygodnia na tydzień staje się gęstsza, bardziej napięta i nawilżona.",
        "keywords": ["stymulator", "biostymul"],
        "sections": [
            ("Dla kogo jest stymulator tkankowy?", [
                ("ul", [
                    "skóra traci napięcie i jędrność, pojawia się wiotkość,",
                    "skóra jest cienka, odwodniona, z drobnymi zmarszczkami,",
                    "chcesz zadbać o profilaktykę – zwykle po 30. roku życia,",
                    "zależy Ci na poprawie szyi i dekoltu,",
                    "chcesz efektu „wypoczętej skóry”, a nie zmiany kształtu twarzy.",
                ]),
            ]),
            ("Czym różni się od wypełniacza?", [
                ("p", "Wypełniacz dodaje objętości w konkretnym miejscu, np. w ustach. Stymulator działa inaczej: nie wypełnia, tylko pobudza Twoją skórę do odbudowy. Efekt jest naturalny i narasta stopniowo – nikt nie zauważy „zabiegu”, zobaczy tylko lepszą skórę."),
                ("p", "Stymulator stosuję też w ustach – jako <a href=\"modelowanie-ust-krakow\">nawilżanie ust</a> bez zmiany ich kształtu."),
            ]),
            ("Jak wygląda zabieg?", [
                ("ol", [
                    "konsultacja, wywiad i ocena skóry,",
                    "dezynfekcja i znieczulenie,",
                    "podanie preparatu w wybrane okolice,",
                    "zalecenia po zabiegu.",
                ]),
                ("p", "Zabieg trwa około 40 minut."),
            ]),
            ("Po zabiegu", [
                ("ul", [
                    "w miejscach podania mogą być widoczne grudki lub lekki obrzęk – zwykle znikają w ciągu 1–2 dni,",
                    "możliwe są drobne siniaki,",
                    "przez 12–24 godziny nie nakładaj makijażu,",
                    "przez 48 godzin unikaj sauny, intensywnego wysiłku i alkoholu.",
                ]),
                ("p", "Efekt narasta przez 2–4 tygodnie. Często polecam serię 2–3 zabiegów – plan ustalamy indywidualnie."),
            ]),
            ("Przeciwwskazania", [
                ("p", "M.in. ciąża i karmienie piersią, aktywne infekcje i stany zapalne skóry, opryszczka, aktywna faza chorób autoimmunologicznych. O przyjmowanych lekach i chorobach przewlekłych porozmawiamy na konsultacji."),
            ]),
        ],
        "prices": [
            ("Stymulator tkankowy", "990 zł", "40 min"),
            ("Nawilżanie ust stymulatorem tkankowym", "599 zł", "40 min"),
            ("Bezpłatna konsultacja online", "0 zł", "15 min"),
        ],
        "faq": [
            ("Kiedy zobaczę efekt?", "Pierwszą poprawę nawilżenia widać po kilku dniach, a pełny efekt – po 2–4 tygodniach, gdy skóra wyprodukuje nowy kolagen."),
            ("Ile zabiegów potrzebuję?", "Zwykle 2–3 zabiegi w odstępach kilku tygodni, a później zabieg podtrzymujący. Dokładny plan zależy od stanu skóry."),
            ("Od jakiego wieku warto?", "Najczęściej po 30. roku życia, gdy skóra zaczyna wolniej się regenerować. Ale ważniejszy od wieku jest stan skóry – ocenimy go na konsultacji."),
            ("Czy zmieni się wygląd mojej twarzy?", "Nie. Stymulator nie zmienia rysów ani proporcji – poprawia jakość skóry, dzięki czemu wyglądasz świeżej."),
        ],
    },
    {
        "slug": "wampirzy-lifting-krakow",
        "nav": "Wampirzy lifting",
        "title": "Wampirzy lifting Kraków – osocze i fibryna | Aleksandra Krajewska Studio",
        "description": "Wampirzy lifting w Krakowie: osocze bogatopłytkowe, fibryna (m.in. cienie pod oczami) i Plasma Complex. Naturalna regeneracja z Twojej krwi. Od 749 zł. Pobranie krwi wykonuje ratowniczka medyczna.",
        "h1": "Wampirzy lifting w Krakowie – osocze i fibryna",
        "lead": "Zabiegi autologiczne wykorzystują to, co najlepsze w Twojej własnej krwi – czynniki wzrostu, które pobudzają skórę do regeneracji. Bez obcych substancji, za to z widoczną poprawą jakości, napięcia i kolorytu skóry.",
        "keywords": ["osocze", "fibryn", "plasma", "autolog", "wampir"],
        "sections": [
            ("Dla kogo jest wampirzy lifting?", [
                ("ul", [
                    "zmęczona, szara skóra bez blasku,",
                    "cienie i cienka skóra pod oczami (szczególnie fibryna),",
                    "drobne zmarszczki i utrata jędrności,",
                    "skóra po trądziku, z bliznami i przebarwieniami,",
                    "osoby, które wolą naturalne metody bez obcych substancji.",
                ]),
            ]),
            ("Osocze, fibryna czy Plasma Complex?", [
                ("p", "<b>Osocze bogatopłytkowe</b> – płynne, świetnie sprawdza się przy ogólnej rewitalizacji twarzy, szyi i dekoltu."),
                ("p", "<b>Fibryna bogatopłytkowa</b> – gęstsza, dłużej uwalnia czynniki wzrostu. Często wybierana przy cieniach i zmęczonej skórze pod oczami."),
                ("p", "<b>Plasma Complex</b> – połączenie osocza i fibryny w jednym zabiegu, czyli najbardziej kompleksowa odbudowa skóry."),
            ]),
            ("Jak wygląda zabieg?", [
                ("ol", [
                    "<b>Pobranie krwi</b> – jak przy zwykłych badaniach. Jako ratowniczka medyczna robię to na co dzień, sprawnie i bezpiecznie.",
                    "<b>Wirowanie</b> – w wirówce oddzielam osocze lub fibrynę bogate w płytki krwi.",
                    "<b>Podanie</b> – igłą lub kaniulą w wybrane okolice, po wcześniejszym znieczuleniu kremem.",
                ]),
                ("p", "Cały zabieg trwa około 40 minut."),
            ]),
            ("Jak się przygotować?", [
                ("ul", [
                    "dobrze się nawodnij dzień wcześniej i w dniu zabiegu,",
                    "zjedz lekki posiłek przed wizytą,",
                    "dzień wcześniej unikaj alkoholu,",
                    "o przyjmowanych lekach (zwłaszcza przeciwzapalnych i przeciwkrzepliwych) powiedz mi wcześniej.",
                ]),
            ]),
            ("Po zabiegu", [
                ("ul", [
                    "możliwe zaczerwienienie, grudki i drobne siniaki – zwłaszcza pod oczami, zwykle przez 1–3 dni,",
                    "przez 12–24 godziny nie nakładaj makijażu,",
                    "przez 48 godzin unikaj sauny, intensywnego wysiłku i alkoholu.",
                ]),
                ("p", "Efekty narastają przez kolejne tygodnie. Najlepsze rezultaty daje zwykle seria 3 zabiegów co 4–6 tygodni."),
            ]),
            ("Przeciwwskazania", [
                ("p", "M.in. zaburzenia krzepnięcia i leki przeciwkrzepliwe, niska liczba płytek krwi, anemia, aktywne infekcje, choroby nowotworowe, ciąża i karmienie piersią. Wszystko omawiamy przed zabiegiem."),
            ]),
        ],
        "prices": [
            ("Osocze bogatopłytkowe", "749 zł", "40 min"),
            ("Fibryna bogatopłytkowa", "749 zł", "40 min"),
            ("Plasma Complex – fibryna + osocze", "899 zł", "40 min"),
            ("Bezpłatna konsultacja online", "0 zł", "15 min"),
        ],
        "faq": [
            ("Czy wampirzy lifting jest bezpieczny?", "Wykorzystuję wyłącznie Twoją własną krew, więc ryzyko uczulenia jest minimalne. Pobranie i przygotowanie odbywa się w sterylnych warunkach, przez osobę z wykształceniem medycznym."),
            ("Czy pobranie krwi boli?", "Tyle co przy zwykłych badaniach krwi – krótkie ukłucie."),
            ("Kiedy widać efekty?", "Skóra wygląda świeżej już po kilku dniach, a efekty regeneracji narastają przez kolejne tygodnie."),
            ("Osocze czy fibryna – co wybrać?", "Przy cieniach pod oczami częściej polecam fibrynę, przy ogólnej rewitalizacji – osocze, a dla najpełniejszego efektu – Plasma Complex. Najlepszą opcję dobierzemy na konsultacji."),
        ],
    },
]

E = html.escape


def render_block(kind, content):
    if kind == "p":
        return f"<p>{content}</p>"
    tag = "ol" if kind == "ol" else "ul"
    return f"<{tag}>" + "".join(f"<li>{li}</li>" for li in content) + f"</{tag}>"


CSS = """
:root{--bg:#fbf7f4;--bg-alt:#f3ebe5;--card:#fff;--ink:#2b1f24;--muted:#6f6166;--accent:#7a3b52;--accent-soft:#efdfe4;--gold:#b48a5a;--line:#e6dad3;--radius:18px;--shadow:0 10px 30px rgba(60,30,40,.08)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.7 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}a{color:var(--accent)}
h1,h2,h3{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;line-height:1.15;margin:0 0 .5em}
h1{font-size:clamp(2.1rem,5vw,3.2rem)}h2{font-size:1.8rem;margin-top:1.8em}
.wrap{max-width:820px;margin:0 auto;padding:0 20px}.wide{max-width:1120px}
.nav{position:sticky;top:0;z-index:20;background:rgba(251,247,244,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;height:62px;max-width:1120px}
.logo{font-family:"Cormorant Garamond",serif;font-size:1.35rem;font-weight:600;text-decoration:none;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:13px 24px;border-radius:999px;font-weight:600;text-decoration:none;border:1.5px solid var(--accent);font-size:1rem}
.btn-primary{background:var(--accent);color:#fff}.btn-ghost{color:var(--accent)}
.nav .btn{padding:9px 16px;font-size:.9rem;white-space:nowrap;flex-shrink:0}
.btns{display:flex;flex-wrap:wrap;gap:12px;margin:22px 0}
.crumbs{font-size:.85rem;color:var(--muted);margin:34px 0 14px}.crumbs a{color:var(--muted)}
.eyebrow{text-transform:uppercase;letter-spacing:.16em;font-size:.75rem;font-weight:600;color:var(--gold);display:block;margin-bottom:10px}
.lead{font-size:1.2rem;color:var(--ink)}
article p,article li{color:#3d3036}article li{margin-bottom:6px}
.prices{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden;margin:16px 0}
.prices div{display:grid;grid-template-columns:1fr auto auto;gap:16px;padding:16px 22px;border-bottom:1px solid var(--line);align-items:baseline}
.prices div:last-child{border-bottom:0}.prices b{color:var(--accent);white-space:nowrap}.prices span{color:var(--muted);font-size:.88rem;white-space:nowrap}
details{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin-bottom:10px}
summary{cursor:pointer;font-weight:600;list-style:none;display:flex;justify-content:space-between;gap:12px}
summary::-webkit-details-marker{display:none}summary::after{content:"+";color:var(--accent);font-size:1.3rem;line-height:1}
details[open] summary::after{content:"–"}details p{margin:10px 0 0;color:var(--muted)}
.cta{background:var(--bg-alt);border:1px solid var(--line);border-radius:var(--radius);padding:28px;margin:44px 0}
.cta h2{margin-top:0}
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));margin-top:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);text-decoration:none;color:inherit;display:flex;flex-direction:column}
.card img{aspect-ratio:4/3;object-fit:cover;width:100%}.card div{padding:16px 18px}
.card h3{font-size:1.2rem;margin:0}
.others{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 60px;padding:0;list-style:none}
.others a{display:inline-block;background:var(--accent-soft);color:var(--accent);border-radius:999px;padding:8px 16px;font-weight:600;text-decoration:none;font-size:.92rem}
.note{font-size:.85rem;color:var(--muted)}
footer{padding:30px 0 50px;color:var(--muted);font-size:.85rem;border-top:1px solid var(--line)}
"""


def render(page):
    url = f"{SITE}/{page['slug']}"
    sections = "\n".join(
        f"<h2>{E(h)}</h2>\n" + "\n".join(render_block(k, c) for k, c in blocks)
        for h, blocks in page["sections"]
    )
    prices = "".join(f"<div>{E(n)}<b>{E(p)}</b><span>{E(d)}</span></div>" for n, p, d in page["prices"])
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in page["faq"])
    others = "".join(
        f'<li><a href="{o["slug"]}">{E(o["nav"])}</a></li>' for o in PAGES if o["slug"] != page["slug"]
    )
    ld = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": page["h1"],
            "description": page["description"],
            "url": url,
            "areaServed": "Kraków",
            "provider": {
                "@type": "MedicalBusiness",
                "name": "Aleksandra Krajewska Studio",
                "telephone": "+48 533 292 100",
                "url": SITE + "/",
                "address": {"@type": "PostalAddress", "streetAddress": "ul. Michała Żaka 19/3U", "postalCode": "30-612", "addressLocality": "Kraków", "addressCountry": "PL"},
            },
            "offers": [
                {"@type": "Offer", "name": n, "price": p.replace(" zł", ""), "priceCurrency": "PLN"} for n, p, _ in page["prices"]
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faq"]
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": page["nav"], "item": url},
            ],
        },
    ]
    ld_json = json.dumps(ld, ensure_ascii=False).replace("<", "\\u003c")
    keywords = json.dumps(page["keywords"])
    return f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(page['title'])}</title>
<meta name="description" content="{E(page['description'])}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{E(page['title'])}">
<meta property="og:description" content="{E(page['description'])}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:image" content="{SITE}/img/gabinet.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<script type="application/ld+json">{ld_json}</script>
<style>{CSS}</style>
</head>
<body>
<nav class="nav"><div class="wrap"><a class="logo" href="./">Aleksandra Krajewska Studio</a><a class="btn btn-primary" href="{BOOKSY}" target="_blank" rel="noopener">Umów wizytę</a></div></nav>
<main class="wrap">
  <div class="crumbs"><a href="./">Strona główna</a> / <a href="./#zabiegi">Zabiegi</a> / {E(page['nav'])}</div>
  <span class="eyebrow">Zabiegi · Kraków, ul. Michała Żaka 19</span>
  <h1>{E(page['h1'])}</h1>
  <p class="lead">{E(page['lead'])}</p>
  <div class="btns"><a class="btn btn-primary" href="{BOOKSY}" target="_blank" rel="noopener">Sprawdź wolne terminy</a><a class="btn btn-ghost" href="tel:{PHONE}">Zadzwoń: {PHONE_TXT}</a></div>
  <article>
{sections}
    <h2>Cennik</h2>
    <div class="prices">{prices}</div>
    <p class="note">Dokładny plan i koszt ustalamy na konsultacji.</p>
    <section id="efekty-zabiegu" hidden>
      <h2>Efekty z mojego gabinetu</h2>
      <div class="grid" id="efektyGrid"></div>
      <p><a href="efekty/">Zobacz wszystkie efekty →</a></p>
    </section>
    <h2>Najczęstsze pytania</h2>
    {faq}
  </article>
  <div class="cta">
    <h2>Umów się na konsultację</h2>
    <p>Jestem ratowniczką medyczną i magistrem kosmetologii (Collegium Medicum UJ). Każdy zabieg poprzedzam wywiadem i analizą skóry – nie pracuję schematami. Nie wiesz, od czego zacząć? Umów <b>bezpłatną konsultację online</b> (15 min).</p>
    <div class="btns"><a class="btn btn-primary" href="{BOOKSY}" target="_blank" rel="noopener">Umów się w Booksy</a><a class="btn btn-ghost" href="tel:{PHONE}">Zadzwoń: {PHONE_TXT}</a></div>
    <p class="note">Gabinet: ul. Michała Żaka 19/3U, 30-612 Kraków · bezpłatny parking przed lokalem.</p>
  </div>
  <h2>Inne zabiegi</h2>
  <ul class="others">{others}</ul>
  <p class="note">Informacje na tej stronie mają charakter ogólny i nie zastępują konsultacji. Ostateczna kwalifikacja do zabiegu następuje po wywiadzie.</p>
</main>
<footer><div class="wrap wide">© Aleksandra Krajewska Studio · ul. Michała Żaka 19/3U, 30-612 Kraków · <a href="tel:{PHONE}">{PHONE_TXT}</a> · <a href="https://www.instagram.com/olakrajevska/" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.facebook.com/aleksandrakrajewskastudio/" target="_blank" rel="noopener">Facebook</a></div></footer>
<script>
(async () => {{
  try {{
    const keys = {keywords};
    const res = await fetch("efekty/posts.json", {{ cache: "no-cache" }});
    if (!res.ok) return;
    const all = await res.json();
    const hit = p => keys.some(k => (p.treatment + " " + p.title).toLowerCase().includes(k));
    const posts = all.filter(hit).slice(0, 3);
    if (!posts.length) return;
    const esc = s => String(s).replace(/[&<>"']/g, c => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }}[c]));
    document.getElementById("efektyGrid").innerHTML = posts.map(p =>
      `<a class="card" href="efekty/${{esc(p.slug)}}"><img src="${{esc(p.image)}}" alt="${{esc(p.image_alt)}}" loading="lazy"><div><h3>${{esc(p.title)}}</h3></div></a>`).join("");
    document.getElementById("efekty-zabiegu").hidden = false;
  }} catch (e) {{}}
}})();
</script>
</body>
</html>
"""


def main():
    for page in PAGES:
        (ROOT / f"{page['slug']}.html").write_text(render(page), encoding="utf-8")
        print("zapisano", page["slug"] + ".html")
    urls = "\n".join(f"<url><loc>{SITE}/{p['slug']}</loc></url>" for p in PAGES)
    (ROOT / "sitemap-strony.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8",
    )
    print("zapisano sitemap-strony.xml")


if __name__ == "__main__":
    main()
