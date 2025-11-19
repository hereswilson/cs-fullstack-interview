"use client";
import { useState, useEffect } from "react";
import type { Client, ClientFormData } from "@/lib/definitions";

interface ClientFormProps {
  initialData?: Client | null;
  onSubmit: (data: ClientFormData) => Promise<void>;
  onCancel: () => void;
  isSubmitting: boolean;
}

export function ClientForm({ initialData, onSubmit, onCancel, isSubmitting }: ClientFormProps) {
  const [formData, setFormData] = useState<ClientFormData>({
    first_name: "", last_name: "", email: "", cell_phone: "", integration_id: "", birth_date: "", ssn: ""
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        first_name: initialData.first_name,
        last_name: initialData.last_name,
        email: initialData.email,
        cell_phone: initialData.cell_phone,
        integration_id: initialData.integration_id,
        birth_date: initialData.birth_date || "",
        ssn: initialData.ssn || "",
      });
    } else {
      setFormData({ first_name: "", last_name: "", email: "", cell_phone: "", integration_id: "", birth_date: "", ssn: "" });
    }
  }, [initialData]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSubmit(formData); }} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <Input name="first_name" label="First Name" value={formData.first_name} onChange={handleChange} required />
        <Input name="last_name" label="Last Name" value={formData.last_name} onChange={handleChange} required />
      </div>
      <Input name="email" label="Email" type="email" value={formData.email} onChange={handleChange} required />
      <Input name="cell_phone" label="Cell Phone" type="tel" value={formData.cell_phone} onChange={handleChange} required />
      <Input name="integration_id" label="Integration ID" value={formData.integration_id} onChange={handleChange} required />
      
      <div className="grid grid-cols-2 gap-4">
        <Input name="birth_date" label="Birth Date" type="date" value={formData.birth_date} onChange={handleChange} />
        <Input name="ssn" label="SSN" value={formData.ssn} onChange={handleChange} placeholder="XXX-XX-XXXX" />
      </div>

      <div className="flex justify-end gap-3 mt-6">
        <button type="button" onClick={onCancel} className="px-4 py-2 text-sm border rounded-md text-black hover:bg-gray-50" disabled={isSubmitting}>
          Cancel
        </button>
        <button type="submit" disabled={isSubmitting} className="px-4 py-2 text-sm text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50">
          {isSubmitting ? "Saving..." : "Save Client"}
        </button>
      </div>
    </form>
  );
}

function Input({ label, ...props }: any) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
      <input className="block w-full rounded-md border-gray-300 shadow-sm border px-3 py-2 sm:text-sm" {...props} />
    </div>
  );
}