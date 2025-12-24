"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { saveToLifeLog } from "@/lib/actions/log-actions";

interface Recording {
  id: string;
  title: string;
  timestamp: Date;
  status?: string;
}

export default function DemoRecordPage() {
  const [isRecording, setIsRecording] = useState(false);
  const [recordings, setRecordings] = useState<Recording[]>([]);

  const handleToggleRecording = async () => {
    if (!isRecording) {
      // Start recording
      setIsRecording(true);
    } else {
      // Stop recording and save to Notion
      setIsRecording(false);

      const newRecording: Recording = {
        id: Date.now().toString(),
        title: `Recording ${recordings.length + 1}`,
        timestamp: new Date(),
        status: "保存中...",
      };

      setRecordings((prev) => [newRecording, ...prev]);

      // Save to localStorage for calendar integration
      const logEntry = {
        id: newRecording.id,
        content: `音声記録: ${newRecording.title}`,
        type: "Diary" as const,
        emotion: "普通",
        date: newRecording.timestamp.toISOString(),
      };

      const existingLogs = localStorage.getItem("clarus_life_logs");
      const logs = existingLogs ? JSON.parse(existingLogs) : [];
      logs.unshift(logEntry);
      localStorage.setItem("clarus_life_logs", JSON.stringify(logs));

      // Call Server Action to save to Notion Life Log DB
      const result = await saveToLifeLog({
        content: logEntry.content,
        type: logEntry.type,
        emotion: logEntry.emotion,
        date: newRecording.timestamp,
      });

      // Update recording status with result
      setRecordings((prev) =>
        prev.map((rec) =>
          rec.id === newRecording.id
            ? { ...rec, status: result.message }
            : rec
        )
      );

      // Console log for verification
      console.log("[Clarus Record]", result);
      console.log("[localStorage] Saved to clarus_life_logs");
    }
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Main Container */}
      <main className="flex flex-col flex-1 max-w-4xl mx-auto w-full">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.34, 1.56, 0.64, 1] }}
          className="px-6 py-8 border-b border-border"
        >
          <h1 className="text-2xl font-semibold text-foreground tracking-tight">
            Clarus Record
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Demo: Voice & thought capture
          </p>
        </motion.header>

        {/* Recording Interface */}
        <div className="flex-1 overflow-y-auto px-6 py-8">
          {/* Record Button */}
          <div className="flex flex-col items-center justify-center py-16">
            <motion.button
              onClick={handleToggleRecording}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              transition={{ type: "spring", stiffness: 400, damping: 30 }}
              className={`
                relative w-32 h-32 rounded-full shadow-medium
                transition-all duration-300
                ${isRecording
                  ? "bg-destructive text-destructive-foreground"
                  : "bg-ink-black text-paper-white hover:shadow-card"
                }
              `}
            >
              {isRecording ? (
                <span className="text-lg font-medium">Stop</span>
              ) : (
                <span className="text-lg font-medium">Record</span>
              )}

              {/* Pulse animation when recording */}
              {isRecording && (
                <motion.div
                  className="absolute inset-0 rounded-full bg-destructive"
                  initial={{ opacity: 0.5, scale: 1 }}
                  animate={{ opacity: 0, scale: 1.4 }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "easeOut",
                  }}
                />
              )}
            </motion.button>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="mt-6 text-sm text-muted-foreground"
            >
              {isRecording ? "Recording... Click to stop" : "Click to start recording"}
            </motion.p>
          </div>

          {/* Recordings List */}
          {recordings.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, ease: [0.2, 0.9, 0.4, 1.0] }}
              className="mt-8 space-y-4"
            >
              <h2 className="text-lg font-semibold text-foreground mb-4">
                Recent Recordings
              </h2>

              {recordings.map((recording) => (
                <motion.div
                  key={recording.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, ease: [0.2, 0.9, 0.4, 1.0] }}
                  className="p-4 rounded-lg bg-paper-cream border border-border hover:shadow-soft transition-all duration-200"
                >
                  <h3 className="font-medium text-foreground">{recording.title}</h3>
                  <p className="text-sm text-muted-foreground mt-1">
                    {recording.timestamp.toLocaleString("en-US", {
                      month: "short",
                      day: "numeric",
                      hour: "numeric",
                      minute: "2-digit",
                    })}
                  </p>
                  {recording.status && (
                    <p className="text-xs text-ink-light mt-2">
                      {recording.status}
                    </p>
                  )}
                </motion.div>
              ))}
            </motion.div>
          )}
        </div>
      </main>
    </div>
  );
}
