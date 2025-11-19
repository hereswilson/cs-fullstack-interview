"use client";

import { useState } from "react";
import { ClientTable } from "./client-table";
import { ClientForm } from "./client-form";
import { Modal } from "./ui/modal";
import { useClients } from "../hooks/use-clients"; 
import type { Client, ClientFormData } from "@/lib/definitions";

export function ClientManager({ initialClients }: { initialClients: Client[] }) {
  const { clients, refresh, saveClient, isSaving, error } = useClients(initialClients);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingClient, setEditingClient] = useState<Client | null>(null);

  const handleEdit = (client: Client) => {
    setEditingClient(client);
    setIsModalOpen(true);
  };

  const handleClose = () => {
    setIsModalOpen(false);
    setTimeout(() => {
      setEditingClient(null);
    }, 300);
  };

  const handleSubmit = async (formData: ClientFormData) => {
    try {
      await saveClient(formData, editingClient?.id);
      handleClose();
    } catch (e) {

    }
  };

  return (
    <div className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Clients</h1>
        <div className="flex gap-2">
          <button onClick={refresh} className="px-4 py-2 text-sm border rounded-md hover:bg-gray-50 hover:text-black">
            Refresh
          </button>
          <button onClick={() => setIsModalOpen(true)} className="px-4 py-2 text-sm text-white bg-indigo-600 rounded-md hover:bg-indigo-700">
            Add Client
          </button>
        </div>
      </div>
      <ClientTable clients={clients} onEdit={handleEdit} />

      <Modal
        isOpen={isModalOpen}
        onClose={handleClose}
        title={editingClient ? "Edit Client" : "Add New Client"}
      >
        <ClientForm
          initialData={editingClient}
          onSubmit={handleSubmit}
          onCancel={handleClose}
          isSubmitting={isSaving}
        />
      </Modal>
    </div>
  );
}