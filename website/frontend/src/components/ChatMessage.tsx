"use client";

import { Bot, User } from "lucide-react";
import { useEffect, useState } from "react";

interface ChatMessageProps {
  id: string;
  text: string;
  sender: "user" | "bot";
  timestamp: string;
  calendarUrl?: string;
}

export default function ChatMessage({
  text,
  sender,
  timestamp,
  calendarUrl,
}: ChatMessageProps) {
  const [formattedTime, setFormattedTime] = useState("");

  useEffect(() => {
    // Format time on client side only to avoid hydration issues
    const time = new Date(timestamp).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    setFormattedTime(time);
  }, [timestamp]);

  return (
    <div
      className={`flex ${sender === "user" ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`max-w-sm lg:max-w-2xl xl:max-w-4xl px-4 py-2 rounded-lg ${
          sender === "user"
            ? "bg-dark-pink text-white"
            : "bg-dark-base border border-dark-magenta text-dark-accent"
        }`}
      >
        <div className="flex items-start space-x-2">
          {sender === "bot" && (
            <Bot className="w-5 h-5 text-dark-accent mt-1 flex-shrink-0" />
          )}
          <div className="flex-1">
            <p className="text-sm whitespace-pre-wrap">{text}</p>
            {calendarUrl && (
              <div className="mt-2">
                <a
                  href={calendarUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-dark-pink hover:bg-dark-lighter text-white px-4 py-2 rounded-lg transition-colors duration-200 inline-block"
                >
                  Add to Calendar
                </a>
              </div>
            )}
            <p
              className={`text-xs mt-1 ${
                sender === "user"
                  ? "text-dark-accent opacity-75"
                  : "text-dark-lighter opacity-75"
              }`}
              suppressHydrationWarning={true}
            >
              {formattedTime}
            </p>
          </div>
          {sender === "user" && (
            <User className="w-5 h-5 text-white mt-1 flex-shrink-0" />
          )}
        </div>
      </div>
    </div>
  );
}
