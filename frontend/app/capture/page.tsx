'use client';

import { useEffect, useState, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useCreateItem } from '@/hooks/useItems';

function CaptureLogic() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const createItem = useCreateItem();
  const [status, setStatus] = useState<'saving' | 'success' | 'error'>('saving');
  
  useEffect(() => {
    // Extract shared data from URL parameters
    const sharedUrl = searchParams.get('url') || searchParams.get('text');
    const title = searchParams.get('title');

    // Basic URL validation
    const isValidUrl = (string: string) => {
      try { return Boolean(new URL(string)); }
      catch(e) { return false; }
    };

    if (sharedUrl && isValidUrl(sharedUrl)) {
      createItem.mutate(
        { raw_url: sharedUrl },
        {
          onSuccess: () => {
            setStatus('success');
            // Auto-redirect back to dashboard after 2 seconds
            setTimeout(() => {
              router.push('/');
            }, 2000);
          },
          onError: (error) => {
            console.error("Failed to save item:", error);
            setStatus('error');
          }
        }
      );
    } else {
      setStatus('error');
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams, router]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-background p-6">
      <div className="glass-card p-8 rounded-[24px] max-w-sm w-full text-center space-y-6 relative overflow-hidden shadow-2xl">
        <div className="absolute inset-0 glow-bg opacity-50 z-0 pointer-events-none"></div>
        
        <div className="relative z-10 flex flex-col items-center justify-center space-y-4">
          {status === 'saving' && (
            <>
              <div className="w-16 h-16 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center animate-pulse">
                <span className="material-symbols-outlined text-3xl text-primary animate-spin">sync</span>
              </div>
              <h2 className="text-2xl font-bold font-heading text-foreground">Saving to Vault...</h2>
              <p className="text-sm text-muted-foreground font-mono">Intercepting transmission</p>
            </>
          )}

          {status === 'success' && (
            <>
              <div className="w-16 h-16 rounded-full bg-secondary/20 border border-secondary/30 flex items-center justify-center scale-in-center">
                <span className="material-symbols-outlined text-3xl text-secondary">check_circle</span>
              </div>
              <h2 className="text-2xl font-bold font-heading text-foreground">Saved!</h2>
              <p className="text-sm text-muted-foreground font-mono">Enrichment started in background</p>
            </>
          )}

          {status === 'error' && (
            <>
              <div className="w-16 h-16 rounded-full bg-destructive/20 border border-destructive/30 flex items-center justify-center">
                <span className="material-symbols-outlined text-3xl text-destructive">error</span>
              </div>
              <h2 className="text-2xl font-bold font-heading text-foreground">Failed to Save</h2>
              <p className="text-sm text-muted-foreground">Invalid URL or network error.</p>
              <button 
                onClick={() => router.push('/')}
                className="mt-4 px-6 py-2 bg-muted hover:bg-muted/80 rounded-full text-sm font-medium transition-colors"
              >
                Return to Dashboard
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default function CapturePage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-background flex items-center justify-center">Loading...</div>}>
      <CaptureLogic />
    </Suspense>
  );
}
