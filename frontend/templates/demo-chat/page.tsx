"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChatMessage } from "@/components/ChatMessage";
import { MessageInput } from "@/components/MessageInput";
import { TypingIndicator } from "@/components/TypingIndicator";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function DemoChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "Welcome to Clarus Chat.\n\nA thinking interface where quiet beauty meets organic dialogue.",
      timestamp: new Date(),
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);

  // Mock chat message sender - simulates AI response with 1.5s delay
  const sendMockChatMessage = async (userContent: string): Promise<Message> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const mockResponse: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: `I hear you. Let's think about this together.\n\nYour message: "${userContent}"`,
          timestamp: new Date(),
        };
        resolve(mockResponse);
      }, 1500); // 1.5 seconds mock delay
    });
  };

  const handleSendMessage = async (content: string) => {
    // Add user message with spring animation
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);

    // Call mock function to simulate AI response
    const assistantMessage = await sendMockChatMessage(content);

    setMessages((prev) => [...prev, assistantMessage]);
    setIsTyping(false);
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Main Chat Container - Paper-like */}
      <main className="flex flex-col flex-1 max-w-4xl mx-auto w-full">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.34, 1.56, 0.64, 1] }}
          className="px-6 py-8 border-b border-border"
        >
          <h1 className="text-2xl font-semibold text-foreground tracking-tight">
            Clarus Chat
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Demo: Monochrome conversation interface
          </p>
        </motion.header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-6 py-8 space-y-6">
          <AnimatePresence mode="popLayout">
            {messages.map((message, index) => (
              <ChatMessage
                key={message.id}
                message={message}
                index={index}
              />
            ))}

            {isTyping && <TypingIndicator key="typing" />}
          </AnimatePresence>
        </div>

        {/* Input Area */}
        <MessageInput onSend={handleSendMessage} disabled={isTyping} />
      </main>
    </div>
  );
}
