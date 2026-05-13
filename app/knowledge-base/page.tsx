"use client";
import { useState, useEffect } from "react";
import { PageShell } from "@/components/page-shell";
import { KnowledgeEntry } from "@/lib/mock-data";
import { apiErrorMessage } from "@/lib/api-error";

type Toast = { msg: string; type: "success" | "error" } | null;

export default function KnowledgeBasePage() {
  const [entries, setEntries] = useState<KnowledgeEntry[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [filter, setFilter] = useState("Tumu");
  const [search, setSearch] = useState("");
  const [toast, setToast] = useState<Toast>(null);
  const [form, setForm] = useState({ title: "", content: "", category: "Teknik Destek" });
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [selectedEntryId, setSelectedEntryId] = useState<string>("");
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState<{role: "user" | "ai", text: string}[]>([
    { role: "ai", text: "Merhaba! Bilgi tabanındaki kayıtlara dayanarak size nasıl yardımcı olabilirim?" }
  ]);

  useEffect(() => {
    fetch("/api/knowledge")
      .then(res => res.json())
      .then((data: KnowledgeEntry[]) => {
        setEntries(data);
        if (data.length > 0) setSelectedEntryId(data[0].id);
      })
      .catch(() => showToast("Veriler yüklenemedi.", "error"));
  
  }, []);

  const categories = ["Tumu", ...Array.from(new Set(entries.map(e => e.category)))];
  const filtered = entries.filter(e =>
    (filter === "Tumu" || e.category === filter) &&
    (e.title.toLowerCase().includes(search.toLowerCase()) ||
     e.content.toLowerCase().includes(search.toLowerCase()))
  );
  const selectedEntry =
    filtered.find(e => e.id === selectedEntryId) ??
    filtered[0] ??
    entries[0];

  const showToast = (msg: string, type: "success" | "error" = "success") => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  };

  const handleSave = async () => {
    if (!form.title.trim() || !form.content.trim()) {
      showToast("Başlık ve içerik zorunludur.", "error");
      return;
    }
    try {
      const res = await fetch("/api/knowledge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: form.title,
          content: form.content,
          category: form.category,
          addedBy: "Oturum Kullanıcısı"
        }),
      });
      const data = await res.json().catch(() => null);
      if (!res.ok) throw new Error(apiErrorMessage(data, "Kayıt eklenemedi."));
      const newEntry: KnowledgeEntry = data.entry;
      setEntries(prev => [newEntry, ...prev]);
      setSelectedEntryId(newEntry.id);
      setShowModal(false);
      setForm({ title: "", content: "", category: "Teknik Destek" });
      showToast("Bilgi tabanına eklendi.");
    } catch (err) {
      showToast("Kayıt eklenemedi: " + (err instanceof Error ? err.message : "hata"), "error");
    }
  };

  const handleDelete = async (id: string) => {
    setDeletingId(id);
    try {
      const res = await fetch(`/api/knowledge?id=${id}`, { method: "DELETE" });
      const data = await res.json().catch(() => null);
      if (!res.ok) throw new Error(apiErrorMessage(data, "Kayıt silinemedi."));
      setEntries(prev => prev.filter(e => e.id !== id));
      if (selectedEntryId === id) {
        const next = entries.find(e => e.id !== id);
        if (next) setSelectedEntryId(next.id);
      }
      showToast("Kayıt silindi.");
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Kayıt silinemedi.", "error");
    } finally {
      setDeletingId(null);
    }
  };

  const handleChat = async () => {
    if (!chatInput.trim()) return;
    const prompt = chatInput.trim();
    setChatInput("");
    setChatHistory(prev => [...prev, { role: "user", text: prompt }]);
    setChatLoading(true);

    const context = entries.map(e => `Başlık: ${e.title}\nKategori: ${e.category}\nİçerik: ${e.content}`).join("\n\n---\n\n");

    try {
      const res = await fetch("/api/agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, context }),
      });
      const data = await res.json().catch(() => null);
      if (res.ok && data.result) {
        setChatHistory(prev => [...prev, { role: "ai", text: data.result }]);
      } else {
        setChatHistory(prev => [...prev, { role: "ai", text: "Üzgünüm, bir hata oluştu ve yanıt oluşturulamadı." }]);
      }
    } catch {
      setChatHistory(prev => [...prev, { role: "ai", text: "Bağlantı hatası oluştu." }]);
    }
    setChatLoading(false);
  };

  return (
    <PageShell
      title="Bilgi Tabanı"
      subtitle="AI yanıt kaynağı; sık sorulan sorular, teknik kılavuzlar ve operasyon prosedürleri."
      badge={`${entries.length} kayıt`}
      rightPanel={
        <div className="context-stack" style={{ display: 'flex', flexDirection: 'column', height: '100%', maxHeight: '600px' }}>
          <div className="context-card context-card--warm" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
            <p className="context-kicker">OpsMind Bilgi Tabanı AI</p>
            <div style={{ flex: 1, overflowY: 'auto', marginBottom: '10px', display: 'flex', flexDirection: 'column', gap: '8px', paddingRight: '4px' }}>
              {chatHistory.map((msg, i) => (
                <div key={i} style={{ alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', background: msg.role === 'user' ? 'var(--accent)' : '#fff', color: msg.role === 'user' ? '#fff' : 'var(--text)', padding: '8px 12px', borderRadius: '12px', maxWidth: '90%', fontSize: '0.85rem', border: msg.role === 'user' ? 'none' : '1px solid var(--border)' }}>
                  {msg.text}
                </div>
              ))}
              {chatLoading && <div style={{ alignSelf: 'flex-start', background: '#fff', padding: '8px 12px', borderRadius: '12px', fontSize: '0.85rem', border: '1px solid var(--border)' }}>Düşünüyor...</div>}
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input
                className="form-input"
                value={chatInput}
                onChange={e => setChatInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleChat()}
                placeholder="Bilgi tabanına sor..."
                style={{ flex: 1 }}
              />
              <button type="button" className="button sm" onClick={handleChat} disabled={chatLoading || !chatInput.trim()}>
                Sor
              </button>
            </div>
          </div>
        </div>
      }
    >
      <div className="toolbar toolbar--split">
        <div className="toolbar" style={{ flex: 1 }}>
          <input
            className="form-input"
            style={{ maxWidth: 300 }}
            placeholder="Başlık veya içerik ara..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <div className="segmented" aria-label="Kategori filtresi">
            {categories.map(cat => (
              <button
                key={cat}
                type="button"
                className={`button sm ${filter === cat ? "is-active" : ""}`}
                onClick={() => setFilter(cat)}
              >
                {cat === "Tumu" ? "Tümü" : cat}
              </button>
            ))}
          </div>
        </div>
        <button type="button" className="button" onClick={() => setShowModal(true)}>
          Yeni Kayıt Ekle
        </button>
      </div>

      {filtered.length === 0 && (
        <div className="card empty-state">
          <p className="muted">Kayıt bulunamadı.</p>
          <button type="button" className="button" onClick={() => setShowModal(true)} style={{ marginTop: 12 }}>
            İlk Kaydı Ekle
          </button>
        </div>
      )}

      <div className="kb-grid">
        {filtered.map(entry => (
          <div
            key={entry.id}
            className={`kb-entry selectable-card ${entry.id === selectedEntry?.id ? "is-selected" : ""}`}
            style={{ opacity: deletingId === entry.id ? 0.4 : 1, transition: "opacity 0.3s" }}
            onClick={() => setSelectedEntryId(entry.id)}
          >
            <div className="kb-entry__header">
              <div className="toolbar">
                <h4 className="kb-entry__title">{entry.title}</h4>
                <span className="pill">{entry.category}</span>
              </div>
              <button
                type="button"
                className="button sm secondary"
                onClick={(e) => { e.stopPropagation(); handleDelete(entry.id); }}
                disabled={deletingId === entry.id}
                style={{ flexShrink: 0, color: "var(--danger)", borderColor: "rgba(189,100,102,0.32)" }}
              >
                Sil
              </button>
            </div>
            <p className="kb-entry__content">{entry.content}</p>
            <p className="kb-entry__meta">
              Ekleyen: {entry.addedBy} · {new Date(entry.addedAt).toLocaleDateString("tr-TR")}
            </p>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3>Yeni Bilgi Tabanı Kaydı</h3>
            <div className="modal-field">
              <label>Başlık</label>
              <input
                className="form-input"
                value={form.title}
                onChange={e => setForm(p => ({ ...p, title: e.target.value }))}
                placeholder="Konu başlığını girin"
                autoFocus
              />
            </div>
            <div className="modal-field">
              <label>Kategori</label>
              <select
                className="form-input"
                value={form.category}
                onChange={e => setForm(p => ({ ...p, category: e.target.value }))}
              >
                <option>Teknik Destek</option>
                <option>Müşteri Hizmetleri</option>
                <option>İade</option>
                <option>Kargo</option>
                <option>Kullanım Kılavuzu</option>
                <option>Operasyon</option>
              </select>
            </div>
            <div className="modal-field">
              <label>İçerik</label>
              <textarea
                className="form-input"
                value={form.content}
                onChange={e => setForm(p => ({ ...p, content: e.target.value }))}
                rows={5}
                placeholder="Bilgi içeriğini girin..."
              />
            </div>
            <div className="stack" style={{ marginTop: 4 }}>
              <button type="button" className="button" onClick={handleSave}>Kaydet</button>
              <button type="button" className="button secondary" onClick={() => setShowModal(false)}>İptal</button>
            </div>
          </div>
        </div>
      )}

      {toast && <div className={`toast ${toast.type}`}>{toast.msg}</div>}
    </PageShell>
  );
}
