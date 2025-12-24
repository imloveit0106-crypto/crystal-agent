"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { MessageSquare, PenTool, Calendar, BarChart3, ArrowRight } from "lucide-react";

export default function Home() {
  const [greeting, setGreeting] = useState("Good day");

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) setGreeting("Good morning");
    else if (hour >= 12 && hour < 18) setGreeting("Good afternoon");
    else setGreeting("Good evening");
  }, []);

  const cards = [
    {
      title: "Chat with Clarus",
      description: "Consult with your AI partner.",
      href: "/demo-chat",
      icon: MessageSquare,
    },
    {
      title: "Quick Record",
      description: "Log your thoughts and expenses.",
      href: "/demo-record",
      icon: PenTool,
    },
    {
      title: "Time Travel",
      description: "Review your timeline.",
      href: "/demo-calendar",
      icon: Calendar,
    },
    {
      title: "Analytics",
      description: "Visualize your life data.",
      href: "/demo-data",
      icon: BarChart3,
    },
  ];

  return (
    <main className="min-h-screen bg-[#ffffff] text-[#37352f] flex flex-col items-center justify-center p-6 md:p-24">
      <div className="max-w-5xl w-full space-y-16">

        {/* Header Section */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center md:text-left space-y-4"
        >
          <h1 className="text-5xl font-bold tracking-tight mb-2">{greeting}.</h1>
          <p className="text-xl text-gray-500 font-light">Your intellectual headquarters</p>
        </motion.div>

        {/* Navigation Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {cards.map((card, index) => (
            <Link key={card.title} href={card.href} className="block group">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
                className="p-8 rounded-xl border border-gray-100 bg-white hover:shadow-lg transition-all duration-300 group-hover:-translate-y-1"
              >
                <div className="flex items-start justify-between">
                  <div className="space-y-4">
                    <div className="p-3 bg-gray-50 rounded-lg w-fit group-hover:bg-gray-100 transition-colors">
                      <card.icon className="w-6 h-6 text-gray-700" />
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold mb-2">{card.title}</h3>
                      <p className="text-gray-500 text-sm leading-relaxed">{card.description}</p>
                    </div>
                  </div>
                  <ArrowRight className="w-5 h-5 text-gray-300 group-hover:text-gray-700 transform group-hover:translate-x-1 transition-all" />
                </div>
              </motion.div>
            </Link>
          ))}
        </div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 1 }}
          className="text-center text-xs text-gray-300 mt-20"
        >
          Clarus Agent • Intellectual Flow System
        </motion.div>

      </div>
    </main>
  );
}
