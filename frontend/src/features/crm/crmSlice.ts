import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

interface CRMState {
  hcp_name: string;
  interaction_type: string;
  interaction_date: string;
  interaction_time: string;
  attendees: string;
  topics_discussed: string;
  materials_shared: string;
  samples_distributed: string;
  sentiment: string;
  outcomes: string;
  follow_up_actions: string;
}

const initialState: CRMState = {
  hcp_name: '',
  interaction_type: 'Meeting',
  interaction_date: '',
  interaction_time: '',
  attendees: '',
  topics_discussed: '',
  materials_shared: '',
  samples_distributed: '',
  sentiment: 'Neutral',
  outcomes: '',
  follow_up_actions: '',
};

const crmSlice = createSlice({
  name: 'crm',
  initialState,
  reducers: {
    updateField: (state, action: PayloadAction<{ field: keyof CRMState; value: string }>) => {
      state[action.payload.field] = action.payload.value;
    },
    updateFromExtraction: (state, action: PayloadAction<Partial<CRMState>>) => {
      Object.keys(action.payload).forEach((key) => {
        const value = action.payload[key as keyof CRMState];
        if (value) {
          state[key as keyof CRMState] = value;
        }
      });
    },
    resetForm: () => initialState,
  },
});

export const { updateField, updateFromExtraction, resetForm } = crmSlice.actions;
export default crmSlice.reducer;
