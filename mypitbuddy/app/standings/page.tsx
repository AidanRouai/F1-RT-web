import Link from "next/link";

export default function Standings() {
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
              {/* Replace with actual data from API */}
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20].map((pos) => (
                <div 
                  key={pos} 
                  className="flex items-center justify-between p-4 bg-[#15151e] rounded"
                >
                  <div className="flex items-center gap-4">
                    <span className="text-[#e10600] font-bold">{pos}</span>
                    <span>Driver Name</span>
                  </div>
                  <span className="font-bold">000 pts</span>
                </div>
              ))}
            </div>
          </div>

          {/* Constructors Championship */}
          <div className="bg-[#1f1f2b] p-6 rounded-lg">
            <h2 className="text-2xl font-bold mb-6">Constructors Championship</h2>
            <div className="space-y-4">
              {/* Replace with actual data from API */}
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((pos) => (
                <div 
                  key={pos} 
                  className="flex items-center justify-between p-4 bg-[#15151e] rounded"
                >
                  <div className="flex items-center gap-4">
                    <span className="text-[#e10600] font-bold">{pos}</span>
                    <span>Team Name</span>
                  </div>
                  <span className="font-bold">000 pts</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
} 