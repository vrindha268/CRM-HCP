
import LogInteractionScreen from './components/LogInteractionScreen';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-semibold mb-6 text-gray-800">Log HCP Interaction</h1>
        <LogInteractionScreen />
      </div>
    </div>
  );
}

export default App;
