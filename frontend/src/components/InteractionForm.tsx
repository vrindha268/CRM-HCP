import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { RootState } from '../store';
import { updateField } from '../features/crm/crmSlice';
import { Mic, Search, Plus, Smile, Meh, Frown, Lock } from 'lucide-react';

const InteractionForm: React.FC = () => {
  const dispatch = useDispatch();
  const formData = useSelector((state: RootState) => state.crm);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    // Disabled manual input as per requirement:
    // dispatch(updateField({ field: e.target.name as any, value: e.target.value }));
  };

  const handleSentimentChange = (sentiment: string) => {
    // Disabled manual input as per requirement
  };

  return (
    <div className="space-y-6 text-sm relative">
      {/* Overlay to indicate it's controlled by AI */}
      <div className="absolute -top-4 right-0 text-xs text-blue-500 font-semibold flex items-center bg-blue-50 px-2 py-1 rounded-full border border-blue-100">
        <Lock className="w-3 h-3 mr-1" /> Form is controlled by AI Assistant
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-gray-700 mb-1 font-medium">HCP Name</label>
          <input
            type="text"
            name="hcp_name"
            value={formData.hcp_name}
            readOnly
            placeholder="Search or select HCP..."
            className="w-full border border-gray-300 rounded px-3 py-2 bg-gray-50 text-gray-600 focus:outline-none cursor-not-allowed"
          />
        </div>
        <div>
          <label className="block text-gray-700 mb-1 font-medium">Interaction Type</label>
          <select
            name="interaction_type"
            value={formData.interaction_type}
            disabled
            className="w-full border border-gray-300 rounded px-3 py-2 bg-gray-50 text-gray-600 focus:outline-none cursor-not-allowed"
          >
            <option>Meeting</option>
            <option>Call</option>
            <option>Email</option>
            <option>Event</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-gray-700 mb-1 font-medium">Date</label>
          <div className="relative">
            <input
              type="date"
              name="interaction_date"
              value={formData.interaction_date}
              readOnly
              className="w-full border border-gray-300 rounded px-3 py-2 bg-gray-50 text-gray-600 focus:outline-none cursor-not-allowed"
            />
          </div>
        </div>
        <div>
          <label className="block text-gray-700 mb-1 font-medium">Time</label>
          <div className="relative">
            <input
              type="time"
              name="interaction_time"
              value={formData.interaction_time}
              readOnly
              className="w-full border border-gray-300 rounded px-3 py-2 bg-gray-50 text-gray-600 focus:outline-none cursor-not-allowed"
            />
          </div>
        </div>
      </div>

      <div>
        <label className="block text-gray-700 mb-1 font-medium">Attendees</label>
        <input
          type="text"
          name="attendees"
          value={formData.attendees}
          readOnly
          placeholder="Enter names or search..."
          className="w-full border border-gray-300 rounded px-3 py-2 bg-gray-50 text-gray-600 focus:outline-none cursor-not-allowed"
        />
      </div>

      <div>
        <label className="block text-gray-700 mb-1 font-medium">Topics Discussed</label>
        <div className="relative">
          <textarea
            name="topics_discussed"
            value={formData.topics_discussed}
            readOnly
            placeholder="Enter key discussion points..."
            className="w-full border border-gray-300 rounded px-3 py-2 h-24 bg-gray-50 text-gray-600 focus:outline-none cursor-not-allowed"
          />
          <Mic className="absolute bottom-3 right-3 text-gray-400 w-5 h-5" />
        </div>
        <button disabled className="mt-2 flex items-center text-sm text-gray-400 bg-gray-100 px-3 py-1.5 rounded border border-gray-200 cursor-not-allowed">
          <Mic className="w-4 h-4 mr-2" /> Summarize from Voice Note (Requires Consent)
        </button>
      </div>

      <div>
        <label className="block text-gray-700 mb-2 font-medium">Materials Shared / Samples Distributed</label>
        <div className="border border-gray-200 rounded p-3 mb-2 flex justify-between items-center bg-gray-50">
          <div>
            <div className="font-medium text-gray-500">Materials Shared</div>
            <div className="text-gray-400 text-xs mt-1">{formData.materials_shared || 'No materials added.'}</div>
          </div>
          <button disabled className="flex items-center px-3 py-1 border border-gray-300 rounded text-gray-400 cursor-not-allowed">
            <Search className="w-4 h-4 mr-1" /> Search/Add
          </button>
        </div>
        <div className="border border-gray-200 rounded p-3 flex justify-between items-center bg-gray-50">
          <div>
            <div className="font-medium text-gray-500">Samples Distributed</div>
            <div className="text-gray-400 text-xs mt-1">{formData.samples_distributed || 'No samples added.'}</div>
          </div>
          <button disabled className="flex items-center px-3 py-1 border border-gray-300 rounded text-gray-400 cursor-not-allowed">
            <Plus className="w-4 h-4 mr-1" /> Add Sample
          </button>
        </div>
      </div>

      <div>
        <label className="block text-gray-700 mb-2 font-medium">Observed/Inferred HCP Sentiment</label>
        <div className="flex space-x-6">
          <label className="flex items-center space-x-2 cursor-not-allowed">
            <input type="radio" name="sentiment" checked={formData.sentiment === 'Positive'} readOnly disabled className="text-blue-500" />
            <Smile className={`w-5 h-5 ${formData.sentiment === 'Positive' ? 'text-green-500' : 'text-gray-400'}`} />
            <span className={formData.sentiment === 'Positive' ? 'font-medium text-gray-600' : 'text-gray-400'}>Positive</span>
          </label>
          <label className="flex items-center space-x-2 cursor-not-allowed">
            <input type="radio" name="sentiment" checked={formData.sentiment === 'Neutral'} readOnly disabled className="text-blue-500" />
            <Meh className={`w-5 h-5 ${formData.sentiment === 'Neutral' ? 'text-blue-500' : 'text-gray-400'}`} />
            <span className={formData.sentiment === 'Neutral' ? 'font-medium text-blue-600' : 'text-gray-400'}>Neutral</span>
          </label>
          <label className="flex items-center space-x-2 cursor-not-allowed">
            <input type="radio" name="sentiment" checked={formData.sentiment === 'Negative'} readOnly disabled className="text-blue-500" />
            <Frown className={`w-5 h-5 ${formData.sentiment === 'Negative' ? 'text-red-500' : 'text-gray-400'}`} />
            <span className={formData.sentiment === 'Negative' ? 'font-medium text-gray-600' : 'text-gray-400'}>Negative</span>
          </label>
        </div>
      </div>

      <div>
        <label className="block text-gray-700 mb-1 font-medium">Outcomes</label>
        <textarea
          name="outcomes"
          value={formData.outcomes}
          readOnly
          placeholder="Key outcomes or agreements..."
          className="w-full border border-gray-300 rounded px-3 py-2 h-20 bg-gray-50 text-gray-600 focus:outline-none cursor-not-allowed"
        />
      </div>

      <div>
        <label className="block text-gray-700 mb-1 font-medium">Follow-up Actions</label>
        <textarea
          name="follow_up_actions"
          value={formData.follow_up_actions}
          readOnly
          placeholder="Enter next steps or tasks..."
          className="w-full border border-gray-300 rounded px-3 py-2 h-20 bg-gray-50 text-gray-600 focus:outline-none cursor-not-allowed"
        />
        {formData.follow_up_actions && (
          <div className="mt-2 text-xs">
            <div className="text-gray-500 mb-1 font-medium">AI Suggested Follow-ups:</div>
            <ul className="text-blue-400 space-y-1">
              <li className="cursor-not-allowed opacity-75">+ Schedule follow-up meeting in 2 weeks</li>
              <li className="cursor-not-allowed opacity-75">+ Send OncoBoost Phase III PDF</li>
              <li className="cursor-not-allowed opacity-75">+ Add Dr. to advisory board invite list</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default InteractionForm;
