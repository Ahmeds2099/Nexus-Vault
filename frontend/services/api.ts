import { ApiResponse, Item, ItemListResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  const data = await response.json();

  if (!response.ok || data.success === false) {
    throw new Error(data.error || 'API request failed');
  }

  return data;
}

export const itemsApi = {
  getAll: async (params?: { 
    category?: string; 
    item_type?: string; 
    is_read?: boolean;
    processing_status?: string;
  }) => {
    const searchParams = new URLSearchParams();
    if (params?.category) searchParams.append('category', params.category);
    if (params?.item_type) searchParams.append('item_type', params.item_type);
    if (params?.processing_status) searchParams.append('processing_status', params.processing_status);
    if (params?.is_read !== undefined) searchParams.append('is_read', String(params.is_read));
    
    const query = searchParams.toString() ? `?${searchParams.toString()}` : '';
    return fetchApi<ItemListResponse>(`/items${query}`);
  },

  getById: async (id: string) => {
    return fetchApi<ApiResponse<Item>>(`/items/${id}`);
  },

  create: async (payload: Partial<Item>) => {
    return fetchApi<ApiResponse<Item>>('/items/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  update: async (id: string, payload: Partial<Item>) => {
    return fetchApi<ApiResponse<Item>>(`/items/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    });
  },

  delete: async (id: string) => {
    return fetchApi<ApiResponse<{ message: string }>>(`/items/${id}`, {
      method: 'DELETE',
    });
  },
};
