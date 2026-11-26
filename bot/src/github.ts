// Minimalny klient GitHub API: odczyt pliku i jeden commit z wieloma plikami.

export interface GitHubConfig {
  token: string;
  repo: string; // "owner/name"
  branch: string;
}

export type FileChange = { path: string; content: string; encoding: "utf-8" | "base64" };

async function gh<T>(cfg: GitHubConfig, path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(`https://api.github.com/repos/${cfg.repo}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${cfg.token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "gabinet-efekty-bot",
      ...(init.body ? { "Content-Type": "application/json" } : {}),
    },
  });
  if (!res.ok) throw new Error(`GitHub ${init.method ?? "GET"} ${path}: ${res.status} ${await res.text()}`);
  return res.json() as Promise<T>;
}

export function b64ToUtf8(b64: string): string {
  const bin = atob(b64.replace(/\n/g, ""));
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new TextDecoder().decode(bytes);
}

/** Zwraca zawartość pliku tekstowego albo null, jeśli plik nie istnieje. */
export async function readTextFile(cfg: GitHubConfig, path: string): Promise<string | null> {
  try {
    const r = await gh<{ content: string }>(cfg, `/contents/${path}?ref=${encodeURIComponent(cfg.branch)}`);
    return b64ToUtf8(r.content);
  } catch (e) {
    if (String(e).includes(": 404 ")) return null;
    throw e;
  }
}

/** Tworzy jeden commit ze wszystkimi plikami naraz (strona przebuduje się tylko raz). */
export async function commitFiles(cfg: GitHubConfig, message: string, files: FileChange[]): Promise<string> {
  const ref = await gh<{ object: { sha: string } }>(cfg, `/git/ref/heads/${cfg.branch}`);
  const parentSha = ref.object.sha;
  const parent = await gh<{ tree: { sha: string } }>(cfg, `/git/commits/${parentSha}`);

  const tree = [];
  for (const f of files) {
    const blob = await gh<{ sha: string }>(cfg, `/git/blobs`, {
      method: "POST",
      body: JSON.stringify({ content: f.content, encoding: f.encoding }),
    });
    tree.push({ path: f.path, mode: "100644", type: "blob", sha: blob.sha });
  }
  const newTree = await gh<{ sha: string }>(cfg, `/git/trees`, {
    method: "POST",
    body: JSON.stringify({ base_tree: parent.tree.sha, tree }),
  });
  const commit = await gh<{ sha: string }>(cfg, `/git/commits`, {
    method: "POST",
    body: JSON.stringify({ message, tree: newTree.sha, parents: [parentSha] }),
  });
  await gh(cfg, `/git/refs/heads/${cfg.branch}`, {
    method: "PATCH",
    body: JSON.stringify({ sha: commit.sha }),
  });
  return commit.sha;
}
