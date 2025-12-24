/**
 * MessageInput Component
 * Input area with organic spring physics and paper-like aesthetic
 */

import { useState, KeyboardEvent } from "react";
import { motion } from "framer-motion";
import { Send } from "lucide-react";
import { cn } from "@/lib/utils";

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function MessageInput({ onSend, disabled }: MessageInputProps) {
  const [message, setMessage] = useState("");
  const [isFocused, setIsFocused] = useState(false);

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        type: "spring",
        stiffness: 200,
        damping: 30,
        mass: 1,
        delay: 0.2,
      }}
      className="border-t border-border p-6"
    >
      <div className="flex items-end gap-3 max-w-4xl mx-auto">
        {/* Textarea Input */}
        <div className="flex-1 relative">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            disabled={disabled}
            placeholder="Share your thoughts..."
            rows={1}
            className={cn(
              "w-full resize-none rounded-lg px-4 py-3",
              "bg-background border-2 transition-all duration-300",
              "text-foreground placeholder:text-muted-foreground",
              "focus:outline-none focus:ring-0",
              "disabled:opacity-50 disabled:cursor-not-allowed",
              "font-sans leading-relaxed",
              isFocused
                ? "border-ink-black shadow-sm"
                : "border-border-soft"
            )}
            style={{
              minHeight: "52px",
              maxHeight: "200px",
            }}
          />
        </div>

        {/* Send Button */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSend}
          disabled={disabled || !message.trim()}
          className={cn(
            "p-3 rounded-lg transition-all duration-300",
            "flex items-center justify-center",
            "disabled:opacity-40 disabled:cursor-not-allowed",
            message.trim() && !disabled
              ? "bg-ink-black text-paper-white shadow-md hover:shadow-lg"
              : "bg-muted text-muted-foreground"
          )}
          transition={{
            type: "spring",
            stiffness: 400,
            damping: 25,
          }}
        >
          <Send className="w-5 h-5" />
        </motion.button>
      </div>

      {/* Helper Text */}
      <p className="text-xs text-muted-foreground mt-2 text-center">
        Press <kbd className="px-1.5 py-0.5 bg-muted rounded text-ink-black">Enter</kbd> to send, <kbd className="px-1.5 py-0.5 bg-muted rounded text-ink-black">Shift + Enter</kbd> for new line
      </p>
    </motion.div>
  );
}
