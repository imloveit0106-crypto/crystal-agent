/**
 * ChatMessage Component
 * Displays individual messages with organic spring physics
 */

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface ChatMessageProps {
  message: Message;
  index: number;
}

const springTransition = {
  type: "spring",
  stiffness: 200,
  damping: 30,
  mass: 1,
};

export function ChatMessage({ message, index }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{
        ...springTransition,
        delay: index * 0.05, // Staggered animation
      }}
      className={cn(
        "flex w-full",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "max-w-[70ch] rounded-lg px-5 py-4 shadow-sm",
          "transition-all duration-300 ease-out",
          isUser
            ? "bg-ink-black text-paper-white"
            : "bg-paper-cream text-ink-black border border-border-subtle"
        )}
      >
        {/* Message Content */}
        <div className="prose prose-sm dark:prose-invert max-w-none">
          {message.content.split("\n\n").map((paragraph, i) => (
            <p
              key={i}
              className={cn(
                "leading-relaxed",
                i > 0 && "mt-4"
              )}
            >
              {paragraph}
            </p>
          ))}
        </div>

        {/* Timestamp */}
        <time
          className={cn(
            "text-xs mt-2 block",
            isUser ? "text-paper-white/60" : "text-ink-light"
          )}
        >
          {message.timestamp.toLocaleTimeString("en-US", {
            hour: "numeric",
            minute: "2-digit",
          })}
        </time>
      </div>
    </motion.div>
  );
}
