import Link from "next/link";

interface Driver {
  position: number;
  driver_number: string;
  full_name: string;
  points: number;
}

interface Constructor {
  position: number;
  name: string;
  points: number;
}

async function getDrivers(): Promise<Driver[]> {
  const res = await fetch('http://localhost:8000/api/standings');
  if (!res.ok) {
    throw new Error('Failed to fetch standings');
  }
  return res.json();
}

async function getConstructors(): Promise<Constructor[]> {
  const res = await fetch('http://localhost:8000/api/standings/constructors');
  if (!res.ok) {
    throw new Error('Failed to fetch constructor standings');
  }
  return res.json();
}

export default async function Standings() {
  const [drivers, constructors] = await Promise.all([
    getDrivers(),
    getConstructors()
  ]);

  return (
    <div className="bg-[#15151e] text-white min-h-screen p-8 pb-20 sm:p-20">
      <main className="max-w-6xl mx-auto">
        <Link 
          href="/" 
          className="text-[#e10600] mb-8 inline-block hover:text-[#b30500]"
        >
          ← Back to Home
        </Link>

        <h1 className="text-4xl font-bold mb-12">Championship Standings</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          {/* Drivers Championship */}
          <div className="bg-[#1f1f2b] p-6 rounded-lg">
            <h2 className="text-2xl font-bold mb-6">Drivers Championship</h2>
            <div className="space-y-4">
              {drivers.map((driver) => (
                <div 
                  key={driver.driver_number} 
                  className="flex items-center justify-between p-4 bg-[#15151e] rounded"
                >
                  <div className="flex items-center gap-4">
                    <span className="text-[#e10600] font-bold">{driver.position}</span>
                    <span>{driver.full_name}</span>
                  </div>
                  <span className="font-bold">{driver.points} pts</span>
                </div>
              ))}
            </div>
          </div>

          {/* Constructors Championship */}
          <div className="bg-[#1f1f2b] p-6 rounded-lg">
            <h2 className="text-2xl font-bold mb-6">Constructors Championship</h2>
            <div className="space-y-4">
              {constructors.map((constructor) => (
                <div 
                  key={constructor.name} 
                  className="flex items-center justify-between p-4 bg-[#15151e] rounded"
                >
                  <div className="flex items-center gap-4">
                    <span className="text-[#e10600] font-bold">{constructor.position}</span>
                    <span>{constructor.name}</span>
                  </div>
                  <span className="font-bold">{constructor.points} pts</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
} 