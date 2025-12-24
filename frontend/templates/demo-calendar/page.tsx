"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, Database } from "lucide-react";
import {
  format,
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  addDays,
  addMonths,
  subMonths,
  isSameMonth,
  isSameDay,
  parseISO,
} from "date-fns";
import { ja } from "date-fns/locale";
import { seedSampleData } from "@/lib/utils/seed-data";

interface LogEntry {
  id: string;
  content: string;
  type: "Task" | "Expense" | "Worry" | "Diary";
  emotion?: string;
  amount?: number;
  date: string; // ISO format
}

export default function DemoCalendarPage() {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [logs, setLogs] = useState<LogEntry[]>([]);

  // Load logs from localStorage
  const loadLogs = () => {
    const storedLogs = localStorage.getItem("clarus_life_logs");
    if (storedLogs) {
      try {
        setLogs(JSON.parse(storedLogs));
      } catch (error) {
        console.error("[Calendar] Failed to parse logs:", error);
      }
    }
  };

  // Load logs on mount
  useEffect(() => {
    loadLogs();
  }, []);

  // Handle sample data loading
  const handleLoadSampleData = () => {
    seedSampleData();
    loadLogs();
  };

  // Navigation functions
  const handlePrevMonth = () => {
    setCurrentMonth(subMonths(currentMonth, 1));
    setSelectedDate(null);
  };

  const handleNextMonth = () => {
    setCurrentMonth(addMonths(currentMonth, 1));
    setSelectedDate(null);
  };

  // Check if a date has any logs
  const hasLogsOnDate = (date: Date): boolean => {
    return logs.some((log) => {
      try {
        const logDate = parseISO(log.date);
        return isSameDay(logDate, date);
      } catch {
        return false;
      }
    });
  };

  // Get logs for a specific date
  const getLogsForDate = (date: Date): LogEntry[] => {
    return logs.filter((log) => {
      try {
        const logDate = parseISO(log.date);
        return isSameDay(logDate, date);
      } catch {
        return false;
      }
    });
  };

  // Generate calendar days
  const generateCalendarDays = () => {
    const monthStart = startOfMonth(currentMonth);
    const monthEnd = endOfMonth(currentMonth);
    const startDate = startOfWeek(monthStart);
    const endDate = endOfWeek(monthEnd);

    const days: Date[] = [];
    let currentDay = startDate;

    while (currentDay <= endDate) {
      days.push(currentDay);
      currentDay = addDays(currentDay, 1);
    }

    return days;
  };

  const calendarDays = generateCalendarDays();
  const selectedDateLogs = selectedDate ? getLogsForDate(selectedDate) : [];

  // Type color mapping
  const getTypeColor = (type: LogEntry["type"]) => {
    switch (type) {
      case "Task":
        return "bg-ink-lighter";
      case "Expense":
        return "bg-ink-light";
      case "Worry":
        return "bg-ink";
      case "Diary":
        return "bg-ink-lightest";
      default:
        return "bg-ink-lightest";
    }
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Main Container */}
      <main className="flex flex-col flex-1 max-w-5xl mx-auto w-full">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.34, 1.56, 0.64, 1] }}
          className="px-6 py-8 border-b border-border"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-semibold text-foreground tracking-tight">
                Clarus Calendar
              </h1>
              <p className="text-sm text-muted-foreground mt-1">
                Demo: Life log timeline
              </p>
            </div>

            {/* Sample Data Button */}
            <button
              onClick={handleLoadSampleData}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-ink-black text-paper-white hover:shadow-medium transition-all duration-200"
            >
              <Database className="w-4 h-4" />
              <span className="text-sm font-medium">サンプルデータ</span>
            </button>
          </div>
        </motion.header>

        {/* Calendar Container */}
        <div className="flex-1 overflow-y-auto px-6 py-8">
          {/* Month Navigation */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.2, 0.9, 0.4, 1.0] }}
            className="flex items-center justify-between mb-8"
          >
            <button
              onClick={handlePrevMonth}
              className="p-2 rounded-lg hover:bg-paper-cream transition-colors duration-200"
            >
              <ChevronLeft className="w-5 h-5 text-ink" />
            </button>

            <h2 className="text-xl font-semibold text-foreground">
              {format(currentMonth, "yyyy年 M月", { locale: ja })}
            </h2>

            <button
              onClick={handleNextMonth}
              className="p-2 rounded-lg hover:bg-paper-cream transition-colors duration-200"
            >
              <ChevronRight className="w-5 h-5 text-ink" />
            </button>
          </motion.div>

          {/* Calendar Grid */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1, ease: [0.2, 0.9, 0.4, 1.0] }}
            className="bg-paper-white rounded-lg border border-border overflow-hidden"
          >
            {/* Weekday Headers */}
            <div className="grid grid-cols-7 border-b border-border">
              {["日", "月", "火", "水", "木", "金", "土"].map((day) => (
                <div
                  key={day}
                  className="py-3 text-center text-sm font-medium text-ink-light"
                >
                  {day}
                </div>
              ))}
            </div>

            {/* Calendar Days Grid */}
            <div className="grid grid-cols-7">
              {calendarDays.map((day, index) => {
                const isCurrentMonth = isSameMonth(day, currentMonth);
                const isSelected = selectedDate && isSameDay(day, selectedDate);
                const hasLogs = hasLogsOnDate(day);
                const isToday = isSameDay(day, new Date());

                return (
                  <motion.button
                    key={day.toISOString()}
                    onClick={() => setSelectedDate(day)}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    transition={{ type: "spring", stiffness: 400, damping: 30 }}
                    className={`
                      relative p-4 min-h-[80px] border-r border-b border-border
                      transition-colors duration-200
                      ${isCurrentMonth ? "bg-background" : "bg-paper-cream"}
                      ${isSelected ? "bg-ink-lightest" : ""}
                      ${index % 7 === 6 ? "border-r-0" : ""}
                      hover:bg-ink-lightest
                    `}
                  >
                    {/* Date Number */}
                    <span
                      className={`
                        text-sm font-medium
                        ${isCurrentMonth ? "text-foreground" : "text-ink-lighter"}
                        ${isToday ? "font-bold" : ""}
                      `}
                    >
                      {format(day, "d")}
                    </span>

                    {/* Log Indicator Dot */}
                    {hasLogs && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: "spring", stiffness: 500, damping: 25 }}
                        className="absolute bottom-2 left-1/2 transform -translate-x-1/2 w-1.5 h-1.5 rounded-full bg-ink"
                      />
                    )}

                    {/* Today Indicator */}
                    {isToday && (
                      <div className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-ink" />
                    )}
                  </motion.button>
                );
              })}
            </div>
          </motion.div>

          {/* Selected Date Logs */}
          <AnimatePresence mode="wait">
            {selectedDate && selectedDateLogs.length > 0 && (
              <motion.div
                key={selectedDate.toISOString()}
                initial={{ opacity: 0, height: 0, y: -20 }}
                animate={{ opacity: 1, height: "auto", y: 0 }}
                exit={{ opacity: 0, height: 0, y: -20 }}
                transition={{ duration: 0.4, ease: [0.2, 0.9, 0.4, 1.0] }}
                className="mt-8 overflow-hidden"
              >
                <h3 className="text-lg font-semibold text-foreground mb-4">
                  {format(selectedDate, "M月d日（E）", { locale: ja })}のログ
                </h3>

                <div className="space-y-3">
                  {selectedDateLogs.map((log, index) => (
                    <motion.div
                      key={log.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{
                        duration: 0.3,
                        delay: index * 0.05,
                        ease: [0.2, 0.9, 0.4, 1.0],
                      }}
                      className="p-4 rounded-lg bg-paper-cream border border-border"
                    >
                      {/* Type Badge */}
                      <div className="flex items-center gap-2 mb-2">
                        <span
                          className={`
                            px-2 py-1 rounded text-xs font-medium text-paper-white
                            ${getTypeColor(log.type)}
                          `}
                        >
                          {log.type}
                        </span>
                        {log.emotion && (
                          <span className="text-xs text-ink-light">
                            {log.emotion}
                          </span>
                        )}
                      </div>

                      {/* Content */}
                      <p className="text-sm text-foreground leading-relaxed">
                        {log.content}
                      </p>

                      {/* Amount (for Expense type) */}
                      {log.type === "Expense" && log.amount && (
                        <p className="text-sm text-ink-light mt-2">
                          金額: ¥{log.amount.toLocaleString()}
                        </p>
                      )}
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}

            {selectedDate && selectedDateLogs.length === 0 && (
              <motion.div
                key={selectedDate.toISOString()}
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.4, ease: [0.2, 0.9, 0.4, 1.0] }}
                className="mt-8 p-8 text-center"
              >
                <p className="text-sm text-muted-foreground">
                  {format(selectedDate, "M月d日", { locale: ja })}
                  のログはありません
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
