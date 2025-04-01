import React, { useState } from "react";

interface Message {
  user: string;
  bot: string;
}

function Chatbox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { user: input, bot: "" }]);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      setMessages((prev) =>
        prev.map((msg, index) =>
          index === prev.length - 1 ? { ...msg, bot: data.response } : msg
        )
      );

      if (input.toLowerCase().startsWith("define")) {
        await fetch("http://127.0.0.1:5000/api/train", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: input }),
        });
      }
    } catch (error) {
      console.error("Error fetching bot response:", error);
    }

    setInput("");
  };

  return (
    <div>
      <div className="chatbox">
        {messages.map((msg, index) => (
          <div key={index}>
            <p>
              <strong>User:</strong> {msg.user}
            </p>
            <p>
              <strong>Bot:</strong> {msg.bot}
            </p>
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chatbox;
