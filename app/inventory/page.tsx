"use client";
import { useState, useEffect } from "react";
import { PageShell } from "@/components/page-shell";
import { InventoryItem } from "@/lib/mock-data";
import { apiErrorMessage } from "@/lib/api-error";

type Toast = { msg: string; type: "success" | "error" } | null;

export default function InventoryPage() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [toast, setToast] = useState<Toast>(null);
  const [loadingSkus, setLoadingSkus] = useState<Set<string>>(new Set());
  const [editItem, setEditItem] = useState<InventoryItem | null>(null);
  const [editStock, setEditStock] = useState("");
  const [editReorderPoint, setEditReorderPoint] = useState("");
  const [editWeeklyVelocity, setEditWeeklyVelocity] = useState("");
  const [editSupplierLeadDays, setEditSupplierLeadDays] = useState("");
  const [selectedSku, setSelectedSku] = useState("");

  useEffect(() => {
    fetch("/api/inventory").then(r => r.json()).then((data: InventoryItem[]) => {
      if (Array.isArray(data) && data.length > 0) {
        setItems(data);
        setSelectedSku(data[0].sku);
      }
    }).catch(() => {});
  }, []);

  const critical = items.filter(i => i.stock <= i.reorderPoint || i.depletionDays <= 7);
  const avgLead = items.length > 0
    ? Math.round(items.reduce((a, i) => a + i.supplierLeadDays, 0) / items.length)
    : 0;
  const selectedItem = items.find(i => i.sku === selectedSku) ?? critical[0] ?? items[0] ?? null;

  const showToast = (msg: string, type: "success" | "error" = "success") => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3500);
  };

  const handleCriticalList = async () => {
    try {
      window.location.href = "/api/inventory/export";
      showToast("Stok raporu indiriliyor...");
    } catch {
      showToast("Rapor indirilemedi.", "error");
    }
  };

  const handleSupplyDraft = async () => {
    const lines = critical.map(i => `• *${i.product}* (${i.sku}): ${i.recommendation}`).join("\n");
    const text = `*OpsMind Tedarik Taslağı*\nTarih: ${new Date().toLocaleDateString("tr-TR")}\n\n${lines}`;
    try {
      const res = await fetch("/api/supply-webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      if (res.ok) {
        showToast("Tedarik taslağı Slack'e gönderildi.");
      } else {
        const data = await res.json().catch(() => null);
        throw new Error(apiErrorMessage(data, "Slack webhook hatası."));
      }
    } catch {
      navigator.clipboard.writeText(text.replace(/\*/g, "")).then(() => {
        showToast("Slack'e ulaşılamadı, taslak panoya kopyalandı.");
      }).catch(() => showToast("Slack'e ulaşılamadı ve panoya kopyalama izni alınamadı.", "error"));
    }
  };

  const handleOrder = async (sku: string) => {
    setLoadingSkus(prev => new Set(prev).add(sku));
    try {
      const res = await fetch("/api/inventory/order", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ sku, quantity: 20 }) });
      const data = await res.json().catch(() => null);
      if (!res.ok || !data?.ok) throw new Error(apiErrorMessage(data, "Siparis verilemedi."));
      if (data.ok) {
        setItems(prev => prev.map(i => i.sku === sku ? { ...i, stock: data.entry.stock, depletionDays: data.entry.depletionDays } : i));
        const item = items.find(i => i.sku === sku);
        const productName = item?.product ?? sku;
        fetch("/api/supply-webhook", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: `*OpsMind Tedarik Siparisi*\n${productName} (${sku}) icin 20 adet tedarik siparisi verildi.` }),
        }).catch(() => {});
        showToast(`${sku} icin tedarik siparisi verildi. Stok guncellendi.`);
      }
    } catch (err) { showToast(err instanceof Error ? err.message : "Siparis verilemedi.", "error"); }
    setLoadingSkus(prev => { const s = new Set(prev); s.delete(sku); return s; });
  };

  const handleEditSave = async () => {
    if (!editItem) return;
    const n = parseInt(editStock);
    const rp = parseInt(editReorderPoint);
    const wv = parseInt(editWeeklyVelocity);
    const ld = parseInt(editSupplierLeadDays);

    if (isNaN(n) || n < 0 || isNaN(rp) || rp < 0 || isNaN(wv) || wv < 0 || isNaN(ld) || ld < 0) { 
      showToast("Tüm değerler geçerli pozitif sayı olmalıdır.", "error"); 
      return; 
    }

    try {
      const res = await fetch(`/api/inventory/${editItem.sku}`, { 
        method: "PUT", 
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify({ 
          stock: n,
          reorder_point: rp,
          weekly_velocity: wv,
          supplier_lead_days: ld
        }) 
      });
      const data = await res.json().catch(() => null);
      if (!res.ok || !data?.ok) throw new Error(apiErrorMessage(data, "Güncelleme başarısız."));
      if (data.ok) {
        setItems(prev => prev.map(i => i.sku === editItem.sku ? { 
          ...i, 
          stock: data.entry.stock, 
          reorderPoint: data.entry.reorderPoint,
          weeklyVelocity: data.entry.weeklyVelocity,
          supplierLeadDays: data.entry.supplierLeadDays,
          depletionDays: data.entry.depletionDays 
        } : i));
        showToast(`${editItem.sku} detayları güncellendi.`);
      }
    } catch (err) { showToast(err instanceof Error ? err.message : "Güncelleme başarısız.", "error"); }
    setEditItem(null);
    setEditStock("");
  };

  return (
    <PageShell
      title="Stok Durumu"
      subtitle="SKU bazlı stok, haftalık hız ve AI tedarik önerileri."
      badge={`${critical.length} kritik SKU`}
      rightPanel={
        <div className="context-stack">
          <div className="context-card context-card--warm">
            <p className="context-kicker">Kritik SKU</p>
            <h3 className="context-title">{selectedItem?.product ?? "Seçili Ürün Yok"}</h3>
            {selectedItem && (
              <div className="context-list">
                <div className="context-row"><span>SKU</span><strong>{selectedItem.sku}</strong></div>
                <div className="context-row"><span>Stok</span><strong>{selectedItem.stock}</strong></div>
                <div className="context-row"><span>Tükenme</span><strong>{selectedItem.depletionDays}g</strong></div>
                <div className="context-row"><span>Tedarik</span><strong>{selectedItem.supplierLeadDays}g</strong></div>
              </div>
            )}
          </div>
          <div className="context-card">
            <p className="context-kicker">Satın alma önerisi</p>
            <p className="muted" style={{ margin: 0 }}>{selectedItem?.recommendation ?? "Öneri bulunmuyor."}</p>
            {selectedItem && (
              <div className="context-actions">
                <button type="button" className="button sm" onClick={() => handleOrder(selectedItem.sku)} disabled={loadingSkus.has(selectedItem.sku)}>
                  Sipariş Ver
                </button>
                <button type="button" className="button sm secondary" onClick={handleSupplyDraft}>
                  Tedarik Taslağı
                </button>
              </div>
            )}
          </div>
          <div className="context-card">
            <p className="context-kicker">Stok özeti</p>
            <div className="context-list">
              <div className="context-row"><span>Kritik SKU</span><strong>{critical.length}</strong></div>
              <div className="context-row"><span>Ort. tedarik</span><strong>{avgLead}g</strong></div>
            </div>
          </div>
        </div>
      }
    >
      <div className="grid grid-3" style={{ marginBottom: 16 }}>
        <article className="card card--metric">
          <div>
            <p className="card__eyebrow">Kritik / takip</p>
            <p className="kpi" style={{ color: critical.length > 0 ? "var(--warning)" : undefined }}>
              {critical.length}
            </p>
          </div>
          <p className="metric-note">Eşik altı veya 7 gün içinde tükenecek</p>
        </article>

        <article className="card card--metric">
          <div>
            <p className="card__eyebrow">Ortalama tedarik süresi</p>
            <p className="kpi">{avgLead}g</p>
          </div>
          <p className="metric-note">Tedarikçi lead time ortalaması</p>
        </article>

        <article className="card card--action">
          <div>
            <p className="card__eyebrow">Hızlı aksiyon</p>
            <p className="metric-note">Kritik SKU listesini indirin veya Slack için tedarik taslağı oluşturun.</p>
          </div>
          <div className="stack">
            <button type="button" className="button" onClick={handleCriticalList}>
              Kritik SKU Listesi
            </button>
            <button type="button" className="button secondary" onClick={handleSupplyDraft}>
              Tedarik Taslağı
            </button>
          </div>
        </article>
      </div>

      <section className="card">
        <div className="table-titlebar">
          <h3>Stok sağlığı</h3>
          <span className="pill info">{items.length} SKU izleniyor</span>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>SKU</th>
                <th>Ürün</th>
                <th>Kategori</th>
                <th>Stok</th>
                <th>Eşik</th>
                <th>Haftalık hız</th>
                <th>Tükenme</th>
                <th>Tedarik</th>
                <th>AI önerisi</th>
                <th>İşlem</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => {
                const isLow = item.stock <= item.reorderPoint || item.depletionDays <= 7;
                const loading = loadingSkus.has(item.sku);
                return (
                  <tr
                    key={item.sku}
                    className={`selectable-row ${isLow ? "row-warning" : ""} ${selectedItem && item.sku === selectedItem.sku ? "is-selected" : ""}`}
                    onClick={() => setSelectedSku(item.sku)}
                  >
                    <td><strong>{item.sku}</strong></td>
                    <td>{item.product}</td>
                    <td><span className="pill">{item.category}</span></td>
                    <td className="numeric">
                      <span style={{ color: isLow ? "var(--warning)" : undefined, fontWeight: isLow ? 750 : undefined }}>
                        {item.stock}
                      </span>
                    </td>
                    <td className="numeric">{item.reorderPoint}</td>
                    <td className="numeric">{item.weeklyVelocity}/hf</td>
                    <td>
                      <span className={item.depletionDays <= 7 ? "stat-trend--warn numeric" : "numeric"}>
                        {item.depletionDays}g
                      </span>
                    </td>
                    <td className="numeric">{item.supplierLeadDays}g</td>
                    <td style={{ minWidth: 220 }}>
                      <span className="muted">{item.recommendation}</span>
                      {isLow && <div style={{ marginTop: 7 }}><span className="pill mid">Eşik altı</span></div>}
                    </td>
                    <td>
                      <div className="stack">
                        <button
                          type="button"
                          className="button sm"
                          onClick={(e) => { e.stopPropagation(); setSelectedSku(item.sku); handleOrder(item.sku); }}
                          disabled={loading}
                          title="Tedarik siparişi ver"
                        >
                          {loading ? "..." : "Sipariş Ver"}
                        </button>
                        <button
                          type="button"
                          className="button sm secondary"
                          onClick={(e) => { e.stopPropagation(); setSelectedSku(item.sku); setEditItem(item); setEditStock(item.stock.toString()); setEditReorderPoint(item.reorderPoint.toString()); setEditWeeklyVelocity(item.weeklyVelocity.toString()); setEditSupplierLeadDays(item.supplierLeadDays.toString()); }}
                          title="Stok güncelle"
                        >
                          Düzenle
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      {editItem && (
        <div className="modal-overlay" onClick={() => setEditItem(null)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3>{editItem.product} - Stok Güncelle</h3>
            <p className="muted">Mevcut stok: {editItem.stock} adet</p>
            <div className="modal-field">
              <label>Yeni stok miktarı</label>
              <input
                type="number"
                className="form-input"
                value={editStock}
                onChange={e => setEditStock(e.target.value)}
                min="0"
                autoFocus
              />
            </div>
            <div className="stack" style={{ marginTop: 4 }}>
              <button type="button" className="button" onClick={handleEditSave}>Kaydet</button>
              <button type="button" className="button secondary" onClick={() => setEditItem(null)}>İptal</button>
            </div>
          </div>
        </div>
      )}

      {toast && <div className={`toast ${toast.type}`}>{toast.msg}</div>}
    </PageShell>
  );
}
