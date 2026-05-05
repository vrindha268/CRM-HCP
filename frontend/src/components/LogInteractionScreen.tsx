import React from 'react';
import InteractionForm from './InteractionForm';
import ChatAssistant from './ChatAssistant';

const LogInteractionScreen: React.FC = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[85vh]">
      <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-gray-200 overflow-y-auto">
        <div className="p-4 border-b border-gray-100 font-semibold text-gray-700">
          Interaction Details
        </div>
        <div className="p-6">
          <InteractionForm />
        </div>
      </div>
      <div className="lg:col-span-1 bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col overflow-hidden">
        <div className="p-4 border-b border-gray-100 flex items-center space-x-2">
          <span className="text-blue-500 font-bold text-xl">🤖</span>
          <div>
            <h2 className="font-semibold text-gray-800">AI Assistant</h2>
            <p className="text-xs text-gray-500">Log interaction via chat</p>
          </div>
        </div>
        <div className="flex-grow overflow-hidden">
          <ChatAssistant />
        </div>
      </div>
    </div>
  );
};

export default LogInteractionScreen;
