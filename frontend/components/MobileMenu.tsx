'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Menu, X, LayoutDashboard, KanbanSquare, Settings, Shield, HelpCircle, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { clearAuth, getStoredUser } from '@/lib/auth';

const mobileNavigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Kanban Board', href: '#', icon: KanbanSquare },
  { name: 'Settings', href: '/settings', icon: Settings },
  { name: 'Privacy Policy', href: '/privacy-policy', icon: Shield },
  { name: 'Support', href: '/support', icon: HelpCircle },
];

export function MobileMenu() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();
  const user = getStoredUser();

  const handleLogout = () => {
    clearAuth();
    router.push('/signin');
  };

  return (
    <div className="md:hidden">
      <Button
        variant="ghost"
        size="icon"
        onClick={() => setOpen(!open)}
        className="fixed top-4 left-4 z-50"
      >
        {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
      </Button>
      {open && (
        <>
          <div
            className="fixed inset-0 bg-background/80 backdrop-blur-sm z-40"
            onClick={() => setOpen(false)}
          />
          <div className="fixed left-0 top-0 z-40 h-screen w-64 border-r bg-card">
            <div className="flex h-full flex-col p-4">
              <h1 className="text-xl font-bold mb-4">Taskz</h1>
              <nav className="flex-1 space-y-2">
                {mobileNavigation.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      onClick={() => setOpen(false)}
                      className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium ${
                        isActive
                          ? 'bg-accent text-accent-foreground'
                          : 'text-muted-foreground hover:bg-accent'
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
              {/* User Profile */}
              <div className="border-t pt-4 mt-4">
                <div className="flex items-center gap-3 mb-4">
                  <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                    <User className="h-4 w-4 text-primary" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">
                      {user?.user_name || 'User'}
                    </div>
                    <div className="text-xs text-muted-foreground truncate">
                      {user?.user_email || 'user@example.com'}
                    </div>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  className="w-full justify-start"
                  onClick={handleLogout}
                >
                  Sign out
                </Button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
