import Link from "next/link";

export default function Home() {
  return (
    <div className="bg-[#15151e] text-white min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-8 items-center max-w-4xl mx-auto">
      <div className="text-center">
          <h1 className="text-[#e10600] text-6xl font- font-bold mb-4">MyPitBuddy</h1>
          <p className="text-xl font- text-gray-300">Your Ultimate F1 Racing Companion</p>
        </div>

        <div 
        className="grid grid-cols-1 sm:grid-cols-2 gap-6 w-full mt-8">
          <Link 
          href="/racecalendar"
          className="bg-[#1f1f2b] p-6 rounded-lg hover:scale-105 transition-transform">
            <h2 className="text-2xl font-bold mb-4">Race Calendar</h2>
            <p className="text-gray-300">Stay updated with upcoming races and schedules</p>
          </Link>

          <Link 
          href="/livetiming"
          className="bg-[#1f1f2b] p-6 rounded-lg hover:scale-105 transition-transform">
            <h2 className="text-2xl font-bold mb-4">Live Timing</h2>
            <p className="text-gray-300">Real-time race positions and lap times</p>
          </Link>

          <Link
            href="/standings"
            className="bg-[#1f1f2b] p-6 rounded-lg hover:scale-105 transition-transform"
          >
            <h2 className="text-2xl font-bold mb-4">Team Standings</h2>
            <p className="text-gray-300">Current constructor and driver championships</p>
          </Link>

          <Link
            href="/pastresults"
            className="bg-[#1f1f2b] p-6 rounded-lg hover:scale-105 transition-transform"
          >
            <h2 className="text-2xl font-bold mb-4"> Past Results</h2>
            <p className="text-gray-300">Past results from previous races</p>
          </Link>
        </div>
      </main>

      <footer className="mt-20 text-center text-gray-400">
        <p>Data and statistics powered by the OpenF1 API.</p>
      </footer>
    </div>
  );
}
