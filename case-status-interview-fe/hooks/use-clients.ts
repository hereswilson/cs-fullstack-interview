import { useState, useCallback } from "react";
import { fetchClients, importClient } from "@/lib/api";
import type { Client, ClientFormData, ImportClientPayload } from "@/lib/definitions";

export function useClients(initialClients: Client[]) {
  const [clients, setClients] = useState<Client[]>(initialClients);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const data = await fetchClients();
      setClients(data);
      setError(null);
    } catch (err) {
      setError("Failed to refresh list");
    }
  }, []);

  const saveClient = async (formData: ClientFormData, editingId?: number) => {
    setIsSaving(true);
    setError(null);

    const previousClients = [...clients];

    const tempId = editingId || -Date.now(); // Negative ID for temp items
    const optimisticClient: Client = {
      id: tempId,
      firm_id: 1,
      ...formData,
      birth_date: formData.birth_date || "",
      ssn: formData.ssn || "",
    };

    setClients((prev) => {
      if (editingId) {
        return prev.map((c) => (c.id === editingId ? optimisticClient : c));
      }
      return [...prev, optimisticClient];
    });

    try {
      const payload: ImportClientPayload = {
        firm_id: 1,
        field_names: {
          first_name: formData.first_name,
          last_name: formData.last_name,
          email: formData.email,
          phone_numbers: [formData.cell_phone],
          integration_id: formData.integration_id,
          ...(formData.birth_date && { birth_date: formData.birth_date }),
          ...(formData.ssn && { ssn: formData.ssn }),
        },
        integration_type: "CSV_IMPORT",
      };

      const savedClient = await importClient(payload);

      setClients((prev) =>
        prev.map((c) => (c.id === tempId ? savedClient : c))
      );
    } catch (err) {
      setClients(previousClients);
      setError(err instanceof Error ? err.message : "Failed to save client");
      throw err;
    } finally {
      setIsSaving(false);
    }
  };

  return { clients, refresh, saveClient, isSaving, error };
}