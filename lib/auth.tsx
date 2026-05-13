"use client";
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useRouter, usePathname } from "next/navigation";

export type AuthUser = {
  id: string;
  name: string;
  email: string;
  role: "Admin" | "Operasyon" | "Destek" | "Satın Alma";
  department: string;
  avatar: string;
};

type AuthCtx = {
  user: AuthUser | null;
  authReady: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
};

const AuthContext = createContext<AuthCtx>({
  user: null,
  authReady: false,
  login: async () => false,
  logout: () => {}
});

const DEMO_USERS: AuthUser[] = [
  { id: "u1", name: "Ahmet Demir", email: "ahmet@opsmind.com", role: "Admin", department: "Yönetim", avatar: "AD" },
  { id: "u2", name: "Selin Kaya", email: "selin@opsmind.com", role: "Operasyon", department: "Kargo & Lojistik", avatar: "SK" },
  { id: "u3", name: "Barış Arslan", email: "baris@opsmind.com", role: "Destek", department: "Müşteri Hizmetleri", avatar: "BA" },
];

const roles: AuthUser["role"][] = ["Admin", "Operasyon", "Destek", "Satın Alma"];

function isAuthUser(value: unknown): value is AuthUser {
  if (!value || typeof value !== "object") return false;
  const candidate = value as Record<string, unknown>;

  return (
    typeof candidate.id === "string" &&
    typeof candidate.name === "string" &&
    typeof candidate.email === "string" &&
    typeof candidate.department === "string" &&
    typeof candidate.avatar === "string" &&
    typeof candidate.role === "string" &&
    roles.includes(candidate.role as AuthUser["role"])
  );
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [authReady, setAuthReady] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    try {
      const stored = localStorage.getItem("opsmind_user");
      if (!stored) return;

      const parsed = JSON.parse(stored);
      if (isAuthUser(parsed)) {
        setUser(parsed);
      } else {
        localStorage.removeItem("opsmind_user");
      }
    } catch {
      localStorage.removeItem("opsmind_user");
    } finally {
      setAuthReady(true);
    }
  }, []);

  useEffect(() => {
    if (!authReady) return;
    if (user && pathname === "/login") {
      router.replace("/");
      return;
    }
    if (!user && pathname !== "/login") {
      router.replace("/login");
    }
  }, [authReady, user, pathname, router]);

  const login = async (email: string, password: string): Promise<boolean> => {
    await new Promise(r => setTimeout(r, 800));
    const found = DEMO_USERS.find(u => u.email === email);
    if (found && password.length >= 4) {
      setUser(found);
      localStorage.setItem("opsmind_user", JSON.stringify(found));
      router.push("/");
      return true;
    }
    return false;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("opsmind_user");
    router.push("/login");
  };

  return (
    <AuthContext.Provider value={{ user, authReady, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
