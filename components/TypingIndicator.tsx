/**
 * TypingIndicator Component
 * Breathing dots animation for "AI is thinking" state
 */

import { motion } from "framer-motion";

const dotVariants = {
  initial: { y: 0, opacity: 0.4 },
  animate: { y: -6, opacity: 1 },
};

const dotTransition = {
  duration: 0.6,
  repeat: Infinity,
  repeatType: "reverse" as const,
  ease: "easeInOut",
};

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{
        type: "spring",
        stiffness: 200,
        damping: 30,
      }}
      className="flex justify-start w-full"
    >
      <div className="bg-paper-cream border border-border-subtle rounded-lg px-5 py-4 shadow-sm">
        <div className="flex items-center gap-1.5">
          {[0, 1, 2].map((index) => (
            <motion.div
              key={index}
              variants={dotVariants}
              initial="initial"
              animate="animate"
              transition={{
                ...dotTransition,
                delay: index * 0.15,
              }}
              className="w-2 h-2 rounded-full bg-ink-black"
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
}
