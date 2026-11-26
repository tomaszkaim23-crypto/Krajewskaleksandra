import Anthropic from "@anthropic-ai/sdk";
import { generatePost, type Post } from "./ai";
import { commitFiles, readTextFile, type GitHubConfig } from "./github";
import { esc, renderListPage, renderPostPage, renderSitemap, slugify, type PostEntry } from "./render";

export interface Env {
  DRAFTS: KVNamespace;
  TELEGRAM_BOT_TOKEN: string;
  TELEGRAM_WEBHOOK_SECRET: string;
  ANTHROPIC_API_KEY: string;
  GITHUB_TOKEN: string;
  ALLOWED_CHAT_IDS: string; // np. "123456789,987654321"
  GITHUB_REPO: string;
  GITHUB_BRANCH: string;
  SITE_URL: string; // bez końcowego "/"
}

interface Draft {
  fileId: string;
  description: string;
  post?: Post;
  awaiting?: "description" | "feedback";
}

// ---------- Telegram ----------

async function tg(env: Env, method: string, payload: object): Promise<any> {
  const res = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}

const send = (env: Env, chatId: number, text: string, extra: object = {}) =>
  tg(env, "sendMessage", { chat_id: chatId, text, parse_mode: "HTML", disable_web_page_preview: true, ...extra });

function bytesToB64(bytes: Uint8Array): string {
  let s = "";
  for (let i = 0; i < bytes.length; i += 0x8000) {
    s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  }
  return btoa(s);
}

async function downloadPhotoB64(env: Env, fileId: string): Promise<string> {
  const info = await tg(env, "getFile", { file_id: fileId });
  if (!info.ok) throw new Error("Nie udało się pobrać zdjęcia z Telegrama.");
  const res = await fetch(`https://api.telegram.org/file/bot${env.TELEGRAM_BOT_TOKEN}/${info.result.file_path}`);
  return bytesToB64(new Uint8Array(await res.arrayBuffer()));
}

const draftKey = (chatId: number) => `draft:${chatId}`;
const getDraft = async (env: Env, chatId: number) => (await env.DRAFTS.get<Draft>(draftKey(chatId), "json")) ?? null;
const saveDraft = (env: Env, chatId: number, d: Draft) =>
  env.DRAFTS.put(draftKey(chatId), JSON.stringify(d), { expirationTtl: 60 * 60 * 24 * 3 });

const HELP = `👋 Cześć! Jestem botem do sekcji <b>Efekty</b> na stronie gabinetu.

<b>Jak dodać wpis:</b>
1. Wyślij mi <b>zdjęcie</b> z zabiegu.
2. W podpisie (albo w następnej wiadomości) napisz krótko: jaki zabieg, jaki był problem, jak poszło. Możesz podyktować – kliknij mikrofon na klawiaturze telefonu.
3. Przygotuję tekst, a Ty zdecydujesz: <b>Publikuj</b>, <b>Popraw</b> albo <b>Anuluj</b>.

⚠️ Publikuj tylko zdjęcia, na które klientka dała <b>pisemną zgodę</b>. Najbezpieczniej zdjęcia bez widocznej twarzy.`;

const KEYBOARD = {
  reply_markup: {
    inline_keyboard: [[
      { text: "✅ Publikuj", callback_data: "pub" },
      { text: "✏️ Popraw", callback_data: "edit" },
      { text: "❌ Anuluj", callback_data: "cancel" },
    ]],
  },
};

function preview(post: Post): string {
  let body = post.sections.map((s) => `<b>${esc(s.heading)}</b>\n${s.paragraphs.map(esc).join("\n\n")}`).join("\n\n");
  if (body.length > 2600) body = body.slice(0, 2600) + "…";
  const warn = post.warnings.length ? `\n\n⚠️ <b>Uwagi:</b>\n${post.warnings.map((w) => "• " + esc(w)).join("\n")}` : "";
  return `📝 <b>${esc(post.title)}</b>\n<i>${esc(post.treatment)}</i>\n\n${esc(post.lead)}\n\n${body}${warn}`;
}

