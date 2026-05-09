import { Search, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function Topbar() {
  return (
    <header className="h-16 border-b border-border/40 bg-background/80 backdrop-blur-md flex items-center justify-between px-6 sticky top-0 z-20">
      <div className="flex-1 flex items-center">
        <div className="relative w-full max-w-md flex items-center group">
          <Search className="w-4 h-4 absolute left-3.5 text-muted-foreground group-focus-within:text-primary transition-colors" />
          <input
            type="text"
            placeholder="Search your vault..."
            className="w-full bg-accent/40 border border-transparent hover:border-border/60 focus:border-primary/30 focus:bg-background focus:ring-4 focus:ring-primary/10 transition-all outline-none rounded-full py-2 pl-10 pr-4 text-sm font-medium placeholder:text-muted-foreground/70"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        {/* Placeholder for Quick Save Button */}
        <Button size="sm" className="rounded-full shadow-md shadow-primary/20 hover:shadow-lg transition-all px-4 font-semibold">
          <Plus className="w-4 h-4 mr-1.5" />
          Quick Save
        </Button>
      </div>
    </header>
  );
}

