"use client";

import { type Client } from "@/lib/definitions";
import { useState, useMemo } from "react";
import { ChevronUpIcon, ChevronDownIcon } from "@heroicons/react/24/solid";

type SortField = keyof Client;
type SortDirection = "asc" | "desc";

interface ClientTableProps {
  clients: Client[];
  onEdit: (client: Client) => void;
}

export function ClientTable({ clients = [], onEdit }: ClientTableProps) {
  const [sortField, setSortField] = useState<SortField>("id");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const sortedClients = useMemo(() => {
    const safeClients = clients || [];
    return [...safeClients].sort((a, b) => {
      const aVal = a[sortField];
      const bVal = b[sortField];

      if (aVal < bVal) return sortDirection === "asc" ? -1 : 1;
      if (aVal > bVal) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }, [clients, sortField, sortDirection]);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) return null;
    return sortDirection === "asc" ? (
      <ChevronUpIcon className="w-4 h-4" />
    ) : (
      <ChevronDownIcon className="w-4 h-4" />
    );
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {[
              { key: "id", label: "ID" },
              { key: "first_name", label: "First Name" },
              { key: "last_name", label: "Last Name" },
              { key: "email", label: "Email" },
              { key: "cell_phone", label: "Phone" },
              { key: "integration_id", label: "Integration ID" },
            ].map(({ key, label }) => (
              <th
                key={key}
                onClick={() => handleSort(key as SortField)}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 select-none"
              >
                <div className="flex items-center gap-1">
                  {label}
                  <SortIcon field={key as SortField} />
                </div>
              </th>
            ))}
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {sortedClients.map((client, index) => (
            <tr
              key={client.id != null ? client.id : `client-row-${index}`}
              className="hover:bg-gray-50"
            >
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {client.id}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {client.first_name}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {client.last_name}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {client.email}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {client.cell_phone}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {client.integration_id}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm">
                <button
                  onClick={() => onEdit(client)}
                  className="text-indigo-600 hover:text-indigo-900"
                >
                  Edit
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}