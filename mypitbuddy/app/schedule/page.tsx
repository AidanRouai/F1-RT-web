import Image from "next/image";
import Link from "next/link";

interface Race {
  round: number;
  raceName: string;
  circuitName: string;
  date: string;
  time: string;
  country: string;
  flagUrl: string;
}

async function getRaceSchedule(): Promise<Race[]> {
  const res = await fetch('http://localhost:8000/api/schedule');
  if (!res.ok) {
    throw new Error('Failed to fetch schedule');
  }
  return res.json();
}

export default async function Schedule() {
  const races = await getRaceSchedule();
  const today = new Date();
  
  // Find the next race
  const nextRace = races.find(race => new Date(`${race.date}T${race.time}`) > today);
  const nextRaceIndex = nextRace ? races.indexOf(nextRace) : 0;

  return (
    <div className="bg-[#15151e] text-white min-h-screen p-8 pb-20 sm:p-20">
      <main className="max-w-7xl mx-auto">
        <Link 
          href="/" 
          className="text-[#e10600] mb-8 inline-block hover:text-[#b30500]"
        >
          ← Back to Home
        </Link>

        <h1 className="text-4xl font-bold mb-12">2024 Race Calendar</h1>

        {/* Next Race Highlight */}
        {nextRace && (
          <div className="mb-16">
            <h2 className="text-2xl font-bold mb-4">Next Race</h2>
            <div className="bg-[#1f1f2b] p-6 rounded-lg">
              <div className="flex items-center gap-4">
                <Image
                  src={nextRace.flagUrl}
                  alt={`${nextRace.country} flag`}
                  width={60}
                  height={40}
                  className="rounded"
                />
                <div>
                  <h3 className="text-xl font-bold">{nextRace.raceName}</h3>
                  <p className="text-gray-400">{nextRace.circuitName}</p>
                  <p className="text-[#e10600]">
                    {new Date(`${nextRace.date}T${nextRace.time}`).toLocaleDateString('en-US', {
                      weekday: 'long',
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Race Timeline */}
        <div className="relative">
          <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-[#e10600]" />
          <div className="flex gap-8 overflow-x-auto pb-8 relative">
            {races.map((race, index) => {
              const raceDate = new Date(`${race.date}T${race.time}`);
              const isPast = raceDate < today;
              const isNext = index === nextRaceIndex;

              return (
                <div 
                  key={race.round}
                  className={`flex-shrink-0 w-64 ${
                    isPast ? 'opacity-60' : ''
                  } ${isNext ? 'scale-110 z-10' : ''}`}
                >
                  <div className={`
                    bg-[#1f1f2b] p-4 rounded-lg transition-all
                    ${isNext ? 'border-2 border-[#e10600]' : ''}
                  `}>
                    <div className="flex items-center gap-3 mb-3">
                      <Image
                        src={race.flagUrl}
                        alt={`${race.country} flag`}
                        width={40}
                        height={30}
                        className="rounded"
                      />
                      <span className="font-bold">Round {race.round}</span>
                    </div>
                    <h3 className="font-bold mb-1">{race.raceName}</h3>
                    <p className="text-sm text-gray-400 mb-2">{race.circuitName}</p>
                    <p className="text-sm text-[#e10600]">
                      {raceDate.toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                      })}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </main>
    </div>
  );
} 