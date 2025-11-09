import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Campus Compass",
  description: "AI-powered chatbot for college students",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className} suppressHydrationWarning={true}>
        <div className="min-h-screen bg-gradient-to-br from-dark-base via-dark-purple to-dark-magenta">
          <header className="bg-dark-base border-b border-dark-purple shadow-lg">
            <div className="container mx-auto px-2 py-3">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-dark-accent rounded-full flex items-center justify-center">
                  <span className="text-dark-base font-bold text-lg">C</span>
                </div>
                <h1 className="text-2xl font-bold text-white">
                  Campus Compass
                </h1>
                <div className="text-sm text-dark-accent ml-auto">
                  Your Campus Helper
                </div>
              </div>
            </div>
          </header>
          <main className="container mx-auto px-2 py-2 h-[calc(100vh-80px)]">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