async function generateAndPreview(env: Env, chatId: number, draft: Draft, feedback?: string) {
  await send(env, chatId, feedback ? "✏️ Poprawiam tekst…" : "✍️ Piszę opis, to potrwa ok. pół minuty…");
  await tg(env, "sendChatAction", { chat_id: chatId, action: "typing" });
  try {
    const img = await downloadPhotoB64(env, draft.fileId);
    const post = await generatePost(
      env.ANTHROPIC_API_KEY,
      img,
      draft.description,
      feedback && draft.post ? { post: draft.post, feedback } : undefined,
    );
    draft.post = post;
    draft.awaiting = undefined;
    await saveDraft(env, chatId, draft);
    await send(env, chatId, preview(post), KEYBOARD);
  } catch (e) {
    const msg =
      e instanceof Anthropic.RateLimitError ? "Za dużo zapytań naraz – spróbuj za minutę."
      : e instanceof Anthropic.AuthenticationError ? "Nieprawidłowy klucz API Anthropic – sprawdź konfigurację bota."
      : e instanceof Anthropic.APIError ? `Błąd API (${e.status}). Spróbuj ponownie za chwilę.`
      : e instanceof Error ? e.message : String(e);
    await send(env, chatId, `😕 Nie udało się przygotować tekstu: ${esc(msg)}`);
  }
}

// ---------- Publikacja ----------

async function publish(env: Env, chatId: number, draft: Draft) {
  if (!draft.post) return;
  const post = draft.post;
  await send(env, chatId, "🚀 Publikuję na stronie…");

  const cfg: GitHubConfig = { token: env.GITHUB_TOKEN, repo: env.GITHUB_REPO, branch: env.GITHUB_BRANCH };
  const raw = await readTextFile(cfg, "efekty/posts.json");
  const entries: PostEntry[] = raw ? JSON.parse(raw) : [];

  const date = new Date().toISOString().slice(0, 10);
  let slug = slugify(post.slug || post.title);
  if (entries.some((e) => e.slug === slug)) slug = `${slug}-${date}`;
  while (entries.some((e) => e.slug === slug)) slug = `${slug}-2`;

  const entry: PostEntry = {
    slug,
    title: post.title,
    lead: post.lead,
    treatment: post.treatment,
    date,
    image: `efekty/img/${slug}.jpg`,
    image_alt: post.image_alt,
  };
  const all = [entry, ...entries];
  const site = env.SITE_URL.replace(/\/+$/, "");
  const img = await downloadPhotoB64(env, draft.fileId);

  await commitFiles(cfg, `Efekty: ${post.title}`, [
    { path: entry.image, content: img, encoding: "base64" },
    { path: `efekty/${slug}.html`, content: renderPostPage(post, entry, site), encoding: "utf-8" },
    { path: "efekty/index.html", content: renderListPage(all, site), encoding: "utf-8" },
    { path: "efekty/posts.json", content: JSON.stringify(all, null, 2) + "\n", encoding: "utf-8" },
    { path: "sitemap.xml", content: renderSitemap(all, site), encoding: "utf-8" },
  ]);

  await env.DRAFTS.delete(draftKey(chatId));
  const url = `${site}/efekty/${slug}.html`;
  await send(env, chatId, `✅ Gotowe! Wpis pojawi się na stronie za ok. 1–2 minuty:\n${url}\n\n👇 Poniżej gotowy post do <b>wizytówki Google</b>. Skopiuj go, wejdź w wizytówkę → „Dodaj aktualność”, wklej tekst, dodaj to samo zdjęcie i przycisk „Dowiedz się więcej” z linkiem powyżej.`);
  await tg(env, "sendMessage", { chat_id: chatId, text: post.gbp_post });
}

// ---------- Obsługa aktualizacji z Telegrama ----------

