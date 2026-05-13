"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/lib/auth";

const links = [
  { href: "/", label: "Genel Bakış", icon: "01" },
  { href: "/inbox", label: "AI Yardım Masası", icon: "02" },
  { href: "/shipping", label: "Kargo Takibi", icon: "03" },
  { href: "/inventory", label: "Stok Durumu", icon: "04" },
  { href: "/knowledge-base", label: "Bilgi Tabanı", icon: "05" },
  { href: "/tasks", label: "Görevler", icon: "06" },
  { href: "/settings", label: "Ayarlar", icon: "07" }
] as const;

export function Navigation() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [collapsed, setCollapsed] = useState(false);

  if (!user) return null;

  return (
    <aside className={`sidebar ${collapsed ? "sidebar--collapsed" : ""}`}>
      <div className="sidebar-brand">
        <img src="/logo.png" alt="OpsMind Logo" className="brand-mark" style={{ width: "auto", height: 32, borderRadius: 8, objectFit: "contain" }} />
        <div className="brand-copy">
          <h2 className="brand-title">OpsMind AI</h2>
          <p className="brand-tagline">Operasyon Platformu</p>
        </div>
        <button
          type="button"
          className="sidebar-toggle"
          onClick={() => setCollapsed(value => !value)}
          aria-label={collapsed ? "Menüyü genişlet" : "Menüyü daralt"}
          title={collapsed ? "Menüyü genişlet" : "Menüyü daralt"}
        >
          {collapsed ? "›" : "‹"}
        </button>
      </div>

      <nav className="sidebar-nav" aria-label="Ana menü">
        {links.map((link) => {
          const active =
            link.href === "/"
              ? pathname === "/"
              : pathname === link.href || pathname.startsWith(`${link.href}/`);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`nav-link ${active ? "nav-link--active" : ""}`}
            >
              <span className="nav-link__icon" aria-hidden>
                {link.icon}
              </span>
              <span className="nav-link__label">{link.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="user-avatar" style={{ overflow: "hidden" }}>
            {user.avatar.startsWith("/") ? (
              <img src={user.avatar} alt={user.name} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            ) : (
              user.avatar
            )}
          </div>
          <div className="user-info">
            <p className="user-name">{user.name}</p>
            <p className="user-role">{user.role} · {user.department}</p>
          </div>
        </div>
        <button type="button" className="logout-btn" onClick={logout}>
          Cikis Yap
        </button>
      </div>
    </aside>
  );
}
