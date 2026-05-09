import React from "react";
import { ItemResponse } from "@/types/item";

interface ContentCardProps {
  item: ItemResponse;
}

export function ContentCard({ item }: ContentCardProps) {
  // Use abstract images if thumbnail is missing for the design aesthetic
  const imageUrl = item.thumbnail || "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop";
  const title = item.title || item.raw_url;
  const description = item.description || "Exploring why local-first software is the new standard for privacy and performance in the modern era...";
  
  // Icon mapping based on type
  const getTypeIcon = (type: string) => {
    switch(type) {
      case 'tool': return 'build';
      case 'video': return 'play_circle';
      case 'article': return 'article';
      default: return 'link';
    }
  };

  return (
    <article className="glass-card w-full max-w-[400px] rounded-[16px] overflow-hidden transition-all duration-300 group hover:-translate-y-1 relative">
      {/* Thumbnail Section */}
      <div className="relative h-56 w-full overflow-hidden bg-muted/20">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img 
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" 
          alt={title} 
          src={imageUrl} 
        />
        {/* Inner Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-background/90 to-transparent"></div>
      </div>
      
      {/* Content Section */}
      <div className="p-6 space-y-4 relative z-10">
        <h2 className="text-xl font-semibold text-foreground leading-tight line-clamp-2 font-heading">
          {title}
        </h2>
        <p className="text-muted-foreground line-clamp-2 text-sm">
          {description}
        </p>
        
        {/* Metadata Badges */}
        <div className="flex flex-wrap gap-2 pt-2">
          {/* Source Badge */}
          {item.source && (
            <div className="flex items-center gap-1.5 px-3 py-1 bg-secondary/10 rounded-full border border-secondary/20">
              <span className="material-symbols-outlined text-[14px] text-secondary">public</span>
              <span className="text-xs font-medium text-secondary">{item.source}</span>
            </div>
          )}
          
          {/* Type Badge */}
          <div className="flex items-center gap-1.5 px-3 py-1 bg-white/5 rounded-full border border-white/10">
            <span className="material-symbols-outlined text-[14px] text-muted-foreground">{getTypeIcon(item.item_type)}</span>
            <span className="text-xs font-medium text-muted-foreground capitalize">{item.item_type}</span>
          </div>

          {/* Processing Status Indicator (Optional for debug/feedback) */}
          {item.processing_status === 'pending' && (
            <div className="flex items-center gap-1.5 px-3 py-1 bg-primary/10 rounded-full border border-primary/20">
              <span className="material-symbols-outlined text-[14px] text-primary animate-spin">sync</span>
              <span className="text-xs font-medium text-primary">Processing</span>
            </div>
          )}
        </div>
      </div>

      {/* Interactive Glow Element */}
      <div className="absolute -bottom-10 -right-10 w-32 h-32 bg-primary/20 blur-[40px] rounded-full opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-0"></div>
    </article>
  );
}
