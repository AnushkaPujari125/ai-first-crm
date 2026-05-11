import React, { useState } from "react";

const ChatPanel = () => {

  const [message, setMessage] = useState("");

  const [chat, setChat] = useState([]);

  const sendMessage = () => {

    if(!message) return;

    setChat([
      ...chat,
      {
        role:"user",
        text:message
      },
      {
        role:"ai",
        text:"Interaction logged successfully ✅"
      }
    ]);

    setMessage("");
  };

  return (

    <div style={styles.container}>

      <h2 style={styles.title}>🤖 AI Assistant</h2>

      <div style={styles.chatBox}>

        {chat.map((c,i)=>(

          <div
            key={i}
            style={
              c.role === "user"
              ? styles.user
              : styles.ai
            }
          >
            {c.text}
          </div>

        ))}

      </div>

      <div style={styles.inputArea}>

        <input
          style={styles.input}
          value={message}
          onChange={(e)=>setMessage(e.target.value)}
          placeholder="Describe interaction..."
        />

        <button
          style={styles.button}
          onClick={sendMessage}
        >
          Send
        </button>

      </div>

    </div>

  );
};

const styles = {

  container:{
    width:"45%",
    background:"#fff",
    borderRadius:"16px",
    padding:"20px",
    boxShadow:"0 4px 12px rgba(0,0,0,0.08)",
    display:"flex",
    flexDirection:"column"
  },

  title:{
    marginBottom:"14px"
  },

  chatBox:{
    flex:1,
    overflowY:"auto",
    border:"1px solid #e2e8f0",
    borderRadius:"10px",
    padding:"14px",
    background:"#f8fafc"
  },

  user:{
    background:"#dcfce7",
    padding:"12px",
    borderRadius:"10px",
    marginBottom:"10px",
    textAlign:"right"
  },

  ai:{
    background:"#e2e8f0",
    padding:"12px",
    borderRadius:"10px",
    marginBottom:"10px"
  },

  inputArea:{
    display:"flex",
    gap:"10px",
    marginTop:"15px"
  },

  input:{
    flex:1,
    padding:"12px",
    borderRadius:"10px",
    border:"1px solid #cbd5e1"
  },

  button:{
    background:"#2563eb",
    color:"#fff",
    border:"none",
    padding:"12px 18px",
    borderRadius:"10px",
    cursor:"pointer"
  }

};

export default ChatPanel;