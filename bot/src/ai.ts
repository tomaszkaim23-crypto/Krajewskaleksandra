import Anthropic from "@anthropic-ai/sdk";
import { betaZodOutputFormat } from "@anthropic-ai/sdk/helpers/beta/zod";
import { z } from "zod";

export const PostSchema = z.object({
  title: z.string().describe("Tytuł podstrony, maks. ok. 70 znaków, z frazą, którą ktoś wpisałby w Google (np. nazwa zabiegu + Kraków)."),
  slug: z.string().describe("Krótki adres URL: małe litery, bez polskich znaków, słowa oddzielone myślnikami, maks. 60 znaków."),
  meta_description: z.string().describe("Opis do wyników Google, maks. ok. 155 znaków."),
  treatment: z.string().describe("Nazwa zabiegu z cennika gabinetu, którego dotyczy wpis, albo 'inny'."),
  lead: z.string().describe("Wstęp: 1–2 zdania zachęcające do przeczytania."),
  sections: z
    .array(z.object({ heading: z.string(), paragraphs: z.array(z.string()) }))
    .describe("2–4 sekcje z nagłówkami, łącznie ok. 250–450 słów."),
  image_alt: z.string().describe("Opis zdjęcia dla osób niewidomych i dla Google (alt), bez danych osobowych."),
  gbp_post: z.string().describe("Gotowy post do wizytówki Google: 600–1200 znaków, zakończony zaproszeniem do zapisu przez Booksy lub telefon 533 292 100."),
  warnings: z.array(z.string()).describe("Uwagi dla Oli przed publikacją, np. widoczna twarz (wymagana pisemna zgoda klientki), brakujące informacje, zbyt ogólny opis. Pusta lista, jeśli wszystko w porządku."),
});
export type Post = z.infer<typeof PostSchema>;

const SYSTEM = `Piszesz wpisy do sekcji „Efekty” na stronie gabinetu Aleksandra Krajewska Studio (medycyna estetyczna i kosmetologia, ul. Michała Żaka 19/3U, 30-612 Kraków, parking przed lokalem).

Właścicielka: Aleksandra (Ola) Krajewska – ratowniczka medyczna i magister kosmetologii, absolwentka Collegium Medicum UJ. Styl gabinetu: naturalne, harmonijne efekty bez przerysowania, bezpieczeństwo, indywidualny plan zabiegów.

Cennik (nazwy zabiegów do pola treatment):
- Bezpłatna konsultacja online – 0 zł
- Konsultacja z Beauty Planem – 250 zł
- Modelowanie ust – 899 zł
- Nawilżanie ust stymulatorem tkankowym – 599 zł
- Dermapen – mezoterapia mikroigłowa z ampułką – 699 zł
- Dermapen + peeling chemiczny – 599 zł
- Stymulator tkankowy – 990 zł
- Osocze bogatopłytkowe (wampirzy lifting) – 749 zł
- Fibryna bogatopłytkowa – 749 zł
- Plasma Complex – fibryna + osocze – 899 zł

Dostajesz zdjęcie z gabinetu i krótki opis od Oli (często podyktowany głosem, z literówkami). Na tej podstawie napisz wpis.

Zasady:
- Pisz po polsku, w pierwszej osobie, głosem Oli: ciepło, rzeczowo, bez lania wody.
- Używaj naturalnie słów, które ludzie wpisują w Google (nazwa zabiegu, problem skóry, „Kraków”), ale bez upychania fraz.
- Opieraj się tylko na tym, co jest w opisie i na zdjęciu. Nie wymyślaj faktów o klientce, liczby zabiegów ani czasu trwania efektu, jeśli Ola ich nie podała.
- Nie podawaj imion, nazwisk ani innych danych klientek.
- Prawo: nie wymieniaj nazw handlowych leków ani preparatów (np. toksyny botulinowej, wypełniaczy, stymulatorów) ani słowa „botoks” – opisuj zabieg ogólnie. Nie obiecuj gwarantowanych efektów, nie używaj słów typu „najlepszy”, „100% skuteczności”, nie porównuj z innymi gabinetami.
- Wpis ma informować i edukować (na czym polegał zabieg, dla kogo, jak wygląda gojenie), a nie nachalnie reklamować.
- Jeśli na zdjęciu widać rozpoznawalną twarz, dodaj ostrzeżenie o konieczności pisemnej zgody klientki.`;

export async function generatePost(
  apiKey: string,
  imageB64: string,
  description: string,
  previous?: { post: Post; feedback: string },
): Promise<Post> {
  const client = new Anthropic({ apiKey });

  let text = `Opis od Oli:\n${description || "(brak opisu – opieraj się na zdjęciu i dodaj ostrzeżenie, że opis jest zbyt ogólny)"}`;
  if (previous) {
    text += `\n\nPoprzednia wersja wpisu (JSON):\n${JSON.stringify(previous.post)}\n\nPoprawki od Oli – wprowadź je, resztę zostaw bez zmian, jeśli nie wymaga poprawy:\n${previous.feedback}`;
  }

  const response = await client.beta.messages.parse({
    model: "claude-opus-5-5",
    max_tokens: 16000,
    betas: ["server-side-fallback-2026-07-01"],
    fallbacks: "default",
    output_config: { effort: "low", format: betaZodOutputFormat(PostSchema) },
    system: SYSTEM,
    messages: [
      {
        role: "user",
        content: [
          { type: "image", source: { type: "base64", media_type: "image/jpeg", data: imageB64 } },
          { type: "text", text },
        ],
      },
    ],
  });

  if (response.stop_reason === "refusal") {
    throw new Error("Model odmówił napisania wpisu dla tego zdjęcia/opisu.");
  }
  if (response.stop_reason === "max_tokens" || !response.parsed_output) {
    throw new Error("Nie udało się wygenerować kompletnego wpisu.");
  }
  return response.parsed_output;
}
