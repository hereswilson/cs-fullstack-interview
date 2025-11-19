// app/page.tsx
import { ClientManager } from "@/components/client-manager";
import { fetchClients } from "@/lib/api";

export default async function Home() {
  const clients = await fetchClients();

  return (
    <div className="flex flex-col w-full">
      <ClientManager initialClients={clients} />
    </div>
  );
}