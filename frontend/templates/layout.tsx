import type { Metadata } from "next";
import { Inter, Noto_Serif_JP } from "next/font/google";
import "./globals.css";

/**
 * Inter - English Typography
 * Optimized for digital reading with optical balance
 */
const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
  weight: ["400", "500", "600"],
});

/**
 * Noto Serif JP - Japanese Typography
 * Serene and elegant Japanese font matching paper-like aesthetic
 */
const notoSerifJP = Noto_Serif_JP({
  variable: "--font-noto-serif-jp",
  subsets: ["latin"],
  display: "swap",
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "Intellectual Flow",
  description: "A thinking interface that fuses the quiet beauty of Notion with organic dialogue",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="antialiased">
      <body
        className={`${inter.variable} ${notoSerifJP.variable}`}
      >
        {children}
      </body>
    </html>
  );
}
