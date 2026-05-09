import { AppShell } from '@/components/layout/app-shell';
import { ContentCard } from '@/components/ui/content-card';
import { useItems } from '@/hooks/useItems';

export default function Home() {
  const { data: items, isLoading } = useItems();

  return (
    <AppShell>
      <div className="space-y-12 pb-12">
        {/* Engaging Hero Section */}
        <section className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-primary/5 via-background to-background p-8 sm:p-12 border border-border/40 shadow-sm">
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
                {items ? items.length : 0} Saved Items
              </span>
            </div>
          </div>
        </section>
        
        {/* Rich Content Grid */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold tracking-tight text-foreground/90">Recently Added</h2>
          </div>
          
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-64 rounded-[16px] bg-muted/20 animate-pulse border border-border/40"></div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center sm:justify-items-start">
              {items?.map((item: any) => (
                <ContentCard key={item.id} item={item} />
              ))}
              {(!items || items.length === 0) && (
                <div className="col-span-full py-12 text-center text-muted-foreground">
                  Your vault is empty. Start saving items!
                </div>
              )}
            </div>
          )}
        </section>
      </div>
    </AppShell>
  );
}
