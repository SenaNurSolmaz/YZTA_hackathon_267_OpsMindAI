export type Order = {
  id: string;
  name: string;
  customer: string;
  city: string;
  totalTry: number;
  paymentStatus: "Odendi" | "Beklemede" | "Iade";
  fulfillmentStatus: "Hazirlaniyor" | "Kargoda" | "Teslim" | "Gecikme";
  itemCount: number;
  channel: "Web" | "WhatsApp" | "Fiziksel";
  product: string;
  createdAt: string;
};

export type Conversation = {
  id: string;
  customer: string;
  channel: "WhatsApp" | "Email" | "Live Chat";
  topic: "Siparis" | "Iade" | "Stok" | "Kargo" | "Teknik";
  lastMessage: string;
  status: "AI Taslagi Hazir" | "Temsilci Bekliyor" | "Cozuldu";
  unread: number;
  sentiment: "Olumlu" | "Notr" | "Olumsuz";
  orderRef: string | null;
  aiDraft: string;
  updatedAt: string;
};

export type Shipment = {
  orderId: string;
  customer: string;
  provider: string;
  trackingNo: string;
  destination: string;
  status: string;
  lastEvent: string;
  risk: "Dusuk" | "Orta" | "Yuksek";
  slaHoursLeft: number;
  estimatedDelivery: string;
  product: string;
};

export type InventoryItem = {
  sku: string;
  product: string;
  category: string;
  stock: number;
  reorderPoint: number;
  weeklyVelocity: number;
  depletionDays: number;
  recommendation: string;
  supplierLeadDays: number;
  unitPrice: number;
};

export type KnowledgeEntry = {
  id: string;
  title: string;
  content: string;
  category: string;
  addedAt: string;
  addedBy: string;
};
