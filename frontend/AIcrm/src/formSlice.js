import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  hcp_name: "",
  interaction_type: "Meeting",
  date: "",
  time: "",
  attendees: "",
  topics: "",
  materials: "",
  sentiment: "",
  outcome: ""
};

const formSlice = createSlice({
  name: "form",

  initialState,

  reducers: {

    setFormData: (state, action) => {

      state.hcp_name = action.payload.hcp_name || "";
      state.interaction_type =
        action.payload.interaction_type || "Meeting";
      state.date = action.payload.date || "";
      state.time = action.payload.time || "";
      state.attendees = action.payload.attendees || "";
      state.topics = action.payload.topics || "";
      state.materials = action.payload.materials || "";
      state.sentiment = action.payload.sentiment || "";
      state.outcome = action.payload.outcome || "";
    }

  }
});

export const { setFormData } = formSlice.actions;

export default formSlice.reducer;