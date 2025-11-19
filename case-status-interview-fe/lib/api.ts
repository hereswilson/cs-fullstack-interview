// lib/api.ts
import type { Client, ImportClientPayload } from "./definitions";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export async function fetchClients(): Promise<Client[]> {
  const response = await fetch(`${API_BASE_URL}/clients`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch clients");
  }

  const data = await response.json();

  if (data.clients && Array.isArray(data.clients)) {
    return data.clients;
  }

  console.error("Invalid API response format. Expected { clients: [] } or array.", data);
  return [];
}

export async function importClient(
  payload: ImportClientPayload
): Promise<Client> {
  const response = await fetch(`${API_BASE_URL}/clients`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.errors?.[0]?.message || "Failed to import client");
  }

  const data = await response.json();
  
  if (data.client) {
    return data.client;
  }

  return data;
}