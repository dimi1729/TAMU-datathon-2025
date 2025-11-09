"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, Loader2 } from "lucide-react";
import axios from "axios";
import ChatMessage from "@/components/ChatMessage";

interface Message {
  id: string;
  text: string;
  sender: "user" | "bot";
  timestamp: string;
  calendarUrl?: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

  useEffect(() => {
    setIsMounted(true);
    setMessages([
      {
        id: "welcome",
        text: "Hello! I'm your college assistant. I can help you with sports, dining, housing, events, academics, and more. What would you like to know?",
        sender: "bot",
        timestamp: new Date().toISOString(),
      },
    ]);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isMounted && messages.length > 0) {
      scrollToBottom();
    }
  }, [messages, isMounted]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      text: inputMessage,
      sender: "user",
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const currentMessage = inputMessage;
    setInputMessage("");
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/chat`, {
        message: currentMessage,
      });

      const botMessage: Message = {
        id: `bot-${Date.now()}`,
        text: response.data.response,
        sender: "bot",
        timestamp: response.data.timestamp || new Date().toISOString(),
        calendarUrl: response.data.calendar_url,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        text: `Sorry, I'm having trouble connecting to the server. Please make sure the backend is running on ${API_URL}`,
        sender: "bot",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickQuestion = (question: string) => {
    setInputMessage(question);
  };

  if (!isMounted) {
    return (
      <div className="w-full h-full bg-dark-purple rounded-lg shadow-xl overflow-hidden border border-dark-magenta flex flex-col">
        <div className="bg-dark-base text-white p-4">
          <h2 className="text-xl font-semibold">
            Chat with your College Assistant
          </h2>
          <p className="text-dark-accent text-sm">
            Ask about sports, dining, housing, events, and academics
          </p>
        </div>
        <div className="flex-1 flex items-center justify-center bg-dark-purple">
          <div className="text-dark-accent">Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-full bg-dark-purple rounded-lg shadow-xl overflow-hidden border border-dark-magenta flex flex-col relative">
      <div className="bg-dark-base text-white p-4">
        <h2 className="text-xl font-semibold">
          Chat with your College Assistant
        </h2>
        <p className="text-dark-accent text-sm">
          Ask about sports, dining, housing, events, and academics
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-dark-purple min-h-0">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            id={message.id}
            text={message.text}
            sender={message.sender}
            timestamp={message.timestamp}
            calendarUrl={message.calendarUrl}
          />
        ))}

      {isLoading && (
          <div className="flex flex-col space-y-2">
            <div className="flex justify-start">
              <img
                src="/monkey.png"
                alt="Loading monkey"
                style={{ height: '150px', width: 'auto', objectFit: 'contain' }}
              />
            </div>
            <div className="flex justify-start">
              <div className="bg-dark-base border border-dark-magenta rounded-lg px-4 py-2 max-w-xs">
                <div className="flex items-center space-x-2">
                  <Bot className="w-5 h-5 text-dark-accent" />
                  <Loader2 className="w-4 h-4 animate-spin text-dark-accent" />
                  <span className="text-sm text-dark-lighter">Thinking...</span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={sendMessage}
        className="p-6 border-t border-dark-magenta bg-dark-purple flex-shrink-0"
      >
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask about college sports, dining, housing, events..."
            className="flex-1 px-3 py-2 bg-white text-dark-base border border-dark-magenta rounded-lg focus:outline-none focus:ring-2 focus:ring-dark-pink focus:border-transparent placeholder-gray-500"
            disabled={isLoading}
            autoComplete="off"
            style={{
              color: "#1a1a1d",
              backgroundColor: "#ffffff",
            }}
          />
          <button
            type="submit"
            disabled={isLoading || !inputMessage.trim()}
            className="bg-dark-pink hover:bg-dark-lighter disabled:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors duration-200 flex items-center space-x-2"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            <span>Send</span>
          </button>
        </div>
      </form>

      <div className="p-6 bg-dark-base border-t border-dark-magenta flex-shrink-0">
        <p className="text-sm text-dark-accent mb-2">Quick questions:</p>
        <div className="flex flex-wrap gap-2">
          {[
            "Tell me about sports programs",
            "Where can I eat on campus?",
            "What housing options are available?",
            "What events are happening?",
          ].map((question, index) => (
            <button
              key={index}
              onClick={() => handleQuickQuestion(question)}
              className="px-3 py-1 bg-dark-purple border border-dark-magenta text-dark-accent rounded-full text-sm hover:bg-dark-magenta hover:text-white transition-colors duration-200"
            >
              {question}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}