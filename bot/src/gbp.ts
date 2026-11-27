// Publikowanie postów (aktualności) w wizytówce Google – Google Business Profile API.
// Działa dopiero, gdy Google przyzna dostęp do API i ustawisz sekrety GBP_* (patrz README).

export interface GbpConfig {
  clientId: string;
  clientSecret: string;
  refreshToken: string;
  accountId?: string; // sama liczba, np. "1234567890"
  locationId?: string; // sama liczba, np. "9876543210"
}

export interface GbpPost {
  summary: string;
  url: string; // link w przycisku „Dowiedz się więcej”
  imageUrl: string; // publiczny adres zdjęcia
}

async function accessToken(cfg: GbpConfig): Promise<string> {
  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: cfg.clientId,
      client_secret: cfg.clientSecret,
      refresh_token: cfg.refreshToken,
      grant_type: "refresh_token",
    }),
  });
  const data: any = await res.json();
  if (!res.ok || !data.access_token) {
    throw new Error(`Logowanie do Google nie powiodło się (${res.status}): ${data.error_description ?? data.error ?? "brak szczegółów"}`);
  }
  return data.access_token;
}

async function gapi(token: string, url: string, init: RequestInit = {}): Promise<any> {
  const res = await fetch(url, {
    ...init,
    headers: { Authorization: `Bearer ${token}`, ...(init.body ? { "Content-Type": "application/json" } : {}) },
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Google API ${res.status}: ${text.slice(0, 400)}`);
  return text ? JSON.parse(text) : {};
}

/** Lista kont i wizytówek – do jednorazowego odczytania GBP_ACCOUNT_ID i GBP_LOCATION_ID. */
export async function listLocations(cfg: GbpConfig): Promise<{ account: string; accountName: string; location: string; title: string }[]> {
  const token = await accessToken(cfg);
  const accounts = await gapi(token, "https://mybusinessaccountmanagement.googleapis.com/v1/accounts");
  const out = [];
  for (const acc of accounts.accounts ?? []) {
    const locs = await gapi(
      token,
      `https://mybusinessbusinessinformation.googleapis.com/v1/${acc.name}/locations?readMask=name,title&pageSize=100`,
    );
    for (const loc of locs.locations ?? []) {
      out.push({
        account: String(acc.name).split("/")[1],
        accountName: acc.accountName ?? "",
        location: String(loc.name).split("/")[1],
        title: loc.title ?? "",
      });
    }
  }
  return out;
}

/** Publikuje post ze zdjęciem i przyciskiem „Dowiedz się więcej”. Zwraca link do posta (jeśli Google go poda). */
export async function createPost(cfg: GbpConfig, post: GbpPost): Promise<string | undefined> {
  if (!cfg.accountId || !cfg.locationId) throw new Error("Brak GBP_ACCOUNT_ID lub GBP_LOCATION_ID w konfiguracji bota.");
  const token = await accessToken(cfg);
  const summary = post.summary.length > 1500 ? post.summary.slice(0, 1497) + "…" : post.summary;
  const created = await gapi(
    token,
    `https://mybusiness.googleapis.com/v4/accounts/${cfg.accountId}/locations/${cfg.locationId}/localPosts`,
    {
      method: "POST",
      body: JSON.stringify({
        languageCode: "pl",
        topicType: "STANDARD",
        summary,
        callToAction: { actionType: "LEARN_MORE", url: post.url },
        media: [{ mediaFormat: "PHOTO", sourceUrl: post.imageUrl }],
      }),
    },
  );
  return created.searchUrl;
}
