"use client";

import { useState, useEffect } from "react";
import { motion, useSpring, useTransform } from "framer-motion";
import { TrendingUp, Calendar, Activity, Database } from "lucide-react";
import { format, parseISO, startOfMonth, endOfMonth, isWithinInterval } from "date-fns";
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

interface CategoryCount {
  type: string;
  count: number;
  percentage: number;
}

// Animated Counter Component
function AnimatedCounter({ value, prefix = "", suffix = "" }: { value: number; prefix?: string; suffix?: string }) {
  const spring = useSpring(0, { duration: 1500 });
  const display = useTransform(spring, (current) =>
    Math.round(current).toLocaleString()
  );

  useEffect(() => {
    spring.set(value);
  }, [spring, value]);

  return (
    <motion.span
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.2, 0.9, 0.4, 1.0] }}
    >
      {prefix}
      <motion.span>{display}</motion.span>
      {suffix}
    </motion.span>
  );
}

export default function DemoDataPage() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [totalExpense, setTotalExpense] = useState(0);
  const [categoryCounts, setCategoryCounts] = useState<CategoryCount[]>([]);
  const [recentLogs, setRecentLogs] = useState<LogEntry[]>([]);

  // Load and calculate data
  const loadAndCalculate = () => {
    const storedLogs = localStorage.getItem("clarus_life_logs");
    if (!storedLogs) {
      setLogs([]);
      setTotalExpense(0);
      setCategoryCounts([]);
      setRecentLogs([]);
      return;
    }

    try {
      const parsedLogs: LogEntry[] = JSON.parse(storedLogs);
      setLogs(parsedLogs);

      // Calculate current month's expenses
      const now = new Date();
      const monthStart = startOfMonth(now);
      const monthEnd = endOfMonth(now);

      const currentMonthExpenses = parsedLogs.filter((log) => {
        if (log.type !== "Expense") return false;
        try {
          const logDate = parseISO(log.date);
          return isWithinInterval(logDate, { start: monthStart, end: monthEnd });
        } catch {
          return false;
        }
      });

      const total = currentMonthExpenses.reduce((sum, log) => sum + (log.amount || 0), 0);
      setTotalExpense(total);

      // Calculate category breakdown
      const counts = new Map<string, number>();
      parsedLogs.forEach((log) => {
        counts.set(log.type, (counts.get(log.type) || 0) + 1);
      });

      const totalCount = parsedLogs.length;
      const categoriesArray: CategoryCount[] = Array.from(counts.entries()).map(
        ([type, count]) => ({
          type,
          count,
          percentage: totalCount > 0 ? (count / totalCount) * 100 : 0,
        })
      );

      // Sort by count descending
      categoriesArray.sort((a, b) => b.count - a.count);
      setCategoryCounts(categoriesArray);

      // Get recent 5 logs
      const recent = parsedLogs.slice(0, 5);
      setRecentLogs(recent);

      console.log("[Analytics] Data loaded:", {
        totalLogs: parsedLogs.length,
        totalExpense: total,
        categories: categoriesArray,
      });
    } catch (error) {
      console.error("[Analytics] Failed to parse logs:", error);
    }
  };

  // Load on mount
  useEffect(() => {
    loadAndCalculate();
  }, []);

  // Handle sample data loading
  const handleLoadSampleData = () => {
    seedSampleData();
    loadAndCalculate();
  };

  // Get category color
  const getCategoryColor = (type: string) => {
    switch (type) {
      case "Task":
        return "bg-ink";
      case "Expense":
        return "bg-ink-light";
      case "Worry":
        return "bg-ink-lighter";
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
                Clarus Data
              </h1>
              <p className="text-sm text-muted-foreground mt-1">
                Demo: Analytics & insights
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

        {/* Analytics Content */}
        <div className="flex-1 overflow-y-auto px-6 py-8">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Total Expense Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1, ease: [0.2, 0.9, 0.4, 1.0] }}
              className="p-6 rounded-lg bg-paper-cream border border-border"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 rounded-lg bg-ink-lightest">
                  <TrendingUp className="w-5 h-5 text-ink" />
                </div>
                <h3 className="text-sm font-medium text-ink-light">
                  今月の支出合計
                </h3>
              </div>
              <div className="text-4xl font-bold text-foreground font-mono">
                <AnimatedCounter value={totalExpense} prefix="¥" />
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                {format(new Date(), "yyyy年M月", { locale: ja })}
              </p>
            </motion.div>

            {/* Total Logs Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.15, ease: [0.2, 0.9, 0.4, 1.0] }}
              className="p-6 rounded-lg bg-paper-cream border border-border"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 rounded-lg bg-ink-lightest">
                  <Activity className="w-5 h-5 text-ink" />
                </div>
                <h3 className="text-sm font-medium text-ink-light">
                  総ログ数
                </h3>
              </div>
              <div className="text-4xl font-bold text-foreground font-mono">
                <AnimatedCounter value={logs.length} />
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                全期間のアクティビティ
              </p>
            </motion.div>
          </div>

          {/* Category Breakdown */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: [0.2, 0.9, 0.4, 1.0] }}
            className="mb-8"
          >
            <h2 className="text-lg font-semibold text-foreground mb-4">
              カテゴリー別の内訳
            </h2>

            {categoryCounts.length > 0 ? (
              <div className="space-y-4">
                {categoryCounts.map((category, index) => (
                  <motion.div
                    key={category.type}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{
                      duration: 0.4,
                      delay: 0.25 + index * 0.05,
                      ease: [0.2, 0.9, 0.4, 1.0],
                    }}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-foreground">
                        {category.type}
                      </span>
                      <span className="text-sm text-ink-light font-mono">
                        {category.count}件 ({category.percentage.toFixed(1)}%)
                      </span>
                    </div>

                    {/* Progress Bar */}
                    <div className="h-2 bg-ink-lightest rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${category.percentage}%` }}
                        transition={{
                          duration: 1.2,
                          delay: 0.3 + index * 0.05,
                          ease: [0.2, 0.9, 0.4, 1.0],
                        }}
                        className={`h-full ${getCategoryColor(category.type)}`}
                      />
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="p-8 text-center">
                <p className="text-sm text-muted-foreground">
                  データがありません。「サンプルデータ」をロードしてください。
                </p>
              </div>
            )}
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3, ease: [0.2, 0.9, 0.4, 1.0] }}
          >
            <h2 className="text-lg font-semibold text-foreground mb-4">
              最近のアクティビティ
            </h2>

            {recentLogs.length > 0 ? (
              <div className="space-y-3">
                {recentLogs.map((log, index) => (
                  <motion.div
                    key={log.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{
                      duration: 0.3,
                      delay: 0.35 + index * 0.05,
                      ease: [0.2, 0.9, 0.4, 1.0],
                    }}
                    className="p-4 rounded-lg bg-paper-cream border border-border hover:shadow-soft transition-all duration-200"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span
                            className={`px-2 py-0.5 rounded text-xs font-medium text-paper-white ${getCategoryColor(
                              log.type
                            )}`}
                          >
                            {log.type}
                          </span>
                          {log.emotion && (
                            <span className="text-xs text-ink-light">
                              {log.emotion}
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-foreground leading-relaxed">
                          {log.content}
                        </p>
                        {log.type === "Expense" && log.amount && (
                          <p className="text-xs text-ink-light mt-1 font-mono">
                            ¥{log.amount.toLocaleString()}
                          </p>
                        )}
                      </div>
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <Calendar className="w-3 h-3" />
                        <span>
                          {format(parseISO(log.date), "M/d", { locale: ja })}
                        </span>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="p-8 text-center">
                <p className="text-sm text-muted-foreground">
                  アクティビティがありません。
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </main>
    </div>
  );
}
