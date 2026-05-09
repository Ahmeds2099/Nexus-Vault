import { AppShell } from '@/components/layout/app-shell';
import { ExternalLink, Clock, MoreHorizontal, FileText, Link as LinkIcon, Edit3 } from 'lucide-react';

export default function Home() {
  return (
    <AppShell>
      <div className="space-y-12 pb-12">
        {/* Engaging Hero Section */}
        <section className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-primary/5 via-background to-background p-8 sm:p-12 border border-border/40 shadow-sm">
          {/* Subtle noise/texture overlay could go here, for now using a radial gradient */}
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary/10 via-transparent to-transparent opacity-50"></div>
          
          <div className="relative z-10 max-w-2xl">
            <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4 text-foreground/90">
              Your Digital Sandbox
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed mb-8">
              A curated space for your knowledge, ideas, and discoveries. Dive back into what matters.
            </p>
            <div className="flex gap-4 items-center">
              <span className="text-sm font-medium px-4 py-2 rounded-full bg-primary/10 text-primary border border-primary/20 shadow-inner">
                12 Unread Items
              </span>
              <span className="text-sm font-medium text-muted-foreground">
                3 Added Today
              </span>
            </div>
          </div>
        </section>
        
        {/* Rich Content Grid */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold tracking-tight text-foreground/90">Recently Added</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            {/* Example Card 1: Article (Blue Accent) */}
            <div className="group flex flex-col rounded-2xl border border-border/40 bg-card overflow-hidden hover:-translate-y-1 hover:shadow-2xl hover:shadow-[var(--cat-article)]/5 hover:border-[var(--cat-article)]/30 transition-all duration-300 cursor-pointer">
              <div className="h-44 w-full bg-muted relative overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop" 
                  alt="Thumbnail" 
                  className="object-cover w-full h-full opacity-70 group-hover:opacity-100 group-hover:scale-105 transition-all duration-700 ease-out"
                />
                <div className="absolute top-3 left-3 bg-background/90 backdrop-blur-md px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-widest text-[var(--cat-article)] border border-[var(--cat-article)]/20 shadow-sm flex items-center gap-1.5">
                  <FileText className="w-3 h-3" />
                  Article
                </div>
              </div>
              <div className="p-5 flex-1 flex flex-col">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-4 h-4 rounded-full bg-background border border-border/50 flex items-center justify-center overflow-hidden">
                    <img src="https://www.google.com/s2/favicons?domain=theverge.com&sz=32" alt="favicon" className="w-full h-full" />
                  </div>
                  <span className="text-xs font-medium text-muted-foreground">theverge.com</span>
                  <span className="text-xs font-medium text-muted-foreground/60 ml-auto flex items-center">
                    <Clock className="w-3 h-3 mr-1"/> 5m read
                  </span>
                </div>
                <h3 className="text-lg font-bold leading-snug mb-2 group-hover:text-[var(--cat-article)] transition-colors line-clamp-2 text-foreground/90">
                  The Future of Local-First Software Architecture
                </h3>
                <p className="text-sm text-muted-foreground line-clamp-2 mb-4 flex-1 leading-relaxed">
                  Why owning your data is becoming increasingly important in a world of cloud outages and expensive subscription models.
                </p>
                <div className="flex items-center justify-between mt-auto pt-4 border-t border-border/40">
                  <span className="text-xs font-medium text-muted-foreground/60">Added 2h ago</span>
                  <button className="text-muted-foreground hover:text-foreground transition-colors p-1.5 rounded-md hover:bg-accent">
                    <MoreHorizontal className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Example Card 2: Note (Amber Accent) */}
            <div className="group flex flex-col rounded-2xl border border-border/40 bg-card overflow-hidden hover:-translate-y-1 hover:shadow-2xl hover:shadow-[var(--cat-note)]/5 hover:border-[var(--cat-note)]/30 transition-all duration-300 cursor-pointer p-5 relative">
               <div className="absolute top-0 right-0 w-32 h-32 bg-[var(--cat-note)]/5 rounded-bl-full blur-2xl pointer-events-none transition-opacity group-hover:opacity-100 opacity-0" />
               <div className="flex items-center justify-between mb-5 relative z-10">
                 <div className="bg-[var(--cat-note)]/10 text-[var(--cat-note)] border border-[var(--cat-note)]/20 px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-widest flex items-center gap-1.5">
                  <Edit3 className="w-3 h-3" />
                  Quick Note
                 </div>
                 <button className="text-muted-foreground hover:text-foreground transition-colors p-1.5 rounded-md hover:bg-accent">
                    <MoreHorizontal className="w-4 h-4" />
                  </button>
               </div>
               <h3 className="text-xl font-bold leading-snug mb-3 group-hover:text-[var(--cat-note)] transition-colors text-foreground/90 relative z-10">
                  Idea for Nexus Vault sync
               </h3>
               <p className="text-[13px] text-muted-foreground/90 leading-relaxed mb-4 flex-1 font-mono bg-background/50 p-3 rounded-xl border border-border/30 relative z-10">
                  What if we used a local CRDT implementation instead of polling? Could potentially use Yjs synced via WebRTC for local network discovery. Needs more research.
               </p>
               <div className="flex items-center justify-between mt-auto pt-4 border-t border-border/40 relative z-10">
                  <span className="text-xs font-medium text-muted-foreground/60">Added Yesterday</span>
               </div>
            </div>

             {/* Example Card 3: Link/Tool (Emerald Accent) */}
             <div className="group flex flex-col rounded-2xl border border-border/40 bg-card overflow-hidden hover:-translate-y-1 hover:shadow-2xl hover:shadow-[var(--cat-tool)]/5 hover:border-[var(--cat-tool)]/30 transition-all duration-300 cursor-pointer p-5 relative">
               <div className="absolute bottom-0 left-0 w-32 h-32 bg-[var(--cat-tool)]/5 rounded-tr-full blur-2xl pointer-events-none transition-opacity group-hover:opacity-100 opacity-0" />
               <div className="flex items-center justify-between mb-6 relative z-10">
                 <div className="bg-[var(--cat-tool)]/10 text-[var(--cat-tool)] border border-[var(--cat-tool)]/20 px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-widest flex items-center gap-1.5">
                  <LinkIcon className="w-3 h-3" />
                  Tool
                 </div>
                 <ExternalLink className="w-4 h-4 text-muted-foreground group-hover:text-[var(--cat-tool)] transition-colors" />
               </div>
               <div className="flex items-center gap-4 mb-5 relative z-10">
                  <div className="w-12 h-12 rounded-2xl bg-background flex items-center justify-center overflow-hidden border border-border/50 shadow-sm group-hover:shadow-md transition-shadow">
                    <img src="https://www.google.com/s2/favicons?domain=linear.app&sz=64" alt="favicon" className="w-7 h-7" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold leading-snug group-hover:text-[var(--cat-tool)] transition-colors text-foreground/90">
                        Linear App
                    </h3>
                    <span className="text-xs font-medium text-muted-foreground">linear.app</span>
                  </div>
               </div>
               <p className="text-sm text-muted-foreground leading-relaxed mb-4 flex-1 relative z-10">
                  The issue tracking tool you'll actually enjoy using. Unbelievably fast and carefully designed.
               </p>
               <div className="flex items-center justify-between mt-auto pt-4 border-t border-border/40 relative z-10">
                  <span className="text-xs font-medium text-muted-foreground/60">Added 3 days ago</span>
               </div>
            </div>

          </div>
        </section>
      </div>
    </AppShell>
  );
}
