import Link from 'next/link';
import { Home, Bookmark, Library, Settings, Inbox, Archive } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SidebarProps {
  className?: string;
}

const NAV_ITEMS = [
  { name: 'Home', icon: Home, href: '/' },
  { name: 'Inbox', icon: Inbox, href: '/inbox' },
  { name: 'Vault', icon: Library, href: '/vault' },
  { name: 'Read Later', icon: Bookmark, href: '/read-later' },
  { name: 'Archive', icon: Archive, href: '/archive' },
];

export function Sidebar({ className }: SidebarProps) {
  // Hardcoded active path for demo purposes
  const currentPath = '/';

  return (
    <aside className={cn('flex flex-col w-64 h-screen border-r bg-sidebar border-border/40 px-4 py-6 gap-6 relative z-10', className)}>
      {/* Brand */}
      <div className="flex items-center px-2 mb-2 group cursor-pointer select-none">
        <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-primary/80 to-primary/30 shadow-inner border border-primary/20 mr-3 flex items-center justify-center transition-all duration-300 group-hover:shadow-primary/20 group-hover:scale-105">
          <span className="text-primary-foreground font-bold text-xs">NV</span>
        </div>
        <span className="font-bold text-lg tracking-tight text-foreground/90 group-hover:text-foreground transition-colors">Nexus Vault</span>
      </div>

      <nav className="flex flex-col gap-1 flex-1">
        <div className="px-3 text-[10px] font-bold text-muted-foreground/60 mb-2 mt-4 uppercase tracking-[0.2em] select-none">
          Library
        </div>
        {NAV_ITEMS.map((item) => {
          const isActive = currentPath === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "group relative flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-300 overflow-hidden",
                isActive 
                  ? "bg-accent/50 text-foreground shadow-sm" 
                  : "text-muted-foreground hover:text-foreground hover:bg-accent/30"
              )}
            >
              {/* Active Indicator Glow */}
              {isActive && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-primary rounded-r-full shadow-[0_0_10px_rgba(255,255,255,0.5)]" />
              )}
              
              <item.icon className={cn(
                "w-4 h-4 transition-transform duration-300 group-hover:scale-110", 
                isActive ? "text-primary" : "text-muted-foreground/80 group-hover:text-foreground"
              )} />
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* Settings Footer */}
      <div className="mt-auto border-t border-border/40 pt-4">
        <Link
          href="/settings"
          className="group flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-accent/30 transition-all duration-300"
        >
          <Settings className="w-4 h-4 opacity-80 group-hover:rotate-45 transition-transform duration-500" />
          Settings
        </Link>
      </div>
    </aside>
  );
}


