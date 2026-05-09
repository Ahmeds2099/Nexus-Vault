export type ItemType = 'article' | 'video' | 'tool' | 'note' | 'link' | 'pdf';
export type ProcessingStatus = 'pending' | 'completed' | 'failed';

export interface Item {
  id: string;
  raw_url: string | null;
  title: string | null;
  description: string | null;
  thumbnail: string | null;
  source: string | null;
  item_type: ItemType;
  category: string; // User folder (Read Later, Important, etc.)
  is_read: boolean;
  metadata_json: Record<string, any> | null;
  processing_status: ProcessingStatus;
  created_at: string;
  updated_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error: string | null;
}

export interface ItemListResponse extends ApiResponse<Item[]> {
  total: number;
}