async function handleUpdate(env: Env, update: any) {
  const allowed = env.ALLOWED_CHAT_IDS.split(",").map((s) => s.trim()).filter(Boolean);

  if (update.callback_query) {
    const cq = update.callback_query;
    const chatId: number = cq.message.chat.id;
    await tg(env, "answerCallbackQuery", { callback_query_id: cq.id });
    if (!allowed.includes(String(chatId))) return;
    await tg(env, "editMessageReplyMarkup", { chat_id: chatId, message_id: cq.message.message_id, reply_markup: { inline_keyboard: [] } });
    const draft = await getDraft(env, chatId);
    if (!draft?.post) return send(env, chatId, "Nie mam szkicu do tej akcji. Wyślij nowe zdjęcie.");
    if (cq.data === "pub") {
      try { await publish(env, chatId, draft); }
      catch (e) { await send(env, chatId, `😕 Publikacja się nie udała: ${esc(String(e)).slice(0, 500)}`); }
    } else if (cq.data === "edit") {
      draft.awaiting = "feedback";
      await saveDraft(env, chatId, draft);
      await send(env, chatId, "Napisz (albo podyktuj), co zmienić – np. „krócej”, „dodaj, że efekt widać po 2 tygodniach”, „inny tytuł”.");
    } else if (cq.data === "cancel") {
      await env.DRAFTS.delete(draftKey(chatId));
      await send(env, chatId, "Anulowane. Możesz wysłać nowe zdjęcie.");
    }
    return;
  }

  const msg = update.message;
  if (!msg) return;
  const chatId: number = msg.chat.id;

  if (!allowed.includes(String(chatId))) {
    await send(env, chatId, `Ten bot jest prywatny.\nTwój identyfikator czatu: <code>${chatId}</code>\n(Jeśli to Ty prowadzisz gabinet, dopisz go w ustawieniu ALLOWED_CHAT_IDS.)`);
    return;
  }

  if (msg.text?.startsWith("/start") || msg.text?.startsWith("/pomoc")) return send(env, chatId, HELP);
  if (msg.text?.startsWith("/anuluj")) {
    await env.DRAFTS.delete(draftKey(chatId));
    return send(env, chatId, "Anulowane.");
  }

  if (msg.photo?.length) {
    const largest = msg.photo[msg.photo.length - 1];
    const draft: Draft = { fileId: largest.file_id, description: (msg.caption ?? "").trim() };
    if (!draft.description) {
      draft.awaiting = "description";
      await saveDraft(env, chatId, draft);
      return send(env, chatId, "📸 Mam zdjęcie! Teraz napisz albo podyktuj krótki opis: jaki zabieg, jaki był problem, jak poszło.");
    }
    await saveDraft(env, chatId, draft);
    return generateAndPreview(env, chatId, draft);
  }

  if (msg.document) {
    return send(env, chatId, "Wyślij zdjęcie jako <b>zdjęcie</b> (nie jako plik), żebym mógł je odczytać.");
  }

  if (msg.voice) {
    return send(env, chatId, "Nagrania głosowego nie odczytam 🙈 Kliknij mikrofon na <b>klawiaturze</b> telefonu i podyktuj – wyślesz wtedy tekst.");
  }

  if (msg.text) {
    const draft = await getDraft(env, chatId);
    if (draft?.awaiting === "description") {
      draft.description = msg.text.trim();
      return generateAndPreview(env, chatId, draft);
    }
    if (draft?.awaiting === "feedback") {
      return generateAndPreview(env, chatId, draft, msg.text.trim());
    }
    return send(env, chatId, "Wyślij zdjęcie z zabiegu z krótkim opisem, a przygotuję wpis. /pomoc – instrukcja.");
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== "POST") return new Response("OK");
    if (request.headers.get("X-Telegram-Bot-Api-Secret-Token") !== env.TELEGRAM_WEBHOOK_SECRET) {
      return new Response("Forbidden", { status: 403 });
    }
    const update: any = await request.json();

    // Telegram może ponowić to samo zdarzenie – obsługujemy je tylko raz.
    const seenKey = `upd:${update.update_id}`;
    if (await env.DRAFTS.get(seenKey)) return new Response("OK");
    await env.DRAFTS.put(seenKey, "1", { expirationTtl: 60 * 60 * 24 });

    try {
      await handleUpdate(env, update);
    } catch (e) {
      console.error(e);
    }
    return new Response("OK");
  },
};
