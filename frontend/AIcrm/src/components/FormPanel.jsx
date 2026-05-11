import React from "react";

const FormPanel = () => {
  return (
    <div style={styles.container}>

      <h1 style={styles.title}>📋 Log HCP Interaction</h1>

      <div style={styles.row}>
        <input style={styles.input} placeholder="HCP Name" />

        <select style={styles.select}>
          <option>Meeting</option>
          <option>Call</option>
          <option>Email</option>
        </select>
      </div>

      <div style={styles.row}>
        <input style={styles.input} placeholder="Date" />
        <input style={styles.input} placeholder="Time" />
      </div>

      <input style={styles.fullInput} placeholder="Attendees" />

      <textarea
        style={styles.textarea}
        placeholder="Topics Discussed"
      />

      <input
        style={styles.fullInput}
        placeholder="Materials Shared"
      />

      <input
        style={styles.fullInput}
        placeholder="Sentiment"
      />

      <textarea
        style={styles.textarea}
        placeholder="Outcome"
      />

    </div>
  );
};

const styles = {

  container:{
    width:"55%",
    background:"#fff",
    borderRadius:"16px",
    padding:"20px",
    boxShadow:"0 4px 12px rgba(0,0,0,0.08)",
    display:"flex",
    flexDirection:"column",
    gap:"14px"
  },

  title:{
    fontSize:"28px",
    fontWeight:"bold"
  },

  row:{
    display:"flex",
    gap:"12px"
  },

  input:{
    flex:1,
    padding:"14px",
    border:"1px solid #dbe3ef",
    borderRadius:"10px",
    fontSize:"14px"
  },

  select:{
    width:"180px",
    padding:"14px",
    border:"1px solid #dbe3ef",
    borderRadius:"10px"
  },

  fullInput:{
    width:"100%",
    padding:"14px",
    border:"1px solid #dbe3ef",
    borderRadius:"10px"
  },

  textarea:{
    width:"100%",
    minHeight:"100px",
    padding:"14px",
    border:"1px solid #dbe3ef",
    borderRadius:"10px",
    resize:"none"
  }

};

export default FormPanel;